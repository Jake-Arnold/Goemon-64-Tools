"""Fail-closed camera reset integration tests: 179 canonical C -> 180 candidate C."""
from __future__ import annotations
import copy
import hashlib
import json
import os
from pathlib import Path
import tempfile
import unittest

from decomp import file11_179_stage, file11_180_stage

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "decomp/manifest.json"

class File11Camera180Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.prior = file11_179_stage.load_fixture()
        cls.candidate = file11_180_stage.load_fixture()
        cls.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        cls.manifest["overlay_file11_stage"] = {"format": file11_180_stage.STAGE_FORMAT}

    def test_contiguous_one_function_insert_and_no_prior_duplication(self):
        old = self.prior["chunks"]
        new = self.candidate["chunks"]
        self.assertEqual((len(old),len(new)), (126,128))
        self.assertEqual((sum(c["kind"]=="c" for c in new),sum(c["kind"]=="asm" for c in new)),(77,51))
        self.assertEqual((new[0]["rom_start"],new[-1]["rom_end"]), (0x587370,0x5B8500))
        for a,b in zip(new,new[1:]):
            self.assertEqual(a["rom_end"], b["rom_start"])
        accepted = {(f["name"],f["rom_offset"],f["size"]) for f in file11_179_stage.entries()}
        proposed = {(f["name"],f["rom_offset"],f["size"]) for f in file11_180_stage.entries()}
        self.assertEqual(proposed-accepted,{("func_801F97D4_5B56E4",0x5B56E4,136)})
        self.assertTrue(accepted.issubset(proposed))
        original_unaffected = [c for c in old if c["rom_start"]!=0x5B4E1C]
        proposed_unaffected = [c for c in new if not 0x5B4E1C<=c["rom_start"]<0x5B64B8]
        self.assertEqual(original_unaffected,proposed_unaffected)

    def test_exact_source_and_object_pins(self):
        self.assertEqual(hashlib.sha256(file11_180_stage.C_PATH.read_bytes()).hexdigest(),
                         file11_180_stage.C_SHA256)
        new = [c for c in self.candidate["chunks"] if 0x5B4E1C<=c["rom_start"]<0x5B64B8]
        self.assertEqual([(c["rom_start"],c["rom_end"],c["kind"]) for c in new],
                         [(0x5B4E1C,0x5B56E4,"asm"),(0x5B56E4,0x5B576C,"c"),
                          (0x5B576C,0x5B64B8,"asm")])
        self.assertEqual(sum(c["size"] for c in new), 5788)
        self.assertEqual(new[1]["source_sha256"],file11_180_stage.C_SHA256)
        self.assertEqual((new[0]["trimmed_obj_sha256"],new[2]["trimmed_obj_sha256"]),
                         ("5d5796c691bd98450bbc4f256c03b5e9b787af6e60d58e816ecc7f0d444ae66c","64f5b4cfc95ac0be408ab21423132e26873077a8dda3834a4053b89ead185444"))
        self.assertEqual(new[1]["original_sha256"],
                         "f6266809ac26ff75f44d5f23cab8c15ae338e6185b88b69ec85bd83dfb7c0b8a")

    def test_reviewed_plan_is_opt_in_and_no_mutation_of_179(self):
        original = copy.deepcopy(self.manifest)
        plan = file11_180_stage.reviewed_plan(self.manifest)
        self.assertEqual((plan["file11_c_total"],plan["file11_c_instruction_bytes"]),(180,5320))
        self.assertEqual((plan["chunks"],plan["c_units"],plan["asm_slices"]),(128,77,51))
        self.assertEqual(self.manifest,original)
        invalid = copy.deepcopy(self.manifest)
        invalid["overlay_file11_stage"]={"format":file11_179_stage.STAGE_FORMAT}
        with self.assertRaises(ValueError):
            file11_180_stage.reviewed_plan(invalid)
        invalid["overlay_file11_stage"]={"format":file11_180_stage.STAGE_FORMAT,"unsafe":True}
        with self.assertRaises(ValueError):
            file11_180_stage.reviewed_plan(invalid)

    def test_splat_and_source_preflight(self):
        plan=file11_180_stage.reviewed_plan(self.manifest)
        original = ("  - name: file_11\n"
                    "    - [0x587370, asm]\n"
                    "    - [0x5B8500, data]\n"
                    "  - name: file_12\n")
        # stage_config requires the actual original Splat segment config;
        # check this using the authenticated original checkout in the ROM gate.
        self.assertEqual(len(plan["ordered_segments"]),128)
        with tempfile.TemporaryDirectory() as tmp:
            paths = file11_180_stage.source_payloads(Path(tmp),plan)
            self.assertEqual(len(paths),77)
            self.assertTrue(any(p.name=="camera_reset_usa_5b56e4.c" for p,_ in paths))

    def test_optional_authentic_usa_rom_slices(self):
        src=os.environ.get("GOEMON_USA_DECOMPRESSED_ROM")
        if not src:
            self.skipTest("Authenticate complete USA ROM by setting GOEMON_USA_DECOMPRESSED_ROM")
        image=Path(src).read_bytes()
        plan=file11_180_stage.reviewed_plan(self.manifest,image)
        self.assertEqual(plan["file11_c_total"],180)

if __name__ == "__main__":
    unittest.main()
