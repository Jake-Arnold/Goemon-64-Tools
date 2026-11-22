"""Fail-closed isolated main-segment C stage after the 1,723-C G2 baseline.

All function bodies originate in the verified research source archive. This
adapter preserves remaining ASM, checks source/ROM/ELF identity, and never
patches MIPS instructions or the ROM. Matching isolated objects is insufficient.
"""
from __future__ import annotations
from collections import Counter, defaultdict
import hashlib, json, re, subprocess, struct
from pathlib import Path
from . import overlay_wide132 as wide
from . import overlay_crossregion47 as cross

ROOT=Path(__file__).resolve().parent
SOURCE=ROOT/'research/pending_isolated233_20261120/sources'
FIXTURE=ROOT/'research/pending_isolated233_20261120/promotion_manifest_241.json'
FORMAT='goemon-usa-isolated241-post-1723-v1'
SHA1='6ea0ed71032ce08fc2745f412d84936382197494'
COUNT=241; BYTES=15364
# Original source units whose remaining ASM is embedded via asm-processor.
# Replacing their pragmas must keep the companion C functions in situ.
EMBEDDED={
    'func_80008798_9398':'92F0.c',
    'func_8000A0F0_ACF0':'92F0.c',
    'func_8000A18C_AD8C':'92F0.c',
    'func_8000A344_AF44':'92F0.c',
    'func_8000A430_B030':'92F0.c',
    'func_8000A4F8_B0F8':'92F0.c',
    'func_8000A548_B148':'92F0.c',
    'func_8000A5C4_B1C4':'92F0.c',
    'func_8000C5E4_D1E4':'dialogue_window.c',
    'func_8000C680_D280':'dialogue_window.c',
    'func_8000C838_D438':'dialogue_window.c',
    'func_80023410_24010':'return_zero.c',
    'func_800237F0_243F0':'return_zero.c',
    'func_80023880_24480':'return_zero.c',
}
LINKED=re.compile(r'build/usa/asm/usa/([A-Za-z0-9_]+)\.s\.o\(\.(text(?:\.archive61)?)\);')
MARKER=re.compile(r'(?m)^nonmatching ([A-Za-z_][A-Za-z0-9_]*), 0x([0-9A-Fa-f]+)$')

def sha(raw):return hashlib.sha256(raw).hexdigest()
def load_fixture():
    j=json.loads(FIXTURE.read_text())
    if (set(j)!={'format','original_rom_sha1','original_canonical_count','original_canonical_instruction_bytes','functions'} or
        j['format']!=FORMAT or j['original_rom_sha1']!=SHA1 or j['original_canonical_count']!=1723 or j['original_canonical_instruction_bytes']!=69344):
        raise ValueError('Unreviewed native233 manifest')
    fs=j['functions']; names=set(); offsets=set(); sources=set()
    if len(fs)!=COUNT or sum(f['size'] for f in fs)!=BYTES:raise ValueError('Native233 count/byte mismatch')
    for f in fs:
        if set(f)!={'name','rom_offset','vma','size','source','source_sha256','original_code_sha256','original_asm'}:
            raise ValueError('Unexpected native233 fields')
        n,o,v,s=f['name'],f['rom_offset'],f['vma'],f['size']
        if (n in names or o in offsets or f['source'] in sources or s<8 or s%4 or o%4 or
            not re.fullmatch('iso233_[0-9]{3}',f['source']) or
            not re.fullmatch('[0-9a-f]{64}',f['source_sha256']) or
            not re.fullmatch('[0-9a-f]{64}',f['original_code_sha256'])):
            raise ValueError('Invalid native233 source identity '+n)
        m=re.fullmatch(r'func_([0-9A-F]{8})_([0-9A-Fa-f]{4,8})',n)
        if m and (int(m[1],16)!=v or int(m[2],16)!=o):raise ValueError('Native233 name/address mismatch '+n)
        names.add(n);offsets.add(o);sources.add(f['source'])
    return j

