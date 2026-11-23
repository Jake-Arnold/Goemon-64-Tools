"""Fail-closed original-JP C-Right function trial against JP2369 canonical baseline.

Never mark PASSED_G2 unless complete ROM, ELF, source, exact relocation multiset,
strict accepted-C identity and local CI pass. The currently known original-Splat
D_3B07A relocation delta is a blocker, not an implicit waiver.
"""
from __future__ import annotations
import argparse, hashlib, json, re, shutil, subprocess
from collections import Counter
from pathlib import Path
from . import japan_jp55_promotion as jp55
from . import japan_noop_port as jp329
from . import glitch_g2_promotion as glitch
from . import overlay_crossregion47 as cross
from .japan_thirtyfour_c import pack_text_metadata

HERE=Path(__file__).resolve().parent
SOURCE=HERE/'research/jp_cright_initializer_20261122/stage_second_symbolic_99of99.c'
TARGET='func_80212514_5CDAA4'
ROM_OFF=0x5CDAA4
VMA=0x80212514
SIZE=396
ROM_SHA='6f8745fecc3a5e7d4918c7a73353eb0726116ded'
CODE_SHA='b89ab4bb95558db39d13686f48070dd323e7cfacd3d590c90305edb9e5e59181'
SRC_SHA='78be8a62d74728bb65c91de8651c8ffe27224fcbaa4e63f0dc077591c8cbb0f3'
BASE_C=2369
BASE_BYTES=126612
STAGE=Path('build/japan_0/jpcright-stage.json')
C_PATH='src/jpcright/stage_initializer.c'

def sha(b): return hashlib.sha256(b).hexdigest()

def original(co):
    data=(co/'config/japan_0/baserom.decompressed.z64').read_bytes()
    if len(data)!=33554432 or hashlib.sha1(data).hexdigest()!=ROM_SHA or sha(data[ROM_OFF:ROM_OFF+SIZE])!=CODE_SHA:
        raise ValueError('Original Japanese ROM or initializer bytes are not authenticated')
    return data

def stage(co):
    rom=original(co)
    if sha(SOURCE.read_bytes())!=SRC_SHA:raise ValueError('Frozen C source changed')
    if (co/'build/japan_0/mnsg.z64').read_bytes()!=rom:raise ValueError('JP2369 baseline full ROM must be exact before staging')
    if not (co/'build/japan_0/jp55-stage.json').is_file():raise ValueError('No verified JP55 stage')
    p=co/STAGE
    if p.exists() or (co/'src/jpcright').exists():raise ValueError('Stale stage/collision')
    ldpath=co/'.splat/japan_0/mnsg.ld'
    ld=ldpath.read_text()
    maps,cache=jp55.parse_owner(co,ld,{TARGET})
    if TARGET not in maps:raise ValueError('Target is not uniquely owned by active original assembly')
    owner,m=maps[TARGET];raw,blocks=cache[owner]
    if int(m['size'],16)!=SIZE or jp55.word_span(raw[m.start():m.end()])!=(ROM_OFF,ROM_OFF+SIZE):
        raise ValueError('ROM, size, or original ASM ownership mismatch')
    if blocks[0].start()==m.start() or blocks[-1].end()==m.end():
        raise ValueError('Unexpected initializer at owner edge; reviewed two-sided split required')
    oldobj=co/f'build/japan_0/{owner}.o'
    glitch.check_nontext(oldobj)
    _,n,_,_=jp329.text_section(oldobj)
    first=jp55.word_span(raw[blocks[0].start():blocks[0].end()])[0]
    last=first+n
    if first!=0x5CD620 or last not in (0x5CE1E0,0x5CE220):raise ValueError('Unexpected active overlay owner extent')
    header=raw[:blocks[0].start()]
    before=raw[:m.start()]
    after=header+raw[m.end():]
    if jp55.word_span(before)!=(first,ROM_OFF) or jp55.word_span(after)!=(ROM_OFF+SIZE,last):
        raise ValueError('Fragment ROM ranges are not contiguous')
    for offs,text in ((first,before),(ROM_OFF+SIZE,after)):
        a,b=jp55.word_span(text)
        if a!=offs or b>len(rom):raise ValueError('Fragment ROM span drift')
    paths=[('asm/japan_0/jpcright_before.s',before),
           (C_PATH,SOURCE.read_bytes()),
           ('asm/japan_0/jpcright_after.s',after)]
    targets=[f'build/japan_0/{name}.o' for name,_ in paths]
    needle=f'build/japan_0/{owner}.o(.text);'
    if ld.count(needle)!=1:raise ValueError('Original owner link reference not unique')
    for sec in ('.data','.rodata','.bss','.sdata','.sbss'):
        if ld.count(f'build/japan_0/{owner}.o({sec});')>1:raise ValueError('Ambiguous original nontext owner')
    edited=ld.replace(needle,'\n'.join('        '+obj+'(.text);' for obj in targets),1)
    for sec in ('.data','.rodata','.bss','.sdata','.sbss'):
        edited=edited.replace(f'build/japan_0/{owner}.o({sec});','')
    if f'build/japan_0/{owner}.o(' in edited:raise ValueError('Unreviewed original owner section')
    for name,source in paths:
        dest=co/name
        if dest.exists():raise FileExistsError('Refuse overwrite: '+str(dest))
        dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_bytes(source if isinstance(source,bytes) else source.encode())
    ldpath.write_text(edited)
    data={'format':'goemon-jpcright-original-G2-trial-v1','original_rom_sha1':ROM_SHA,
          'baseline_c':BASE_C,'name':TARGET,'rom_offset':ROM_OFF,'vma':VMA,
          'size':SIZE,'source':C_PATH,'source_sha256':SRC_SHA,
          'original_code_sha256':CODE_SHA,'owner':owner,'orig_start':first,'orig_end':last,
          'before':paths[0][0],'after':paths[2][0],
          'expected_elf':7376,'expected_original_relocations':80747}
    p.write_text(json.dumps(data,indent=2)+'\n')
    return data

