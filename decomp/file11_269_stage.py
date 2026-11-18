"""Opt-in deduplicated 269-function USA file_11 central C/ASM stage.

This adapter extends the proven 187-function stage by precisely 82
new original-ROM function identities (3,512 bytes). Its fixture is pinned
by the original retail decompressed ROM and by native per-object hashes.
"""
from __future__ import annotations
from collections import Counter
import copy,hashlib,json,re
from pathlib import Path
from . import overlay_file11,file11_187_stage
from .research.file11_143_candidate.verify_file11_143 import read_relocations,read_symbols,trim_text_object

ROOT=Path(__file__).resolve().parent
FIXTURE=ROOT/'research/file11_143_candidate/file11_269_allpending_source_fixture.json'
STAGE_FORMAT='goemon-file11-269-central-v1'
START=0x587370;END=0x5B8500
OLD_SPLAT='    - [0x587370, asm]\n    - [0x5B8500, data]'
OLD_LINKER='.file_11 0x801CB460 : AT(file_11_ROM_START) SUBALIGN(16)'
NEW_LINKER=OLD_LINKER.replace('SUBALIGN(16)','SUBALIGN(4)')
LEGACY_NOP_ALIAS_ASM_OFFSETS=frozenset((0x5995E8,0x59D4DC,0x5AEBDC))


def sha256(data:bytes)->str:return hashlib.sha256(data).hexdigest()

def load_fixture():return json.loads(FIXTURE.read_text())

def entries():
    return [{'name':f['name'],'rom_offset':f['off'],'vma':f['vma'],'size':f['size']}
            for c in load_fixture()['chunks'] if c['kind']=='c' for f in c['functions']]

def reviewed_plan(manifest:dict,original_rom:bytes|None=None):
    if manifest.get('overlay_file11_stage')!={'format':STAGE_FORMAT}:raise ValueError('Not a reviewed 269 stage manifest')
    base_manifest=copy.deepcopy(manifest)
    # Later main/overlay stages must not contaminate the historical 210-C preflight.
    base_manifest.pop("overlay_native87_stage", None)
    base_manifest.pop("overlay_highbyte26_stage", None)
    base_manifest.pop("overlay_file27_stage", None)
    if 'overlay_crossregion47_stage' in base_manifest:
        from . import overlay_crossregion47 as cross
        if base_manifest.pop('overlay_crossregion47_stage') != {'format':cross.STAGE_FORMAT}:
            raise ValueError('Unreviewed cross-overlay stage in 269-C historical audit')
    base_manifest['overlay_file11_stage']={'format':file11_187_stage.STAGE_FORMAT}
    previous=file11_187_stage.reviewed_plan(base_manifest,original_rom)
    old=file11_187_stage.load_fixture()['chunks'];new=load_fixture()['chunks'];d=load_fixture()
    if (len(old)!=142 or d['total_represented_functions']!=269 or d['all_C_text_bytes']!=9088 or
            d['unique_new_C']!=82 or d['unique_new_C_bytes']!=3512 or len(entries())!=269 or
            len({f['rom_offset'] for f in entries()})!=269 or len(new)!=240):
        raise ValueError('file11_184 source fixture extent/identity changed')
    for c in new:
        a,b=c['rom_start'],c['rom_end']
        if a<START or b>END or a>=b or c['size']!=b-a or a%4 or b%4:raise ValueError('Invalid original file11 chunk interval')
        if original_rom is not None and sha256(original_rom[a:b])!=c['original_sha256']:
            raise ValueError('Original file11 slice bytes mismatch: '+hex(a))
        if c['kind']=='c':
            if sha256(c['source'].encode())!=c['source_sha256'] or 'GLOBAL_ASM' in c['source']:
                raise ValueError('Unreviewed file11 source: '+str(c['name']))
            if sum(f['size'] for f in c['functions'])!=c['size']:
                raise ValueError('C ownership interval mismatch')
            if any(f['vma']!=overlay_file11.VMA_START+f['off']-START for f in c['functions']):
                raise ValueError('Mismatched original function VMA')
    if new[0]['rom_start']!=START or new[-1]['rom_end']!=END or any(a['rom_end']!=b['rom_start'] for a,b in zip(new,new[1:])):
        raise ValueError('Noncontinuous overlay source ownership')
    all_entries=entries()
    if (len({f['name'] for f in all_entries})!=len(all_entries) or
            len({f['vma'] for f in all_entries})!=len(all_entries)):
        raise ValueError('Duplicate original function identity in 269-file11 fixture')
    expected_c={(f['name'],f['rom_offset'],f['size']) for f in file11_187_stage.entries()}
    actual_c={(f['name'],f['rom_offset'],f['size']) for f in entries()}
    if not expected_c.issubset(actual_c) or len(actual_c-expected_c)!=82:
        raise ValueError('Promotion overlaps/forgets a previously promoted function')
    for c in old:
        child=[n for n in new if c['rom_start']<=n['rom_start']<c['rom_end']]
        if not child or child[0]['rom_start']!=c['rom_start'] or child[-1]['rom_end']!=c['rom_end']:
            raise ValueError('Parent layout not preserved')
        if c['kind']=='c' and (len(child)!=1 or child[0]!=c):
            raise ValueError('Previously promoted C source changed in the 269 stage')
        if c['kind']=='asm' and any(n['kind'] not in ('asm','c') for n in child):
            raise ValueError('Unknown ASM split owner')
    return {'ordered_segments':[(c['rom_start'],c['kind'],c['name']) for c in new],
            'c_sources':{c['name']:c['source'] for c in new if c['kind']=='c'},
            'chunks':len(new),'c_units':sum(c['kind']=='c' for c in new),'asm_slices':sum(c['kind']=='asm' for c in new),
            'file11_c_total':269,'file11_c_instruction_bytes':9088}

