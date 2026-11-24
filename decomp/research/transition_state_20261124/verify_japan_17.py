#!/usr/bin/env python3
"""Private independent-original-reference and native JP transition replay.
Requires fresh exact canonical JP2534 checkout. No canonical files modified.
"""
import argparse, collections, csv, hashlib, json, pathlib, re, shutil, subprocess
from decomp import usa_cright4_promotion as shared, japan_cright6_promotion as prev, japan_cright_promotion as cright, overlay_crossregion47 as cross, glitch_g2_promotion as glitch, usa_opening_new2_promotion as opening, japan_jp55_promotion as jp55, inventory
P=pathlib.Path; B=P(__file__).resolve().parent; R='japan_0'; BASE='4efacadb87c1d3f14fc082959e280325ccec5185'; PIN='7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee'; LEDGER='10313aba367418d71cd6c332086d2d6a9bf83e39'
OWNERS=['jp1686_280_005.s','jp1686_280_008.s']
def sha(b):return hashlib.sha256(b).hexdigest()
def need(x,msg):
    if not x:raise ValueError(msg)
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--checkout',type=P,required=True);p.add_argument('--work',type=P,required=True);p.add_argument('--uv',required=True);p.add_argument('--ledger',type=P,required=True);p.add_argument('--jobs',type=int,default=3);a=p.parse_args();c=a.checkout.resolve();w=a.work.resolve();w.mkdir(parents=True,exist_ok=False);bd=c/'build/japan_0';elf=bd/'mnsg.elf';ldp=c/'.splat/japan_0/mnsg.ld';ld0=ldp.read_text();rom=shared.original(c,R);retail=(c/'config/japan_0/baserom.z64').read_bytes()
    need(sha(elf.read_bytes())==prev.RESEARCH_ELF and (bd/'mnsg.z64').read_bytes()==rom,'wrong canonical JP2534 predecessor');need(len(retail)==16777216 and hashlib.sha1(retail).hexdigest()==prev.RETAIL_SHA,'wrong original retail');need(sha((c/'tools/ido-5.3/cc').read_bytes())==prev.COMPILER_SHA,'wrong IDO');need(subprocess.check_output(['git','rev-parse','HEAD'],cwd=c,text=True).strip()==PIN,'wrong original upstream')
    le=a.ledger.read_bytes()[:58440];need(hashlib.sha1(b'blob '+str(len(le)).encode()+b'\0'+le).hexdigest()==LEDGER,'ledger drift; review current compiler ledger')
    old=w/'prior.elf';shutil.copyfile(elf,old);names0=cright.c_identities(old);g0=opening.stable_globals(old);f0=cross._funcs(old);r0=glitch.all_semantic_relocations(old);need(len(names0)==2534 and r0[1:]==(80745,prev.RELOC_SHA),'canonical inventory or relocations drift')
    j=B/'japan';rows=[x for x in csv.DictReader((j/'crosswalk.csv').open()) if x['status']=='ISOLATED_EXACT_RESEARCH_ONLY'];data=json.loads((j/'native_replay.json').read_text());records={r['name']:r for r in data['rows'] if r['exact']};records.update({r['name']:r for r in json.loads((j/'alias_free_replay.json').read_text())['rows']});targets={x['jp_function']:x for x in rows};need(len(targets)==17 and not targets.keys()&names0 and sum(int(x['jp_size_bytes']) for x in rows)==1432,'wrong target set')
    for name,row in targets.items():
        r=records[name];off=int(row['jp_rom_offset'],16);z=int(row['jp_size_bytes']);src=j/'source'/(r['variant']+'.c');need(r['exact'] and r['numeric_relocs_equal'] and r['size']==z and sha(rom[off:off+z])==r['original_sha256'] and sha(src.read_bytes())==r['source_sha256'],'wrong source/ROM reference '+name)
    auto=(c/'.splat/japan_0/undefined_syms_auto.ld').read_text();offsets={};oldasm={};delta=collections.Counter();group=[]
    # Numeric references are assembled from the original Splat ASM, not native output.
    for owner in OWNERS:
        ap=c/'asm/japan_0'/owner;op=bd/'asm/japan_0'/(owner+'.o');raw=ap.read_text();oldasm[ap]=raw;ms=list(jp55.BLOCK.finditer(raw));need(ms and all(m['name'] in targets for m in ms),'unexpected original owner '+owner);glitch.check_nontext(op);header=raw[:ms[0].start()];section=opening.elf_sections(op.read_bytes())['.text'];start=int(targets[ms[0]['name']]['jp_rom_offset'],16);end=start+section['size'];need(jp55.word_span(raw)==(start,end),'original owner extent drift');group.append((owner,raw,header,ms,start,end));
        def conv(m):
            kind,n=m.groups();v=int(n,16);need(re.search(r'(?m)^D_'+n+r'\s*=\s*0x0*'+n+r'\s*;',auto,re.I),'original generated ABS offset not proven '+n);offsets[n]=v
            return str((v+0x8000)>>16 if kind=='hi' else (v+0x8000)%65536-0x8000)
        shadow=re.sub(r'%(hi|lo)\(D_([0-9A-Fa-f]{1,7})\)',conv,raw);need(shadow!=raw,'missing original numeric-reference distinction');ap.write_text(shadow)
    need(set(m['name'] for _,_,_,ms,_,_ in group for m in ms)==set(targets),'original owner target set mismatch')
    def link(tag):
        elf.unlink();(bd/'mnsg.z64').unlink();shared.runmake(c,R,ldp.read_text(),['build/japan_0/mnsg.z64'],w/f'{tag}-link.log',a.uv,a.jobs);need((bd/'mnsg.z64').read_bytes()==rom,tag+' full original ROM differs');need(cross._funcs(elf)==f0 and sum(f0.values())==7376,tag+' original FUNC identities differ');need(opening.stable_globals(elf)==g0,tag+' stable globals changed');rp=w/f'{tag}-retail.z64';subprocess.run([a.uv,'run','python','tools/rommy.py','compress','--input','build/japan_0/mnsg.z64','--output',str(rp),'--manifest','config/japan_0/rommy.yaml','--pad','--verify'],cwd=c,check=True,stdout=subprocess.DEVNULL);need(rp.read_bytes()==retail,tag+' original retail mismatch');rp.unlink();shutil.copyfile(elf,w/f'{tag}.elf');return glitch.all_semantic_relocations(elf)
    objs=[f'build/japan_0/asm/japan_0/{x}.o' for x in OWNERS];shared.runmake(c,R,ld0,objs,w/'shadow-compile.log',a.uv,a.jobs)
    for owner,raw,header,ms,start,end in group:cross._trim_object(bd/'asm/japan_0'/(owner+'.o'),end-start,rom[start:end])
    rshadow=link('shadow');need(cright.c_identities(elf)==names0,'shadow C ownership changed');removed=r0[0]-rshadow[0];need(not (rshadow[0]-r0[0]),'unexpected added shadow relocations')
    expected=collections.Counter()
    for name,row in targets.items():
        start=int(name.split('_')[1],16);end=start+int(row['jp_size_bytes']);rr=records[name];rel=[k for k in r0[0] if k[0]=='.rel.main' and start<=k[1]<end and k[2] in ('R_MIPS_HI16','R_MIPS_LO16') and k[4][2:] in offsets and k[3]==offsets[k[4][2:]]];need(sum(r0[0][k] for k in rel)==rr['named_relocs']-rr['numeric_relocs'],'unexpected original reference offset count '+name);expected.update({k:r0[0][k] for k in rel})
    need(expected==removed,'original vs independent shadow relocation delta differs')
    # Restore original assembly files and replace the two complete active owners with
    # separately compiled exact C functions, plus the original trailing zero padding.
    for ap,raw in oldasm.items():ap.write_text(raw)
    dest=c/'src/transition17';dest.mkdir(exist_ok=False);shutil.copyfile(j/'source/jp_transition.h',c/'src/jp_transition.h');ld=ld0;newobjs=[];frags=[]
    for owner,raw,header,ms,start,end in group:
        paths=[];cursor=start
        for m in ms:
            name=m['name'];row=targets[name];off=int(row['jp_rom_offset'],16);size=int(row['jp_size_bytes']);need(cursor==off and jp55.word_span(raw[m.start():m.end()])==(off,off+size),'original function extent mismatch '+name);cursor=off+size;source=dest/(name+'.c');shutil.copyfile(j/'source'/(records[name]['variant']+'.c'),source);path=f'build/japan_0/src/transition17/{name}.c.o';paths.append(path);newobjs.append((name,path,off,size))
        if cursor<end:
            tail=raw[ms[-1].end():];need(jp55.word_span(tail)==(cursor,end) and not any(rom[cursor:end]),'original tail padding drift');pp=f'asm/japan_0/transition17_{owner}';(c/pp).write_text(header+tail);path=f'build/japan_0/{pp}.o';paths.append(path);frags.append((path,cursor,end-cursor))
        oldpath=f'build/japan_0/asm/japan_0/{owner}.o';needle=oldpath+'(.text);';need(ld.count(needle)==1,'active owner not unique');ld=ld.replace(needle,'\n'.join(x+'(.text);' for x in paths),1)
        for sec in ('.data','.rodata','.bss','.sdata','.sbss'):ld=ld.replace(oldpath+'('+sec+');','')
        need(oldpath+'(' not in ld,'unexpected original section')
    ldp.write_text(ld);shared.runmake(c,R,ld,[p for _,p,_,_ in newobjs]+[p for p,_,_ in frags],w/'native-compile.log',a.uv,a.jobs)
    for name,path,off,z in newobjs:
        obj=c/path;glitch.check_nontext(obj);text=subprocess.check_output(['readelf','-Ws',str(obj)],text=True);sy=[s.split() for s in text.splitlines() if s.split() and s.split()[-1]==name and ' FUNC ' in s];need(len(sy)==1 and int(sy[0][1],16)==0 and int(sy[0][2])==z,'native FUNC extent mismatch '+name);cross._trim_object(obj,z,rom[off:off+z])
    for path,off,z in frags:cross._trim_object(c/path,z,rom[off:off+z])
    rn=link('native');need(rn==rshadow,'native vs independently assembled original full semantic relocations differ');names=cright.c_identities(elf);need(names==names0|set(targets),'exact new C ownership mismatch');inv=inventory.summarize_inventory(subprocess.check_output(['readelf','-Ws',str(old)],text=True),subprocess.check_output(['readelf','-Ws',str(elf)],text=True),set(targets));need(inv['identified_function_entries']==7376 and inv['newly_matching_c']==17 and inv['remaining_assembly_entries']==4825 and not inv['size_annotation_differences'],'strict inventory mismatch')
    result={'status':'FULL_ROM_EXACT_RESEARCH_NOT_PROMOTED','base_commit':BASE,'region':R,'before_C':2534,'after_C':2551,'added_C':17,'added_bytes':1432,'prior_elf_sha256':sha(old.read_bytes()),'shadow_elf_sha256':sha((w/'shadow.elf').read_bytes()),'candidate_elf_sha256':sha(elf.read_bytes()),'expanded_rom_sha1':prev.ROM_SHA,'retail_rom_sha1':prev.RETAIL_SHA,'expanded_rom_bytes':len(rom),'retail_rom_bytes':len(retail),'positive_function_identities':sum(f0.values()),'stable_globals':sum(g0.values()),'prior_relocations':r0[1],'native_relocations':rn[1],'native_relocation_sha256':rn[2],'independent_shadow_exact':True,'removed_original_abs_offset_relocations':[list(k) for k in sorted(removed.elements())],'new_c_names':sorted(targets),'inventory':inv,'source_records':[records[k] for k in sorted(targets)],'compiler_outcome':'EXISTING_QUIRK_REPRODUCED','full_canonical_CI':'NOT_RUN'};(w/'proof.json').write_text(json.dumps(result,indent=2)+'\n');print('JP2551 full native and independent original ROM/ELF/inventory exact')
if __name__=='__main__':main()
