"""Heuristic original-ROM opcode census of already accepted USA G2 functions."""
import argparse,hashlib,json,struct
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--rom',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();rows=json.loads((a.repo/'decomp/results/combined.json').read_text())['comparison']['functions'];rom=a.rom.read_bytes();assert hashlib.sha1(rom).hexdigest()=='6ea0ed71032ce08fc2745f412d84936382197494';assert len(rows)==3066
op=lambda w:w>>26;rs=lambda w:(w>>21)&31;rt=lambda w:(w>>16)&31;rd=lambda w:(w>>11)&31
hits=[]
for r in rows:
 off=int(r['rom_offset'],16);z=r['size'];w=struct.unpack('>'+str(z//4)+'I',rom[off:off+z]);assert hashlib.sha256(rom[off:off+z]).hexdigest()==r['expected_sha256']
 for i in range(len(w)-3):
  x,c,d,e=w[i:i+4]
  if op(x)==35 and rs(x)==29 and rt(x)==4 and op(c)==0 and c&63==33 and rd(c)==1 and op(d)==3 and op(e)==43 and rs(e)==1:hits.append(dict(kind='reload_add_jal_store',name=r['name'],offset=i*4))
 for i,x in enumerate(w):
  if op(x)!=12 or x&65535 not in (15,240,255):continue
  t=rt(x)
  for k in range(i+1,min(len(w),i+11)):
   c=w[k]
   if op(c) in (4,5,20,21) and t in (rs(c),rt(c)) and rs(c) and rt(c):hits.append(dict(kind='masked_two_register_branch',name=r['name'],mask=x&65535,offset=i*4,branch_offset=k*4,mask_operand='rs' if rs(c)==t else 'rt'));break
out=dict(accepted_functions=len(rows),original_sha1=hashlib.sha1(rom).hexdigest(),heuristic_only=True,window_words=10,hits=hits);a.out.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
