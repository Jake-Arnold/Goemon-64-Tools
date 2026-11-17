"""Fail-closed original-ROM 47-overlay C promotion atop a verified USA 346-C candidate.

This is an opt-in, versioned native linker stage. It does not fetch ROMs or
compiler assets and it does not modify the original upstream source checkout.
"""
from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import struct
import subprocess

STAGE_FORMAT = 'goemon-usa-47-overlay-c-original-link-v2'
USA_SHA1 = '6ea0ed71032ce08fc2745f412d84936382197494'
OVERLAYS = ('file_12', 'file_13', 'file_14', 'file_15', 'file_17', 'file_18', 'file_19')
EXACT_COUNTS = {'file_12':7051,'file_13':9589,'file_14':3041,'file_15':1625,'file_17':1739,'file_18':3365,'file_19':1078}
FIXTURE = Path(__file__).resolve().parent / 'research/jp_recomp_to_c/overlay47_promoted_manifest.json'
SOURCE_BASE = Path(__file__).resolve().parent / 'research/jp_recomp_to_c/src'


def digest(data:bytes, algo='sha256')->str:
    return hashlib.new(algo, data).hexdigest()


def load_fixture() -> dict:
    p = json.loads(FIXTURE.read_text(encoding='utf8'))
    if (p.get('format')!=STAGE_FORMAT or p.get('original_usa_sha1')!=USA_SHA1
            or p.get('canonical346_elf_sha256')!='02e355ab8765881608f27982e33e3b6895e6d042bba6c396837dde5ddd16bfdc'):
        raise ValueError('Unreviewed cross-region 47 source fixture')
    entries = p.get('functions')
    if not isinstance(entries,list) or len(entries)!=47 or sum(e['size'] for e in entries)!=2220:
        raise ValueError('Expected exactly 47 original-address source entries / 2220 bytes')
    seen=set();offsets=set();counts=Counter()
    for e in entries:
        if not isinstance(e,dict) or set(e)!={'name','section','rom_offset','vma','size','source_sha256','original_code_sha256'}:
            raise ValueError('Invalid original C fixture keys')
        name=e['name'];s=e['section'];start=e['rom_offset'];size=e['size']
        if (s not in OVERLAYS or re.fullmatch(r'func_[0-9A-F]{8}_[0-9A-F]{5,6}',name) is None
                or start!=int(name.rsplit('_',1)[1],16)
                or size<8 or size%4 or start%4 or name in seen or start in offsets):
            raise ValueError('Unsafe/duplicate original matching-C function')
        if re.fullmatch('[0-9a-f]{64}',e['source_sha256']) is None or re.fullmatch('[0-9a-f]{64}',e['original_code_sha256']) is None:
            raise ValueError('Unpinned source or code hash')
        seen.add(name);offsets.add(start);counts[s]+=1
    if counts!={'file_12':5,'file_13':15,'file_14':8,'file_15':2,'file_17':1,'file_18':9,'file_19':7}:
        raise ValueError('Overlay contribution differs from reviewed 47-C research')
    return p


def validate_sources(original_rom:bytes, fixture:dict, source_base:Path=SOURCE_BASE) -> None:
    if len(original_rom)!=33554432 or digest(original_rom,'sha1')!=USA_SHA1:
        raise ValueError('Not original 32MiB USA decompressed ROM')
    for e in fixture['functions']:
        source=source_base/(e['name']+'.c')
        if not source.is_file() or digest(source.read_bytes())!=e['source_sha256']:
            raise ValueError('Source SHA-256 is not independently matched: '+e['name'])
        at=e['rom_offset'];end=at+e['size']
        if end>len(original_rom) or digest(original_rom[at:end])!=e['original_code_sha256']:
            raise ValueError('Original USA MIPS instruction identity mismatch: '+e['name'])