def validate_sources(rom,fixture,root=SOURCE):
    if len(rom)!=33554432 or hashlib.sha1(rom).hexdigest()!=SHA1:raise ValueError('Wrong retail USA expanded image')
    for f in fixture['functions']:
        if sha((root/(f['source']+'.c')).read_bytes())!=f['source_sha256']:
            raise ValueError('Native233 C source fingerprint mismatch: '+f['name'])
        if sha(rom[f['rom_offset']:f['rom_offset']+f['size']])!=f['original_code_sha256']:
            raise ValueError('Native233 ROM instruction anchor mismatch: '+f['name'])

def find_owners(checkout,fixture):
    checkout=Path(checkout)
    ld=(checkout/'.splat/usa/mnsg.ld').read_text()
    active={p for p,_ in LINKED.findall(ld)}
    names={f['name'] for f in fixture['functions'] if f['name'] not in EMBEDDED}
    owners={}
    for parent in sorted(active):
        path=checkout/'asm/usa'/(parent+'.s')
        if not path.is_file():raise ValueError('Native233 missing active ASM '+parent)
        for name,sizehex in MARKER.findall(path.read_text()):
            if name in names:
                if name in owners:raise ValueError('Native233 duplicate ASM ownership '+name)
                owners[name]=(parent,int(sizehex,16))
    if set(owners)!=names:raise ValueError('Native233 sources not ASM owned: '+repr(sorted(names-set(owners))))
    return owners
def parent_targets(owners):return wide.parent_targets(owners)

