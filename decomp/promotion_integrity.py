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
            if (stage.get('status')!='PASSED_G2_LOCAL' or stage.get('accepted_after')!=2072
                    or stage.get('rom_sha1')!=ORIGINAL_SHA1 or
                    stage.get('new_C')!=108 or stage.get('semantic_relocations')!=82103):
                failures.append('Reconcile108 stage proof mismatch')
    if manifest.get('overlay_crossregion7_stage'):
        from . import usa_crossregion7 as cross7
        evidence=root/'results/usa_crossregion7_2079_g2_20261122.json'
        if not evidence.exists():
            failures.append('Crossregion7 accepted without dated combined original-ROM/ELF proof')
        else:
            doc=json.loads(evidence.read_text())
            if (doc.get('status')!='PASSED_G2' or doc.get('after_c')!=2079 or
                    doc.get('added_c')!=7 or doc.get('after_bytes')!=93016 or
                    doc.get('original_rom_sha1')!=ORIGINAL_SHA1 or
                    doc.get('original_elf_functions')!=7376 or
                    doc.get('semantic_relocations_unchanged') is not True):
                failures.append('Crossregion7 proof is not a reviewed full-ROM acceptance')
    # Post2090 C stages preserve the original published Mini11 predecessor proof
    # and inventory as immutable historical evidence, rather than rewriting its
    # ELF object fingerprints to equal later candidate link outputs.
    new2_stage = manifest.get('overlay_usa_opening_new2_stage') is not None
    mini_predecessor_inv=inv
    if new2_stage:
        historical_proof=root/'results/combined_2090_pre_opening_new2_20261123.json'
        historical_inv=root/'results/inventory_2090_pre_opening_new2_20261123.json'
        if not historical_proof.is_file() or not historical_inv.is_file():
            failures.append('Post2090 new2 missing frozen 2090 predecessor proof/inventory')
        else:
            prev_proof=json.loads(historical_proof.read_text())
            mini_predecessor_inv=json.loads(historical_inv.read_text())
            if (prev_proof.get('status')!='matched' or
                prev_proof.get('comparison',{}).get('matched_functions')!=2090 or
                prev_proof.get('comparison',{}).get('matched_function_bytes')!=94668 or
                prev_proof.get('comparison',{}).get('full_rom_match') is not True or
                mini_predecessor_inv.get('summary',{}).get('newly_matching_c')!=2090):
                failures.append('Post2090 frozen predecessor accepted-C proof invalid')
    if manifest.get('overlay_mini10_stage') or manifest.get('overlay_mini_selector_stage'):
        # Both native USA Mini stages must be reconciled atomically into the
        # complete current-branch proof. A scratch pristine ROM is not enough.
        if (manifest.get('overlay_mini10_stage') != {'format':'goemon-usa-mini10-post2079-v1'} or
            manifest.get('overlay_mini_selector_stage') != {'format':'goemon-usa-mini-selector-post2089-v1'}):
            failures.append('Mini11 incomplete canonical stage pairing')
        ledger=root/'results/usa_mini11_2090_g2_20261123.json'
        if not ledger.is_file():
            failures.append('Mini11 G2 stage proof is missing')
        else:
            doc=json.loads(ledger.read_text())
            if (doc.get('format')!='goemon-usa-mini-11-post-2079-canonical-G2-v1' or
                doc.get('status')!='PASSED_G2_LOCAL' or
                doc.get('accepted_c_prior')!=2079 or
                doc.get('accepted_c_after')!=2090 or
                doc.get('new_c_functions')!=11 or
                doc.get('new_original_instruction_bytes')!=1652 or
                doc.get('accepted_original_bytes_after')!=94668 or
                doc.get('remaining_assembly_entries')!=5273 or
                doc.get('original_expanded_rom_sha1')!=ORIGINAL_SHA1 or
                doc.get('original_32MiB_ROM_bytes_exact')!=33554432 or
                doc.get('positive_elf_function_identities_exact')!=7376 or
                doc.get('semantic_relocations_exact')!=82103 or
                doc.get('complete_semantic_relocation_sha256')!='f7f25e257c9bce27c00e756b85ca7bfa5774137925d5aba9a6626ba4693e5a97' or
                doc.get('original_elf_sha256')!=inv.get('baseline_elf_sha256') or
                doc.get('candidate_elf_sha256')!=mini_predecessor_inv.get('candidate_elf_sha256') or
                doc.get('canonical_verifier_status')!='PASS' or
                doc.get('canonical_inventory_status')!='PASS' or
                any(doc.get('stages',{}).get(k,{}).get('status')!='PASSED_G2_LOCAL' for k in ('mini10','selector'))):
                failures.append('Mini11 current combined original-ROM/ELF G2 proof mismatch')
            if (count,code_bytes)!=((2092,94760) if new2_stage else (2090,94668)):
                failures.append('Mini11/post2090 accepted count and ROM bytes changed')
            if len(doc.get('functions',[]))!=11 or sum(f['size'] for f in doc.get('functions',[]))!=1652:
                failures.append('Mini11 native source/size ledger incomplete')
    if new2_stage:
        from . import usa_opening_new2_promotion as opening
        evidence=root/'results/usa_file18_new2_2092_g2_20261123.json'
        if manifest.get('overlay_usa_opening_new2_stage')!={'format':opening.FORMAT}:
            failures.append('New2 original-source stage identity wrong')
        if not evidence.is_file():
            failures.append('New2 post2090 canonical 2092 full-ROM/ELF proof missing')
        else:
            e=json.loads(evidence.read_text())
            stage=proof.get('overlay_usa_opening_new2_stage') or {}
            if (e.get('status')!='PASSED_G2_LOCAL' or
                e.get('prior_c')!=2090 or e.get('accepted_c_after')!=2092 or
                e.get('accepted_original_bytes_after')!=94760 or
                e.get('added_original_bytes')!=92 or
                e.get('full_rom_sha1')!=ORIGINAL_SHA1 or
                e.get('complete_semantic_relocations')!=82103 or
                e.get('semantic_relocation_sha256')!=opening.RELOC_HASH or
                e.get('candidate_elf_sha256')!=inv.get('candidate_elf_sha256') or
                e.get('baseline_elf_sha256')!=inv.get('baseline_elf_sha256') or
                e.get('source_manifest_sha256')!=opening.FIXTURE_HASH or
                e.get('strict_inventory')!='PASS' or
                e.get('complete_local_ci')!='PASS' or
                stage.get('status')!='PASSED_G2_LOCAL' or
                stage.get('accepted_c_after')!=2092 or
                stage.get('all_semantic_relocations_equal') is not True or
                stage.get('stable_ELF_globals_equal') is not True or
                len(e.get('new_functions',[]))!=2 or
                sum(x.get('size',0) for x in e.get('new_functions',[]))!=92):
                failures.append('Post2090 new2 full canonical G2/ELF/inventory proof mismatch')
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
