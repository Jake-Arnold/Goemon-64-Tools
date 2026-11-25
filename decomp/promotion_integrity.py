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
    if manifest.get('usa_batch302_promotion'):
        from . import batch302_promotion as batch302
        return batch302.audit_usa(root,manifest,proof,inv)
    if manifest.get('usa_consolidated29_promotion'):
        from . import consolidated_batch_promotion as batch
        return batch.audit(root,manifest,proof,inv)
    if manifest.get('usa_transition_final_promotion'):
        from . import transition_final_promotion as tf
        return tf.audit(root,manifest,proof,inv)
    if manifest.get('usa_transition1_promotion'):
        from . import transition_promotion as tr
        return tr.audit_usa(root,manifest,proof,inv)
    if manifest.get('usa_cright4_promotion'):
        return _audit_cright4(root,manifest,proof,inv)
    if manifest.get('usa_script_vm_dual_reference'):
        return _audit_vmdual(root,manifest,proof,inv)
    if manifest.get('usa_script_vm440_promotion'):
        return _audit_vm440(root,manifest,proof,inv)
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


def _audit_vm440(root,manifest,proof,inv):
    from .verify import claimed_functions,load_manifest
    from . import usa_script_vm440_promotion as stage
    failures=[]
    frozen={
        'manifest_2316_before_vm440_20261123.json':'4eaa2acc8468abecb5d2f2c7f89d7892e25e57cd65361be8b6ca00f8dd8d7b31',
        'combined_2316_before_vm440_20261123.json':'94a445d074af7107515f06e009cce7f9b024abbaf1591e2f3ec8b919fb956ebd',
        'inventory_2316_before_vm440_20261123.json':'5461ea400968d2e5fab865a6a447a5f7c45bfac91b6ac866260dfc3202d90055'}
    try:
        for name,h in frozen.items():
            if hashlib.sha256((root/'results'/name).read_bytes()).hexdigest()!=h:raise ValueError('Historical proof changed: '+name)
        before=load_manifest(root/'results/manifest_2316_before_vm440_20261123.json')
        if before!={k:v for k,v in manifest.items() if k!=stage.KEY}:raise ValueError('VM440 predecessor manifest changed')
        oldproof=json.loads((root/'results/combined_2316_before_vm440_20261123.json').read_text())
        oldinv=json.loads((root/'results/inventory_2316_before_vm440_20261123.json').read_text())
        failures.extend(_audit_native151(root,before,oldproof,oldinv)['errors'])
        stage.validate_predecessor(manifest)
    except (ValueError,KeyError,FileNotFoundError) as exc:
        return {'status':'FAIL','errors':['VM440 predecessor disagree: '+str(exc)]}
    claims=claimed_functions(manifest);count=len(claims);size=sum(f['size'] for f in claims)
    c=proof.get('comparison') or {};i=inv.get('summary') or {};p=proof.get(stage.KEY) or {}
    if proof.get('status')!='matched' or c.get('full_rom_match') is not True or (c.get('matched_functions'),c.get('claimed_functions'),c.get('matched_function_bytes'))!=(count,count,size):failures.append('VM440 manifest and full ROM G2 disagree')
    if (c.get('expected_sha1'),c.get('candidate_sha1'),c.get('rom_size'),inv.get('decompressed_sha1'))!=(ORIGINAL_SHA1,ORIGINAL_SHA1,33554432,ORIGINAL_SHA1):failures.append('VM440 original ROM identity mismatch')
    if (count,size)!=(2317,110288) or (i.get('newly_matching_c'),i.get('current_unmarked_entries'),i.get('remaining_assembly_entries'),i.get('identified_function_entries'),i.get('extra_positive_alias_entries'))!=(count,count+13,7376-count-13,7376,0):failures.append('VM440 inventory C count/ownership mismatch')
    if inv.get('baseline_elf_sha256')!=oldinv.get('baseline_elf_sha256') or i.get('function_entry_identity_sha256')!=oldinv['summary']['function_entry_identity_sha256'] or i.get('size_annotation_differences')!=oldinv['summary']['size_annotation_differences']:failures.append('VM440 historical ELF identity changed')
    rows=c.get('functions',[]);oldrows=oldproof['comparison']['functions'];oldby={x['name']:x for x in oldrows};newby={x['name']:x for x in rows}
    expected={(x['name'],x['size'],x['rom_offset'],x.get('vma',x['rom_offset']+0x80000000-0xC00)) for x in claims}
    try:actual={(x['name'],x['size'],int(x['rom_offset'],16),int(x['guest_address'],16)) for x in rows}
    except (KeyError,ValueError,TypeError):actual=set()
    if len(rows)!=count or actual!=expected or any(x.get('matched') is not True or x.get('expected_sha256')!=x.get('candidate_sha256') for x in rows):failures.append('VM440 full original function list mismatch')
    if set(newby)-set(oldby)!={stage.NAME} or any(newby.get(name)!=row for name,row in oldby.items()):failures.append('VM440 earlier function proof changed')
    row=newby.get(stage.NAME,{})
    key=stage.SOURCE.relative_to(ROOT).as_posix()
    oldsources=oldproof['sources_sha256_lf'];sources=proof.get('sources_sha256_lf',{})
    if row.get('expected_sha256')!=stage.CODE_SHA or sources.get(key)!=stage.SOURCE_SHA or any(sources.get(k)!=v for k,v in oldsources.items()) or set(sources)-set(oldsources)!={key}:failures.append('VM440 original source or code fingerprint mismatch')
    checks={'status':'PASSED_G2_LOCAL','base_c':2316,'accepted_c_after':2317,'added_c':1,'added_original_bytes':440,'accepted_original_bytes_after':110288,'remaining_assembly':5046,'full_rom_match':True,'original_rom_sha1':ORIGINAL_SHA1,'original_32MiB_ROM_bytes_exact':33554432,'positive_elf_function_identities_exact':7376,'semantic_relocations_exact':82103,'semantic_relocation_sha256':stage.RELOC_SHA,'stable_global_symbols_exact':26714,'source_sha256':stage.SOURCE_SHA,'mixed_source_sha256':stage.MERGED_SHA,'original_code_sha256':stage.CODE_SHA,'original_elf_sha256':inv.get('baseline_elf_sha256'),'predecessor_elf_sha256':oldinv.get('candidate_elf_sha256'),'candidate_elf_sha256':inv.get('candidate_elf_sha256'),'unit_text_bytes_exact':10112,'unit_text_relocations_exact':740,'unit_rodata_relocations_exact':15,'metadata_only_changed_bytes':2,'ownership_exact':True,'compiler_quirk_outcome':'EXISTING_QUIRK_REPRODUCED'}
    if any(p.get(k)!=v for k,v in checks.items()):failures.append('VM440 current canonical ELF/relocation transaction mismatch')
    try:
        dated=json.loads((root/'results/usa_script_vm440_2317_g2_20261123.json').read_text())
        if dated!=p:failures.append('VM440 dated G2 proof mismatch')
    except (FileNotFoundError,ValueError):failures.append('VM440 missing dated G2 proof')
    if stage.NAME in proof.get('retained_assembly_functions',[]):failures.append('VM440 still retained as ASM')
    return {'status':'FAIL' if failures else 'PASS','accepted_C':count,'accepted_original_bytes':size,'remaining_assembly':7376-count-13,'errors':failures,'notice':'Stored proof only; fresh G2 and full CI separately required.'}



