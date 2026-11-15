"""ROM-free tests for the fail-closed full-central-promotion gate."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from decomp import promote_file11 as p


def canonical():
    return {"format":"goemon-matching-decomp-v1",
            "units":[{"functions":[{"name": f"f{i}"} for i in range(156)]}],
            "existing_source_patches":[{"source":"patched.c"}],
            "overlay_file43_stage":{"function":{"name":"file43"}},
            "overlay_file12_stages":[{"function":{"name":"file12a"}},
                                     {"function":{"name":"file12b"}}]}


def fake_g2():
    new=p.expected_file11_names()
    names=[f"existing_{i}" for i in range(160)]+sorted(new)
    sig={name:(rom,size,h) for name,rom,size,h in p.overlay_file11.FUNCTIONS}
    noh=p.sha256(p.usa_file11_noop_groups.ORIGINAL_NOOP)
    sig.update({name:(rom,12,noh) for name,rom in p.usa_file11_noop_groups.entries()})
    rows=[]
    for name in names:
        row={"name":name,"matched":True,"size":8}
        if name in sig:
            rom,size,signature=sig[name]
            row.update(size=size,rom_offset=f"0x{rom:X}",
                       guest_address=f"0x{p.overlay_file11.VMA_START+rom-p.overlay_file11.ROM_START:08X}",
                       expected_sha256=signature,candidate_sha256=signature)
        rows.append(row)
    return {"format":"goemon-matching-build-result-v1","status":"matched","stage":"complete",
            "comparison":{"full_rom_match":True,"expected_sha1":p.ORIGINAL_SHA1,
                          "candidate_sha1":p.ORIGINAL_SHA1,"rom_size":p.ORIGINAL_ROM_BYTES,
                          "matched_functions":210,"claimed_functions":210,
                          "matched_function_bytes":13336,"functions":rows},
            "overlay_file11_stage":{"stage":p.STAGE["format"],
                "total_overlay_c_functions":50,"total_overlay_c_bytes":1064,
                "ordered_linker_objects":12,"rom_bytes":33554432,
                "rom_sha1":p.ORIGINAL_SHA1,"relocations":8825,
                "relocations_same_order":True}}


def fake_inventory():
    return {"format":"goemon-function-inventory-v1","decompressed_sha1":p.ORIGINAL_SHA1,
        "summary":{"identified_function_entries":7376,"upstream_unmarked_entries":13,
                   "newly_matching_c":210,"current_unmarked_entries":223,
                   "remaining_assembly_entries":7153}}


class PromotionTests(unittest.TestCase):
    def test_candidate_preserves_canonical(self):
        original=canonical();copy_orig=copy.deepcopy(original)
        actual=p.candidate_manifest(original)
        self.assertEqual(original,copy_orig)
        self.assertEqual(actual["overlay_file11_stage"],p.STAGE)

    def test_already_staged_manifest_rejected(self):
        m=canonical();m['overlay_file11_stage']=p.STAGE
        with self.assertRaises(ValueError):p.candidate_manifest(m)

    def test_wrong_base_count_rejected(self):
        m=canonical();m['units'][0]['functions'].pop()
        with self.assertRaises(ValueError):p.candidate_manifest(m)

    def test_real_13_plus_37_unique(self):
        self.assertEqual(len(p.expected_file11_names()),50)

    def test_valid_full_central_proof(self):
        self.assertEqual(p.verify_g2_report(fake_g2(),p.expected_file11_names())["g2_bytes"],13336)

    def test_partial_prior_research_proof_is_not_enough(self):
        g=fake_g2();g['comparison']['claimed_functions']=50
        with self.assertRaises(ValueError):p.verify_g2_report(g,p.expected_file11_names())

    def test_all_50_must_be_present(self):
        g=fake_g2();g['comparison']['functions'][-1]['name']='duplicate_of_prior'
        with self.assertRaises(ValueError):p.verify_g2_report(g,p.expected_file11_names())

    def test_wrong_original_function_hash_rejected(self):
        g=fake_g2()
        g['comparison']['functions'][-1]['candidate_sha256']='0'*64
        with self.assertRaises(ValueError):p.verify_g2_report(g,p.expected_file11_names())

    def test_wrong_original_function_vma_rejected(self):
        g=fake_g2()
        g['comparison']['functions'][-1]['guest_address']='0x00000000'
        with self.assertRaises(ValueError):p.verify_g2_report(g,p.expected_file11_names())

    def test_wrong_rom_rejected(self):
        g=fake_g2();g['comparison']['full_rom_match']=False
        with self.assertRaises(ValueError):p.verify_g2_report(g,p.expected_file11_names())

    def test_wrong_relwc_rejected(self):
        g=fake_g2();g['overlay_file11_stage']['relocations']=8824
        with self.assertRaises(ValueError):p.verify_g2_report(g,p.expected_file11_names())

    def test_wrong_relocation_order_rejected(self):
        g=fake_g2();g['overlay_file11_stage']['relocations_same_order']=False
        with self.assertRaises(ValueError):p.verify_g2_report(g,p.expected_file11_names())

    def test_verified_inventory(self):
        self.assertEqual(p.verify_inventory_report(fake_inventory())['remaining_assembly_entries'],7153)

    def test_bad_inventory_cannot_promote(self):
        i=fake_inventory();i['summary']['newly_matching_c']=209
        with self.assertRaises(ValueError):p.verify_inventory_report(i)

    def test_missing_input_does_not_write_canonical_manifest(self):
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as outputs:
            d=Path(tmp)
            out=Path(outputs)
            src=d/'decomp';src.mkdir()
            (src/'manifest.json').write_text(json.dumps(canonical()))
            a=mock.Mock(source_dir=src,upstream=d/'upstream',retail_rom=d/'rom',
                workdir=out/'g2',output_dir=out/'out',uv='uv',jobs=2,
                baseline_cache=None,binutils_root=None)
            def fail(*args,**kwargs):
                raise RuntimeError('synthetic interrupt')
            with mock.patch.object(p,'invoke',side_effect=fail):
                with self.assertRaises(RuntimeError):p.promote(a)
            self.assertEqual(json.loads((src/'manifest.json').read_text()),canonical())
            self.assertFalse((out/'out'/'PROMOTION_REVIEW.json').exists())

    def test_exclusive_outputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'safe.json'
            p.write_exclusive(path,b'first')
            with self.assertRaises(FileExistsError):p.write_exclusive(path,b'second')
            self.assertEqual(path.read_bytes(),b'first')

if __name__=='__main__':unittest.main()