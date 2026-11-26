#!/usr/bin/env python3
"""Private complete-ROM literal-pool integration and independent reference trial.
The named assembly comparison and local-pool comparison are both retained.
No production comparator relaxation or instruction/relocation rewriting.
"""
import argparse, hashlib, json, os, re, shutil, struct, subprocess, sys, traceback
from collections import Counter
from pathlib import Path
from replay import META, ROM, COMPILER, sha, run

PRE={'usa':'1107b0f4d2d7eaf17107323ae5119076476a773aabba01f77d27113353abb6ff','japan_0':'8b62b85eb9e32bc5b499017ac882c54e34ad666bdd47f3cd3867d36477935b0d'}
DAT={'usa':('file_12','5E3C90',0x5E3C90,0x12bb0),'japan_0':('5E8AC0','5E8AC0',0x5E8AC0,0x12b50)}
ASFLAGS='-EB -mtune=vr4300 -march=vr4300 -mabi=32 -Iinclude -I.'.split()

def trim_pool(p,expected):
    # Existing zero-padding/section-alignment procedure, restricted to a single
    # four-byte pool verified from the ORIGINAL ROM, with all relocations intact.
    from decomp.usa_opening_new2_promotion import elf_sections
    from decomp.probe import Elf32
    before=p.read_bytes();b=bytearray(before);e=Elf32(before);i=e.names.index('.rodata');s=e.sections[i];d=e.payload(i)
    assert d[:4]==expected and not any(d[4:]) and len(d) in (4,16) and not e.relocations(i)
    h=struct.unpack_from('>I',b,32)[0]+i*struct.unpack_from('>H',b,46)[0]
    assert struct.unpack_from('>I',b,h+20)[0]==len(d) and struct.unpack_from('>I',b,h+32)[0] in (4,16)
    struct.pack_into('>I',b,h+20,4);struct.pack_into('>I',b,h+32,4)
    assert all(h+20<=i<h+24 or h+32<=i<h+36 for i,(a,c) in enumerate(zip(before,b)) if a!=c)
    p.write_bytes(b)
    return {'input_bytes':len(d),'retained_bytes':4,'only_zero_padding_trimmed':True,'relocation_records_unmodified':True}

