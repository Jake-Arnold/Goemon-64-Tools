#!/usr/bin/env python3
"""Read-only regional counterpart search; normalized matches are candidates, not native proof."""
import argparse,json,struct,sys,hashlib
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--usa',type=Path,required=True);p.add_argument('--japan',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
sys.path.insert(0,str(a.repo.resolve()));from decomp.japan_function_map import read_verified_rom,normalized_instruction
u=read_verified_rom(a.usa,'usa');j=read_verified_rom(a.japan,'japan_0')
inv=a.repo/'decomp/results/japan_0_2528_native100_inventory_20261123.json';x=json.loads(inv.read_text());accepted=set(x['previous_C_names'])|set(x['new_C_names']);assert len(accepted)==2528
start,end=0x1050,0x53430
jw=tuple(map(normalized_instruction,struct.unpack_from(f'>{(end-start)//4}I',j,start)))
rows=[]
for label,off,size in [('F6E8',0x402e8,48),('F038',0x3fc38,196),('F480',0x40080,164),('DE80',0x3ea80,232)]:
    raw=u[off:off+size];uw=tuple(map(normalized_instruction,struct.unpack(f'>{size//4}I',raw)))
    hits=[i for i in range(len(jw)-len(uw)+1) if jw[i]==uw[0] and jw[i:i+len(uw)]==uw]
    assert len(hits)==1,(label,hits)
    i=hits[0];jp_off=start+i*4;jp_vma=jp_off+0x7ffff400;name=f'func_{jp_vma:X}_{jp_off:X}'
    assert jw[i+1:i+1+len(uw)]!=uw and jw[i-1:i-1+len(uw)]!=uw
    is_accepted=name in accepted;assert not is_accepted
    rows.append(dict(target=label,usa_offset=hex(off),usa_vma=hex(off+0x7ffff400),japan_offset=hex(jp_off),japan_vma=hex(jp_vma),size=size,normalized_words=size//4,normalized_full_matches=1,japan_candidate_name=name,japan_accepted_c=is_accepted,usa_code_sha256=hashlib.sha256(raw).hexdigest(),japan_code_sha256=hashlib.sha256(j[jp_off:jp_off+size]).hexdigest(),negative_controls=['offset_plus_4','offset_minus_4']))
result=dict(status='REGIONAL_COUNTERPART_CANDIDATES_ONLY',usa_rom_sha1=hashlib.sha1(u).hexdigest(),japan_rom_sha1=hashlib.sha1(j).hexdigest(),japan_accepted_names=len(accepted),japan_inventory_sha256=hashlib.sha256(inv.read_bytes()).hexdigest(),rows=rows,japan_native_compile='NOT_RUN',canonical_promotion='NOT_RUN')
a.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