def _audit_vmdual(root,manifest,proof,inv):
    from .verify import claimed_functions,load_manifest
    from . import usa_script_vm_dual_reference as stage
    failures=[]
    frozen={
        'manifest_2317_before_vmdual_20261123.json':'7b3b2f83da1934b71bba77cc3971e8611ee7349d7fc0af5c122dabbd1377eaee',
        'combined_2317_before_vmdual_20261123.json':'a951b4a3511a16dffb2c1cfd9d1c709742810684229f3b3db451385ed7b2d18a',
        'inventory_2317_before_vmdual_20261123.json':'54a7e786fc50acaa670f3199a0c219875db8247ccb670d0b14b2b0f518e8bad2'}
    try:
        for name,h in frozen.items():
            if hashlib.sha256((root/'results'/name).read_bytes()).hexdigest()!=h:raise ValueError('Historical proof changed: '+name)
        before=load_manifest(root/'results/manifest_2317_before_vmdual_20261123.json')
        if before!={k:v for k,v in manifest.items() if k!=stage.KEY}:raise ValueError('VM dual predecessor manifest changed')
        oldproof=json.loads((root/'results/combined_2317_before_vmdual_20261123.json').read_text())
        oldinv=json.loads((root/'results/inventory_2317_before_vmdual_20261123.json').read_text())
        failures.extend(_audit_vm440(root,before,oldproof,oldinv)['errors'])
        prior=stage.validate_predecessor(manifest)
    except (ValueError,KeyError,FileNotFoundError) as exc:
        return {'status':'FAIL','errors':['VM dual predecessor disagree: '+str(exc)]}
    claims=prior+stage.claims();count=len(claims);size=sum(f['size'] for f in claims)
    c=proof.get('comparison') or {};i=inv.get('summary') or {};p=proof.get(stage.KEY) or {}
    if proof.get('status')!='matched' or c.get('full_rom_match') is not True or (c.get('matched_functions'),c.get('claimed_functions'),c.get('matched_function_bytes'))!=(count,count,size):failures.append('VM dual manifest and full ROM G2 disagree')
    if (c.get('expected_sha1'),c.get('candidate_sha1'),c.get('rom_size'),inv.get('decompressed_sha1'))!=(ORIGINAL_SHA1,ORIGINAL_SHA1,33554432,ORIGINAL_SHA1):failures.append('VM dual original ROM identity mismatch')
    if (count,size)!=(2319,111008) or (i.get('newly_matching_c'),i.get('current_unmarked_entries'),i.get('remaining_assembly_entries'),i.get('identified_function_entries'),i.get('extra_positive_alias_entries'))!=(count,count+13,7376-count-13,7376,0):failures.append('VM dual inventory C count/ownership mismatch')
    if inv.get('baseline_elf_sha256')!=oldinv.get('baseline_elf_sha256') or inv.get('candidate_elf_sha256')!=stage.NEW_ELF or i.get('function_entry_identity_sha256')!=oldinv['summary']['function_entry_identity_sha256'] or i.get('size_annotation_differences')!=oldinv['summary']['size_annotation_differences']:failures.append('VM dual historical ELF identity changed')
    rows=c.get('functions',[]);oldby={x['name']:x for x in oldproof['comparison']['functions']};newby={x['name']:x for x in rows}
    expected={(x['name'],x['size'],x['rom_offset'],x.get('vma',x['rom_offset']+0x80000000-0xC00)) for x in claims}
    try:actual={(x['name'],x['size'],int(x['rom_offset'],16),int(x['guest_address'],16)) for x in rows}
    except (KeyError,ValueError,TypeError):actual=set()
    if len(rows)!=count or actual!=expected or any(x.get('matched') is not True or x.get('expected_sha256')!=x.get('candidate_sha256') for x in rows):failures.append('VM dual full original function list mismatch')
    if set(newby)-set(oldby)!={f['name'] for f in stage.TARGETS} or any(newby.get(name)!=row for name,row in oldby.items()):failures.append('VM dual earlier function proof changed')
    oldsources=oldproof['sources_sha256_lf'];sources=proof.get('sources_sha256_lf',{})
    if any(sources.get(k)!=v for k,v in oldsources.items()) or set(sources)-set(oldsources)!={f['source'] for f in stage.TARGETS}:failures.append('VM dual earlier source proof changed')
    for f in stage.TARGETS:
        if newby.get(f['name'],{}).get('expected_sha256')!=f['code_sha256'] or sources.get(f['source'])!=f['source_sha256'] or f['name'] in proof.get('retained_assembly_functions',[]):failures.append('VM dual original source/ownership mismatch '+f['name'])
    checks={'status':'PASSED_G2_DUAL_REFERENCE_LOCAL','base_c':2317,'accepted_c_after':2319,'added_c':2,'added_original_bytes':720,'accepted_original_bytes_after':111008,'remaining_assembly':5044,'original_rom_sha1':ORIGINAL_SHA1,'full_rom_match':True,'original_32MiB_ROM_bytes_exact':33554432,'retail_rom_sha1':stage.RETAIL_SHA,'retail_rom_exact':True,'original_16MiB_ROM_bytes_exact':16777216,'predecessor_elf_sha256':stage.PRIOR_ELF,'candidate_elf_sha256':stage.NEW_ELF,'original_asm_sha256':stage.ORIG_ASM,'original_data_sha256':stage.ORIG_DATA,'independent_prior_asm_sha256':stage.PRIOR_ASM,'independent_shadow_asm_sha256':stage.SHADOW_ASM,'mixed_source_sha256':stage.MIXED_SHA,'targets':[dict(x) for x in stage.TARGETS],'native_object_relocations_unmodified':True,'original_named_relocations':82103,'independent_prior_relocations':82103,'native_relocations':82102,'independent_shadow_relocations':82102,'native_predecessor_relocation_sha256':stage.vm440.RELOC_SHA,'native_shadow_relocation_sha256':stage.NEW_RELOC,'entire_reference_relocations_equal':True,'removed_named_records':45,'added_section_records':44,'native_function_identities':7376,'native_stable_globals':26714,'independent_function_identities':7376,'independent_stable_globals':26714,'unchanged_cross_reference_metadata_sha256':stage.CROSS_METADATA,'original_named_relocation_gate_exact':False,'ordinary_comparator_unchanged':True,'compiler_quirk_outcome':'EXISTING_QUIRK_REPRODUCED'}
    if any(p.get(k)!=v for k,v in checks.items()):failures.append('VM dual independent reference/ROM/ELF transaction mismatch')
    if set(p.get('negative_controls_rejected',[]))!={'wrong_removed_symbol','wrong_added_target','missing_table_reference','wrong_count','wrong_pool_entry','wrong_branch','wrong_pool_addend'}:failures.append('VM dual negative controls incomplete')
    if p.get('independent_prior_elf_sha256')!='3f3aea199f8cf79d879399199e710a4a0884f4cf72e360e90e71c4aab1d4c666' or p.get('independent_shadow_elf_sha256')!='9462f9ca428f72765323b0dbcdfcb15c92c960114e5a0178cf7a472bf6019bd6':failures.append('VM dual independent reference ELF fingerprint changed')
    try:
        dated=json.loads((root/'results/usa_script_vm_dual_2319_g2_20261123.json').read_text())
        if dated!=p:failures.append('VM dual dated G2 proof mismatch')
    except (FileNotFoundError,ValueError):failures.append('VM dual missing dated G2 proof')
    return {'status':'FAIL' if failures else 'PASS','accepted_C':count,'accepted_original_bytes':size,'remaining_assembly':7376-count-13,'errors':failures,'notice':'Stored dual-reference proof only; fresh G2 and full CI separately required.'}