def build(co,deps,runtime):
    p=co/STAGE;x=json.loads(p.read_text());original(co)
    if x.get('name')!=TARGET or sha((co/x['source']).read_bytes())!=SRC_SHA:
        raise ValueError('Staged source drift')
    pre=json.loads((co/'build/japan_0/glitch-g2-stage.json').read_text())
    vm=json.loads((co/'build/japan_0/vm-g2-stage.json').read_text())
    jp=json.loads((co/'build/japan_0/jp55-stage.json').read_text())
    if len(jp['functions'])!=55:raise ValueError('Wrong accepted JP55 prerequisite')
    sources=[e['source'] for e in pre['new_functions']]+[e['source'] for e in vm['functions']]
    sources+=[e['source'] for e in jp['functions']]+[x['source']]
    args=glitch.makeargs(co,'japan_0',{'new_functions':[{'source':s} for s in sources]})
    objects=[f'build/japan_0/{y}.o' for y in (x['before'],x['source'],x['after'])]
    env=jp329.env_for(deps,runtime)
    subprocess.run(args+objects,cwd=co,env=env,check=True,stdout=subprocess.DEVNULL)
    for item,expected in ((x['before'],ROM_OFF-x['orig_start']),
                          (x['source'],SIZE),(x['after'],x['orig_end']-(ROM_OFF+SIZE))):
        obj=co/f'build/japan_0/{item}.o'
        _,actual,code,align=jp329.text_section(obj)
        if actual not in (expected,(expected+15)&~15) or align not in (4,16):
            raise ValueError(f'Object source extent/layout mismatch: {item}, {actual}, {align}')
        if actual>expected:
            if code[expected:]!=bytes(actual-expected):raise ValueError('Nonzero compiler/assembler pad')
            obj.write_bytes(pack_text_metadata(obj.read_bytes(),expected)[0])
        _,newsize,_,newalign=jp329.text_section(obj)
        if newsize!=expected or newalign not in (4,16):
            raise ValueError('Unreviewed object size after pack')
        section_start = x['orig_start'] if item==x['before'] else (ROM_OFF if item==x['source'] else ROM_OFF+SIZE)
        if section_start % newalign:
            raise ValueError('Object ELF section alignment would shift original address')
    for f in ('mnsg.elf','mnsg.z64'):
        dest=co/'build/japan_0'/f
        if dest.exists():dest.unlink()
    subprocess.run(args+['build/japan_0/mnsg.z64'],cwd=co,env=env,check=True,stdout=subprocess.DEVNULL)
    new=(co/'build/japan_0/mnsg.z64').read_bytes();rom=original(co)
    mismatch=next((i for i,(a,b) in enumerate(zip(new,rom)) if a!=b),None)
    res={'status':'FULL_ROM_EXACT' if new==rom else 'FAILED_ROM',
         'bytes':len(new),'sha1':hashlib.sha1(new).hexdigest(),
         'first_mismatch':mismatch}
    (co/'build/japan_0/jpcright-build.json').write_text(json.dumps(res,indent=2)+'\n')
    return res