def _subsegments(splat_yaml:str):
    result={}
    for overlay in OVERLAYS:
        m=re.search(r'(?m)^  - name: '+re.escape(overlay)+r'\s*$',splat_yaml)
        if m is None:raise ValueError('Missing overlay '+overlay)
        end=re.search(r'(?m)^  - name: \S+\s*$',splat_yaml[m.end():])
        text=splat_yaml[m.end():m.end()+end.start()] if end else splat_yaml[m.end():]
        if 'subsegments:\n' not in text:raise ValueError('Missing Splat subsegment list '+overlay)
        lines=re.findall(r'(?m)^    - \[0x([0-9A-Fa-f]+), (asm|c|data)(?:, ([A-Za-z0-9_]+))?\]',text)
        if len(lines)<2:raise ValueError('Empty Splat overlay '+overlay)
        parsed=[]
        for offset,kind,name in lines:
            addr=int(offset,16)
            if not name and kind=='asm':name=f'{addr:X}'
            parsed.append((addr,kind,name))
        for (start,k,name),(end,_,_) in zip(parsed,parsed[1:]):
            if start>=end:raise ValueError('Nonmonotonic Splat overlay '+overlay)
            if k=='asm':
                if name in result: raise ValueError('Duplicate original ASM source '+name)
                result[name]=(overlay,start,end)
    return result


def _object_nontext_empty(path:Path)->None:
    raw=subprocess.check_output(['readelf','-SW',str(path)],text=True)
    for section in ('.data','.rodata','.bss'):
        match=re.search(r'(?m)^\s*\[\s*\d+\]\s+'+re.escape(section)+r'\s+\S+\s+[0-9a-fA-F]+\s+[0-9a-fA-F]+\s+([0-9a-fA-F]+)\s',raw)
        if match and int(match.group(1),16)!=0:
            raise ValueError('Cannot discard original nontext object section: '+str(path)+' '+section)


def _text_header(raw:bytearray):
    if (raw[:6]!=b'\x7fELF\x01\x02' or len(raw)<52 or struct.unpack_from('>H',raw,18)[0]!=8):
        raise ValueError('Expected big endian ELF32 MIPS')
    off=struct.unpack_from('>I',raw,32)[0]
    n=struct.unpack_from('>H',raw,48)[0];ents=struct.unpack_from('>H',raw,46)[0]
    if ents!=40 or not 1<n<200 or off+n*ents>len(raw):raise ValueError('Invalid ELF section headers')
    sections=[]
    for i in range(n):
        h=off+i*ents;type_,flags=struct.unpack_from('>II',raw,h+4)
        if type_==1 and flags==6:
            sections.append(h)
    if len(sections)!=1:raise ValueError('Missing or repeated executable ELF .text')
    return sections[0]


def _trim_object(path:Path, length:int, original_code:bytes, name:str|None=None):
    raw=bytearray(path.read_bytes());h=_text_header(raw)
    offset,size=struct.unpack_from('>II',raw,h+16)
    align=struct.unpack_from('>I',raw,h+32)[0]
    if length%4 or not length or size<length or size-length>15 or align not in (4,16) or offset+size>len(raw):
        raise ValueError('Unapproved ASM/C object text extent '+str(path)+' '+str((length,size,align)))
    # MIPS assembler objects retain unresolved R_MIPS relocations, so their
    # pre-link instruction bytes need not equal the original linked ROM.
    # Source-compiled C objects (which have zero external relocations) must match.
    if name is not None and raw[offset:offset+length]!=original_code:
        raise ValueError('Compiled original C machine code differs: '+str(path))
    if any(raw[offset+length:offset+size]):
        raise ValueError('Nonzero alignment padding '+str(path))
    if name:
        symbols=subprocess.check_output(['readelf','-Ws',str(path)],text=True)
        matching=[]
        for line in symbols.splitlines():
            p=line.split()
            if len(p)>=8 and p[3]=='FUNC' and p[7]==name:matching.append(p)
        if len(matching)!=1 or int(matching[0][1],16)!=0 or int(matching[0][2])!=length:
            raise ValueError('C object named FUNC symbol not exact '+name)
        relocation=subprocess.check_output(['readelf','-Wr',str(path)],text=True)
        if 'R_MIPS_' in relocation:
            raise ValueError('C function has unreviewed MIPS relocation '+name)
    struct.pack_into('>I',raw,h+20,length)
    struct.pack_into('>I',raw,h+32,4)
    path.write_bytes(raw)
    return {'original_text_bytes':length,'compiler_section_bytes':size,'zero_padding_removed':size-length,
            'trimmed_object_sha256':digest(raw)}


