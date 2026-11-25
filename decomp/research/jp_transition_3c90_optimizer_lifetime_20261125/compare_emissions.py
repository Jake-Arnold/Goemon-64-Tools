#!/usr/bin/env python3
"""Compare stock IDO diagnostic emission sequences; raw traces remain private."""
import json, hashlib
from pathlib import Path
p=Path(__file__).resolve().parent
s=json.loads((p/'evidence/stage_summary.json').read_text())
base='func_80003090_3C90_direct_control'
traces={}
for r in s['variants']:
    n=r['variant'].removesuffix('.c')
    t=(p/'private_traces'/f'{n}.log').read_text()
    traces[n]=[l for l in t.splitlines() if l.startswith('emit_')]
    assert traces[n]
rows={n:dict(emission_count=len(e),emission_sha256=hashlib.sha256('\n'.join(e).encode()).hexdigest(),equal_direct_control=e==traces[base]) for n,e in traces.items()}
print(json.dumps(rows,indent=2))