def split_data(co,original,r,doc,rom,prior,work):
    from decomp.probe import Elf32
    active,reference,base,size=DAT[r];src=co/f'asm/{r}/data/{active}.data.s';original_src=original/f'asm/{r}/data/{reference}.data.s';raw=src.read_text();assert raw==original_src.read_text()
    old=co/f'build/{r}/asm/{r}/data/{active}.data.s.o';e0=Elf32(old.read_bytes());old_data=e0.payload(e0.names.index('.data'));assert len(old_data)==size
    old_syms={}
    for l in subprocess.check_output(['readelf','-Ws',str(prior)],text=True).splitlines():
      x=l.split()
      if len(x)==8 and x[3]=='OBJECT' and x[4]=='GLOBAL':old_syms[x[-1]]=x
    splits=[];new=raw
    for i,(n,z,owner,symbol,*_) in enumerate(META[r]):
      v,o=map(lambda x:int(x,16),symbol.split('_')[1:]);m=re.search(r'(^dlabel '+symbol+r'\n)([^\n]+\n)',new,re.M);assert m and f'{o:X} {v:08X}' in m[2] and '.float' in m[2]
      sym=old_syms[symbol];assert int(sym[1],16)==v;extent=int(sym[2]);assert extent>=4
      before=m.group();switch=f'.section .data.phase2_{i+1}, "wa"\n.align 0\n';new=new.replace(before,m[1]+switch,1)
      assert new.count('enddlabel '+symbol+'\n')==1;new=new.replace('enddlabel '+symbol+'\n',f'.size {symbol}, {extent}\n',1)
      splits.append({'function':n,'symbol':symbol,'rom_offset':o,'vma':v,'symbol_extent':extent,'original_pool_sha256':sha(rom[o:o+4])})
    # Assemble the data source from the unchanged original Splat source minus
    # three words; source metadata sizes are retained explicitly across sections.
    # Later data-section fragments may begin at 4 mod 8. Disable relative
    # auto-alignment after each original alignment directive in the last fragment;
    # original data bytes/relocations and all linked symbols are checked below.
    head,tail=new.split('.section .data.phase2_3, "wa"\n',1)
    new=head+'.section .data.phase2_3, "wa"\n.Lphase2_data_start:\n'+re.sub(r'(?m)^\.align ([23])[ \t]*$', lambda m: f'.space (-((. - .Lphase2_data_start) + {splits[-1]["vma"]+4})) & {(1<<int(m[1]))-1}\n.align 0',tail)
    path=co/f'asm/{r}/data/phase2_data.s';path.write_text(new);obj=co/f'build/{r}/asm/{r}/data/phase2_data.s.o';obj.parent.mkdir(parents=True,exist_ok=True);run(['mips-linux-gnu-as',*ASFLAGS,'-o',obj,path],co)
    e=Elf32(obj.read_bytes());parts=['.data']+[f'.data.phase2_{i+1}' for i in range(3)];extents=[base]+[x['rom_offset']+4 for x in splits];ends=[x['rom_offset'] for x in splits]+[base+size];
    # Check raw data and all original named relocations (including addends) before linking.
    def rels(e,sec,offset):
      i=e.names.index(sec);return Counter((x.offset+offset,x.relocation_type,x.symbol.name or e.names[x.symbol.section]) for x in e.relocations(i))
    r0=rels(e0,'.data',base);r1=Counter();trimmed=bytearray(obj.read_bytes());allowed=set();padding=[]
    for sec,b,end in zip(parts,extents,ends):
      ix=e.names.index(sec);payload=e.payload(ix);expected=old_data[b-base:end-base];assert payload[:len(expected)]==expected and len(payload)-len(expected) in range(16) and not any(payload[len(expected):]),(r,sec,len(payload),len(expected));r1+=rels(e,sec,b)
      assert all(x.offset+4<=len(expected) for x in e.relocations(ix))
      # Only shrink authenticated trailing assembler padding and reduce input
      # section alignment where needed. No data, relocation or symbol is edited.
      h=struct.unpack_from('>I',trimmed,32)[0]+ix*40;struct.pack_into('>I',trimmed,h+20,len(expected));allowed.update(range(h+20,h+24));
      if sec!='.data':struct.pack_into('>I',trimmed,h+32,4);allowed.update(range(h+32,h+36))
      padding.append({'section':sec,'raw_bytes':len(payload),'retained_bytes':len(expected),'zero_padding_removed':len(payload)-len(expected)})
    assert all(i in allowed for i,(a,b) in enumerate(zip(obj.read_bytes(),trimmed)) if a!=b);obj.write_bytes(trimmed)
    assert r0==r1,('data relocation mismatch',len(r0-r1),len(r1-r0))
    # The section metadata is independent of candidate code; same split for
    # original named reference, original local reference, and native C links.
    ldpath=co/f'.splat/{r}/mnsg.ld';ld=ldpath.read_text();needle=f'build/{r}/asm/{r}/data/{active}.data.s.o(.data);';assert ld.count(needle)==1
    target={x['name']:x['staged_path'] for x in doc['functions']};lines=[]
    for i,sec in enumerate(parts):
      lines.append(f'        build/{r}/asm/{r}/data/phase2_data.s.o({sec});')
      if i<3:lines.append(f'        build/{r}/{target[splits[i]["function"]]}.o(.rodata);')
    ld=ld.replace(needle,'\n'.join(lines),1);ldpath.write_text(ld)
    return {'source_sha256':sha(raw.encode()),'split_source_sha256':sha(new.encode()),'original_data_bytes':size,'retained_data_bytes':size-12,'data_relocations':sum(r0.values()),'all_retained_data_relocations_exact':True,'splits':splits,'source_original_exact':True,'padding':padding}

