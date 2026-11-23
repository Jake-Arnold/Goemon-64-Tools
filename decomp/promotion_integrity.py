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
    try:
        proof=json.loads((root/'results/combined.json').read_text())
        inv=json.loads((root/'results/inventory.json').read_text())
    except (FileNotFoundError,ValueError) as exc:
        return {'status':'FAIL','errors':['Missing/malformed canonical proof/inventory: '+str(exc)]}
    if manifest.get('usa_native151_promotion'):
        return _audit_native151(root,manifest,proof,inv)
    return _audit_historical(root,manifest,proof,inv,claims)


def _audit_historical(root,manifest,proof,inv,claims):
    failures=[]
    count=len(claims)
    code_bytes=sum(f['size'] for f in claims)
    names=[f['name'] for f in claims]
    ranges=sorted((f['rom_offset'],f['rom_offset']+f['size'],f['name']) for f in claims)
    if count!=len(set(names)):
        failures.append('Canonical C names repeat')
    if any(a[1]>b[0] for a,b in zip(ranges,ranges[1:])):
        failures.append('Canonical C ROM ranges overlap')
    # The original 2164-C proof and ELF inventory must remain immutable.
    # A VM436 promotion is an additive final stage, not a rewrite of short72.
    vm436_stage = manifest.get('usa_script_vm436_promotion') is not None
    frozen_2164_inv = inv
    if vm436_stage:
        from . import usa_script_vm436_promotion as vm436
        if manifest.get('usa_script_vm436_promotion') != {'format':vm436.FORMAT}:
            failures.append('Unreviewed VM436 source stage')
        frozen_p = root/'results/combined_2164_before_vm436_20261123.json'
        frozen_i = root/'results/inventory_2164_before_vm436_20261123.json'
        if not frozen_p.is_file() or not frozen_i.is_file():
            failures.append('VM436 missing immutable original 2164-C snapshots')
        else:
            frozen_p_hash=hashlib.sha256(frozen_p.read_bytes()).hexdigest()
            frozen_i_hash=hashlib.sha256(frozen_i.read_bytes()).hexdigest()
            if (frozen_p_hash!='0e50cb93034e48ba721c76d69906a997e44f2e5ff2a2c6eb4b35a386af941b2e' or
                    frozen_i_hash!='4dd32f74c5bf051f99a3da108b766faeb6c64812ae4e7ba9ce786011c5fa4f20'):
                failures.append('VM436 original accepted G2 snapshot bytes changed')
            frozen_proof=json.loads(frozen_p.read_text())
            frozen_2164_inv=json.loads(frozen_i.read_text())
            cp=frozen_proof.get('comparison') or {}
            summary_old=frozen_2164_inv.get('summary') or {}
            if (frozen_proof.get('status')!='matched' or cp.get('matched_functions')!=2164 or
                    cp.get('matched_function_bytes')!=99604 or cp.get('full_rom_match') is not True or
                    summary_old.get('newly_matching_c')!=2164 or
                    summary_old.get('remaining_assembly_entries')!=5199):
                failures.append('VM436 original 2164-C predecessor identity failed')
            if frozen_2164_inv.get('baseline_elf_sha256')!=inv.get('baseline_elf_sha256'):
                failures.append('VM436 original ELF baseline changed')
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
    short72_stage = manifest.get('overlay_usa_short72_stage') is not None
    new2_stage = manifest.get('overlay_usa_opening_new2_stage') is not None
    short72_predecessor_inv=inv
    if short72_stage:
        short72_predecessor_proof=root/'results/combined_2092_before_short72_20261123.json'
        short72_predecessor_inv_path=root/'results/inventory_2092_before_short72_20261123.json'
        if not short72_predecessor_proof.is_file() or not short72_predecessor_inv_path.is_file():
            failures.append('Post2092 short72 historical canonical predecessor evidence missing')
        else:
            oldproof=json.loads(short72_predecessor_proof.read_text())
            short72_predecessor_inv=json.loads(short72_predecessor_inv_path.read_text())
            if (oldproof.get('status')!='matched' or
                oldproof.get('comparison',{}).get('matched_functions')!=2092 or
                oldproof.get('comparison',{}).get('matched_function_bytes')!=94760 or
                oldproof.get('comparison',{}).get('full_rom_match') is not True or
                short72_predecessor_inv.get('summary',{}).get('newly_matching_c')!=2092):
                failures.append('Post2092 short72 historical canonical predecessor mismatch')

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
            if (count,code_bytes)!=((2165,100040) if vm436_stage else (2164,99604) if short72_stage else (2092,94760) if new2_stage else (2090,94668)):
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
                e.get('candidate_elf_sha256')!=short72_predecessor_inv.get('candidate_elf_sha256') or
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
    if short72_stage:
        from . import usa_short72_promotion as short72
        evidence=root/'results/usa_short72_2164_g2_20261123.json'
        if manifest.get('overlay_usa_short72_stage')!={'format':short72.FORMAT}:
            failures.append('Post2092 short72 source-stage format mismatch')
        if not evidence.is_file():
            failures.append('Post2092 short72 current whole-ROM G2 evidence missing')
        else:
            e=json.loads(evidence.read_text())
            stage=proof.get('overlay_usa_short72_stage') or {}
            if (e.get('status')!='PASSED_G2_LOCAL' or
                e.get('prior_c')!=2092 or e.get('accepted_c_after')!=2164 or
                e.get('added_c')!=72 or e.get('added_original_bytes')!=4844 or
                e.get('accepted_original_bytes_after')!=99604 or
                e.get('original_rom_sha1')!=ORIGINAL_SHA1 or
                e.get('original_32MiB_ROM_bytes_exact')!=33554432 or
                e.get('positive_elf_function_identities_exact')!=7376 or
                e.get('semantic_relocations_exact')!=82103 or
                e.get('semantic_relocation_sha256')!=short72.RELOC_HASH or
                e.get('stable_global_symbol_identities_exact')!=26714 or
                e.get('original_elf_sha256')!=inv.get('baseline_elf_sha256') or
                e.get('candidate_elf_sha256')!=frozen_2164_inv.get('candidate_elf_sha256') or
                e.get('original_source_manifest_sha256')!=short72.FROZEN_FIXTURE_HASH or
                e.get('strict_inventory')!='PASS' or
                e.get('complete_local_ci')!='PASS' or
                stage.get('status')!='PASSED_G2_LOCAL' or
                stage.get('accepted_c_after')!=2164 or
                stage.get('all_semantic_relocations_equal') is not True or
                stage.get('stable_ELF_globals_equal') is not True or
                (count,code_bytes)!=((2165,100040) if vm436_stage else (2164,99604))):
                failures.append('Post2092 short72 atomic canonical G2/ELF/relocation/local CI evidence mismatch')
    if vm436_stage:
        from . import usa_script_vm436_promotion as vm436
        stage=proof.get('usa_script_vm436_promotion') or {}
        path=root/'results/usa_script_vm436_2165_g2_20261123.json'
        if not path.is_file():
            failures.append('VM436 missing new 2165-C exact original-ROM G2 record')
        else:
            dated=json.loads(path.read_text())
            if (dated.get('status')!='PASSED_G2_LOCAL' or dated.get('name')!=vm436.NAME or
                    dated.get('source_sha256')!=vm436.ORIGINAL_C_SOURCE_SHA256 or
                    dated.get('rom_sha1')!=ORIGINAL_SHA1 or dated.get('accepted_c')!=2165 or
                    dated.get('remaining_assembly')!=5198 or dated.get('elf_function_identities')!=7376 or
                    dated.get('semantic_relocations')!=82103 or
                    dated.get('candidate_elf_sha256')!=inv.get('candidate_elf_sha256') or
                    dated.get('predecessor_elf_sha256')!=frozen_2164_inv.get('candidate_elf_sha256') or
                    dated.get('full_rom_g2')!='PASS' or dated.get('inventory')!='PASS'):
                failures.append('VM436 dated G2/inventory transaction mismatched')
        if (stage.get('status')!='PASSED_G2_LOCAL' or
                stage.get('base_matching_C')!=2164 or stage.get('accepted_c_after')!=2165 or
                stage.get('added_matching_C')!=1 or stage.get('added_instruction_bytes')!=436 or
                stage.get('accepted_original_bytes_after')!=100040 or
                stage.get('remaining_assembly')!=5198 or stage.get('full_rom_match') is not True or
                stage.get('original_rom_sha1')!=ORIGINAL_SHA1 or
                stage.get('complete_original_ROM_bytes_exact')!=33554432 or
                stage.get('original_positive_ELF_functions_exact')!=7376 or
                stage.get('canonical_semantic_relocations_exact')!=82103 or
                stage.get('canonical_semantic_relocation_sha256')!='f7f25e257c9bce27c00e756b85ca7bfa5774137925d5aba9a6626ba4693e5a97' or
                stage.get('stable_global_symbols_exact')!=26714 or
                stage.get('source_original_C_sha256')!=vm436.ORIGINAL_C_SOURCE_SHA256 or
                stage.get('compiled_original_source_sha256')!=vm436.MERGED_VM_SOURCE_SHA256 or
                stage.get('canonical_predecessor_ELF_sha256')!=frozen_2164_inv.get('candidate_elf_sha256') or
                stage.get('original_candidate_ELF_sha256')!=inv.get('candidate_elf_sha256') or
                proof.get('retained_assembly_functions',[]).count(vm436.NAME)!=0 or
                inv.get('summary',{}).get('size_annotation_differences')!=
                    [{'name':'func_8003F6E8_402E8','baseline_size':48,'candidate_size':56}]):
            failures.append('VM436 current 2165-C exact original-ROM/ELF/relocation proof mismatch')
    return {'status':'PASS' if not failures else 'FAIL',
            'accepted_C':count,'accepted_original_bytes':code_bytes,
            'remaining_assembly':7376-count-13,'errors':failures,
            'notice':'Stored published canonical proof only; original-ROM G2 and ELF audits must be freshly run before promotion.'}


