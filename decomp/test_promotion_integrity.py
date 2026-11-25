"""Regression tests for the 2026-11-22 unintegrated-source false promotion."""
from __future__ import annotations
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from decomp import promotion_integrity as integrity
from decomp import usa_canonical_reconcile108 as reconcile
from decomp.verify import load_manifest,claimed_functions


class CanonicalPromotionIntegrityTests(unittest.TestCase):
    def test_exact_final_c_claims_and_frozen_original_addresses(self):
        manifest=load_manifest(integrity.ROOT/'manifest.json')
        claims=claimed_functions(manifest)
        self.assertEqual(len(claims),2556)
        self.assertEqual(sum(f['size'] for f in claims),144092)
        self.assertEqual(len({f['name'] for f in claims}),2556)
        self.assertEqual(len(reconcile.fixture()['functions']),108)
        self.assertEqual(reconcile.fixture()['source_ownership_exception'][0]['name'],
                         'func_800108BC_114BC')

    def _temporary(self, *, manifest=None, proof=None, inventory=None):
        folder=tempfile.TemporaryDirectory()
        root=Path(folder.name)
        (root/'results').mkdir()
        canonical=integrity.ROOT
        for path,override in [('manifest.json',manifest),('results/combined.json',proof),
                              ('results/inventory.json',inventory),
                              ('results/usa_canonical_reconcile108_2072_g2_20261122.json',None),
                              ('results/usa_crossregion7_2079_g2_20261122.json',None),
                              ('results/usa_mini11_2090_g2_20261123.json',None),
                              ('results/combined_2090_pre_opening_new2_20261123.json',None),
                              ('results/inventory_2090_pre_opening_new2_20261123.json',None),
                              ('results/usa_file18_new2_2092_g2_20261123.json',None),
                              ('results/combined_2092_before_short72_20261123.json',None),
                              ('results/inventory_2092_before_short72_20261123.json',None),
                              ('results/usa_short72_2164_g2_20261123.json',None),
                              ('results/combined_2164_before_vm436_20261123.json',None),
                              ('results/inventory_2164_before_vm436_20261123.json',None),
                              ('results/usa_script_vm436_2165_g2_20261123.json',None),
                              ('results/manifest_2165_before_native151_20261123.json',None),
                              ('results/combined_2165_before_native151_20261123.json',None),
                              ('results/inventory_2165_before_native151_20261123.json',None),
                              ('results/manifest_2316_before_vm440_20261123.json',None),
                              ('results/combined_2316_before_vm440_20261123.json',None),
                              ('results/inventory_2316_before_vm440_20261123.json',None),
                              ('results/usa_script_vm440_2317_g2_20261123.json',None),
                              ('results/manifest_2317_before_vmdual_20261123.json',None),
                              ('results/combined_2317_before_vmdual_20261123.json',None),
                              ('results/inventory_2317_before_vmdual_20261123.json',None),
                              ('results/usa_script_vm_dual_2319_g2_20261123.json',None),
                              ('results/manifest_2319_before_cright4_20261124.json',None),
                              ('results/combined_2319_before_cright4_20261124.json',None),
                              ('results/inventory_2319_before_cright4_20261124.json',None),
                              ('results/usa_cright4_2323_g2_20261124.json',None)]:
            dst=root/path
            frozen={'manifest.json':'manifest_2323_before_transition_20261124.json','results/combined.json':'combined_2323_before_transition_20261124.json','results/inventory.json':'inventory_2323_before_transition_20261124.json'}
            src=canonical/'results'/frozen[path] if path in frozen else canonical/path
            if not src.is_file():
                raise ValueError('Missing canonical test proof '+str(src))
            dst.write_text(src.read_text() if override is None else json.dumps(override))
        return folder,root

    def test_current_canonical_manifest_matches_stored_g2_and_inventory(self):
        audit=integrity.audit()
        self.assertEqual(audit['status'],'PASS',audit['errors'])
        self.assertEqual((audit['accepted_C'],audit['accepted_original_bytes']),
                         (2556,144092))

    def test_staged_only_manifest_from_previous_commit_fails_closed(self):
        manifest=json.loads((integrity.ROOT/'results/manifest_2323_before_transition_20261124.json').read_text())
        manifest.pop('usa_cright4_promotion')
        manifest.pop('usa_script_vm_dual_reference')
        manifest.pop('usa_script_vm440_promotion')
        manifest.pop('usa_native151_promotion')
        manifest.pop('usa_script_vm436_promotion')  # Project original 2164/earlier historical view.
        manifest.pop('overlay_usa_short72_stage')  # This is a historical post2092 source stage.
        manifest.pop('overlay_usa_opening_new2_stage')  # This is a historical predecessor projection.
        manifest.pop('overlay_mini_selector_stage')
        manifest.pop('overlay_mini10_stage')
        manifest.pop('overlay_crossregion7_stage')
        manifest.pop('overlay_reconcile108_stage')
        folder,root=self._temporary(manifest=manifest)
        with folder:
            bad=integrity.audit(root)
            self.assertEqual(bad['status'],'FAIL')
            self.assertTrue(any('disagree' in e for e in bad['errors']),bad['errors'])

    def test_forged_inventory_count_fails_closed(self):
        inv=json.loads((integrity.ROOT/'results/inventory_2323_before_transition_20261124.json').read_text())
        inv['summary']['newly_matching_c']=1964
        folder,root=self._temporary(inventory=inv)
        with folder:
            bad=integrity.audit(root)
            self.assertEqual(bad['status'],'FAIL')
            self.assertTrue(any('inventory C count' in e for e in bad['errors']),bad['errors'])

    def test_forged_full_rom_or_function_list_fails_closed(self):
        report=json.loads((integrity.ROOT/'results/combined_2323_before_transition_20261124.json').read_text())
        report['comparison']['full_rom_match']=False
        report['comparison']['functions'].pop()
        folder,root=self._temporary(proof=report)
        with folder:
            bad=integrity.audit(root)
            self.assertEqual(bad['status'],'FAIL')
            self.assertGreaterEqual(len(bad['errors']),2)

    def test_mini11_stage_proof_cannot_be_forged(self):
        folder,root=self._temporary()
        with folder:
            stage=root/'results/usa_mini11_2090_g2_20261123.json'
            doc=json.loads(stage.read_text())
            doc['semantic_relocations_exact']=0
            stage.write_text(json.dumps(doc))
            bad=integrity.audit(root)
            self.assertEqual(bad['status'],'FAIL')
            self.assertTrue(any('Mini11' in e for e in bad['errors']),bad['errors'])

    def test_stale_reconciled_stage_proof_fails_closed(self):
        folder,root=self._temporary()
        with folder:
            p=root/'results/usa_canonical_reconcile108_2072_g2_20261122.json'
            record=json.loads(p.read_text())
            record['accepted_after']=1964
            p.write_text(json.dumps(record))
            bad=integrity.audit(root)
            self.assertEqual(bad['status'],'FAIL')
            self.assertTrue(any('stage proof mismatch' in e for e in bad['errors']))


if __name__=='__main__':unittest.main()
