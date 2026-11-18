"""Fail-closed staging of the 87 native-exact original-USA main/overlay functions.

Runs *after* the existing canonical overlay split stages. Splits only the
remaining linked assembly fragments; never mutates original input code bytes.
"""
from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import subprocess

from . import overlay_crossregion47 as cross

ROOT = Path(__file__).resolve().parent
SOURCE_BASE = ROOT / 'research/usa_main_overlay_87_20261118/sources'
FIXTURE = ROOT / 'research/usa_main_overlay_87_20261118/promotion_manifest.json'
STAGE_FORMAT = 'goemon-usa-main-overlay-87-original-c-v1'
RETAIL_SHA1 = '6ea0ed71032ce08fc2745f412d84936382197494'
OVERLAY_NAMES = ('main', 'file_13', 'file_14', 'file_15', 'file_17', 'file_18', 'file_19', 'file_20')
FUNCTION_MARKER = re.compile(r'(?m)^nonmatching (func_[0-9A-F]{8}_[0-9A-F]+), 0x([0-9A-Fa-f]+)$')
TEXT_WORD = re.compile(r'/\* ([0-9A-F]{4,6}) [0-9A-F]{8} [0-9A-F]{8} \*/')
LINKED_ASM = re.compile(r'build/usa/asm/usa/([A-Za-z0-9_]+)\.s\.o\(\.text\);')


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def load_fixture() -> dict:
    doc = json.loads(FIXTURE.read_text(encoding='utf-8'))
    if set(doc) != {'format', 'original_rom_sha1', 'functions'} or doc['format'] != STAGE_FORMAT or doc['original_rom_sha1'] != RETAIL_SHA1:
        raise ValueError('Unreviewed native87 fixture format/ROM')
    rows = doc['functions']
    if len(rows) != 87 or sum(e['size'] for e in rows) != 912:
        raise ValueError('Native87 candidate number/bytes changed')
    names, offsets = set(), set()
    for entry in rows:
        if set(entry) != {'name','rom_offset','vma','size','section','source_sha256','original_code_sha256','original_asm'}:
            raise ValueError('Unexpected native87 candidate metadata')
        name, off, size = entry['name'], entry['rom_offset'], entry['size']
        m = re.fullmatch(r'func_([0-9A-F]{8})_([0-9A-F]{4,6})',name)
        if (not m or int(m[1],16) != entry['vma'] or int(m[2],16) != off or
            size < 8 or size % 4 or off % 4 or entry['section'] not in OVERLAY_NAMES or
            name in names or off in offsets or not re.fullmatch('[0-9a-f]{64}',entry['source_sha256']) or
            not re.fullmatch('[0-9a-f]{64}',entry['original_code_sha256'])):
            raise ValueError('Unsafe/duplicate native87 original address '+name)
        names.add(name); offsets.add(off)
    return doc


def validate_sources(rom:bytes, fixture:dict, source_base:Path=SOURCE_BASE) -> None:
    # Source hashes are checked first so mutation tests can fail closed
    # without bundling a copyrighted 32 MiB original ROM.
    for e in fixture['functions']:
        name,off,size = e['name'],e['rom_offset'],e['size']
        src = source_base/(name+'.c')
        if not src.is_file() or sha256(src.read_bytes()) != e['source_sha256']:
            raise ValueError('Native87 C source modified: '+name)
    if len(rom) != 33554432 or hashlib.sha1(rom).hexdigest() != RETAIL_SHA1:
        raise ValueError('Not original decompressed USA ROM')
    for e in fixture['functions']:
        name,off,size = e['name'],e['rom_offset'],e['size']
        if sha256(rom[off:off+size]) != e['original_code_sha256']:
            raise ValueError('Native87 original code differs: '+name)


def find_owners(checkout:Path, fixture:dict):
    """Find unique *currently linked* assembly owners, not stale Splat parents."""
    checkout=Path(checkout)
    linker=(checkout/'.splat/usa/mnsg.ld').read_text(encoding='utf-8')
    owners={}
    active=set(LINKED_ASM.findall(linker))
    if not active:
        raise ValueError('No active original ASM linker objects')
    names={e['name'] for e in fixture['functions']}
    for parent in sorted(active):
        path=checkout/'asm/usa'/(parent+'.s')
        if not path.is_file():raise ValueError('Missing active original ASM: '+parent)
        body=path.read_text(encoding='utf-8')
        for name,size_hex in FUNCTION_MARKER.findall(body):
            if name in names:
                if name in owners:raise ValueError('Native87 target has two active ASM owners: '+name)
                owners[name]=(parent,int(size_hex,16))
    if set(owners)!=names:
        raise ValueError('Native87 targets no longer singly ASM owned: '+str(sorted(names-set(owners))))
    return owners