def stage_linker(checkout,rom,fixture,owners,root=SOURCE):
    validate_sources(rom,fixture,root)
    checkout=Path(checkout);ld=checkout/'.splat/usa/mnsg.ld';linker=ld.read_text()
    grouped=defaultdict(list)
    for f in fixture['functions']:
        if f['name'] in EMBEDDED:continue
        parent,size=owners[f['name']]
        if size!=f['size']:raise ValueError('Current ASM symbol extent mismatch: '+f['name'])
        grouped[parent].append(f)
    active={p for p,_ in LINKED.findall(linker)}
    if not set(grouped)<=active:raise ValueError('Native233 targets not still active ASM')
    fragments=[];parents=[];region_by_parent={}; region=None
    for line in linker.splitlines():
        m=re.match(r'^\s*\.(main|file_\d+)\s+0x[0-9A-Fa-f]+\s*:\s*AT\(',line)
        if m:region=m.group(1)
        for parent in grouped:
            if any(f'build/usa/asm/usa/{parent}.s.o(.{suffix});' in line for suffix in ('text','text.archive61')):
                if parent in region_by_parent:raise ValueError('Multiple linker owners: '+parent)
                region_by_parent[parent]=region
    if set(region_by_parent)!=set(grouped) or any(not re.fullmatch(r'(?:main|file_[0-9]+)',x or '') for x in region_by_parent.values()):
        raise ValueError('Native233 original overlay/ROM ownership not established')
    for parent,items in sorted(grouped.items()):
        items.sort(key=lambda f:f['rom_offset'])
        original=checkout/'asm/usa'/(parent+'.s');full=original.read_text()
        split=full.find('/* Generated by')
        if split<0:
            m=MARKER.search(full);w=wide.TEXT_WORD.search(full)
            if m is None or w is None:raise ValueError('Missing ASM header '+parent)
            split=min(m.start(),w.start())
        header,body=full[:split],full[split:]
        begin,end=wide._span(body)
        cross._object_nontext_empty(checkout/f'build/usa/asm/usa/{parent}.s.o')
        original_input_suffix=next((suffix for suffix in ('text','text.archive61') if f'build/usa/asm/usa/{parent}.s.o(.{suffix});' in linker),None)
        if original_input_suffix is None:raise ValueError('Missing original ASM input section '+parent)
        pieces=[];child=[];cursor=0;pos=begin
        for i,f in enumerate(items):
            n,o,s=f['name'],f['rom_offset'],f['size']
            m=re.search(r'(?m)^nonmatching '+re.escape(n)+r', 0x([0-9A-Fa-f]+)$',body)
            if m is None or int(m[1],16)!=s or m.start()<cursor or o<pos or o+s>end:
                raise ValueError('Native233 missing/stale original ASM entry '+n)
            lead=body[cursor:m.start()]
            if o>pos:
                if wide._span(lead)!=(pos,o):raise ValueError('Native233 missing leading original ASM bytes: '+n)
                alias=f'{parent}_w233_{i:03}';file=checkout/'asm/usa'/(alias+'.s')
                file.write_text(header+lead)
                obj=f'build/usa/asm/usa/{alias}.s.o';pieces.append(obj);fragments.append({'object':obj,'start':pos,'end':o});child.append((obj,pos,o))
            elif wide.TEXT_WORD.search(lead):raise ValueError('Native233 unexpected ASM code before C: '+n)
            endmark=body.find('endlabel '+n,m.end())
            if endmark<0:raise ValueError('Missing endlabel: '+n)
            endmark+=len('endlabel '+n)
            block=body[m.start():endmark]
            if wide._span(block)!=(o,o+s) or MARKER.findall(block)!=[(n,f'0x{s:X}')]:
                # Accept decimal/zero-prefix differences only after numeric extent and name tests
                markers=[(name,int(size,16)) for name,size in MARKER.findall(block)]
                if markers!=[(n,s)]:raise ValueError('Native233 original ASM function content mismatch '+n)
            dest=checkout/'src'/(f['source']+'.c')
            if dest.exists():raise ValueError('Native233 source collision')
            dest.write_bytes((root/(f['source']+'.c')).read_bytes())
            obj=f'build/usa/src/{f["source"]}.c.o';pieces.append(obj);child.append((obj,o,o+s))
            cursor=endmark;pos=o+s
        if pos<end:
            tail=body[cursor:]
            if wide._span(tail)!=(pos,end):raise ValueError('Native233 missing trailing original ASM bytes: '+parent)
            alias=f'{parent}_w233_{len(items):03}';(checkout/'asm/usa'/(alias+'.s')).write_text(header+tail)
            obj=f'build/usa/asm/usa/{alias}.s.o';pieces.append(obj);fragments.append({'object':obj,'start':pos,'end':end});child.append((obj,pos,end))
        child.sort(key=lambda x:x[1])
        if (not child or child[0][1]!=begin or child[-1][2]!=end or any(a[2]!=b[1] for a,b in zip(child,child[1:]))):
            raise ValueError('Native233 partition lost instructions: '+parent)
        old=f'build/usa/asm/usa/{parent}.s.o(.{original_input_suffix});'
        if linker.count(old)!=1:raise ValueError('Native233 source object missing in linker '+parent)
        linker=linker.replace(old,'\n'.join(obj+f'(.{original_input_suffix});' if obj.startswith('build/usa/asm/') else obj+'(.text);' for obj in pieces),1)
        for section in ('.data','.rodata','.bss'):
            old=f'build/usa/asm/usa/{parent}.s.o({section});'
            if linker.count(old)>1:raise ValueError('Duplicate native233 non-text owner')
            linker=linker.replace(old,'')
        parents.append({'source':parent,'input_section':original_input_suffix,'section':region_by_parent[parent],'start':begin,'end':end,'children':child})
    for region in set(region_by_parent.values()):
        pattern=r'(?m)^(\s*\.'+re.escape(region)+r'\s+0x[0-9A-Fa-f]+\s*:\s*AT\([^)]+\)) SUBALIGN\(16\)'
        linker,n=re.subn(pattern,r'\1 SUBALIGN(4)',linker)
        if n>1:raise ValueError('Native233 ambiguous subalignment '+region)
    ld.write_text(linker)
    embed_original(checkout,fixture,root)
    return {'functions':fixture['functions'],'assembly':fragments,'parents':parents,'linker_sha256':sha(linker.encode()),'sections':sorted(set(region_by_parent.values()))}