def stage_splat(original:str,plan:dict)->str:
    overlay_file11.stage_config(original)
    matches=list(re.finditer(r'(?m)^  - name: (\S+)\s*$',original));names=[m.group(1) for m in matches]
    pos=names.index('file_11');i=matches[pos].start();j=matches[pos+1].start()
    block=original[i:j]
    if block.count(OLD_SPLAT)!=1 or len(plan['ordered_segments'])!=240:raise ValueError('Pinned original file11 Splat section lost')
    inserted='\n'.join(f'    - [0x{a:X}, {kind}'+(f', {stem}' if kind=='c' else '')+']'
                       for a,kind,stem in plan['ordered_segments'])+'\n    - [0x5B8500, data]'
    return original[:i]+block.replace(OLD_SPLAT,inserted,1)+original[j:]

def source_payloads(checkout:Path,plan:dict):
    out=[]
    for stem,source in plan['c_sources'].items():
        if not re.fullmatch('[a-z][a-z0-9_]*',stem):raise ValueError('Unsafe source name')
        dst=Path(checkout)/'src'/(stem+'.c')
        if dst.exists():raise ValueError('Source filename collision')
        out.append((dst,source))
    if len(out)!=166 or len({p for p,_ in out})!=166:raise ValueError('Expected exactly 166 C object sources')
    return out

def source_objects():
    out=[]
    for c in load_fixture()['chunks']:
        p=(Path('build/usa/src')/(c['name']+'.c.o')) if c['kind']=='c' else (Path('build/usa/asm/usa')/(f"{c['rom_start']:X}.s.o"))
        out.append((p,c['size'],c))
    return out

def object_targets():return [p.as_posix() for p,_,_ in source_objects()]

def normalize_added_nop_alias(checkout:Path):
    """Preserve all prior original NOP-label corrections exactly once.

    The 82 candidate boundaries target original function starts, never a
    synthetic four-byte NOP. Keep the separately reviewed 187-C fixes.
    """
    return file11_187_stage.normalize_added_nop_alias(checkout)


def prepare_objects(checkout:Path):
    staged=[]
    for path,size,c in source_objects():
        raw=(Path(checkout)/path).read_bytes()
        adjusted=trim_text_object(raw,size)
        actual=sha256(adjusted)
        if actual!=c['trimmed_obj_sha256']:
            if c['kind']=='asm' and c['rom_start'] in LEGACY_NOP_ALIAS_ASM_OFFSETS:
                pass  # Proven old 50-function nop-alias normalization; code and relocations unchanged.
            else:
                raise ValueError(f'269 native object hash differs: {path}: {actual} expected {c["trimmed_obj_sha256"]}')
        staged.append((Path(checkout)/path,adjusted))
    script=Path(checkout)/'.splat/usa/mnsg.ld';s=script.read_text()
    if s.count(OLD_LINKER)!=1:raise ValueError('Pinned file11 linker alignment lost')
    for p,b in staged:p.write_bytes(b)
    script.write_text(s.replace(OLD_LINKER,NEW_LINKER,1))
    return {'format':'goemon-file11-269-exact-object-layout-v1','objects_original_address_exact':len(staged),
            'original_source_C_objects':166,'original_source_ASM_objects':74,
            'unreviewed_object_hashes':[]}

def verify_linked(checkout:Path,expected_rom:bytes,original_elf:Path):
    c=Path(checkout);assembled=(c/'build/usa/mnsg.z64').read_bytes()
    if len(expected_rom)!=33554432 or assembled!=expected_rom or hashlib.sha1(assembled).hexdigest()!=overlay_file11.ROM_SHA1:
        raise ValueError('269 C not exact 32 MiB USA ROM')
    before=read_relocations(Path(original_elf));after=read_relocations(c/'build/usa/mnsg.elf')
    if len(before)!=8825 or len(after)!=8825 or Counter(before)!=Counter(after):raise ValueError('file11 relocation tuples differ')
    syms=read_symbols(c/'build/usa/mnsg.elf')
    for fn in entries():
        if syms.get(fn['name'])!=(fn['vma'],fn['size']):raise ValueError('Original func name VMA size changed '+fn['name'])
    mapped=(c/'build/usa/mnsg.map').read_text()
    for path,size,chunk in source_objects():
        expected_vma=overlay_file11.VMA_START+chunk['rom_start']-START
        pattern=r'(?m)^\s*\.text\s+0x([0-9a-fA-F]+)\s+0x([0-9a-fA-F]+)\s+'+re.escape(path.as_posix())+r'\s*$'
        matches=re.findall(pattern,mapped)
        if len(matches)!=1 or tuple(int(x,16) for x in matches[0])!=(expected_vma,size):raise ValueError('Link map object shift '+path.as_posix())
        raw=(c/path).read_bytes()
        if sha256(raw)!=chunk['trimmed_obj_sha256']:
            if chunk['kind']=='asm' and chunk['rom_start'] in LEGACY_NOP_ALIAS_ASM_OFFSETS:pass
            else:raise ValueError('Post-link object identity differs '+path.as_posix())
        if chunk['kind']=='c' and sha256((c/'src'/(chunk['name']+'.c')).read_bytes())!=chunk['source_sha256']:
            raise ValueError('Post-compile C source changed')
    return {'format':'goemon-file11-269-original-link-v1','status':'PASS',
            'original_address_matching_c':269,'file11_C_instruction_bytes':9088,
            'original_native_object_provenance_checked':len(source_objects()),
            'original_semantic_file11_relocations':8825,'candidate_semantic_file11_relocations':8825,
            'original_rom_sha1':overlay_file11.ROM_SHA1,'complete_rom_bytes_equal':len(assembled)}
