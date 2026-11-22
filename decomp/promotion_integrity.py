"""Fail-closed ROM-free canonical promotion transaction consistency check.

A dated research/native/G2 report is not acceptance. Only entries in the
current canonical manifest with matching stored full-ROM G2 and strict inventory
may be reported as accepted. This prevents staged-only commits being reported
as production promotions, the failure observed 2026-11-22.

The actual private-ROM verifier/ELF/relocation gate remains mandatory and
independent. This module does not mint native or ROM proof.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
ORIGINAL_SHA1='6ea0ed71032ce08fc2745f412d84936382197494'


def audit(root:Path=ROOT)->dict:
    root=Path(root)
    from .verify import claimed_functions,load_manifest
    failures=[]
    try:
        manifest=load_manifest(root/'manifest.json')
        claims=claimed_functions(manifest)
    except (ValueError,KeyError,FileNotFoundError) as exc:
        return {'status':'FAIL','errors':['Canonical manifest/source invalid: '+str(exc)]}
    count=len(claims)
    code_bytes=sum(f['size'] for f in claims)
    names=[f['name'] for f in claims]
    ranges=sorted((f['rom_offset'],f['rom_offset']+f['size'],f['name']) for f in claims)
    if count!=len(set(names)):
        failures.append('Canonical C names repeat')
    if any(a[1]>b[0] for a,b in zip(ranges,ranges[1:])):
        failures.append('Canonical C ROM ranges overlap')
    try:
        proof=json.loads((root/'results/combined.json').read_text())
        inv=json.loads((root/'results/inventory.json').read_text())
    except (FileNotFoundError,ValueError) as exc:
        return {'status':'FAIL','errors':['Missing/malformed canonical proof/inventory: '+str(exc)]}
    comparison=proof.get('comparison') or {}
    summary=inv.get('summary') or {}
    if proof.get('status')!='matched' or comparison.get('full_rom_match') is not True:
        failures.append('Canonical whole-ROM G2 is not matched')
    for field in ('claimed_functions','matched_functions'):
        if type(comparison.get(field)) is not int or comparison[field]!=count:
            failures.append(f'Manifest and combined.{field} disagree ({count} vs {comparison.get(field)})')
    if comparison.get('matched_function_bytes')!=code_bytes:
        failures.append('Manifest C original instruction bytes disagree with combined G2')
    if summary.get('newly_matching_c')!=count:
        failures.append('Canonical inventory C count does not match manifest')
    if summary.get('current_unmarked_entries')!=count+summary.get('upstream_unmarked_entries',-10000):
        failures.append('Canonical inventory C baseline partition does not match')
    if summary.get('identified_function_entries')!=7376 or summary.get('remaining_assembly_entries')!=7376-count-13:
        failures.append('Canonical inventory total ELF C+ASM function partition does not match')
    if summary.get('extra_positive_alias_entries') not in (0,None):
        failures.append('Unexpected extra positive ELF function labels')
    if (comparison.get('rom_size')!=33554432 or
            comparison.get('expected_sha1')!=ORIGINAL_SHA1 or
            comparison.get('candidate_sha1')!=ORIGINAL_SHA1 or
            inv.get('decompressed_sha1')!=ORIGINAL_SHA1):
        failures.append('Original full 32 MiB ROM SHA-1 or size not authenticated')
    proof_entries=comparison.get('functions') or []
    if len(proof_entries)!=count:
        failures.append('Combined G2 does not contain every one of the canonical C function entries')
    else:
        details=Counter((f.get('name'),int(f.get('size',-1))) for f in proof_entries)
        expected=Counter((f['name'],f['size']) for f in claims)
        if details!=expected:
            failures.append('Combined G2 C function names/sizes differ from accepted manifest')
        if any(f.get('matched') is not True for f in proof_entries):
            failures.append('Combined G2 contains unmatched individual C functions')
    if manifest.get('overlay_reconcile108_stage'):
        f=root/'results/usa_canonical_reconcile108_2072_g2_20261122.json'
        if not f.exists():
            failures.append('Accepted reconciliation stage lacks published stage-level full-ROM/ELF proof')
        else:
            stage=json.loads(f.read_text())
            if (stage.get('status')!='PASSED_G2_LOCAL' or stage.get('accepted_after')!=count
                    or stage.get('rom_sha1')!=ORIGINAL_SHA1 or
                    stage.get('new_C')!=108 or stage.get('semantic_relocations')!=82103):
                failures.append('Reconcile108 stage proof mismatch')
    return {'status':'PASS' if not failures else 'FAIL',
            'accepted_C':count,'accepted_original_bytes':code_bytes,
            'remaining_assembly':7376-count-13,'errors':failures,
            'notice':'Stored published canonical proof only; original-ROM G2 and ELF audits must be freshly run before promotion.'}


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--validate',action='store_true',help='Validate authoritative manifest, full G2 report and strict inventory')
    parser.add_argument('--status',action='store_true',help='Print accepted counts and validation status')
    parser.add_argument('--root',type=Path,default=ROOT)
    a=parser.parse_args(argv)
    r=audit(a.root)
    print(json.dumps(r,indent=2))
    return 0 if r['status']=='PASS' else 1

if __name__=='__main__':
    raise SystemExit(main())