def embed_original(checkout,fixture,root=SOURCE):
    grouped=defaultdict(list)
    for f in fixture['functions']:
        if f['name'] in EMBEDDED:grouped[EMBEDDED[f['name']]].append(f)
    for filename,items in grouped.items():
        path=Path(checkout)/'src'/filename
        code=path.read_text()
        for f in items:
            pattern=(r'(?m)^#pragma GLOBAL_ASM\("asm/usa/nonmatchings/[^"\n]*/'
                     +re.escape(f['name'])+r'\.s"\)$')
            if len(re.findall(pattern,code))!=1:
                raise ValueError('Native233 missing original GLOBAL_ASM in '+filename+': '+f['name'])
            text=(root/(f['source']+'.c')).read_text()
            # Existing sources already include common.h and own standard MIPS scalars.
            text=re.sub(r'^typedef signed char s8;[^\n]*\n','',text,count=1)
            text=text.replace('#define NULL ((void*)0)\n','')
            if filename=='92F0.c' and f['name']=='func_80008798_9398':
                text=text.replace('typedef struct{u32 w0,w1;} Gfx;', 'typedef struct{u32 w0,w1;} Iso233Gfx;')
                text=text.replace('Gfx *', 'Iso233Gfx *')
            if filename=='dialogue_window.c':
                text=text.replace('extern s32 D_80167C48_168848;\n','')
                text=text.replace('*(&D_80167C48_168848 + arg0)', 'D_80167C48_168848[arg0]')
            code=re.sub(pattern,lambda m: '/* Original native C for '+f['name']+' */\n'+text,code,count=1)
        if filename=='return_zero.c':
            # Standalone IDO candidates rely on unprototyped libultra calls.
            # The old common.h prototypes change MIPS ABI argument coercion;
            # the native source must retain original assembler call contracts.
            scalars=('typedef signed char s8; typedef unsigned char u8; '
                     'typedef short s16; typedef unsigned short u16; '
                     'typedef int s32; typedef unsigned int u32; '
                     'typedef long long s64; typedef unsigned long long u64; '
                     'typedef float f32; typedef double f64;')
            code=code.replace('#include "common.h"', scalars,1)
        if filename=='92F0.c':
            declarations=('void func_8000A344_AF44(void);\n'
                          'void func_8000A430_B030(void);\n'
                          'void func_8000A4F8_B0F8(void);\n'
                          'void func_8000A5C4_B1C4(void *);\n'
                          'void func_8000A480_B080(CLS_GBG_W *);\n')
            code=code.replace('#include "common.h"\n','#include "common.h"\n'+declarations,1)
        path.write_text(code)

def object_targets(plan):
    return ([f'build/usa/src/{f["source"]}.c.o' for f in plan['functions'] if f['name'] not in EMBEDDED]
       +[f'build/usa/src/{p}.o' for p in sorted(set(EMBEDDED.values()))]
       +[x['object'] for x in plan['assembly']])

def _trim_archive_asm(path,length):
    """Trim only the original executable .text.archive61 input section.

    GNU assembler emits a separate empty .text; never drop or reinterpret
    original .rel.text.archive61 relocation records.
    """
    path=Path(path);data=bytearray(path.read_bytes())
    if data[:6]!=b'\x7fELF\x01\x02':raise ValueError('Not MIPS BE ELF32')
    off=struct.unpack_from('>I',data,32)[0];num=struct.unpack_from('>H',data,48)[0];ent=struct.unpack_from('>H',data,46)[0]
    if ent!=40:raise ValueError('Unknown MIPS ELF sections')
    matches=[]
    for i in range(num):
        h=off+i*ent
        ty,flags=struct.unpack_from('>II',data,h+4)
        sec_off,size,align=struct.unpack_from('>III',data,h+16)[0],struct.unpack_from('>I',data,h+20)[0],struct.unpack_from('>I',data,h+32)[0]
        if ty==1 and flags==6 and size:matches.append((h,sec_off,size,align))
    if len(matches)!=1:raise ValueError('Ambiguous original archive61 text sections')
    h,so,size,align=matches[0]
    if not length or length%4 or size<length or size-length>15 or align not in (4,16) or any(data[so+length:so+size]):
        raise ValueError('Unapproved native233 archive executable padding')
    struct.pack_into('>I',data,h+20,length)
    struct.pack_into('>I',data,h+32,4)
    path.write_bytes(data)
    return {'original_text_bytes':length,'compiler_section_bytes':size,'zero_padding_removed':size-length,'trimmed_object_sha256':sha(data)}

