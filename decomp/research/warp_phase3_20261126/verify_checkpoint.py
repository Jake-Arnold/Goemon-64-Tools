"""ROM-free source/evidence consistency only; never native acceptance."""
import hashlib,json
from pathlib import Path
P=Path(__file__).resolve().parent

def main():
 assert __debug__
 s=json.loads((P/'checkpoint.json').read_text());r=json.loads((P/'selected-replay.json').read_text());a=json.loads((P/'all-variants.json').read_text());o=json.loads((P/'owner-replay.json').read_text());h=json.loads((P/'host.json').read_text())
 assert s['status']=='RESEARCH_ONLY' and s['canonical_counts']=={'usa':3066,'japan_0':3004} and all(s[k]=='NOT_RUN' for k in ('full_candidate_G2','strict_candidate_inventory','candidate_promotion_integrity','gameplay'))
 assert len(a)==179 and len({(x['region'],x['source_sha256']) for x in a})==178 and sum('error' not in x for x in a)==149 and sum(x['exact'] for x in a)==20
 for x in a+r:
  p=P/'sources'/x['source']
  if p.exists():assert hashlib.sha256(p.read_bytes()).hexdigest()==x['source_sha256'],p
 for region in ('usa','japan_0'):
  q={x['source'].removeprefix(region+'_').removesuffix('.c'):x for x in r if x['region']==region};assert set(q)=={'candidate','scale','negative_bound','negative_value'}
  assert all((P/'sources'/v['source']).is_file() for v in q.values())
  assert q['candidate']['exact'] and q['candidate']['extent_exact'] and q['candidate']['linked_matching_words']==118 and q['candidate']['named_relocations_exact'] and q['candidate']['reference_relocations']==48
  assert q['scale']['linked_matching_words']==109 and q['scale']['raw_first_difference']==168 and q['scale']['named_relocations_exact'];assert q['negative_bound']['linked_matching_words']==116 and q['negative_value']['linked_matching_words']==46
  assert all(not q[k]['exact'] for k in ('scale','negative_bound','negative_value'))
  c=json.loads((P/f'{region}-candidates.json').read_text());assert len(c)==1 and c[0]['source_sha256']==q['candidate']['source_sha256'] and c[0]['negative_sha256']==q['negative_bound']['source_sha256'] and c[0]['code_sha256']==q['candidate']['original_code_sha256'] and c[0]['original_bytes']==472
 assert len(o)==2 and all(x['status']=='UNIT_TEXT_EXACT' and x['rom_exact'] and x['function_identities_exact'] and x['semantic_relocations_exact'] for x in o)
 assert (sum(x['text_bytes'] for x in o),sum(x['original_functions'] for x in o),sum(x['original_relocations'] for x in o))==(203120,920,7117)
 assert sum(x['cases'] for x in h)==8192 and all(x['status']=='PASS' for x in h)
 print('PASS: Phase 3 source-only research checkpoint consistency; no canonical promotion.')
if __name__=='__main__':main()
