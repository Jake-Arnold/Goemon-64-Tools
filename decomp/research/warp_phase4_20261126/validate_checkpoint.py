#!/usr/bin/env python3
"""ROM-free evidence consistency only; never grants canonical ownership."""
import hashlib,json
from pathlib import Path
p=Path(__file__).resolve().parent
c=json.loads((p/'checkpoint.json').read_text());rows=json.loads((p/'native-results.json').read_text())
assert c['status']=='FAILED_NATIVE' and c['new_accepted_c']==0
assert len(rows)==16 and len({x['source_sha256'] for x in rows})==16
assert {x['source'] for x in rows}=={x.name for x in (p/'sources').glob('*.c')}
for row in rows:
    b=(p/'sources'/row['source']).read_bytes();assert hashlib.sha256(b).hexdigest()==row['source_sha256'];assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==row['source_git_blob_sha1']
    assert row['original_reference_exact'] and row['native_status']=='FAILED_NATIVE' and not row['exact'] and 'error' not in row
for region in ('usa','japan_0'):
    r=[x for x in rows if x['region']==region];assert len(r)==8
    best=next(x for x in r if x['source']==region+'_scalar.c');assert best['linked_matching_words']==max(x['linked_matching_words'] for x in r)==61
    assert best['extent_exact'] and best['named_relocations_exact'] and best['relocation_count']==best['reference_relocations']==24
    assert best['raw_difference_offsets']==c['remaining_mismatch_offsets'] and best['first_expected_word']=='8fa40028' and best['first_actual_word']=='002c0821'
    base=next(x for x in r if x['source']==region+'_baseline.c');assert base['linked_matching_words']==12 and not base['extent_exact']
print('Phase 4 research checkpoint consistency PASS (no native promotion)')
