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
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--region',choices=tuple(META),required=True);p.add_argument('--predecessor',type=Path,required=True);p.add_argument('--original',type=Path,required=True);p.add_argument('--pristine',type=Path,required=True);p.add_argument('--work',type=Path,required=True);p.add_argument('--uv',required=True);p.add_argument('--jobs',type=int,default=3);p.add_argument('--pool-proof',type=Path,required=True);a=p.parse_args();sys.path.insert(0,str(a.repo))
 from decomp.consolidated_batch_promotion import FLAGS, rels, text, probe, jp55, stage, cross, opening, glitch, inventory, splice
 from decomp.research.wave194_20261125.prefix_stage import stage_with_prefix
 from decomp import usa_short72_promotion as short72,native251_promotion as native251
 from decomp.research.promo367_20261125.inline_metadata import restore_inline
 from decomp.probe import Elf32
 r=a.region;w=a.work;co=w/'checkout';bd=co/f'build/{r}';elf=bd/'mnsg.elf';prior=w/'prior.elf';rom=stage.original(co,r);assert sha(prior.read_bytes())==PRE[r]
 d=json.loads((w/'summary.json').read_text());doc=d['staging'];proof={x['name']:x for x in json.loads(a.pool_proof.read_text()) if x['region']==r};save=lambda:(w/'summary.json').write_text(json.dumps(d,indent=2)+'\n')
 try:
  f0=cross._funcs(prior);g0=opening.stable_globals(prior);rel0=glitch.all_semantic_relocations(prior);oldtxt=run(['readelf','-Ws',prior],co);_,markers0=inventory.parse_inventory_symbols(oldtxt)
  ld=(co/f'.splat/{r}/mnsg.ld').read_text();objects={f['name']:(bd/(f['staged_path']+'.o'),{k:w/f'{f["name"]}.{k}.o' for k in ('named','shadow','native')}) for f in doc['functions']}
  # Link three complete images. No original bytes/relocation tuples are changed.
  def link(label):
   if (w/f'{label}.elf').exists() and label in d['links']:
    saved=w/f'{label}.elf';assert sha(saved.read_bytes())==d['links'][label]['elf_sha256'];return glitch.all_semantic_relocations(saved),run(['readelf','-Ws',saved],co)
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
  assert (bd/'mnsg.z64').read_bytes()==rom;retail=w/'retail.z64';run([a.uv,'run','python','tools/rommy.py','compress','--input',bd/'mnsg.z64','--output',retail,'--manifest',f'config/{r}/rommy.yaml','--pad','--verify'],co);d['retail_exact']=retail.read_bytes()==(co/f'config/{r}/baserom.z64').read_bytes();assert d['retail_exact'];d['retail_sha1']=hashlib.sha1(retail.read_bytes()).hexdigest();retail.unlink();d['strict_inventory_delta']=inventory.summarize_inventory(oldtxt,txt,set(objects));assert d['strict_inventory_delta']['newly_matching_c']==3;d['status']='LOCAL_DUAL_REFERENCE_EXACT_PENDING_CANONICAL_VALIDATOR';d['stage']='complete';save()
 except Exception as e:d['error']=str(e);save();traceback.print_exc();raise
if __name__=='__main__':main()
