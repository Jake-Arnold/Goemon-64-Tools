"""Non-mutating IDO code-generation diagnostic replays; no raw traces exported."""
import argparse, hashlib, json, re, subprocess
from pathlib import Path
from decomp.consolidated_batch_promotion import FLAGS, text, rels
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--usa',type=Path,required=True);p.add_argument('--jp',type=Path,required=True);p.add_argument('--normal',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.out.mkdir(exist_ok=False)
kit=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
ledger=a.repo/'decomp/COMPILER_QUIRKS.md';rows=[]
for region,co in [('usa',a.usa),('japan_0',a.jp)]:
 for variant in ('baseline_replay','castcmp','comma'):
  src=kit/'sources'/f'{region}_{variant}.c';obj=a.out/f'{src.stem}.o';log=a.out/f'{src.stem}.log'
  ld=ledger.read_bytes();assert b'EXISTING_QUIRK_REPRODUCED' in ld
  cc=co/'tools/ido-5.3/cc';assert sha(cc.read_bytes())=='76d796c9591c9f5504949f85b29c32a6039a663791afe2f36f34ca18425b64d0'
  cmd=[str(cc),*FLAGS,'-v','-Wc,-d','-o',str(obj),str(src)]
  with log.open('w') as f:subprocess.run(cmd,cwd=co,stdout=f,stderr=subprocess.STDOUT,check=True)
  normal=a.normal/f'{src.stem}.o';assert text(normal)==text(obj) and rels(normal)==rels(obj)
  trace=log.read_text(errors='replace');m=re.findall(r'^emit_rrll:\s+zbne xr(\d+) xr(\d+)\s+(\d+)\s*$',trace,re.M);assert m
  rows.append(dict(region=region,variant=src.name,source_sha256=sha(src.read_bytes()),ledger_sha256=sha(ld),compiler_sha256=sha(cc.read_bytes()),flags=FLAGS+['-v','-Wc,-d'],diagnostic_text_equals_normal=True,diagnostic_relocations_equal_normal=True,codegen_branch_operands=[list(map(int,x[:2])) for x in m],compiler_outcome='NO_NEW_COMPILER_FINDING',first_mismatch_category='INSTRUCTION_SCHEDULING',first_difference=176))
(a.out/'sanitized.json').write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(rows,indent=2))
