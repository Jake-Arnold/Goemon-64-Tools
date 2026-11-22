#!/usr/bin/env python3
"""Reproduce seven new USA Mini SGI IDO C functions at original VMAs.
Source-only. User supplies private USA ROM, native IDO, ELF and MIPS tools.
Fail-closed. Pristine original-address proof, NOT canonical production G2.
"""
import argparse,hashlib,json,re,subprocess,tempfile
from pathlib import Path
from replay_native import symbol_table,relocations,FLAGS,cmd,EXPECTED_SHA,PINNED
FUNCTIONS=[
 ('func_801E2180_59E090',0x59E090,0x801E2180,160,11,'mini_2180_exact.c','ff95a979a03a0dc470a881c40d2976c44a2cd9d7d2be6fb3f58f2337a1309955'),
 ('func_801E2220_59E130',0x59E130,0x801E2220,68,3,'mini_2220.c','f7d6a88fe45130e84e21cc0b34c3ed570b4af58c046804edb20cb34162cedc26'),
 ('func_801E2800_59E710',0x59E710,0x801E2800,176,1,'mini_2800_exact.c','aa6224bdda5cd7c607cc32bd9b8cb00e961cbe83ed8825c570d42cc63ff8bf56'),
 ('func_801E2AA0_59E9B0',0x59E9B0,0x801E2AA0,180,4,'mini_2aa0.c','024443dac01cd6982847cd66f1f92a4fd6fd0e75cc18482350c59da8c8375b14'),
 ('func_801E2BA8_59EAB8',0x59EAB8,0x801E2BA8,168,1,'mini_2ba8_exact.c','dc94b908a5ac9c6345a078539da322022d3fa0bbc40726857565dee840e3f870'),
 ('func_801E2CEC_59EBFC',0x59EBFC,0x801E2CEC,64,1,'mini_2cec.c','1257615c7ee0b6c8750857190faa82b7aebffe341bfb34818d22b633b6b9c670'),
 ('func_801E2D74_59EC84',0x59EC84,0x801E2D74,188,2,'mini_2d74.c','49f909a1dbc901591a4aec92d24cb71ac144d8e9adcc8f540bcda4927ddc2c9a'),
]
def replay(args):
    here=Path(__file__).resolve().parent; up=args.upstream.resolve()
    assert cmd(['git','-C',up,'rev-parse','HEAD']).strip()==PINNED
    rom=args.rom.read_bytes(); assert len(rom)==33554432 and hashlib.sha1(rom).hexdigest()==EXPECTED_SHA
    assert rom==args.built_rom.read_bytes(),'pristine original ROM mismatch'
    base_sym=symbol_table(args.elf)
    results=[]
    with tempfile.TemporaryDirectory(prefix='goemon_native_7_') as tmp:
        t=Path(tmp)
        for name,off,vma,size,nrels,filename,sha in FUNCTIONS:
            source=here/filename
            assert hashlib.sha256(source.read_bytes()).hexdigest()==sha,(filename,'source changed')
            assert (vma,size,'FUNC','16') in base_sym.get(name,[]),(name,'original ELF function mismatch')
            obj=t/(name+'.o');aligned=t/(name+'.aligned.o');elf=t/(name+'.elf');binary=t/(name+'.bin');script=t/(name+'.ld')
            cmd([up/'tools/ido-5.3/cc',*FLAGS,'-o',obj,source],cwd=up)
            assert any(rec[1]==size and rec[2]=='FUNC' for rec in symbol_table(obj)[name]),(name,'compiled function extent differs')
            cr=relocations(obj,'.rel.text');orig=relocations(args.elf,'.rel.file_11',origin=vma,start=vma,size=size)
            assert sorted(cr)==sorted(orig) and len(cr)==nrels,(name,'symbolic relocation mismatch',cr,orig)
            cmd(['mips-linux-gnu-objcopy','--set-section-alignment','.text=4',obj,aligned])
            defs=[]
            for sym in sorted(set(x[2] for x in cr)):
                if re.fullmatch(r'(?:D|func)_[0-9A-Fa-f]{8}_[0-9A-Fa-f]+',sym):v=int(sym.split('_')[1],16)
                else:
                    assert sym in base_sym and base_sym[sym],(name,'symbol unknown',sym)
                    v=base_sym[sym][0][0]
                defs.append('--defsym='+sym+'=0x%08X'%v)
            script.write_text('OUTPUT_ARCH(mips)\nSECTIONS { . = 0x%08X; .text : { *(.text) } /DISCARD/ : { *(.mdebug) *(.reginfo) *(.options) *(.note*) *(.comment) }}\n'%vma)
            cmd(['mips-linux-gnu-ld','-m','elf32btsmip','-T',script,*defs,'-o',elf,aligned]);cmd(['mips-linux-gnu-objcopy','-O','binary','-j','.text',elf,binary])
            linked=binary.read_bytes()[:size];original=rom[off:off+size]
            assert len(linked)==size and linked==original,(name,'linked native code mismatches',size)
            assert any(rec[:3]==(vma,size,'FUNC') for rec in symbol_table(elf)[name]),(name,'linked FUNC identity mismatch')
            results.append({'name':name,'rom_offset':'0x%X'%off,'guest_vma':'0x%X'%vma,'original_code_bytes_exact':size,'original_relocations_exact':nrels,'source_sha256':sha,'original_code_sha256':hashlib.sha256(original).hexdigest(),'status':'PASSED_ISOLATED_LINKED_NATIVE'})
            print('EXACT',name,size,nrels,flush=True)
    assert sum(x['original_code_bytes_exact'] for x in results)==1004
    assert sum(x['original_relocations_exact'] for x in results)==23
    out={'status':'PASSED_SEVEN_ISOLATED_LINKED_NATIVE_RESEARCH_ONLY','original_rom_sha1':EXPECTED_SHA,'pristine_rom_bytes_exact':33554432,'pinned_upstream':PINNED,'functions':results,'new_functions':7,'new_original_instruction_bytes':1004,'original_relocations_exact':23,'combined_production_G2':'NOT_RUN','production_promotion':False}
    if args.json:args.json.write_text(json.dumps(out,indent=2)+'\n')
    print('SEVEN_NATIVE_EXACT_PASS',json.dumps({'functions':7,'original_bytes':1004,'relocations':23}),flush=True)
    return out
if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    for x in ['upstream','rom','elf','built-rom']:ap.add_argument('--'+x,type=Path,required=True)
    ap.add_argument('--json',type=Path)
    replay(ap.parse_args())