def parent_targets(owners:dict) -> list[str]:
    return [f'build/usa/asm/usa/{p}.s.o' for p in sorted({p for p,_ in owners.values()})]


def _span(body:str):
    words=[int(n,16) for n in TEXT_WORD.findall(body)]
    if not words or any(b-a != 4 for a,b in zip(words,words[1:])):
        raise ValueError('Non-contiguous original ASM instruction comments')
    return words[0], words[-1]+4


def stage_linker(checkout:Path,rom:bytes,fixture:dict,owners:dict,source_base:Path=SOURCE_BASE):
    validate_sources(rom,fixture,source_base)
    checkout=Path(checkout);ld=checkout/'.splat/usa/mnsg.ld'
    linker=ld.read_text(encoding='utf-8')
    grouped={}
    for e in fixture['functions']:
        parent,original_size=owners[e['name']]
        if original_size != e['size']:
            raise ValueError('Native87 ASM extent changed: '+e['name'])
        grouped.setdefault(parent,[]).append(e)
    assembled=[];functions=[];parent_rows=[]
    for parent,entries in sorted(grouped.items()):
        entries.sort(key=lambda e:e['rom_offset'])
        input_file=checkout/'asm/usa'/(parent+'.s')
        full=input_file.read_text(encoding='utf-8')
        spl=full.find('/* Generated by')
        if spl<0:
            # Crossregion47-generated fragments retain the assembler directives
            # but often omit the original spimdisasm provenance comment.
            first=FUNCTION_MARKER.search(full)
            first_instruction=TEXT_WORD.search(full)
            if first is None or first_instruction is None:
                raise ValueError('Unrecognised original ASM header: '+parent)
            # Crossregion47 fragments may start with isolated nop words *before*
            # their first original function marker. Those words belong to ASM.
            spl=min(first.start(),first_instruction.start())
        header=full[:spl];body=full[spl:]
        begin,end=_span(body)
        obj=checkout/f'build/usa/asm/usa/{parent}.s.o'
        cross._object_nontext_empty(obj)
        replacement=[];cursor=0;position=begin
        for i,e in enumerate(entries):
            name,target,size=e['name'],e['rom_offset'],e['size']
            m=re.search(r'(?m)^nonmatching '+re.escape(name)+r', 0x([0-9A-Fa-f]+)$',body)
            if not m or int(m[1],16)!=size or target < position or target+size > end or m.start()<cursor:
                raise ValueError('Native87 target outside linked ASM span: '+name)
            leading=body[cursor:m.start()]
            if position<target:
                if _span(leading)!=(position,target):
                    raise ValueError('Lost original pre-C ASM range: '+name)
                name_asm=f'{parent}_n87_{i:02}'
                (checkout/'asm/usa'/(name_asm+'.s')).write_text(header+leading,encoding='utf-8')
                replacement.append(f'build/usa/asm/usa/{name_asm}.s.o')
                assembled.append({'object':replacement[-1],'start':position,'end':target})
            elif TEXT_WORD.search(leading):
                raise ValueError('Unexpected original ASM before C boundary '+name)
            endmarker=body.find('endlabel '+name,m.end())
            if endmarker<0:raise ValueError('Missing function endlabel: '+name)
            endmarker+=len('endlabel '+name)
            block=body[m.start():endmarker]
            if _span(block)!=(target,target+size) or len(FUNCTION_MARKER.findall(block))!=1:
                raise ValueError('Native87 function block extent changed: '+name)
            out=checkout/'src'/(name+'.c')
            if out.exists():raise ValueError('Collision in existing canonical C: '+name)
            out.write_bytes((source_base/(name+'.c')).read_bytes())
            replacement.append(f'build/usa/src/{name}.c.o')
            functions.append(e)
            position=target+size;cursor=endmarker
        if position<end:
            tail=body[cursor:]
            if _span(tail)!=(position,end):raise ValueError('Lost original trailing ASM: '+parent)
            name_asm=f'{parent}_n87_{len(entries):02}'
            (checkout/'asm/usa'/(name_asm+'.s')).write_text(header+tail,encoding='utf-8')
            replacement.append(f'build/usa/asm/usa/{name_asm}.s.o')
            assembled.append({'object':replacement[-1],'start':position,'end':end})
        original=f'build/usa/asm/usa/{parent}.s.o(.text);'
        if linker.count(original)!=1:raise ValueError('Original ASM linker ownership changed: '+parent)
        linker=linker.replace(original,'\n'.join(item+'(.text);' for item in replacement),1)
        for section in ('.data','.rodata','.bss'):
            old=f'build/usa/asm/usa/{parent}.s.o({section});'
            if linker.count(old)>1:raise ValueError('Native87 duplicate nontext ownership '+parent)
            linker=linker.replace(old,'')
        children=[(item['object'],item['start'],item['end']) for item in assembled
                  if item['object'].startswith(f'build/usa/asm/usa/{parent}_n87_')]
        children += [(f'build/usa/src/{e["name"]}.c.o',e['rom_offset'],e['rom_offset']+e['size'])
                     for e in entries]
        children.sort(key=lambda part:part[1])
        if (not children or children[0][1]!=begin or children[-1][2]!=end or
                any(left[2]!=right[1] for left,right in zip(children,children[1:]))):
            raise ValueError('Native87 split changed original continuous ASM extent '+parent)
        parent_rows.append({'source':parent,'start':begin,'end':end,
                            'new_c':len(entries),'children':children})
    # file_20 originally links one unsplit 16-byte-aligned ASM object.
    # New original 8-byte functions need 4-byte object subalignment.
    anchor=re.compile(r'(?m)^(\s*\.file_20\s+0x[0-9A-F]+\s*:\s*AT\([^)]+\)) SUBALIGN\(16\)')
    linker,changed=anchor.subn(r'\1 SUBALIGN(4)',linker)
    if changed!=1:raise ValueError('Original file_20 linker subalignment unexpectedly differs')
    if len(functions)!=87 or sum(e['size'] for e in functions)!=912:
        raise ValueError('Native87 original-source split incomplete')
    ld.write_text(linker,encoding='utf-8')
    return {'functions':functions,'assembly':assembled,'parents':parent_rows,
            'linker_sha256':sha256(linker.encode())}


