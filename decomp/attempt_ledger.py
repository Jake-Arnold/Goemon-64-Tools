"""Versioned, fail-closed evidence records for native function probes.

This module records research outcomes. It never promotes a function into the
matching manifest or treats an isolated function probe as a whole-ROM proof.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re


LEDGER_FORMAT = 'goemon-attempt-ledger-v1'
RECORD_FORMAT = 'goemon-function-attempt-v1'
LEGACY_FORMAT = 'goemon-batch-report-v1'
EXACTNESS_TIERS = {'none', 'object', 'isolated_function', 'unit', 'full_rom'}
SHA1_RE = re.compile(r'[0-9a-f]{40}\Z')
SHA256_RE = re.compile(r'[0-9a-f]{64}\Z')


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def _canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode()


def attempt_signature(record):
    payload = {key: value for key, value in record.items()
               if key not in ('attempt_signature', 'record_id')}
    return sha256(_canonical(payload))


def input_signature(function, identity, recipe):
    """Identify reproducible inputs while excluding wall-clock budgets."""
    evidence = {
        'format': 'goemon-attempt-input-v1',
        'function': function['name'],
        'original': {
            'rom_sha1': identity.get('rom_sha1'),
            'elf_sha256': identity.get('elf_sha256'),
            'vma': function['address'],
            'rom_offset': function.get('rom_offset'),
            'rom_offset_evidence': 'ROM_SLICE_CONFIRMED' if function.get('rom_offset') is not None else 'OFFSET_UNRESOLVED',
            'size': function['size'],
            'code_sha256': sha256(function['expected']),
        },
        'unit': function.get('source') or None,
        'assembly_sha256': sha256(function.get('asm', '').encode()),
        'context_sha256': recipe.get('context_sha256'),
        'compiler': {
            'ido_toolchain_sha256': recipe.get('ido_toolchain_sha256'),
            'binutils': recipe.get('binutils'),
            'm2c_pin': recipe.get('m2c_pin'),
            'python_version': recipe.get('python_version'),
            'python_sha256': recipe.get('python_sha256'),
            'dependency_lock_sha256': recipe.get('dependency_lock_sha256'),
            'flags': recipe.get('flags'),
            'pipeline_source_hashes': recipe.get('source_hashes'),
        },
        'search_seconds': recipe.get('search_seconds', 0),
        'permuter_pin': recipe.get('permuter_pin'),
    }
    return sha256(_canonical(evidence))


def _safe_blocker(result):
    status = result.get('status', 'failed')
    reason = result.get('reason')
    if not isinstance(reason, str) or not re.fullmatch(r'[a-z_]+(?::[.a-z_]+)?', reason):
        reason = None
    return {'status': status, 'reason': reason}


def make_attempt_record(function, identity, recipe, result, input_sig, run_id=None, recipe_id=None):
    """Build a sanitized record and validate it before it reaches SQLite."""
    comparison = result.get('comparison') or {}
    status = result.get('status')
    tier = 'isolated_function' if status == 'linked_match' else 'none'
    mismatch_offset = comparison.get('first_mismatch_offset')
    mismatch = None
    if mismatch_offset is not None:
        mismatch = {
            'offset': mismatch_offset,
            'address': function['address'] + mismatch_offset,
        }
    candidate_sha = result.get('candidate_sha256')
    record = {
        'format': RECORD_FORMAT,
        'input_signature': input_sig,
        'function': function['name'],
        'unit': {
            'original_assembly_source': function.get('source') or None,
            'assembly_source_sha256': sha256(function.get('asm', '').encode()),
            'candidate_translation_unit': None,
        },
        'original': {
            'upstream_commit': identity.get('upstream_commit'),
            'rom_sha1': identity.get('rom_sha1'),
            'elf_sha256': identity.get('elf_sha256'),
            'vma': function['address'],
            'rom_offset': function.get('rom_offset'),
            'rom_offset_evidence': 'ROM_SLICE_CONFIRMED' if function.get('rom_offset') is not None else 'OFFSET_UNRESOLVED',
            'size': function['size'],
            'code_sha256': sha256(function['expected']),
        },
        'candidate': {
            'source_sha256': candidate_sha,
            'linked_code_sha256': comparison.get('actual_sha256'),
        },
        'compiler': {
            'ido_toolchain_sha256': recipe.get('ido_toolchain_sha256'),
            'binutils': recipe.get('binutils'),
            'm2c_pin': recipe.get('m2c_pin'),
            'python_version': recipe.get('python_version'),
            'python_sha256': recipe.get('python_sha256'),
            'dependency_lock_sha256': recipe.get('dependency_lock_sha256'),
            'flags': recipe.get('flags'),
            'pipeline_source_hashes': recipe.get('source_hashes', {}),
            'context_sha256': recipe.get('context_sha256'),
        },
        'exactness_tier': tier,
        'tests': {'status': 'NOT_RUN', 'runs': []},
        'comparison': {
            'status': status,
            'first_mismatch': mismatch,
            'failed_word_offsets': comparison.get('word_mismatch_offsets', []),
        },
        'blocker': None if status == 'linked_match' else _safe_blocker(result),
        'proof_run': {
            'run_id': run_id,
            'recipe_id': recipe_id,
            'scope': 'isolated_function' if tier == 'isolated_function' else 'candidate_generation_or_probe',
            'tier': tier,
            'full_rom_match': False,
            'report_sha256': None,
        },
    }
    signature = attempt_signature(record)
    record['attempt_signature'] = signature
    record['record_id'] = 'sha256:' + signature
    errors = validate_attempt_record(record)
    if errors:
        raise ValueError('Invalid generated attempt record: ' + '; '.join(errors))
    return record


def validate_attempt_record(record):
    """Return schema/proof-boundary errors for one immutable attempt record."""
    errors = []
    if not isinstance(record, dict) or record.get('format') != RECORD_FORMAT:
        return ['Unsupported attempt record format']
    original = record.get('original')
    if not isinstance(original, dict):
        return ['Missing original function provenance']
    if not isinstance(original.get('upstream_commit'), str) or not re.fullmatch(r'[0-9a-f]{40}', original['upstream_commit']):
        errors.append('Missing original upstream provenance')
    if not isinstance(original.get('rom_sha1'), str) or not SHA1_RE.fullmatch(original['rom_sha1']):
        errors.append('Missing or malformed original ROM identity')
    if not isinstance(original.get('elf_sha256'), str) or not SHA256_RE.fullmatch(original['elf_sha256']):
        errors.append('Missing or malformed original ELF identity')
    if not isinstance(original.get('vma'), int) or original['vma'] <= 0:
        errors.append('Missing original function VMA')
    if not isinstance(original.get('size'), int) or original['size'] <= 0:
        errors.append('Missing original function size')
    if original.get('rom_offset') is not None and (
            not isinstance(original.get('rom_offset'), int) or original['rom_offset'] < 0):
        errors.append('Malformed original ROM offset')
    if original.get('rom_offset_evidence') not in ('ROM_SLICE_CONFIRMED', 'OFFSET_UNRESOLVED'):
        errors.append('Missing original ROM offset evidence')
    if ((original.get('rom_offset') is None) != (original.get('rom_offset_evidence') == 'OFFSET_UNRESOLVED')):
        errors.append('Original ROM offset and evidence disagree')
    if not isinstance(original.get('code_sha256'), str) or not SHA256_RE.fullmatch(original['code_sha256']):
        errors.append('Missing original function bytes hash')
    if not isinstance(record.get('function'), str) or not record['function']:
        errors.append('Missing function name')
    if not isinstance(record.get('input_signature'), str) or not SHA256_RE.fullmatch(record['input_signature']):
        errors.append('Missing input signature')
    candidate = record.get('candidate')
    if not isinstance(candidate, dict):
        errors.append('Missing candidate provenance')
    else:
        for key in ('source_sha256', 'linked_code_sha256'):
            value = candidate.get(key)
            if value is not None and (not isinstance(value, str) or not SHA256_RE.fullmatch(value)):
                errors.append('Malformed candidate ' + key)
    compiler = record.get('compiler')
    if not isinstance(compiler, dict):
        errors.append('Missing compiler provenance')
    else:
        for key in ('ido_toolchain_sha256', 'python_sha256', 'dependency_lock_sha256', 'context_sha256'):
            if not isinstance(compiler.get(key), str) or not SHA256_RE.fullmatch(compiler[key]):
                errors.append('Missing or malformed compiler ' + key)
        if not isinstance(compiler.get('m2c_pin'), str) or not re.fullmatch(r'[0-9a-f]{40}', compiler['m2c_pin']):
            errors.append('Missing or malformed compiler m2c_pin')
        if not isinstance(compiler.get('python_version'), str) or not compiler['python_version']:
            errors.append('Missing compiler Python version')
        if not isinstance(compiler.get('flags'), list) or any(not isinstance(flag, str) for flag in compiler['flags']):
            errors.append('Missing compiler flags')
        binutils = compiler.get('binutils')
        if (not isinstance(binutils, dict) or not binutils
                or any(not isinstance(value, str) or not SHA256_RE.fullmatch(value) for value in binutils.values())):
            errors.append('Missing or malformed binutils hashes')
        source_hashes = compiler.get('pipeline_source_hashes')
        if (not isinstance(source_hashes, dict) or not source_hashes
                or any(not isinstance(value, str) or not SHA256_RE.fullmatch(value) for value in source_hashes.values())):
            errors.append('Missing or malformed pipeline source hashes')
    if record.get('exactness_tier') not in EXACTNESS_TIERS:
        errors.append('Invalid exactness tier')
    unit = record.get('unit')
    if (not isinstance(unit, dict) or 'original_assembly_source' not in unit
            or not isinstance(unit.get('assembly_source_sha256'), str)
            or not SHA256_RE.fullmatch(unit.get('assembly_source_sha256', ''))
            or 'candidate_translation_unit' not in unit):
        errors.append('Missing unit ownership fields')
    elif record.get('exactness_tier') in ('unit', 'full_rom') and (
            not isinstance(unit.get('candidate_translation_unit'), str)
            or not unit['candidate_translation_unit']):
        errors.append('Unit exactness requires candidate translation-unit ownership')
    elif record.get('exactness_tier') == 'isolated_function' and unit.get('candidate_translation_unit') is not None:
        errors.append('Isolated function probe cannot claim translation-unit ownership')
    tests = record.get('tests')
    if not isinstance(tests, dict) or tests.get('status') not in ('NOT_RUN', 'PASS', 'FAIL') or not isinstance(tests.get('runs'), list):
        errors.append('Malformed test evidence')
    elif (tests['status'] == 'NOT_RUN' and tests['runs']) or (
            tests['status'] in ('PASS', 'FAIL') and not tests['runs']):
        errors.append('Test status and recorded test runs disagree')
    comparison = record.get('comparison')
    if not isinstance(comparison, dict) or not isinstance(comparison.get('failed_word_offsets'), list):
        errors.append('Malformed comparison evidence')
    else:
        offsets = comparison['failed_word_offsets']
        if comparison.get('status') not in ('linked_match', 'mismatch', 'needs_layout', 'compile_failed',
                                            'unresolved_symbols', 'link_failed', 'generation_failed',
                                            'needs_context', 'unsupported', 'needs_source', 'timeout', 'failed'):
            errors.append('Missing or invalid attempt comparison status')
        if any(not isinstance(offset, int) or offset < 0 or offset % 4 for offset in offsets):
            errors.append('Malformed failed-word offsets')
        if offsets != sorted(set(offsets)):
            errors.append('Failed-word offsets must be sorted and unique')
        first = comparison.get('first_mismatch')
        if first is not None and (not isinstance(first, dict)
                                  or not isinstance(first.get('offset'), int)
                                  or first['offset'] < 0
                                  or first.get('address') != original.get('vma', -1) + first['offset']):
            errors.append('Malformed first mismatch provenance')
        if first is None and offsets:
            errors.append('Failed words require a first mismatch')
        if first is not None and offsets and first.get('offset') != offsets[0]:
            errors.append('First mismatch must be the first failed word')
    blocker = record.get('blocker')
    if record.get('exactness_tier') == 'none' and not isinstance(blocker, dict):
        errors.append('Non-exact attempt requires a blocker')
    if record.get('exactness_tier') != 'none' and blocker is not None:
        errors.append('Exact attempt cannot carry a failure blocker')
    proof = record.get('proof_run')
    if not isinstance(proof, dict):
        errors.append('Missing proof-run classification')
    else:
        tier = record.get('exactness_tier')
        if not isinstance(proof.get('run_id'), int) or proof['run_id'] <= 0:
            errors.append('Missing proof-run identifier')
        if not isinstance(proof.get('recipe_id'), str) or not SHA256_RE.fullmatch(proof['recipe_id']):
            errors.append('Missing proof-run recipe identity')
        expected_scope = {
            'none': 'candidate_generation_or_probe',
            'object': 'object',
            'isolated_function': 'isolated_function',
            'unit': 'translation_unit',
            'full_rom': 'full_rom',
        }.get(tier)
        if proof.get('scope') != expected_scope:
            errors.append('Proof-run scope disagrees with exactness tier')
        if proof.get('tier') != tier:
            errors.append('Proof tier and exactness tier disagree')
        if tier == 'isolated_function' and (
                not isinstance(candidate, dict)
                or not isinstance(candidate.get('source_sha256'), str)
                or not SHA256_RE.fullmatch(candidate['source_sha256'])
                or not isinstance(candidate.get('linked_code_sha256'), str)
                or not SHA256_RE.fullmatch(candidate['linked_code_sha256'])):
            errors.append('Isolated exactness requires candidate source and linked-code hashes')
        if tier in ('none', 'object', 'isolated_function', 'unit') and proof.get('full_rom_match') is not False:
            errors.append('Non-ROM proof is conflated with full-ROM proof')
        if tier == 'full_rom':
            if proof.get('full_rom_match') is not True or not isinstance(proof.get('report_sha256'), str) or not SHA256_RE.fullmatch(proof['report_sha256']):
                errors.append('Full-ROM exactness requires a bound successful proof report')
            if proof.get('rom_sha1') != original.get('rom_sha1'):
                errors.append('Full-ROM proof identity must match the original ROM')
            if original.get('rom_offset') is None or original.get('rom_offset_evidence') != 'ROM_SLICE_CONFIRMED':
                errors.append('Full-ROM exactness requires a confirmed original ROM extent')
            for key in ('manifest_sha256', 'inventory_sha256'):
                if not isinstance(proof.get(key), str) or not SHA256_RE.fullmatch(proof[key]):
                    errors.append('Full-ROM exactness requires ' + key)
    if record.get('attempt_signature') != attempt_signature(record):
        errors.append('Attempt signature does not match record contents')
    if record.get('record_id') != 'sha256:' + str(record.get('attempt_signature')):
        errors.append('Record ID does not match attempt signature')
    return errors


def validate_ledger(ledger):
    if not isinstance(ledger, dict) or ledger.get('format') != LEDGER_FORMAT:
        return ['Unsupported attempt ledger format']
    records = ledger.get('records')
    if not isinstance(records, list):
        return ['Attempt ledger records must be a list']
    errors = []
    seen = set()
    for record in records:
        errors.extend(validate_attempt_record(record))
        record_id = record.get('record_id') if isinstance(record, dict) else None
        if record_id in seen:
            errors.append('Duplicate immutable record ID: ' + str(record_id))
        seen.add(record_id)
    legacy = ledger.get('legacy_imports', [])
    if not isinstance(legacy, list):
        errors.append('Legacy imports must be a list')
    else:
        for item in legacy:
            if not isinstance(item, dict) or item.get('original_provenance') != 'INCOMPLETE' or item.get('attempt_signature') is not None:
                errors.append('Legacy imports must remain unsigned and provenance-incomplete')
    return errors


def import_legacy_report_bytes(raw):
    """Project a historical v1 report without changing it or upgrading its proof."""
    report = json.loads(raw)
    if not isinstance(report, dict) or report.get('format') != LEGACY_FORMAT:
        raise ValueError('Expected a goemon-batch-report-v1 report')
    if report.get('newly_verified_full_rom_functions') != 0:
        raise ValueError('Legacy batch report has an unexpected full-ROM promotion count')
    linked = report.get('linked_probe_matches', [])
    if not isinstance(linked, list):
        raise ValueError('Malformed legacy linked-probe list')
    summaries = []
    for item in linked:
        if not isinstance(item, dict) or not isinstance(item.get('name'), str) or not isinstance(item.get('size'), int):
            raise ValueError('Malformed legacy candidate summary')
        summaries.append({
            'function': item['name'],
            'size': item['size'],
            'candidate_source_sha256': item.get('source_sha256'),
            'candidate_code_sha256': item.get('code_sha256'),
            'original_provenance': 'INCOMPLETE',
            'exactness_tier': 'legacy_isolated_candidate',
            'attempt_signature': None,
        })
    imported = {
        'format': 'goemon-legacy-report-import-v1',
        'source_format': LEGACY_FORMAT,
        'source_report_sha256': sha256(raw),
        'baseline': report.get('baseline'),
        'candidate_summaries': summaries,
        'newly_verified_full_rom_functions': 0,
        'original_provenance': 'INCOMPLETE',
        'attempt_signature': None,
    }
    return imported


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    legacy = sub.add_parser('import-legacy', help='read-only import of a historical v1 batch report')
    legacy.add_argument('--report', type=Path, required=True)
    legacy.add_argument('--output', type=Path, help='create a new import file; existing files are never replaced')
    args = parser.parse_args(argv)
    try:
        result = import_legacy_report_bytes(args.report.read_bytes())
        rendered = json.dumps(result, indent=2, ensure_ascii=False) + '\n'
        if args.output:
            with args.output.open('x', encoding='utf-8') as stream:
                stream.write(rendered)
        else:
            print(rendered, end='')
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