def main():
 if not __debug__:raise RuntimeError("assertions required")
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--region',choices=tuple(META),required=True);p.add_argument('--predecessor',type=Path,required=True);p.add_argument('--original',type=Path,required=True);p.add_argument('--pristine',type=Path,required=True);p.add_argument('--work',type=Path,required=True);p.add_argument('--uv',required=True);p.add_argument('--jobs',type=int,default=3);p.add_argument('--pool-proof',type=Path,required=True);a=p.parse_args();a.work.mkdir(parents=True,exist_ok=False);sys.path.insert(0,str(a.repo))
 from decomp.consolidated_batch_promotion import FLAGS, rels, text, probe, jp55, stage, cross, opening, glitch, inventory, splice
 from decomp.research.wave194_20261125.prefix_stage import stage_with_prefix
 from decomp import usa_short72_promotion as short72,native251_promotion as native251
 from decomp.research.promo367_20261125.inline_metadata import restore_inline
 from decomp.probe import Elf32
 r=a.region;w=a.work;co=w/'checkout';shutil.copytree(a.predecessor,co,symlinks=True);bd=co/f'build/{r}';elf=bd/'mnsg.elf';prior=w/'prior.elf';shutil.copyfile(elf,prior);rom=stage.original(co,r);assert sha(prior.read_bytes())==PRE[r] and (bd/'mnsg.z64').read_bytes()==rom and stage.original(a.original,r)==rom
 assert hashlib.sha1((co/f'config/{r}/baserom.z64').read_bytes()).hexdigest()==ROM[r][0] and sha((co/'tools/ido-5.3/cc').read_bytes())==COMPILER
 assert run(['git','rev-parse','HEAD'],co).strip()==run(['git','rev-parse','HEAD'],a.original).strip()=='7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee'
 source_root=Path(__file__).parent/'sources';ledger=a.repo/'decomp/COMPILER_QUIRKS.md';proof=json.loads(a.pool_proof.read_text());proof={x['name']:x for x in proof if x['region']==r};d={'region':r,'base_commit':'8b195d8ce5a31723a71af428ee4f7bccf32b0bf8','status':'RESEARCH_ONLY','stage':'preflight','prior_elf_sha256':PRE[r],'native':[],'links':{}};save=lambda:(w/'summary.json').write_text(json.dumps(d,indent=2)+'\n');save()
 try:
  f0=cross._funcs(prior);g0=opening.stable_globals(prior);rel0=glitch.all_semantic_relocations(prior);oldtxt=run(['readelf','-Ws',prior],co);_,markers0=inventory.parse_inventory_symbols(oldtxt);rows=[]
  for n,z,owner,sym,*_ in META[r]:
   v,off=map(lambda x:int(x,16),n.split('_')[1:]);src=source_root/n/'02_literal_chain.c';assert n in markers0 and sha(src.read_bytes())==proof[n]['native_sha256'];rows.append({'name':n,'region':r,'vma':v,'rom_offset':off,'original_bytes':z,'owner':owner+'.s','source':str(src.resolve()),'source_sha256':sha(src.read_bytes()),'code_sha256':sha(rom[off:off+z]),'relocation_count':proof[n]['named_relocations']})
  doc=stage_with_prefix(co,r,candidates=rows,namespace='warpphase2');d['staging']=doc;save();assert not doc['blocked'] and len(doc['functions'])==3,doc['blocked'];d['stage']='split_data';save();d['data']=split_data(co,a.original,r,doc,rom,prior,w);save()
  ld=(co/f'.splat/{r}/mnsg.ld').read_text();frags=[f'build/{r}/{x["path"]}.o' for x in doc['fragments']];stage.runmake(co,r,ld,frags,w/'fragments.log',a.uv,a.jobs) if frags else None
  for f in doc['fragments']:
   p=bd/(f['path']+'.o');lo,hi=f['start'],f['end'];splice._trim_archive_asm(p,hi-lo) if f['suffix']=='.text.archive61' else cross._trim_object(p,hi-lo,rom[lo:hi])
  objects={};d['stage']='native_objects';save()
  for f in doc['functions']:
   n=f['name'];z=f['original_bytes'];off=f['rom_offset'];o=bd/(f['staged_path']+'.o');o.parent.mkdir(parents=True,exist_ok=True);src=co/f['staged_path'];assert sha(src.read_bytes())==f['source_sha256'];sym=proof[n]['pool_symbol'];pv=proof[n]['pool_rom_offset'];
   # Independently assemble the original named and original local-pool forms again.
   own=a.original/f'asm/{r}/{f["owner"]}';raw=own.read_text();probe.get_original_splat_lines(own,n,off,f['vma'],z,rom[off:off+z]);m=[m for m in jp55.BLOCK.finditer(raw) if m['name']==n];assert len(m)==1;body=m[0].group();assert sha(body.encode())==proof[n]['original_asm_sha256'];origdata=(a.original/f'asm/{r}/data/{DAT[r][1]}.data.s').read_text();m=re.search(r'^dlabel '+sym+r'\n([^\n]+)',origdata,re.M);assert m and sha(m[1].encode())==proof[n]['original_data_line_sha256'];pool=m[1].split('*/',1)[1].strip();shadow=body.replace(f'%hi({sym})','%hi(.Lphase2_pool)').replace(f'%lo({sym})','%lo(.Lphase2_pool)');assert sha(shadow.encode())==proof[n]['independent_local_asm_sha256']
   objs={}
   for label,b in [('named',body),('shadow',shadow)]:
    s=w/f'{n}.{label}.s';s.write_text('.include "macro.inc"\n.set noat\n.set noreorder\n.set gp=64\n.section .text, "ax"\n'+b+'\n.section .rodata, "a"\n.balign 4\n.Lphase2_pool:\n'+pool+'\n');p=w/f'{n}.{label}.o';run(['mips-linux-gnu-as',*ASFLAGS,'-o',p,s],co);objs[label]=p
   lb=ledger.read_bytes();native=w/f'{n}.native.o';run([co/'tools/ido-5.3/cc',*FLAGS,'-o',native,src],co);objs['native']=native
   assert text(objs['named'])[:z]==text(objs['shadow'])[:z]==text(native)[:z] and rels(native)==rels(objs['shadow']) and rels(objs['named'])!=rels(native)
   rec={'name':n,'source_sha256':f['source_sha256'],'ledger_sha256':sha(lb),'flags':FLAGS,'original_asm_reference_exact':True,'local_relocations_exact':True,'strict_named_gate_exact':False,'outcome':'EXISTING_QUIRK_REPRODUCED','pool_trim':{}}
   for label,p in objs.items():
    assert probe.check_size(run(['readelf','-Ws',p],co),n,z)[0];cross._trim_object(p,z,rom[off:off+z]);rec['pool_trim'][label]=trim_pool(p,rom[pv:pv+4]);
   d['native'].append(rec);objects[n]=(o,objs);save()
  # Link three complete images. No original bytes/relocation tuples are changed.
  def link(label):
   for n,(dest,objs) in objects.items():shutil.copyfile(objs[label],dest);os.utime(dest,None)
   elf.unlink(missing_ok=True);(bd/'mnsg.z64').unlink(missing_ok=True);stage.runmake(co,r,ld,[f'build/{r}/mnsg.z64'],w/f'{label}-link.log',a.uv,a.jobs)
   for n,(dest,objs) in objects.items():assert dest.read_bytes()==objs[label].read_bytes(),('object unexpectedly rebuilt',label,n)
   if r=='usa':short72.restore_original_abs_label_type(elf,prior);native251.restore_inline_usa(elf,prior);restore_inline(elf,a.pristine/'build/usa/mnsg.elf',prior)
   img=(bd/'mnsg.z64').read_bytes();f1=cross._funcs(elf);g1=opening.stable_globals(elf);rel1=glitch.all_semantic_relocations(elf);txt=run(['readelf','-Ws',elf],co);_,markers=inventory.parse_inventory_symbols(txt)
   rec={'expanded_rom_exact':img==rom,'expanded_sha1':hashlib.sha1(img).hexdigest(),'first_rom_mismatch':next((i for i,(a,b) in enumerate(zip(img,rom)) if a!=b),None),'function_identities_exact':f1==f0,'function_identities':sum(f1.values()),'globals_exact':g1==g0,'stable_globals':sum(g1.values()),'globals_removed':list((g0-g1).items())[:20],'globals_added':list((g1-g0).items())[:20],'semantic_relocation_count':rel1[1],'semantic_relocation_sha256':rel1[2],'ordinary_named_comparator_exact':rel1==rel0,'relocations_removed':list((rel0[0]-rel1[0]).items())[:30],'relocations_added':list((rel1[0]-rel0[0]).items())[:30],'ownership_exact':(markers0-markers==set(objects) and not markers-markers0) if label=='native' else markers0==markers,'elf_sha256':sha(elf.read_bytes())}
   d['links'][label]=rec;save();print(r,label,{k:rec[k] for k in ('expanded_rom_exact','function_identities_exact','globals_exact','ordinary_named_comparator_exact','ownership_exact')},flush=True);assert rec['expanded_rom_exact'] and rec['function_identities_exact'] and rec['globals_exact'] and rec['ownership_exact'],rec
   shutil.copyfile(elf,w/f'{label}.elf');return rel1,txt
  d['stage']='full_links';save();named,_=link('named');assert named==rel0;shadow,_=link('shadow');native,txt=link('native');assert shadow==native and shadow!=named
  missing=named[0]-shadow[0];added=shadow[0]-named[0];assert sum(missing.values())==sum(added.values())==6
  expected={x['pool_symbol'] for x in proof.values()};assert {x[-1] for x in missing}==expected
  assert Counter((x[0],x[1],x[2]) for x in missing.elements())==Counter((x[0],x[1],x[2]) for x in added.elements());assert {x[-1] for x in added}=={'.file_12'}
  d['semantic_relocation_dual_reference']={'entire_named_reference_equals_predecessor':True,'entire_native_equals_independent_shadow':True,'named_removed':list(missing.items()),'local_added':list(added.items()),'ordinary_named_comparator_exact':False,'comparator_unmodified':True};save()
  retail=w/'retail.z64';run([a.uv,'run','python','tools/rommy.py','compress','--input',bd/'mnsg.z64','--output',retail,'--manifest',f'config/{r}/rommy.yaml','--pad','--verify'],co);d['retail_exact']=retail.read_bytes()==(co/f'config/{r}/baserom.z64').read_bytes();assert d['retail_exact'];d['retail_sha1']=hashlib.sha1(retail.read_bytes()).hexdigest();retail.unlink();d['strict_inventory_delta']=inventory.summarize_inventory(oldtxt,txt,set(objects));assert d['strict_inventory_delta']['newly_matching_c']==3;d['status']='LOCAL_DUAL_REFERENCE_EXACT_PENDING_CANONICAL_VALIDATOR';d['stage']='complete';save()
 except Exception as e:d['error']=str(e);save();traceback.print_exc();raise
if __name__=='__main__':main()