def object_targets(plan):
    return [f'build/usa/src/{e["name"]}.c.o' for e in plan['functions']]+[a['object'] for a in plan['assembly']]


def pack_objects(checkout:Path,rom:bytes,plan:dict):
    checkout=Path(checkout)
    compiled=[];assembly=[]
    for entry in plan['functions']:
        name,off,size=entry['name'],entry['rom_offset'],entry['size']
        path=checkout/f'build/usa/src/{name}.c.o'
        compiled.append({'name':name,**cross._trim_object(path,size,rom[off:off+size],name=name)})
    for entry in plan['assembly']:
        path=checkout/entry['object'];start,end=entry['start'],entry['end']
        assembly.append({'object':entry['object'],**cross._trim_object(path,end-start,rom[start:end])})
    return {'functions':len(compiled),'bytes':sum(x['original_text_bytes'] for x in compiled),
            'c_packed':compiled,'asm_packed':assembly}


def _main_entry_relocations(elf:Path) -> dict[str,list[tuple]]:
    """Read all original main/entry REL sites, excluding only symbol-index metadata."""
    sections={};active=None
    for row in subprocess.check_output(['readelf','-Wr',str(elf)],text=True).splitlines():
        found=re.match(r"Relocation section '\.rel\.(main|entry)' at offset 0x[0-9a-f]+ contains (\d+) entries",row)
        if found:
            active=found[1]
            if active in sections:raise ValueError('Duplicate main/entry REL section')
            sections[active]=[]
            continue
        if row.startswith('Relocation section '):active=None
        if active:
            cells=row.split()
            if len(cells)>=5 and cells[2].startswith('R_MIPS_'):
                sections[active].append((int(cells[0],16),cells[2],cells[3],cells[4],''.join(cells[5:])))
    if set(sections)!={'main','entry'}:
        raise ValueError('Missing original main or entry REL section')
    return sections


def _relocation_fingerprint(rows:list[tuple]) -> str:
    return sha256(json.dumps(sorted(rows),separators=(',',':')).encode())


