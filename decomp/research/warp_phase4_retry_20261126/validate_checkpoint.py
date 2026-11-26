"""ROM-free research consistency only. No promotion."""
from pathlib import Path
import hashlib,json
p=Path(__file__).resolve().parent
load=lambda f:json.loads((p/f).read_text())
def verify(f,root):
 for r in load(f):
  assert hashlib.sha256((p/root/'sources'/r['source']).read_bytes()).hexdigest()==r['source_sha256']
rows=load('native-results.json');verify('native-results.json',Path('.'));assert len(rows)==12 and len({r['source_sha256'] for r in rows})==12
assert all(not r['exact'] and r['original_reference_exact'] for r in rows)
for region in ('usa','japan_0'):
 rr={r['source'].split(region+'_')[1].split('.')[0]:r for r in rows if r['region']==region};assert len(rr)==6
 for k,v in {'baseline_replay':61,'castcmp':61,'comma':61,'prepgroup':61,'ptrtemp':32,'valuetemp':54}.items():assert rr[k]['linked_matching_words']==v
 for k in ('baseline_replay','castcmp','comma','prepgroup'):
  assert rr[k]['raw_difference_offsets']==[176,180,212] and rr[k]['extent_exact'] and rr[k]['named_relocations_exact'] and rr[k]['relocation_count']==24
for f in ('donor-line','donor-byte'):verify(f+'/results.json',Path(f))
assert [r['linked_matching_words'] for r in load('donor-line/results.json')]==[45,41]
assert [r['linked_matching_words'] for r in load('donor-byte/results.json')]==[13,0,0,13]
assert [r['matching_words'] for r in load('jp-donor-results.json')]==[26,23]
d=load('diagnostics.json');assert len(d)==6 and all(r['diagnostic_text_equals_normal'] and r['diagnostic_relocations_equal_normal'] and r['codegen_branch_operands']==[[2,14]] for r in d)
assert load('donor-census.json')['accepted_functions']==3066 and len(load('donor-census.json')['hits'])==1
print('Phase 4 retry evidence consistency PASS; 0 new promotions')
