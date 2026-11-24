"""Fresh JP6 isolated native verification; not a promotion gate."""
import argparse,hashlib,json,os,shlex,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser(description=__doc__);p.add_argument('repo',type=Path);p.add_argument('upstream',type=Path);p.add_argument('out',type=Path);a=p.parse_args()
repo=a.repo.resolve();co=a.upstream.resolve();out=a.out.resolve();out.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(repo))
from decomp.native_probe_helpers251 import get_original_splat_lines,check_exact,check_size
from decomp.usa_opening_new2_promotion import elf_sections
sha=lambda b:hashlib.sha256(b).hexdigest()
b=repo/'decomp/research/cright_promotion_checkpoint_20261124';e=json.loads((b/'evidence.json').read_text());rom=(co/'config/japan_0/baserom.decompressed.z64').read_bytes();assert len(rom)==33554432 and hashlib.sha1(rom).hexdigest()==e['japan_0']['expanded_sha1']; cc=co/'tools/ido-5.3/cc';assert sha(cc.read_bytes())==e['compiler_sha256']; inv=json.loads((repo/'decomp/results/japan_0_2528_native100_inventory_20261123.json').read_text());old=set(inv['previous_C_names'])|set(inv['new_C_names']);assert len(old)==2528; flags=shlex.split(e['compiler_flags']); rows=[]
for f in e['functions']:
 if f['region']!='japan_0':continue
 name=f['name'];offset=int(f['rom_offset'],16);vma=int(f['vma'],16);size=f['size'];source=b/f['source'];code=rom[offset:offset+size];assert sha(code)==f['original_code_sha256'] and sha(source.read_bytes())==f['source_sha256'] and name not in old
 owners=[q for q in (co/'asm/japan_0').glob('*.s') if f'glabel {name}\n' in q.read_text()];assert len(owners)==1,name
 lines=get_original_splat_lines(owners[0],name,offset,vma,size,code)
 ledger=(repo/'decomp/COMPILER_QUIRKS.md').read_bytes();assert b'NO_NEW_COMPILER_FINDING' in ledger
 obj=out/(name+'.o');subprocess.run([str(cc),*flags,'-o',str(obj),str(source)],cwd=co,check=True,capture_output=True)
 raw=obj.read_bytes();sec=elf_sections(raw)['.text'];text=raw[sec['offset']:sec['offset']+sec['size']];rel=subprocess.check_output(['readelf','-rW',obj],text=True);sym=subprocess.check_output(['readelf','-sW',obj],text=True);ok,reason,diff,actual,expected=check_exact(text,code,rel,lines,size);extent,_=check_size(sym,name,size);assert ok and extent,(name,reason,diff)
 # Negative controls: corrupt one non-relocated instruction and omit named relocation.
 relocated={x[0] for x in actual}; at=next(i for i in range(0,size,4) if i not in relocated); bad=bytearray(text);bad[at]^=1
 bad_word=check_exact(bytes(bad),code,rel,lines,size);assert not bad_word[0] and bad_word[1]=='WORD_DIFF' and bad_word[2]==at
 from decomp.native_probe_helpers251 import RELOC_RE
 bad_reloc=RELOC_RE.sub('',rel,count=1);bad_reloc_result=check_exact(text,code,bad_reloc,lines,size);assert not bad_reloc_result[0] and bad_reloc_result[1]=='RELOC_MISMATCH'
 rows.append(dict(negative_controls={'changed_instruction_rejected_at':at,'missing_named_relocation_rejected':True},name=name,rom_offset=f['rom_offset'],vma=f['vma'],size=size,owner=owners[0].name,source_sha256=sha(source.read_bytes()),original_code_sha256=sha(code),matched_words=size//4,named_relocations=len(actual),function_extent_exact=extent,compiler_quirk_outcome='NO_NEW_COMPILER_FINDING',ledger_sha256=sha(ledger),first_mismatch=diff,already_accepted=False)); print(name,size//4,len(actual),'PASS',flush=True)
assert len(rows)==6 and sum(x['size'] for x in rows)==624
result=dict(status='PASS_ISOLATED_ONLY',region='japan_0',base_accepted_C=2528,prospective_C=2534,original_ROM_sha1=hashlib.sha1(rom).hexdigest(),compiler_sha256=sha(cc.read_bytes()),compiler_flags=flags,functions=rows,canonical_link_replayed=False,full_candidate_CI=False,promotion=False)
(out/'jp6-isolated-report.json').write_text(json.dumps(result,indent=2)+'\n')