def verify_link(baseline:Path,candidate:Path,rom:bytes,plan:dict,fixture:dict):
    baseline=Path(baseline);candidate=Path(candidate)
    bimg=(candidate/'build/usa/mnsg.z64').read_bytes()
    if bimg!=rom or hashlib.sha1(bimg).hexdigest()!=RETAIL_SHA1:
        raise ValueError('Native87 canonical combined full USA ROM mismatch')
    orig=baseline/'build/usa/mnsg.elf';built=candidate/'build/usa/mnsg.elf'
    old_funcs=cross._funcs(orig);new_funcs=cross._funcs(built)
    annotation_removed=Counter({('func_8000D3B8_DFB8',0x8000D3B8,64):1,('func_8003F6E8_402E8',0x8003F6E8,48):1})
    annotation_added=Counter({('func_8000D3B8_DFB8',0x8000D3B8,72):1,('func_8003F6E8_402E8',0x8003F6E8,56):1})
    if (sum(old_funcs.values())!=7376 or sum(new_funcs.values())!=7376 or
        old_funcs-new_funcs!=annotation_removed or new_funcs-old_funcs!=annotation_added):
        raise ValueError('Native87 original ELF FUNC entries changed')
    # The 864-C accepted production baseline had already replaced 105 original
    # .rel.main records (15,058 -> 14,953). Authenticate its complete semantic
    # .rel.main identity by a pinned SHA-256 over every (site,type,value,symbol,addend)
    # tuple. New 87-C main assembly splitting must not change even one such record.
    main_old=_main_entry_relocations(orig)
    main_new=_main_entry_relocations(built)
    expected={
        'entry':(6,'08b6e3f1949f4015f78ccd7df02f1dc9e3cf79c0789a1606a0ae4a801e36e095',
                 6,'08b6e3f1949f4015f78ccd7df02f1dc9e3cf79c0789a1606a0ae4a801e36e095'),
        'main':(15058,'3bcda7347c27cb22e423e6ddf448840e39c2965ed80765c27f0fa66d7735a1e5',
                 14953,'d7b6fdadb7f42929e475225307320ff0941dee879efec760ce14650e1fd82c11'),
    }
    for section,(n_old,h_old,n_new,h_new) in expected.items():
        if (len(main_old[section])!=n_old or _relocation_fingerprint(main_old[section])!=h_old or
                len(main_new[section])!=n_new or _relocation_fingerprint(main_new[section])!=h_new):
            raise ValueError('Native87 original/accepted main REL regression: '+section)
    old_rel=cross._relocations(orig);new_rel=cross._relocations(built)
    # Crossregion47 already guards seven overlays; native87 also alters main and file20.
    # The existing 864-C file_11 stage uses two overlay-alias *symbol names*
    # (same physical symbol value and original MIPS_26 site) in 14 existing
    # relocations. This exact pre-existing difference was independently measured
    # on the untouched 864-C candidate. Reject any unapproved new difference.
    # No address, type, value or instruction change is tolerated.
    aliases = [
        (range(2149494836, 2149495145, 44), '801eb180',
         'func_801EB180_5A7090', 'func_801EB180_616560'),
        ((2149510552,2149510588,2149510624,2149519568,2149519604,2149519640),
         '801eedf8', 'func_801EEDF8_5AAD08', 'D_801EEDF8_65DC48'),
    ]
    allowed_before=Counter()
    allowed_after=Counter()
    for sites,value,old_name,new_name in aliases:
        for site in sites:
            allowed_before[(site,'R_MIPS_26',value,old_name,'')]+=1
            allowed_after[(site,'R_MIPS_26',value,new_name,'')]+=1
    all_section_names=set(old_rel)|set(new_rel)
    for section in all_section_names:
        before=Counter(old_rel.get(section,[]))
        after=Counter(new_rel.get(section,[]))
        permitted_old=allowed_before if section=='file_11' else Counter()
        permitted_new=allowed_after if section=='file_11' else Counter()
        if before-after!=permitted_old or after-before!=permitted_new:
            raise ValueError('Native87 semantic relocation drift: '+section)
    maptext=(candidate/'build/usa/mnsg.map').read_text(encoding='utf-8')
    symbols=subprocess.check_output(['readelf','-Ws',str(built)],text=True)
    for entry in fixture['functions']:
        name,off,size,vma=entry['name'],entry['rom_offset'],entry['size'],entry['vma']
        if (name+'.NON_MATCHING' in symbols or
            not any(n==name and a==vma and s==size for n,a,s in new_funcs.elements()) or
            f'build/usa/src/{name}.c.o' not in maptext or
            rom[off:off+size]!=bimg[off:off+size]):
            raise ValueError('Native87 linked original-address C identity failed: '+name)
    return {'status':'PASS','original_address_matching_c':87,'original_instruction_bytes':912,
            'all_rom_bytes_equal':len(bimg),'sha1':RETAIL_SHA1,'original_elf_function_entries':7376,
            'semantic_relocations':{'entry':len(main_new['entry']), 'main':len(main_new['main']), **{s:len(old_rel[s]) for s in sorted(old_rel)}},
            'main_original_relocations':15058,'main_accepted_before_native87':14953,
            'main_accepted_after_native87':14953,
            'linked_asm_fragments':len(plan['assembly'])}
