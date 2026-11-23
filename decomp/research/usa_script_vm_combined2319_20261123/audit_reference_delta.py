#!/usr/bin/env python3
"""Research only: require the complete linked relocation delta to agree with independent ASM reference proofs."""
import argparse, copy, hashlib, json, struct, sys
from collections import Counter
from pathlib import Path

def require(ok,msg):
    if not ok:raise ValueError(msg)

def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--rom',type=Path,required=True);p.add_argument('--object',type=Path,required=True);p.add_argument('--combined',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();sys.path.insert(0,str(a.repo.resolve()));from decomp.probe import Elf32
    rom=a.rom.read_bytes();require(hashlib.sha1(rom).hexdigest()=='6ea0ed71032ce08fc2745f412d84936382197494','wrong ROM')
    evidence=Path(__file__).resolve().parent.parent;f=json.loads((evidence/'usa_script_vm_f37c_reference_20261123/evidence.json').read_text());d=json.loads((evidence/'usa_script_vm_df98_reference_20261123/evidence.json').read_text())
    require(f['shadow_native_relocations_exact'] and d['shadow_native_relocations_exact'] and f['native_relocations']==19 and d['native_text_relocations']==59 and d['shadow_native_table_relocations']==40,'independent references incomplete')
    old=Counter();new=Counter();types={2:'R_MIPS_32',5:'R_MIPS_HI16',6:'R_MIPS_LO16',10:'R_MIPS_PC16'};T=0x8003cfa0;R=0x8007d02c;M=0x80000450
    def word(b,off):return struct.unpack_from('>I',b,off)[0]
    def orig(v):return word(rom,v-0x80000000+0xc00)
    def symbol_vma(name):return int(name.split('_')[1] if name.startswith(('D_','jtbl_')) else name[2:].split('_')[0],16)
    for start,refs,local in ((0x8003f37c,f['original_to_shadow_removed'],f['original_to_shadow_added']),(0x8003df98,d['original_to_shadow_text_removed'],d['original_to_shadow_text_added'])):
        for off,typ,name in refs:old[('.rel.main',start+off,types[typ],symbol_vma(name),name)]+=1
        for off,typ,name in local:
            require(name=='.rodata','unexpected reference section');new[('.rel.main',start+off,types[typ],M,'.main')]+=1
    for off,typ,name in d['original_to_shadow_table_removed']:
        require(typ==2 and symbol_vma(name)==orig(0x8007d068+off),'reference table target differs from ROM');old[('.rel.main',0x8007d068+off,types[typ],symbol_vma(name),name)]+=1
    for off,typ,name in d['original_to_shadow_table_added']:
        require(typ==2 and name=='.text','unexpected local table relocation');new[('.rel.main',0x8007d068+off,types[typ],M,'.main')]+=1
    require(sum(old.values())==45 and sum(new.values())==44,'wrong independent reference delta')
    def audit(raw,proof):
        require(proof['rom_exact'] and proof['functions_exact'] and proof['function_count']==7376 and proof['global_count']==26714 and not proof['globals_removed'] and not proof['globals_added'],'whole-ROM/ELF gate failed')
        require((proof['relocation_before'],proof['relocation_after'])==(82103,82102),'unexpected relocation count')
        require(Counter({tuple(k):n for k,n in proof['relocation_removed']})==old and Counter({tuple(k):n for k,n in proof['relocation_added']})==new,'complete linked delta differs from independent references')
        e=Elf32(raw);ti=e.names.index('.text');ri=e.names.index('.rodata');text=e.payload(ti);pool=e.payload(ri);require(len(text)==10112 and len(pool)==224,'wrong mixed-unit extent')
        tr={r.offset:r for r in e.relocations(ti)};rr={r.offset:r for r in e.relocations(ri)}
        def signed(x):return x-65536 if x>=32768 else x
        for hi,lo,target in ((0x8003dfbc,0x8003dfc4,0x8007d068),(0x8003f380,0x8003f384,0x8007d108)):
            for site,kind in ((hi,5),(lo,6)):
                r=tr[site-T];require(r.relocation_type==kind and (r.symbol.kind,r.symbol.section,r.symbol.value)==(3,ri,0),'wrong native section-relative relocation')
            add=((word(text,hi-T)&65535)<<16)+signed(word(text,lo-T)&65535);require(R+add==target,'wrong native pool addend');require(((orig(hi)&65535)<<16)+signed(orig(lo)&65535)==target,'original linked target changed')
        for i in range(40):
            off=60+i*4;r=rr[off];require(r.relocation_type==2 and (r.symbol.kind,r.symbol.section,r.symbol.value)==(3,ti,0) and T+word(pool,off)==orig(R+off),'wrong native dispatch destination')
        require(pool[220:]==rom[0x7dd08:0x7dd0c],'wrong float literal')
        branch=0x8003dfb4;require(branch-T not in tr and word(text,branch-T)==orig(branch) and branch+4+4*signed(word(text,branch-T)&65535)==0x8003e190,'wrong locally resolved branch')
    raw=a.object.read_bytes();proof=json.loads(a.combined.read_text());audit(raw,proof);cases=[]
    for label in ('wrong_removed_symbol','wrong_added_target','missing_table_reference','wrong_count'):
        bad=copy.deepcopy(proof)
        if label=='wrong_removed_symbol':bad['relocation_removed'][0][0][-1]='wrong_symbol'
        elif label=='wrong_added_target':bad['relocation_added'][0][0][3]+=4
        elif label=='missing_table_reference':bad['relocation_removed'].pop()
        else:bad['relocation_after']+=1
        try:audit(raw,bad)
        except ValueError:cases.append(label)
        else:raise AssertionError('negative accepted: '+label)
    e=Elf32(raw)
    for label,off in [('wrong_pool_entry',e.sections[e.names.index('.rodata')][4]+63),('wrong_branch',e.sections[e.names.index('.text')][4]+0x1017),('wrong_pool_addend',e.sections[e.names.index('.text')][4]+0x23e7)]:
        bad=bytearray(raw);bad[off]^=1
        try:audit(bytes(bad),proof)
        except ValueError:cases.append(label)
        else:raise AssertionError('negative accepted: '+label)
    result={'status':'RESEARCH_ONLY_ALL_DELTA_RECORDS_EXACT_AGAINST_INDEPENDENT_REFERENCE','original_named_removed':45,'native_section_records_added':44,'verified_jump_table_targets':40,'verified_pool_pairs':2,'verified_local_branch':1,'negative_controls_rejected':cases,'strict_named_relocation_gate':'FAIL','canonical_promotion':'NOT_RUN'};a.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

if __name__=='__main__':main()