def _audit_cright4(root,manifest,proof,inv):
    from .verify import load_manifest
    from . import usa_cright4_promotion as stage
    errors=[]
    frozen={
        'manifest_2319_before_cright4_20261124.json':'91d8d1b7e7192b4e792e6d5cc868227e6d71b7366dc853a510b8b4a821582fd5',
        'combined_2319_before_cright4_20261124.json':'7e5fa0d4eddf10f6f28b76aa5b16180322b6b69ade91a4f3675b0ce43f25c876',
        'inventory_2319_before_cright4_20261124.json':'166c0fa060a878845e1dae3252ddc7b2af9c256fac2bd7f1278d6fdd203865e5'}
    try:
        for name,h in frozen.items():
            if hashlib.sha256((root/'results'/name).read_bytes()).hexdigest()!=h:raise ValueError('Historical proof changed: '+name)
        before=load_manifest(root/'results/manifest_2319_before_cright4_20261124.json')
        if before!={k:v for k,v in manifest.items() if k!=stage.KEY}:raise ValueError('C-Right4 predecessor manifest changed')
        oldproof=json.loads((root/'results/combined_2319_before_cright4_20261124.json').read_text())
        oldinv=json.loads((root/'results/inventory_2319_before_cright4_20261124.json').read_text())
        errors.extend(_audit_vmdual(root,before,oldproof,oldinv)['errors'])
        prior=stage.validate_predecessor(manifest)
    except (ValueError,KeyError,FileNotFoundError) as exc:
        return {'status':'FAIL','errors':['C-Right4 predecessor disagree: '+str(exc)]}
    claims=prior+stage.claims();count=len(claims);size=sum(f['size'] for f in claims)
    c=proof.get('comparison') or {};i=inv.get('summary') or {};p=proof.get(stage.KEY) or {}
    if proof.get('status')!='matched' or c.get('full_rom_match') is not True or (c.get('matched_functions'),c.get('claimed_functions'),c.get('matched_function_bytes'))!=(count,count,size):errors.append('C-Right4 manifest and full ROM G2 disagree')
    if (c.get('expected_sha1'),c.get('candidate_sha1'),c.get('rom_size'),inv.get('decompressed_sha1'))!=(ORIGINAL_SHA1,ORIGINAL_SHA1,33554432,ORIGINAL_SHA1):errors.append('C-Right4 original ROM identity mismatch')
    if (count,size)!=(2323,111736) or (i.get('newly_matching_c'),i.get('current_unmarked_entries'),i.get('remaining_assembly_entries'),i.get('identified_function_entries'),i.get('extra_positive_alias_entries'))!=(count,count+13,7376-count-13,7376,0):errors.append('C-Right4 inventory C count/ownership mismatch')
    if inv.get('baseline_elf_sha256')!=oldinv.get('baseline_elf_sha256') or inv.get('candidate_elf_sha256')!=stage.NEW_ELF or i.get('function_entry_identity_sha256')!=oldinv['summary']['function_entry_identity_sha256'] or i.get('size_annotation_differences')!=oldinv['summary']['size_annotation_differences']:errors.append('C-Right4 historical ELF identity changed')
    rows=c.get('functions',[]);oldby={x['name']:x for x in oldproof['comparison']['functions']};newby={x['name']:x for x in rows}
    expected={(x['name'],x['size'],x['rom_offset'],x.get('vma',x['rom_offset']+0x80000000-0xC00)) for x in claims}
    try:actual={(x['name'],x['size'],int(x['rom_offset'],16),int(x['guest_address'],16)) for x in rows}
    except (KeyError,ValueError,TypeError):actual=set()
    if len(rows)!=count or actual!=expected or any(x.get('matched') is not True or x.get('expected_sha256')!=x.get('candidate_sha256') for x in rows):errors.append('C-Right4 full original function list mismatch')
    targets=stage.rows('usa');names={f['name'] for f in targets}
    if set(newby)-set(oldby)!=names or any(newby.get(name)!=row for name,row in oldby.items()):errors.append('C-Right4 earlier function proof changed')
    oldsources=oldproof['sources_sha256_lf'];sources=proof.get('sources_sha256_lf',{})
    if any(sources.get(k)!=v for k,v in oldsources.items()) or set(sources)-set(oldsources)!={stage.source_path(f) for f in targets}:errors.append('C-Right4 earlier source proof changed')
    for f in targets:
        if newby.get(f['name'],{}).get('expected_sha256')!=f['code_sha256'] or sources.get(stage.source_path(f))!=f['source_sha256'] or f['name'] in proof.get('retained_assembly_functions',[]):errors.append('C-Right4 original source/ownership mismatch '+f['name'])
    checks={'status':'PASSED_G2_LOCAL','base_c':2319,'accepted_c_after':2323,'added_c':4,'added_original_bytes':728,'accepted_original_bytes_after':111736,'remaining_assembly':5040,'full_rom_match':True,'original_32MiB_ROM_bytes_exact':33554432,'original_rom_sha1':ORIGINAL_SHA1,'retail_rom_exact':True,'original_16MiB_ROM_bytes_exact':16777216,'retail_rom_sha1':stage.RETAIL_SHA,'positive_elf_function_identities_exact':7376,'semantic_relocations_exact':82102,'semantic_relocation_sha256':stage.vmdual.NEW_RELOC,'stable_global_symbols_exact':26714,'predecessor_elf_sha256':stage.vmdual.NEW_ELF,'candidate_elf_sha256':stage.NEW_ELF,'source_manifest_sha256':stage.MANIFEST_SHA,'ownership_exact':True,'new_c_names':sorted(names),'compiler_quirk_outcome':'EXISTING_QUIRK_REPRODUCED'}
    if any(p.get(k)!=v for k,v in checks.items()):errors.append('C-Right4 ROM/ELF/source/ownership transaction mismatch')
    fixes=p.get('guarded_metadata_corrections',[])
    if len(fixes)!=3 or [x.get('symbol') for x in fixes]!=['D_3B03C','D_080019A0_71D420','D_08001710_71D190'] or any(x.get('code_and_relocations_unchanged') is not True for x in fixes[:2]) or fixes[2].get('metadata_byte_offset')!=95641596 or fixes[2].get('pre_sha256')!='63365de21a9f64cbb80439594c5d15d9e9f62840cd1e1021f935e5bd301e16a5' or fixes[2].get('post_sha256')!=stage.NEW_ELF or fixes[0].get('st_info_bytes_changed')!=1 or fixes[0].get('undefined_size')!=0:errors.append('C-Right4 guarded metadata provenance mismatch')
    try:
        dated=json.loads((root/'results/usa_cright4_2323_g2_20261124.json').read_text())
        if dated!=p:errors.append('C-Right4 dated G2 proof mismatch')
    except (FileNotFoundError,ValueError):errors.append('C-Right4 missing dated G2 proof')
    return {'status':'FAIL' if errors else 'PASS','accepted_C':count,'accepted_original_bytes':size,'remaining_assembly':7376-count-13,'errors':errors,'notice':'Stored proof only; fresh G2 and full CI separately required.'}


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