def stage_linker(checkout:Path, original_rom:bytes, fixture:dict, source_base:Path=SOURCE_BASE):
    """Split only original ASM text into exact function-bounded C/ASM object chunks."""
    checkout=Path(checkout);validate_sources(original_rom,fixture,source_base)
    cfg=(checkout/'config/usa/splat.yaml').read_text(encoding='utf8')
    parent_ranges=_subsegments(cfg)
    ld=checkout/'.splat/usa/mnsg.ld'
    linker=ld.read_text(encoding='utf8')
    # Parent original ASM files must contain each intended C function once.
    groups={}
    for e in fixture['functions']:
        matches=[]
        for parent,(segment,start,end) in parent_ranges.items():
            if segment==e['section'] and start<=e['rom_offset'] and e['rom_offset']+e['size']<=end:
                matches.append(parent)
        if len(matches)!=1:raise ValueError('ASM parent ownership missing or ambiguous '+e['name'])
        groups.setdefault(matches[0],[]).append(e)
    all_asm=[];all_c=[];parent_info=[];touched=set()
    for parent,group in groups.items():
        group.sort(key=lambda e:e['rom_offset'])
        section,start,end=parent_ranges[parent]
        src=checkout/'asm/usa'/(parent+'.s')
        obj=checkout/'build/usa/asm/usa'/(parent+'.s.o')
        body=src.read_text(encoding='utf8')
        header=body[:body.index('/* Generated by')]
        _object_nontext_empty(obj)
        span=start;pos=0;replacement=[]
        for i,e in enumerate(group):
            name=e['name'];target=e['rom_offset'];finish=target+e['size']
            m=re.search(r'(?m)^nonmatching '+re.escape(name)+r', 0x([0-9A-Fa-f]+)$',body)
            if m is None or int(m.group(1),16)!=e['size'] or target<span or m.start()<pos:
                raise ValueError('Unpinned compiler/ASM target '+name)
            if span<target:
                piece=body[pos:m.start()]
                if not piece.strip():raise ValueError('Lost original ASM preceding '+name)
                part=f'{parent}_cross47_{i:02}'
                new_asm=checkout/'asm/usa'/(part+'.s')
                if new_asm.exists():raise ValueError('Duplicate split ASM filename')
                new_asm.write_text((header if pos else '')+piece,encoding='utf8')
                replacement.append(f'build/usa/asm/usa/{part}.s.o')
                all_asm.append({'object':replacement[-1],'start':span,'end':target,'section':section})
            elif body[pos:m.start()].strip():
                raise ValueError('Unexpected nonempty ASM between function boundaries '+name)
            endmark=body.find('endlabel '+name,m.end())
            if endmark<0:raise ValueError('Missing original MIPS function end label '+name)
            endmark+=len('endlabel '+name)
            if '\nnonmatching ' in body[m.start():endmark]:raise ValueError('Embedded function marker in C span')
            dest=checkout/'src'/(name+'.c')
            if dest.exists():raise ValueError('Destination C already exists '+name)
            dest.write_bytes((source_base/(name+'.c')).read_bytes())
            replacement.append(f'build/usa/src/{name}.c.o')
            all_c.append(e)
            span=finish;pos=endmark
        if span<end:
            piece=body[pos:]
            if not piece.strip():raise ValueError('Missing original ASM tail '+parent)
            part=f'{parent}_cross47_{len(group):02}'
            new_asm=checkout/'asm/usa'/(part+'.s')
            if new_asm.exists():raise ValueError('Duplicate final ASM fragment')
            new_asm.write_text(header+piece,encoding='utf8')
            replacement.append(f'build/usa/asm/usa/{part}.s.o')
            all_asm.append({'object':replacement[-1],'start':span,'end':end,'section':section})
        original=f'build/usa/asm/usa/{parent}.s.o(.text);'
        if linker.count(original)!=1:raise ValueError('Original .text linker ownership not exactly one '+parent)
        linker=linker.replace(original,'\n'.join(x+'(.text);' for x in replacement),1)
        for sec in ('.data','.rodata','.bss'):
            old=f'build/usa/asm/usa/{parent}.s.o({sec});'
            if linker.count(old)>1:raise ValueError('Duplicate obsolete nontext linkage '+parent)
            linker=linker.replace(old,'')
        touched.add(parent);parent_info.append({'parent':parent,'section':section,'start':start,'end':end,'new_c':len(group)})
    # The original unsplit overlays had 16-byte object subalignment. Every
    # original function remains 4-byte aligned; extra 16-byte linker gaps
    # would shift symbols/data once a new C object is interposed.
    for section in ('file_14','file_15','file_17','file_18','file_19'):
        anchor=re.compile(r'(?m)^(\s*\.'+re.escape(section)+r'\s+0x[0-9A-F]+\s*:\s*AT\([^)]+\)) SUBALIGN\(16\)')
        linker,n=anchor.subn(r'\1 SUBALIGN(4)',linker)
        if n!=1:raise ValueError('Original linker subalignment anchor changed: '+section)
    # Only overlay linker inputs are edited; original code and game data are never modified.
    if len(all_c)!=47 or sum(e['size'] for e in all_c)!=2220:
        raise ValueError('Crossregion C split incomplete')
    ld.write_text(linker,encoding='utf8')
    return {'functions':all_c,'assembly':all_asm,'parents':parent_info,'original_rom_sha1':USA_SHA1,
            'original_linker_sha256':digest(linker.encode())}