def _audit_native151(root,manifest,proof,inv):
    from .verify import claimed_functions,load_manifest
    from . import native251_promotion as stage
    failures=[]
    frozen={
        'manifest_2165_before_native151_20261123.json':'b1f5dbf5fd60bf3cd3e44a5a0fa878b63f9ac7b3be8deeee4f92b67a5e837ce3',
        'combined_2165_before_native151_20261123.json':'3af4fde80100020bc88b8696c6f7cc5b59e5c8e0300383ec02efc6f9ca9eb9dc',
        'inventory_2165_before_native151_20261123.json':'33dc55248db3654de72639c3e7ceed80b85c9ce142661db75a2ee573d5e9b0e3'}
    try:
        for file,expected in frozen.items():
            if hashlib.sha256((root/'results'/file).read_bytes()).hexdigest()!=expected:raise ValueError('Historical proof changed: '+file)
        previous=load_manifest(root/'results/manifest_2165_before_native151_20261123.json')
        prior={k:v for k,v in manifest.items() if k!='usa_native151_promotion'}
        if previous!=prior:raise ValueError('Native151 changed original accepted predecessor manifest')
        oldproof=json.loads((root/'results/combined_2165_before_native151_20261123.json').read_text());oldinv=json.loads((root/'results/inventory_2165_before_native151_20261123.json').read_text())
        a=_audit_historical(root,previous,oldproof,oldinv,claimed_functions(previous));failures.extend(a['errors'])
        fs=stage.validate_predecessor(manifest)
    except (ValueError,KeyError,FileNotFoundError) as exc:
        return {'status':'FAIL','errors':['Native151 predecessor disagree: '+str(exc)]}
    claims=claimed_functions(manifest);count=len(claims);size=sum(x['size'] for x in claims)
    c=proof.get('comparison') or {};i=inv.get('summary') or {};p=proof.get('usa_native151_promotion') or {}
    if proof.get('status')!='matched' or not c.get('full_rom_match') or (c.get('matched_functions'),c.get('claimed_functions'),c.get('matched_function_bytes'))!=(count,count,size):failures.append('Native151 manifest and full ROM G2 disagree')
    if (c.get('expected_sha1'),c.get('candidate_sha1'),c.get('rom_size'),inv.get('decompressed_sha1'))!=(ORIGINAL_SHA1,ORIGINAL_SHA1,33554432,ORIGINAL_SHA1):failures.append('Native151 original ROM identity mismatch')
    if (i.get('newly_matching_c'),i.get('current_unmarked_entries'),i.get('remaining_assembly_entries'),i.get('identified_function_entries'),i.get('extra_positive_alias_entries'))!=(count,count+13,7376-count-13,7376,0):failures.append('Native151 inventory C count/ownership mismatch')
    if inv.get('baseline_elf_sha256')!=oldinv.get('baseline_elf_sha256') or i.get('function_entry_identity_sha256')!=oldinv['summary']['function_entry_identity_sha256'] or i.get('size_annotation_differences')!=oldinv['summary']['size_annotation_differences']:failures.append('Native151 historical ELF identity changed')
    rows=c.get('functions',[]);expected={(x['name'],x['size'],x['rom_offset']) for x in claims}
    try:actual={(x['name'],x['size'],int(x['rom_offset'],16)) for x in rows}
    except (KeyError,ValueError,TypeError):actual=set()
    if len(rows)!=count or actual!=expected or any(x.get('matched') is not True for x in rows):failures.append('Native151 full original function list mismatch')
    if (p.get('status'),p.get('base_c'),p.get('accepted_c_after'),p.get('added_c'),p.get('added_original_bytes'),p.get('accepted_original_bytes_after'),p.get('original_32MiB_ROM_bytes_exact'),p.get('positive_elf_function_identities_exact'),p.get('semantic_relocations_exact'),p.get('stable_global_symbols_exact'),p.get('source_manifest_sha256'),p.get('semantic_relocation_sha256'),p.get('candidate_elf_sha256'),p.get('original_elf_sha256'))!=('PASSED_G2_LOCAL',2165,2316,151,9808,109848,33554432,7376,82103,26714,stage.MANIFEST_SHA,stage.RELOCS['usa'][1],inv.get('candidate_elf_sha256'),inv.get('baseline_elf_sha256')) or p.get('full_rom_match') is not True or p.get('ownership_exact') is not True:
        failures.append('Native151 current canonical ELF/relocation transaction mismatch')
    fingerprints={x['name']:x for x in rows}
    for x in fs:
        row=fingerprints.get(x['name'],{});key='research/promotion251_20261123/'+x['source']
        if row.get('guest_address')!=f'0x{x["vma"]:08X}' or row.get('expected_sha256')!=x['code_sha256'] or row.get('candidate_sha256')!=x['code_sha256'] or proof.get('sources_sha256_lf',{}).get(key)!=x['source_sha256']:failures.append('Native151 function/source fingerprint mismatch '+x['name'])
    return {'status':'FAIL' if failures else 'PASS','accepted_C':count,'accepted_original_bytes':size,'remaining_assembly':7376-count-13,'errors':failures,'notice':'Stored proof only; fresh G2 and full CI separately required.'}


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