def c_identities(elf):
    from . import japan_1686_promotion as jp1686
    text=subprocess.check_output(['mips-linux-gnu-objdump','-t',str(elf)],text=True)
    funcs={};marked=set()
    for line in text.splitlines():
        m=jp1686.jp39.F_SYMBOL.fullmatch(line)
        if not m:continue
        adr,kind,sec,size,name=m.groups()
        if sec not in ('.main','.entry','.ipl3') and not re.fullmatch(r'\.file_\d+',sec):continue
        if kind=='F' and int(size,16)>0:funcs[name]=(sec,int(adr,16),int(size,16))
        elif kind=='O' and name.endswith('.NON_MATCHING'):marked.add(name[:-13])
    return set(funcs)-marked

def verify(co,baseline):
    rom=original(co)
    if (co/'build/japan_0/mnsg.z64').read_bytes()!=rom or (baseline/'build/japan_0/mnsg.z64').read_bytes()!=rom:
        raise ValueError('FAILED_ROM: complete ROM differs')
    oldelf=baseline/'build/japan_0/mnsg.elf';newelf=co/'build/japan_0/mnsg.elf'
    identities_old=cross._funcs(oldelf);identities_new=cross._funcs(newelf)
    if identities_old!=identities_new or sum(identities_new.values())!=7376:
        raise ValueError('FAILED_ELF: positive function identities differ')
    orig,n0,h0=glitch.all_semantic_relocations(oldelf)
    cand,n1,h1=glitch.all_semantic_relocations(newelf)
    removed=list((orig-cand).elements());added=list((cand-orig).elements())
    diagnostic={'format':'jpcright-strict-G2-audit-v1','baseline_c':BASE_C,
                'target':TARGET,'rom_bytes':len(rom),'rom_sha1':ROM_SHA,
                'elf_identities':7376,'baseline_relocations':n0,'candidate_relocations':n1,
                'baseline_reloc_sha256':h0,'candidate_reloc_sha256':h1,
                'removed_relocations':removed[:20],'added_relocations':added[:20],
                'relocations_exact':not removed and not added and n0==n1,
                'native_bytes_exact':True}
    (co/'build/japan_0/jpcright-reloc-audit.json').write_text(json.dumps(diagnostic,indent=2)+'\n')
    if n0!=80747 or h0!='e5420c90550fb564bb6c839357e92d5ab28f90b4e945734dc2dcfd892eb41f20':
        raise ValueError('FAILED_RELOC: original accepted baseline provenance drift')
    if removed or added or n0!=n1 or h0!=h1:
        raise ValueError(f'FAILED_RELOC: removed={removed[:8]} added={added[:8]}')
    before=c_identities(oldelf);after=c_identities(newelf)
    if len(before)!=BASE_C or len(after)!=BASE_C+1 or after-before!={TARGET} or before-after:
        raise ValueError('FAILED_INVENTORY: original ASM/accepted C ownership mismatch')
    proof={**diagnostic,'status':'PASSED_G2_LOCAL','accepted_c':len(after),
           'accepted_original_bytes':BASE_BYTES+SIZE,'assembly_remaining':7376-len(after)}
    (co/'build/japan_0/jpcright-G2-proof.json').write_text(json.dumps(proof,indent=2)+'\n')
    return proof

def main():
    p=argparse.ArgumentParser();p.add_argument('action',choices=('stage','build','verify'))
    p.add_argument('--checkout',required=True,type=Path)
    p.add_argument('--baseline',type=Path);p.add_argument('--deps',type=Path);p.add_argument('--runtime',type=Path)
    a=p.parse_args();co=a.checkout.resolve()
    if a.action=='stage':res=stage(co)
    elif a.action=='build':res=build(co,a.deps.resolve(),a.runtime.resolve())
    else:res=verify(co,a.baseline.resolve())
    print(json.dumps(res,indent=2)[:8000])
if __name__=='__main__':main()