def object_targets(plan:dict):
    return [f'build/usa/src/{e["name"]}.c.o' for e in plan['functions']]+[x['object'] for x in plan['assembly']]


def pack_objects(checkout:Path, original_rom:bytes, plan:dict):
    checkout=Path(checkout);recs=[]
    for e in plan['functions']:
        start=e['rom_offset'];end=start+e['size']
        p=checkout/f'build/usa/src/{e["name"]}.c.o'
        rec=_trim_object(p,e['size'],original_rom[start:end],name=e['name'])
        recs.append(dict(name=e['name'],**rec))
    asmrecs=[]
    for e in plan['assembly']:
        p=checkout/e['object']
        rec=_trim_object(p,e['end']-e['start'],original_rom[e['start']:e['end']])
        asmrecs.append(dict(object=e['object'],**rec))
    return {'c_packed':recs,'asm_packed':asmrecs,'functions':len(recs),
            'original_c_instruction_bytes':sum(x['original_text_bytes'] for x in recs)}


def _funcs(elf:Path)->Counter:
    result=Counter()
    for line in subprocess.check_output(['readelf','-Ws',str(elf)],text=True).splitlines():
        x=line.split()
        if len(x)>=8 and x[3]=='FUNC' and x[6]!='UND' and int(x[2])>0:
            result[(x[7],int(x[1],16),int(x[2]))]+=1
    return result


def _relocations(elf:Path):
    all_sections={};section=None
    for row in subprocess.check_output(['readelf','-Wr',str(elf)],text=True).splitlines():
        m=re.match(r"Relocation section '\.rel\.(file_\d+)' at offset 0x[0-9a-f]+ contains (\d+) entries",row)
        if m:section=m.group(1);all_sections[section]=[];continue
        if row.startswith('Relocation section ') or row.startswith('There are no relocations'):
            section=None;continue
        if section:
            cells=row.split()
            if len(cells)>=5 and cells[2].startswith('R_MIPS_'):
                all_sections[section].append((int(cells[0],16),cells[2],cells[3],cells[4],''.join(cells[5:])))
    return all_sections


def verify_link(baseline:Path,candidate:Path,original_rom:bytes,plan:dict,packed:dict):
    baseline=Path(baseline);candidate=Path(candidate)
    built=(candidate/'build/usa/mnsg.z64').read_bytes()
    if len(built)!=33554432 or built!=original_rom or digest(built,'sha1')!=USA_SHA1:
        raise ValueError('Combined original USA 346+47 ROM G2 failed')
    before=_funcs(baseline/'build/usa/mnsg.elf');after=_funcs(candidate/'build/usa/mnsg.elf')
    if sum(before.values())!=7376 or before!=after:
        raise ValueError('Combined 393-C source introduced ELF function identity or size drift')
    oldrel=_relocations(baseline/'build/usa/mnsg.elf');newrel=_relocations(candidate/'build/usa/mnsg.elf')
    rels={}
    for section,count in EXACT_COUNTS.items():
        if (len(oldrel.get(section,[]))!=count or len(newrel.get(section,[]))!=count
                or Counter(oldrel[section])!=Counter(newrel[section])):
            raise ValueError('Merged C/ASM semantic relocations changed in '+section)
        rels[section]=count
    # A native proof only; the official decomp inventory separately checks
    # the 342 canonical C claims plus exactly these 47 named conversions.
    return {'status':'LINKED_346_PLUS_47_EXACT_NATIVE_G2_PASS', 'new_c':47,
            'new_c_original_bytes':2220,'candidate_sha1':USA_SHA1,
            'candidate_elf_sha256':digest((candidate/'build/usa/mnsg.elf').read_bytes()),
            'original_elf_functions':7376,'relocations':rels,
            'packer':packed,'original_linker_sha256':plan['original_linker_sha256']}
