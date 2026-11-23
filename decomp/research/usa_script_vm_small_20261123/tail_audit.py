#!/usr/bin/env python3
"""Read-only audit of repeated terminal return sequences in the authenticated USA ELF."""
import argparse,hashlib,json,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--baseline',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
sys.path.insert(0,str(a.repo.resolve()));from decomp.probe import Elf32
rom=(a.baseline/'config/usa/baserom.decompressed.z64').read_bytes();assert len(rom)==33554432 and hashlib.sha1(rom).hexdigest()=='6ea0ed71032ce08fc2745f412d84936382197494' and (a.baseline/'build/usa/mnsg.z64').read_bytes()==rom
raw=(a.baseline/'build/usa/mnsg.elf').read_bytes();base=Elf32(raw);proof=(a.repo/'decomp/results/combined.json').read_bytes();acc={f['name'] for f in json.loads(proof)['comparison']['functions'] if f['matched']};assert len(acc)==2319
pair=bytes.fromhex('03e0000800000000');tail=pair*2;rows=[]
for f in base.symbols:
    if f.kind!=2 or not f.size or not f.name or f.section>=len(base.sections):continue
    try:c=base.code(f)
    except ValueError:continue
    if c.endswith(tail):rows.append(dict(name=f.name,size=f.size,accepted=f.name in acc))
assert len({x['name'] for x in rows})==len(rows)==80 and not any(x['accepted'] for x in rows)
assert any(x['name']=='func_8003F6E8_402E8' and x['size']==48 for x in rows)
assert not pair.endswith(tail) and not (pair+b'\x00'*8).endswith(tail)
result=dict(status='RESEARCH_ONLY_DUAL_RETURN_TAIL_INVENTORY',original_elf_sha256=hashlib.sha256(raw).hexdigest(),accepted_proof_sha256=hashlib.sha256(proof).hexdigest(),published_c=len(acc),dual_tail_functions=len(rows),accepted_dual_tail_functions=0,negative_controls=['single_return_pair','return_plus_zero_padding'],functions=sorted(rows,key=lambda x:x['name']),interpretation='Pattern only. No inferred split, no extent reclassification, no native proof or padding substitution.')
a.out.write_text(json.dumps(result,indent=2)+'\n');print({k:v for k,v in result.items() if k!='functions'})
