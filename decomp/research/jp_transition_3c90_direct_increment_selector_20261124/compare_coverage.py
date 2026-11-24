#!/usr/bin/env python3
"""Compare complementary native outputs without merging or patching code."""
import hashlib,json,os,sys
from pathlib import Path
here=Path(__file__).resolve().parent
work=Path(os.environ.get('GOEMON_WORK','/tmp/jp3c90'))
rom=(work/'mnsg-japan/config/japan_0/baserom.decompressed.z64').read_bytes()
assert hashlib.sha1(rom).hexdigest()=='6f8745fecc3a5e7d4918c7a73353eb0726116ded'
orig=rom[0x3c90:0x3c90+444]
rows={}
for name in ('baseline','direct_control'):
 p=here/'out'/('func_80003090_3C90_'+name)
 ev=json.loads(p.with_suffix('.json').read_text())
 b=p.with_suffix('.bin').read_bytes()[:ev['generated_size']]
 assert len(b)==len(orig) and hashlib.sha256(b).hexdigest()==ev['linked_sha256']
 rows[name]={i for i in range(0,len(orig),4) if orig[i:i+4]==b[i:i+4]}
 assert len(rows[name])==ev['matching_words']
a,b=rows.values()
r={'scope':'diagnostic only; no combined machine code generated','original_words':111,'baseline_matching_words':len(a),'direct_control_matching_words':len(b),'both_matching_words':len(a&b),'either_matching_words':len(a|b),'neither_matching_offsets':[hex(i) for i in sorted(set(range(0,444,4))-(a|b))],'baseline_only_offsets':[hex(i) for i in sorted(a-b)],'direct_only_offsets':[hex(i) for i in sorted(b-a)],'direct_exact_suffix_bytes':200,'canonical_delta':0}
print(json.dumps(r,indent=2))
