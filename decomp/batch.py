"""Persistent local batching for pinned Goemon MIPS reconstruction.

Generated assembly/C, queue databases and compiler objects stay in local research
storage. A linked probe match is a review candidate, never a whole-ROM claim.
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
from contextlib import contextmanager
from datetime import datetime, timezone
import argparse
from collections import Counter
import hashlib
import json
import math
import os
from pathlib import Path
import re
import shutil
import signal
import sqlite3
import subprocess
import sys
import time

from .probe import Elf32, compare_code, linker_script
from .attempt_ledger import (LEDGER_FORMAT, input_signature as ledger_input_signature,
                            make_attempt_record, validate_attempt_record, validate_ledger)
from .verify import load_manifest

ROOT = Path(__file__).resolve().parent
M2C_PIN = 'a21c1dcd7255b176c032bb932f521846e98d4372'
PERMUTER_PIN = 'ec2efeebb33e2b1de81e39fbf7cbe3cd97350472'
C_PRELUDE = '#ifndef NULL\n#define NULL 0\n#endif\n'
FLAGS = ['-c', '-G', '0', '-non_shared', '-Xfullwarn', '-Xcpluscomm',
         '-Iinclude', '-Ilibultra/include', '-Ilibultra/include/PR', '-Isrc', '-I.',
         '-Wab,-r4300_mul', '-woff', '649,838,712', '-D_LANGUAGE_C', '-D_FINALROM',
         '-DF3DEX_GBI', '-D__sgi', '-DNDEBUG', '-O2', '-mips2']


def sha(data):
    return hashlib.sha256(data).hexdigest()


def now():
    return datetime.now(timezone.utc).isoformat()


def capture(command, cwd=None):
    return subprocess.check_output(command, cwd=cwd, text=True, stderr=subprocess.STDOUT).strip()


def local_storage(path):
    path = Path(path).resolve()
    project = ROOT.parent.resolve()
    if path.is_relative_to(project) and not any(path.is_relative_to(project / p) for p in ('decomp/local', 'practice/diagnostics')):
        raise ValueError('Raw research storage must be outside the repository or in an explicitly ignored research directory')
    return path


@contextmanager
def exclusive_cache(cache):
    if os.name != 'posix':
        raise ValueError('Run batch compiler jobs inside Linux/WSL')
    import fcntl
    with (Path(cache) / 'run.lock').open('a+') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise ValueError('Another operation owns this cache') from exc
        try:
            yield
        finally:
            fcntl.flock(lock, fcntl.LOCK_UN)


class Queue:
    def __init__(self, path):
        self.db = sqlite3.connect(path)
        self.db.row_factory = sqlite3.Row
        self.db.executescript('''
            PRAGMA foreign_keys=ON;
            CREATE TABLE IF NOT EXISTS meta(key TEXT PRIMARY KEY, value TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS functions(
                name TEXT PRIMARY KEY, address INTEGER NOT NULL, size INTEGER NOT NULL,
                section TEXT NOT NULL, source TEXT NOT NULL, asm TEXT NOT NULL,
                expected BLOB NOT NULL, verified INTEGER NOT NULL, rom_offset INTEGER);
            CREATE TABLE IF NOT EXISTS runs(id INTEGER PRIMARY KEY, recipe TEXT NOT NULL, started TEXT NOT NULL, ended TEXT, configuration TEXT NOT NULL, selected INTEGER NOT NULL, elapsed REAL);
            CREATE TABLE IF NOT EXISTS attempts(
                id INTEGER PRIMARY KEY, name TEXT NOT NULL REFERENCES functions(name),
                recipe TEXT NOT NULL, ordinal INTEGER NOT NULL, status TEXT NOT NULL,
                started TEXT NOT NULL, ended TEXT, result TEXT, input_signature TEXT, run_id INTEGER,
                UNIQUE(name, recipe, ordinal));
        ''')
        # Existing local caches predate the ledger. Add nullable columns so their
        # attempt history remains untouched and is never retroactively signed.
        function_columns = {row['name'] for row in self.db.execute('PRAGMA table_info(functions)')}
        if 'rom_offset' not in function_columns:
            self.db.execute('ALTER TABLE functions ADD COLUMN rom_offset INTEGER')
        attempt_columns = {row['name'] for row in self.db.execute('PRAGMA table_info(attempts)')}
        if 'input_signature' not in attempt_columns:
            self.db.execute('ALTER TABLE attempts ADD COLUMN input_signature TEXT')
        if 'run_id' not in attempt_columns:
            self.db.execute('ALTER TABLE attempts ADD COLUMN run_id INTEGER')
        self.db.execute('CREATE INDEX IF NOT EXISTS attempts_input_signature ON attempts(input_signature,status)')

    def close(self):
        self.db.close()

    def meta(self, key, value=None):
        if value is not None:
            self.db.execute('INSERT OR REPLACE INTO meta VALUES (?, ?)', (key, json.dumps(value)))
            self.db.commit()
        row = self.db.execute('SELECT value FROM meta WHERE key=?', (key,)).fetchone()
        return json.loads(row[0]) if row else None

    def register(self, identity, functions):
        if self.meta('identity') not in (None, identity):
            raise ValueError('Cache baseline identity differs; use a new cache')
        with self.db:
            for fn in functions:
                fn.setdefault('rom_offset', None)
                if not re.fullmatch(r'[A-Za-z_.$][A-Za-z0-9_.$]*', fn['name']) or fn['size'] <= 0 or len(fn['expected']) != fn['size']:
                    raise ValueError('Invalid queued function')
                old = self.db.execute('SELECT * FROM functions WHERE name=?', (fn['name'],)).fetchone()
                if old and any(old[key] != fn[key] for key in ('address', 'size', 'section', 'source', 'asm', 'expected')):
                    raise ValueError('Baseline function contents changed: ' + fn['name'])
                if old and old['rom_offset'] is not None and fn['rom_offset'] != old['rom_offset']:
                    raise ValueError('Baseline function ROM offset changed: ' + fn['name'])
                if old:
                    self.db.execute('UPDATE functions SET verified=?,rom_offset=COALESCE(rom_offset,?) WHERE name=?',
                                    (fn['verified'], fn['rom_offset'], fn['name']))
                else:
                    self.db.execute('''INSERT INTO functions
                        (name,address,size,section,source,asm,expected,verified,rom_offset)
                        VALUES (:name,:address,:size,:section,:source,:asm,:expected,:verified,:rom_offset)''', fn)
            self.db.execute('INSERT OR REPLACE INTO meta VALUES (?, ?)', ('identity', json.dumps(identity)))

    def recover(self):
        # Caller holds the OS cache lock, including after a coordinator crash.
        with self.db:
            self.db.execute("UPDATE attempts SET status='interrupted', ended=? WHERE status='running'", (now(),))
            self.db.execute('UPDATE runs SET ended=? WHERE ended IS NULL', (now(),))

    def select(self, recipe, limit, maximum, scope='generated', region='all', retry=False, max_attempts=1,
               input_signatures=None):
        rows = self.db.execute('''
            SELECT f.*, (SELECT COUNT(*) FROM attempts a WHERE a.name=f.name AND a.recipe=?) AS used,
            (SELECT status FROM attempts a WHERE a.name=f.name AND a.recipe=? ORDER BY id DESC LIMIT 1) AS last
            FROM functions f WHERE verified=0 AND size<=? ORDER BY size, name
        ''', (recipe, recipe, maximum))
        selected = []
        input_signatures = input_signatures or {}
        terminal = ('mismatch', 'linked_match', 'needs_context', 'needs_layout', 'unresolved_symbols',
                    'compile_failed', 'link_failed', 'generation_failed', 'unsupported', 'needs_source')
        signatures = sorted({value for value in input_signatures.values() if value})
        completed_inputs = set()
        status_marks = ','.join('?' for _ in terminal)
        for start in range(0, len(signatures), 500):
            batch = signatures[start:start + 500]
            input_marks = ','.join('?' for _ in batch)
            completed_inputs.update(row['input_signature'] for row in self.db.execute(
                'SELECT DISTINCT input_signature FROM attempts WHERE input_signature IN ('+input_marks+
                ') AND status IN ('+status_marks+')', (*batch, *terminal)))
        for row in rows:
            if scope == 'generated' and not row['name'].startswith('func_'):
                continue
            if region != 'all' and ((row['section'] == '.main') != (region == 'main')):
                continue
            if row['used'] >= max_attempts or row['last'] == 'linked_match' or (row['used'] and not retry):
                continue
            signature = input_signatures.get(row['name'])
            if signature in completed_inputs and not retry:
                continue
            selected.append(dict(row))
            if len(selected) == limit:
                break
        return selected

    def claim(self, name, recipe, input_sig=None, run_id=None):
        with self.db:
            ordinal = self.db.execute('SELECT COUNT(*) FROM attempts WHERE name=? AND recipe=?', (name, recipe)).fetchone()[0] + 1
            row = self.db.execute('INSERT INTO attempts(name,recipe,ordinal,status,started,input_signature,run_id) VALUES (?,?,?,?,?,?,?)',
                                  (name, recipe, ordinal, 'running', now(), input_sig, run_id))
            return row.lastrowid

    def finish(self, attempt, result, attempt_record=None):
        if attempt_record is not None:
            row = self.db.execute('SELECT name,input_signature,status,recipe,run_id FROM attempts WHERE id=?', (attempt,)).fetchone()
            if row is None or row['status'] != 'running':
                raise ValueError('Attempt is not running')
            if attempt_record.get('function') != row['name'] or attempt_record.get('input_signature') != row['input_signature']:
                raise ValueError('Attempt record does not match its queued input')
            if (attempt_record.get('proof_run', {}).get('recipe_id') != row['recipe']
                    or attempt_record.get('proof_run', {}).get('run_id') != row['run_id']):
                raise ValueError('Attempt record does not match its proof run')
            if attempt_record.get('comparison', {}).get('status') != result.get('status'):
                raise ValueError('Attempt record status does not match its result')
            record_errors = validate_attempt_record(attempt_record)
            if record_errors:
                raise ValueError('Attempt record validation failed: ' + '; '.join(record_errors))
            result = dict(result, attempt_record=attempt_record)
        with self.db:
            changed = self.db.execute('UPDATE attempts SET status=?, ended=?, result=? WHERE id=? AND status=?',
                                      (result['status'], now(), json.dumps(result), attempt, 'running'))
            if changed.rowcount != 1: raise ValueError('Attempt is not running')

    def start_run(self, recipe, configuration, selected):
        with self.db:
            return self.db.execute('INSERT INTO runs(recipe,started,configuration,selected) VALUES (?,?,?,?)',
                                   (recipe, now(), json.dumps(configuration), selected)).lastrowid

    def end_run(self, ident, elapsed):
        with self.db:
            self.db.execute('UPDATE runs SET ended=?,elapsed=? WHERE id=?', (now(), round(elapsed,3), ident))

    def results(self, recipe):
        rows = self.db.execute('''SELECT a.* FROM attempts a WHERE recipe=? AND id=(
            SELECT MAX(b.id) FROM attempts b WHERE b.recipe=a.recipe AND b.name=a.name) ORDER BY name''', (recipe,))
        return [dict(row) for row in rows]

    def attempt_records(self, recipe):
        rows = self.db.execute('SELECT result FROM attempts WHERE recipe=? AND result IS NOT NULL ORDER BY id', (recipe,))
        records = []
        legacy = 0
        for row in rows:
            value = json.loads(row['result'])
            record = value.get('attempt_record')
            if record is None:
                legacy += 1
            else:
                records.append(record)
        return records, legacy


def assembly_index(baseline, names):
    result = {}
    start_pattern = re.compile(r'^\s*glabel\s+(\S+)\s*$', re.MULTILINE)
    for path in sorted((Path(baseline) / 'asm').rglob('*.s')):
        text = path.read_text(encoding='utf-8')
        for match in start_pattern.finditer(text):
            name = match[1]
            if name not in names:
                continue
            end = re.compile(r'^\s*endlabel\s+' + re.escape(name) + r'\s*$', re.MULTILINE).search(text, match.end())
            if end is None:
                continue
            body = text[match.start():end.end()] + '\n'
            if name in result and result[name][1] != body:
                raise ValueError('Ambiguous assembly source: ' + name)
            result[name] = (str(path.relative_to(baseline)), body)
    return result


def verified_rom_offset(name, expected, image):
    """Return an encoded ROM offset only when the pinned image confirms bytes."""
    match = re.search(r'_([0-9A-Fa-f]+)\Z', name)
    if not match:
        return None
    offset = int(match[1], 16)
    if image[offset:offset + len(expected)] != expected:
        return None
    return offset


def initialize(cache, baseline, m2c, python, context=None, permuter=None):
    cache = local_storage(cache)
    cache.mkdir(parents=True, exist_ok=True)
    baseline, m2c = Path(baseline).resolve(), Path(m2c).resolve()
    for tool in ('mips-linux-gnu-as', 'mips-linux-gnu-ld'):
        if shutil.which(tool) is None: raise ValueError('Missing tool: '+tool)
    manifest = load_manifest(ROOT / 'manifest.json')
    if capture(['git', 'rev-parse', 'HEAD'], baseline) != manifest['upstream_commit']:
        raise ValueError('Baseline is not pinned upstream')
    if capture(['git', 'diff', '--name-only'], baseline):
        raise ValueError('Baseline has tracked modifications')
    if capture(['git', 'rev-parse', 'HEAD'], m2c) != M2C_PIN or capture(['git', 'status', '--porcelain', '--untracked-files=no'], m2c):
        raise ValueError('m2c must be the clean pinned tool')
    image = (baseline / 'build/usa/mnsg.z64').read_bytes()
    if hashlib.sha1(image).hexdigest() != manifest['decompressed_sha1']:
        raise ValueError('Baseline ROM identity mismatch')
    elf_data = (baseline / 'build/usa/mnsg.elf').read_bytes()
    elf = Elf32(elf_data)
    marked = {s.name[:-len('.NON_MATCHING')] for s in elf.symbols if s.name.endswith('.NON_MATCHING') and s.section}
    native = {s.name: s for s in elf.symbols if s.kind == 2 and s.size and 0 < s.section < len(elf.sections)}
    report = json.loads((ROOT / 'results/combined.json').read_text())
    if report['upstream_commit'] != manifest['upstream_commit'] or report['status'] != 'matched' or not report['comparison']['full_rom_match'] or report['comparison']['candidate_sha1'] != manifest['decompressed_sha1']:
        raise ValueError('Published verified reference is invalid')
    verified = {fn['name'] for fn in report['comparison']['functions'] if fn['matched']}
    if len(verified) != report['comparison']['claimed_functions'] or not verified <= (set(native) & marked):
        raise ValueError('Published function reference is inconsistent')
    candidates = set(native) & marked
    index = assembly_index(baseline, candidates)
    functions = []
    for name in sorted(candidates):
        symbol = native[name]
        source, asm = index.get(name, ('', ''))
        expected = elf.code(symbol)
        functions.append(dict(name=name, address=symbol.value, size=symbol.size, section=elf.names[symbol.section],
                              source=source, asm=asm, expected=expected, verified=int(name in verified),
                              rom_offset=verified_rom_offset(name, expected, image)))
    identity = dict(upstream_commit=manifest['upstream_commit'],
                    rom_sha1=manifest['decompressed_sha1'], elf_sha256=sha(elf_data))
    config = dict(baseline=str(baseline), m2c=str(m2c), python=str(Path(python).absolute()),
                  context=str(Path(context).resolve()) if context else str(ROOT / 'batch_context.h'),
                  permuter=str(Path(permuter).resolve()) if permuter else None)
    with exclusive_cache(cache):
        queue = Queue(cache / 'queue.sqlite')
        try:
            queue.register(identity, functions)
            queue.meta('config', config)
            queue.meta('reference', dict(upstream_c=len(native)-len(candidates), newly_verified=len(verified),
                                         identified=len(native), indexed_asm=len(index)))
        finally:
            queue.close()
    return dict(identified=len(native), queued=len(candidates)-len(verified), indexed_asm=len(index), already_verified=len(verified))


class StageTimeout(Exception):
    def __init__(self, message, stage='process'):
        super().__init__(message)
        self.stage = stage


def bounded(command, cwd, output, deadline, stderr=None, stage='process'):
    remaining = deadline - time.monotonic()
    if remaining <= 0:
        raise StageTimeout('Budget exhausted before process start', stage)
    with Path(output).open('wb') as stdout:
        with (Path(stderr).open('wb') if stderr else open(os.devnull, 'wb')) as error:
            process = subprocess.Popen(command, cwd=cwd, stdout=stdout, stderr=error if stderr else subprocess.STDOUT,
                                       start_new_session=(os.name == 'posix'))
            try:
                code = process.wait(timeout=remaining)
            except BaseException as exc:
                if process.poll() is None:
                    if os.name == 'posix':
                        try: os.killpg(process.pid, signal.SIGKILL)
                        except ProcessLookupError: pass
                    else:
                        process.kill()
                process.wait()
                if isinstance(exc, subprocess.TimeoutExpired):
                    raise StageTimeout('Process group exceeded its budget', stage) from exc
                raise
    return code


def recipe_snapshot(cache, config, seconds, search_seconds, context=None):
    baseline = Path(config['baseline'])
    context_text = Path(context or config['context']).read_text(encoding='utf-8').replace('\r\n', '\n')
    # Context is preprocessed C, never shell text or automatically guessed prototypes.
    tools = {path.name: sha(path.read_bytes()) for path in sorted((baseline/'tools/ido-5.3').iterdir()) if path.is_file()}
    recipe = dict(format='goemon-batch-recipe-v1', context_sha256=sha(context_text.encode()), ido_files=tools,
                  binutils={name: sha(Path(shutil.which(name)).read_bytes()) for name in ('mips-linux-gnu-as','mips-linux-gnu-ld')},
                  python_version=capture([config['python'], '--version']),
                  python_sha256=sha(Path(config['python']).read_bytes()),
                  dependency_lock_sha256=sha((baseline/'uv.lock').read_bytes()),
                  m2c_pin=capture(['git', 'rev-parse', 'HEAD'], config['m2c']), flags=FLAGS,
                  source_hashes={name: sha((ROOT/name).read_bytes().replace(b'\r\n', b'\n'))
                                 for name in ('batch.py', 'probe.py', 'attempt_ledger.py')},
                  seconds=seconds, search_seconds=search_seconds)
    if recipe['m2c_pin'] != M2C_PIN or capture(['git', 'status', '--porcelain', '--untracked-files=no'], config['m2c']):
        raise ValueError('m2c identity changed')
    if search_seconds:
        if not config.get('permuter') or capture(['git', 'rev-parse', 'HEAD'], config['permuter']) != PERMUTER_PIN:
            raise ValueError('Bounded search requires pinned local decomp-permuter')
        if capture(['git', 'status', '--porcelain', '--untracked-files=no'], config['permuter']):
            raise ValueError('Permuter has tracked modifications')
        recipe['permuter_pin'] = PERMUTER_PIN
    key = sha(json.dumps(recipe, sort_keys=True).encode())
    directory = cache / 'recipes' / key
    if not directory.exists():
        directory.mkdir(parents=True)
        (directory/'context.c').write_text(context_text, encoding='utf-8')
        (directory/'recipe.json').write_text(json.dumps(recipe, indent=2)+'\n', encoding='utf-8')
    elif ((directory/'context.c').read_text(encoding='utf-8') != context_text or
          json.loads((directory/'recipe.json').read_text(encoding='utf-8')) != recipe):
        raise ValueError('Cached context snapshot changed')
    return key, directory, context_text


def compile_probe(source, name, address, expected, baseline, globals_map, directory, deadline, tag='probe'):
    candidate_sha256 = sha(source.read_bytes())
    obj = directory / (tag + '.o')
    code = bounded([str(baseline/'tools/ido-5.3/cc'), *FLAGS, str(source), '-o', str(obj)], baseline,
                   directory/(tag+'-compile.log'), deadline, stage='compile')
    if code:
        return dict(status='compile_failed', stage='compile', exit_code=code, candidate_sha256=candidate_sha256)
    image = Elf32(obj.read_bytes())
    reason = image.layout_reason(name)
    if reason:
        return dict(status='needs_layout', stage='object', reason=reason, candidate_sha256=candidate_sha256)
    function = image.function(name)
    if function.size != len(expected):
        return dict(status='mismatch', stage='object', reason='code_size', expected_size=len(expected),
                    actual_size=function.size, candidate_sha256=candidate_sha256)
    try:
        script = linker_script(name, address, image.undefined(), globals_map)
    except ValueError as exc:
        return dict(status='unresolved_symbols', stage='link', reason=str(exc), candidate_sha256=candidate_sha256)
    link = directory/(tag+'.ld')
    link.write_text(script, encoding='utf-8')
    executable = directory/(tag+'.elf')
    code = bounded(['mips-linux-gnu-ld', '-T', str(link), '-o', str(executable), str(obj)], baseline,
                   directory/(tag+'-link.log'), deadline, stage='link')
    if code:
        return dict(status='link_failed', stage='link', exit_code=code, candidate_sha256=candidate_sha256)
    linked = Elf32(executable.read_bytes())
    symbol = linked.function(name)
    actual = linked.code(symbol)
    comparison = compare_code(expected, actual)
    matched = actual == expected and symbol.value == address
    return dict(status='linked_match' if matched else 'mismatch', stage='linked_probe', comparison=comparison,
                guest_address=f'0x{symbol.value:08X}', candidate_source=source.name, candidate_sha256=sha(source.read_bytes()),
                linked_elf=executable.name, linked_elf_sha256=sha(executable.read_bytes()))


def search_candidate(fn, config, context_text, directory, globals_map, baseline, deadline, seconds):
    import shlex
    # Assemble and link a target probe; verify extraction before using it as a scorer target.
    target_source = directory/'target.s'
    target_source.write_text('.include "macro.inc"\n.set noat\n.set noreorder\n.set gp=64\n.section .text,"ax"\n'+fn['asm'])
    target_object = directory/'target-reloc.o'
    code = bounded(['mips-linux-gnu-as', '-EB', '-mtune=vr4300', '-march=vr4300', '-mabi=32', '-Iinclude',
                    str(target_source), '-o', str(target_object)], baseline, directory/'target-assemble.log', deadline)
    if code: return dict(search_status='target_assemble_failed')
    target_elf = Elf32(target_object.read_bytes())
    (directory/'target.ld').write_text(linker_script(fn['name'], fn['address'], target_elf.undefined(), globals_map))
    code = bounded(['mips-linux-gnu-ld', '-T', str(directory/'target.ld'), '-o', str(directory/'target.o'), str(target_object)],
                   baseline, directory/'target-link.log', deadline)
    if code: return dict(search_status='target_link_failed')
    target_elf = Elf32((directory/'target.o').read_bytes())
    if target_elf.code(target_elf.function(fn['name'])) != fn['expected']:
        return dict(search_status='target_extraction_mismatch')
    safe = re.compile(r'[A-Za-z_.$][A-Za-z0-9_.$]*\Z')
    definitions = [f'PROVIDE({name} = 0x{value:08X});' for name, value in sorted(globals_map.items()) if name != fn['name'] and safe.fullmatch(name)]
    (directory/'search.ld').write_text(f'ENTRY({fn["name"]})\nSECTIONS {{ .text 0x{fn["address"]:08X} : SUBALIGN(4) {{ *(.text) }} /DISCARD/ : {{ *(*) }} }}\n'+'\n'.join(definitions))
    (directory/'base.c').write_text((directory/'candidate.c').read_text())
    compiler = ' '.join(shlex.quote(str(x)) for x in [baseline/'tools/ido-5.3/cc', *FLAGS])
    script = '#!/bin/sh\nset -e\ninput=$(realpath -- "$1")\noutput=$(realpath -- "$3")\n'
    script += 'cd '+shlex.quote(str(baseline))+'\n'+compiler+' "$input" -o "$output.reloc.o"\n'
    script += 'exec mips-linux-gnu-ld -T '+shlex.quote(str(directory/'search.ld'))+' -o "$output" "$output.reloc.o"\n'
    (directory/'compile.sh').write_text(script)
    (directory/'compile.sh').chmod(0o755)
    (directory/'settings.toml').write_text(f'func_name = "{fn["name"]}"\ncompiler_type = "ido"\n[weight_overrides]\nperm_randomize_external_type = 0.0\nperm_randomize_function_type = 0.0\nperm_remove_ast = 0.0\n')
    search_end = min(deadline, time.monotonic()+seconds)
    try:
        bounded([config['python'], '-B', str(Path(config['permuter'])/'permuter.py'), str(directory), '-j1', '--stop-on-zero', '--best-only'],
                directory, directory/'search.log', search_end)
        status = 'finished'
    except StageTimeout:
        status = 'budget_exhausted'
    for result in sorted(directory.glob('output-0-*/source.c')):
        source = directory/'searched.c'
        source.write_bytes(result.read_bytes())
        checked = compile_probe(source, fn['name'], fn['address'], fn['expected'], baseline, globals_map, directory, deadline, 'searched')
        if checked['status'] == 'linked_match':
            return dict(checked, search_status='revalidated_match')
    return dict(search_status=status)


def draft_issue(draft):
    if re.search(r'\b(?:asm|__asm__|__asm)\s*\(', draft):
        return 'inline_assembly'
    if re.search(r'(?m)(?:^\s*(?:extern\s+)?|[(,]\s*)\?(?:\s|\*)', draft) or 'M2C_UNK' in draft:
        return 'unknown_type'
    if 'M2C_ERROR' in draft:
        return 'unsupported_translation'
    for name in re.findall(r'\bvoid\s*\*\s*(\w+)', draft):
        if re.search(r'\b'+re.escape(name)+r'\s*->', draft):
            return 'untyped_structure'
    return None


def attempt(fn, attempt_id, cache, config, recipe_dir, context_text, globals_map, seconds, search_seconds, use_cache):
    started = time.monotonic()
    deadline = started + seconds
    directory = cache/'attempts'/f'{attempt_id:06d}-{fn["name"]}'
    directory.mkdir(parents=True, exist_ok=False)
    result = dict(status='failed', stage='prepare')
    try:
        if not fn['asm']:
            result = dict(status='needs_source', stage='extract')
        else:
            source = directory/'source.s'
            source.write_text('.section .text\n'+fn['asm'], encoding='utf-8')
            command = [config['python'], '-B', str(Path(config['m2c'])/'m2c.py'), '--target', 'mips-ido',
                       '--context', str(recipe_dir/'context.c'), '-f', fn['name'], str(source)]
            if not use_cache: command.insert(3, '--no-cache')
            code = bounded(command, directory, directory/'draft.c', deadline, directory/'m2c.log', stage='m2c')
            if code:
                result = dict(status='generation_failed', stage='m2c', exit_code=code)
            else:
                draft = (directory/'draft.c').read_text(encoding='utf-8')
                issue = draft_issue(draft)
                if issue:
                    result = dict(status='unsupported' if issue in ('inline_assembly','unsupported_translation') else 'needs_context', stage='m2c', reason=issue)
                else:
                    candidate = directory/'candidate.c'
                    candidate.write_text(C_PRELUDE+context_text+'\n'+draft, encoding='utf-8')
                    baseline = Path(config['baseline'])
                    result = compile_probe(candidate, fn['name'], fn['address'], fn['expected'], baseline, globals_map, directory, deadline)
                    if result['status'] == 'mismatch' and search_seconds:
                        try:
                            result.update(search_candidate(fn, config, context_text, directory, globals_map, baseline, deadline, search_seconds))
                        except StageTimeout as exc:
                            result.update(search_status='total_budget_exhausted', search_stage=exc.stage)
    except StageTimeout as exc:
        result = dict(status='timeout', stage=exc.stage, reason=str(exc))
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        result = dict(status='failed', stage=result.get('stage', 'process'), reason=str(exc))
    result.update(function=fn['name'], size=fn['size'], elapsed_seconds=round(time.monotonic()-started, 3),
                  artifacts=str(directory.relative_to(cache)))
    (directory/'result.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    return result


def run(cache, limit=100, maximum=128, workers=2, seconds=20, search_seconds=0, retry=False, max_attempts=1,
        scope='generated', region='all', context=None):
    cache = local_storage(cache)
    if not math.isfinite(seconds) or not math.isfinite(search_seconds) or min(limit, maximum, workers, seconds, max_attempts) <= 0 or workers > 16 or search_seconds < 0 or search_seconds >= seconds:
        raise ValueError('Invalid job limits; search must fit inside each total budget')
    with exclusive_cache(cache):
        queue = Queue(cache/'queue.sqlite')
        try:
            config = queue.meta('config')
            if not config: raise ValueError('Initialize the cache first')
            baseline = Path(config['baseline'])
            identity = queue.meta('identity')
            if sha((baseline/'build/usa/mnsg.elf').read_bytes()) != identity['elf_sha256']:
                raise ValueError('Cached baseline ELF changed')
            if capture(['git', 'rev-parse', 'HEAD'], baseline) != identity['upstream_commit'] or capture(['git', 'diff', '--name-only'], baseline):
                raise ValueError('Baseline source identity changed')
            queue.recover()
            recipe, recipe_dir, context_text = recipe_snapshot(cache, config, seconds, search_seconds, context)
            recipe_data = json.loads((recipe_dir/'recipe.json').read_text())
            attempt_recipe = dict(recipe_data)
            attempt_recipe['ido_toolchain_sha256'] = sha(json.dumps(recipe_data['ido_files'], sort_keys=True).encode())
            baseline_elf = Elf32((baseline/'build/usa/mnsg.elf').read_bytes())
            globals_map = baseline_elf.globals()
            input_signatures = {}
            for row in queue.db.execute('SELECT * FROM functions WHERE verified=0 AND size<=?', (maximum,)):
                function = dict(row)
                input_signatures[function['name']] = ledger_input_signature(function, identity, attempt_recipe)
            selected = queue.select(recipe, limit, maximum, scope, region, retry, max_attempts, input_signatures)
            for fn in selected:
                symbol = baseline_elf.function(fn['name'])
                if symbol.value != fn['address'] or baseline_elf.code(symbol) != fn['expected']:
                    raise ValueError('Queue reference changed: '+fn['name'])
            queue.meta('last_recipe', recipe)
            queue.meta('run_started', now())
            run_started = time.monotonic()
            run_id = queue.start_run(recipe, dict(limit=limit, max_size=maximum, workers=workers, seconds=seconds, search_seconds=search_seconds, scope=scope, region=region, retry=retry, max_attempts=max_attempts), len(selected))
            queue.meta('recipe:'+recipe, recipe_data)
            if selected:
                # Populate the m2c context cache before launching concurrent readers.
                fn = selected.pop(0); input_sig = input_signatures[fn['name']]
                ident = queue.claim(fn['name'], recipe, input_sig, run_id)
                result = attempt(fn, ident, cache, config, recipe_dir, context_text, globals_map, seconds, search_seconds, True)
                record = make_attempt_record(fn, identity, attempt_recipe, result, input_sig, run_id, recipe)
                queue.finish(ident, result, record)
                print(json.dumps(dict(done=1, **result)), flush=True)
                has_cache = Path(str(recipe_dir/'context.c')+'.m2c').exists()
                with ThreadPoolExecutor(max_workers=workers) as pool:
                    waiting = iter(selected)
                    mapping = {}
                    def schedule():
                        fn = next(waiting, None)
                        if fn is None: return
                        input_sig = input_signatures[fn['name']]
                        ident = queue.claim(fn['name'], recipe, input_sig, run_id)
                        future = pool.submit(attempt, fn, ident, cache, config, recipe_dir, context_text, globals_map, seconds, search_seconds, has_cache)
                        mapping[future] = (ident, fn, input_sig)
                    for _ in range(workers): schedule()
                    done = 1
                    while mapping:
                        future = next(as_completed(mapping))
                        result = future.result()
                        ident, fn, input_sig = mapping.pop(future)
                        record = make_attempt_record(fn, identity, attempt_recipe, result, input_sig, run_id, recipe)
                        queue.finish(ident, result, record)
                        done += 1
                        print(json.dumps(dict(done=done, **result)), flush=True)
                        schedule()
            queue.end_run(run_id, time.monotonic()-run_started)
            return report_cache(queue, recipe)
        finally:
            queue.close()


def report_cache(queue, recipe=None):
    recipe = recipe or queue.meta('last_recipe')
    rows = queue.results(recipe) if recipe else []
    statuses = Counter(row['status'] for row in rows)
    candidates = []
    for row in rows:
        result = json.loads(row['result']) if row['result'] else {}
        if row['status'] == 'linked_match':
            candidates.append(dict(name=row['name'], size=result['size'], source_sha256=result['candidate_sha256'],
                                   code_sha256=result['comparison']['actual_sha256']))
    description = queue.meta('recipe:'+recipe) if recipe else None
    recipe_evidence = {key: description[key] for key in ('context_sha256','source_hashes','m2c_pin','python_version','seconds','search_seconds') if key in description} if description else {}
    if description: recipe_evidence['ido_toolchain_sha256'] = sha(json.dumps(description['ido_files'],sort_keys=True).encode())
    run_rows = list(queue.db.execute('SELECT recipe,started,ended,configuration,selected,elapsed FROM runs WHERE recipe=? ORDER BY id', (recipe,))) if recipe else []
    runs = [dict(row, configuration=json.loads(row['configuration'])) for row in run_rows]
    deferred = []
    for row in rows:
        if row['status'] == 'linked_match': continue
        result = json.loads(row['result']) if row['result'] else {}
        reason = result.get('reason', '')
        if not re.fullmatch(r'[a-z_]+(?::[.a-z_]+)?', reason): reason = row['status']
        deferred.append(dict(name=row['name'],status=row['status'],reason=reason))
    records, legacy_attempts = queue.attempt_records(recipe) if recipe else ([], 0)
    attempt_ledger = dict(format=LEDGER_FORMAT, records=records, legacy_imports=[],
                          legacy_unstructured_attempts=legacy_attempts)
    ledger_errors = validate_ledger(attempt_ledger)
    if ledger_errors:
        raise ValueError('Attempt ledger validation failed: ' + '; '.join(ledger_errors))
    return dict(format='goemon-batch-report-v1', baseline=queue.meta('identity'), verified_reference=queue.meta('reference'),
                recipe=recipe, recipe_evidence=recipe_evidence, runs=runs, deferred_candidates=deferred, latest_attempts=len(rows), statuses=dict(statuses), linked_probe_matches=candidates,
                linked_probe_bytes=sum(row['size'] for row in candidates), newly_verified_full_rom_functions=0,
                attempt_ledger=attempt_ledger)


def export_matches(cache, destination, recipe=None):
    cache, destination = local_storage(cache), local_storage(destination)
    with exclusive_cache(cache):
        queue = Queue(cache/'queue.sqlite')
        try:
            recipe = recipe or queue.meta('last_recipe')
            rows = queue.results(recipe) if recipe else []
            if recipe and not rows and queue.meta('recipe:'+recipe) is None: raise ValueError('Unknown recipe')
            if destination.exists(): raise ValueError('Export destination already exists')
            summary = report_cache(queue, recipe)
            reviewed = []
            for row in rows:
                if row['status'] != 'linked_match': continue
                result = json.loads(row['result'])
                folder = (cache/result['artifacts']).resolve()
                if not folder.is_relative_to(cache): raise ValueError('Invalid artifact path')
                if Path(result['candidate_source']).name != result['candidate_source'] or Path(result['linked_elf']).name != result['linked_elf']:
                    raise ValueError('Invalid candidate artifact name')
                source = folder/result['candidate_source']
                if sha(source.read_bytes()) != result['candidate_sha256']:
                    raise ValueError('Candidate source changed since probing')
                elf_data = (folder/result['linked_elf']).read_bytes()
                if sha(elf_data) != result['linked_elf_sha256']:
                    raise ValueError('Probe ELF changed since matching')
                image = Elf32(elf_data)
                symbol = image.function(row['name'])
                original = queue.db.execute('SELECT address,expected FROM functions WHERE name=?', (row['name'],)).fetchone()
                if symbol.value != original['address'] or image.code(symbol) != original['expected']:
                    raise ValueError('Probe proof disagrees with baseline function')
                reviewed.append((source, row['name']))
            destination.mkdir(parents=True, exist_ok=False)
            for source, name in reviewed: shutil.copyfile(source, destination/(name+'.c'))
            (destination/'review.json').write_text(json.dumps(summary, indent=2)+'\n')
            (destination/'README.txt').write_text('Local review candidates only. No automatic manifest or full-ROM promotion. Review interfaces/data layout, integrate by original unit, test, then run decomp.verify.\n')
            return summary
        finally:
            queue.close()


def prepare_context(baseline, source, output):
    baseline, source, output = Path(baseline).resolve(), Path(source).resolve(), Path(output)
    if output.exists(): raise ValueError('Context output already exists')
    command = ['gcc','-E','-P','-Iinclude','-Ilibultra/include','-Ilibultra/include/PR','-Isrc','-I.',
               '-I'+str(source.parent),'-D_LANGUAGE_C','-D_FINALROM','-DF3DEX_GBI','-D__sgi','-DNDEBUG','-x','c',str(source)]
    content = subprocess.check_output(command,cwd=baseline,text=True,stderr=subprocess.PIPE,timeout=30)
    with output.open('x',encoding='utf-8') as destination: destination.write(content)
    return dict(context_sha256=sha(content.encode()),lines=len(content.splitlines()))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest='command', required=True)
    ctx = subs.add_parser('context')
    ctx.add_argument('--baseline',type=Path,required=True)
    ctx.add_argument('--source',type=Path,required=True)
    ctx.add_argument('--output',type=Path,required=True)
    init = subs.add_parser('init')
    init.add_argument('--cache', type=Path, required=True)
    init.add_argument('--baseline', type=Path, required=True)
    init.add_argument('--m2c', type=Path, required=True)
    init.add_argument('--python', type=Path, required=True)
    init.add_argument('--context', type=Path)
    init.add_argument('--permuter', type=Path)
    work = subs.add_parser('run')
    work.add_argument('--cache', type=Path, required=True)
    work.add_argument('--limit', type=int, default=100)
    work.add_argument('--max-size', type=int, default=128)
    work.add_argument('--workers', type=int, default=2)
    work.add_argument('--seconds', type=float, default=20)
    work.add_argument('--search-seconds', type=float, default=0)
    work.add_argument('--max-attempts', type=int, default=1)
    work.add_argument('--retry', action='store_true')
    work.add_argument('--scope', choices=['generated','all'], default='generated')
    work.add_argument('--region', choices=['all','main','overlays'], default='all')
    work.add_argument('--context', type=Path)
    report = subs.add_parser('report')
    report.add_argument('--cache', type=Path, required=True)
    report.add_argument('--output', type=Path)
    report.add_argument('--recipe', help='Inspect a previous recipe instead of the most recent')
    export = subs.add_parser('export')
    export.add_argument('--cache', type=Path, required=True)
    export.add_argument('--output', type=Path, required=True)
    export.add_argument('--recipe', help='Export a previous matching recipe')
    args = parser.parse_args(argv)
    try:
        if args.command == 'context': result = prepare_context(args.baseline,args.source,args.output)
        elif args.command == 'init': result = initialize(args.cache, args.baseline, args.m2c, args.python, args.context, args.permuter)
        elif args.command == 'run': result = run(args.cache, args.limit, args.max_size, args.workers, args.seconds, args.search_seconds,
                                               args.retry, args.max_attempts, args.scope, args.region, args.context)
        elif args.command == 'export': result = export_matches(args.cache, args.output, args.recipe)
        else:
            with exclusive_cache(args.cache):
                queue = Queue(args.cache/'queue.sqlite')
                try:
                    if args.recipe and not queue.results(args.recipe) and queue.meta('recipe:'+args.recipe) is None: raise ValueError('Unknown recipe')
                    result = report_cache(queue,args.recipe)
                finally: queue.close()
            if args.output:
                with args.output.open('x', encoding='utf-8') as output:
                    json.dump(result, output, indent=2); output.write('\n')
    except (OSError, ValueError, sqlite3.Error, subprocess.SubprocessError) as exc:
        parser.exit(1, str(exc)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