def pack_objects(checkout,rom,plan):
    checkout=Path(checkout);c=[];asm=[]
    for f in plan['functions']:
        if f['name'] in EMBEDDED:continue
        p=checkout/f'build/usa/src/{f["source"]}.c.o'
        symbol=subprocess.check_output(['readelf','-Ws',str(p)],text=True)
        got=[]
        for line in symbol.splitlines():
            parts=line.split()
            if len(parts)>=8 and parts[3]=='FUNC' and parts[7]==f['name'] and parts[6] not in ('UND','ABS'):
                got.append((int(parts[1],16),int(parts[2])))
        if got != [(0,f['size'])]:raise ValueError('Native233 compiled symbol extent mismatch: '+f['name']+' '+str(got))
        reloc=subprocess.check_output(['readelf','-Wr',str(p)],text=True)
        c.append({'source':f['source'],'relocatable':'R_MIPS_' in reloc,**cross._trim_object(p,f['size'],rom[f['rom_offset']:f['rom_offset']+f['size']],name=None if 'R_MIPS_' in reloc else f['name'])})
    for a in plan['assembly']:
        asm.append({'object':a['object'],**(_trim_archive_asm(checkout/a['object'],a['end']-a['start']) if a['object'].startswith('build/usa/asm/usa/libultra_wa33_02_wa61_01_w233_') else cross._trim_object(checkout/a['object'],a['end']-a['start'],rom[a['start']:a['end']]))})
    return {'functions':COUNT,'embedded':len(EMBEDDED),'instruction_bytes':sum(f['size'] for f in plan['functions']),'C_objects':c,'retained_ASM_objects':asm}

def verify_link(baseline,accepted_elf,candidate,rom,plan):
    baseline,accepted_elf,candidate=map(Path,(baseline,accepted_elf,candidate))
    img=(candidate/'build/usa/mnsg.z64').read_bytes()
    if len(img)!=33554432 or img!=rom or hashlib.sha1(img).hexdigest()!=SHA1:
        off=next((i for i,(a,b) in enumerate(zip(img,rom)) if a!=b),None)
        raise ValueError(f'Native233 entire USA ROM mismatch: first_offset={off} candidate_sha1={hashlib.sha1(img).hexdigest()}')
    before=cross._funcs(accepted_elf);after=cross._funcs(candidate/'build/usa/mnsg.elf');original=cross._funcs(baseline/'build/usa/mnsg.elf')
    if sum(original.values())!=7376 or sum(before.values())!=7376 or before!=after:raise ValueError('Native233 accepted 7376 ELF FUNC identities not preserved')
    oldrel=cross._relocations(accepted_elf);newrel=cross._relocations(candidate/'build/usa/mnsg.elf')
    if set(oldrel)!=set(newrel) or any(Counter(oldrel[k])!=Counter(newrel[k]) for k in oldrel):
        bad=[k for k in sorted(set(oldrel)|set(newrel)) if Counter(oldrel.get(k,[]))!=Counter(newrel.get(k,[]))]
        raise ValueError('Native233 semantic relocations differ in sections '+repr(bad))
    linkmap=(candidate/'build/usa/mnsg.map').read_text();syms=set(after.elements())
    for f in plan['functions']:
        if ((f['name'],f['vma'],f['size']) not in syms or f['name']+'.NON_MATCHING' in linkmap or
            (f'build/usa/src/{f["source"]}.c.o' if f['name'] not in EMBEDDED else f'build/usa/src/{EMBEDDED[f["name"]]}.o') not in linkmap or img[f['rom_offset']:f['rom_offset']+f['size']]!=rom[f['rom_offset']:f['rom_offset']+f['size']]):
            raise ValueError('Native233 new source missing original ELF/code identity '+f['name'])
    return {'status':'PASS','count':COUNT,'bytes':BYTES,'rom_bytes':len(img),'sha1':SHA1,'positive_elf_function_entries':7376,'semantic_relocation_counts':{k:len(v) for k,v in newrel.items()},'C_units':COUNT,'retained_ASM_fragments':len(plan['assembly'])}
