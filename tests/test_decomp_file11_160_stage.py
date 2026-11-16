"""ROM-free structural acceptance tests for the opt-in 323-C USA trial.

These tests do not certify a native combined ROM. Full G2 + original inventory
and the complete local CI remain mandatory for production promotion.
"""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

from decomp import file11_152_stage as old
from decomp import file11_160_stage as new
from decomp import review_file11_143 as review
from decomp import verify

ROOT = Path(__file__).resolve().parents[1] / "decomp"


class File11160StageTests(unittest.TestCase):
    def setUp(self):
        self.canonical = json.loads((ROOT / "manifest.json").read_text())
        self.trial = copy.deepcopy(self.canonical)
        self.trial["overlay_file11_stage"] = {"format": new.STAGE_FORMAT}

    def test_canonical_unmodified_and_trial_count(self):
        self.assertEqual(verify.file11_stage_mode(self.canonical), 152)
        self.assertEqual(len(verify.claimed_functions(self.canonical)), 315)
        self.assertEqual(verify.file11_stage_mode(self.trial), 160)
        claims = verify.claimed_functions(self.trial)
        self.assertEqual((len(claims), len({f["name"] for f in claims})), (323, 323))
        self.assertEqual(sum(f["size"] for f in claims), 17_012)
        self.assertEqual((len(new.entries()), sum(f["size"] for f in new.entries())), (160, 4628))
        self.assertEqual(json.loads((ROOT / "manifest.json").read_text()), self.canonical)

    def test_exact_three_way_split_and_existing_88_chunks(self):
        old_chunks = old.load_fixture()["chunks"]
        chunks = new.load_fixture()["chunks"]
        self.assertEqual((len(old_chunks), len(chunks)), (88, 90))
        self.assertEqual(chunks[:59], old_chunks[:59])
        self.assertEqual(chunks[62:], old_chunks[60:])
        self.assertEqual([(c["rom_start"], c["rom_end"], c["kind"]) for c in chunks[59:62]], [
            (0x5A63F8, 0x5A6F30, "asm"),
            (0x5A6F30, 0x5A7090, "c"),
            (0x5A7090, 0x5A74CC, "asm"),
        ])
        self.assertEqual((len([x for x in chunks if x["kind"] == "c"]),
                          len([x for x in chunks if x["kind"] == "asm"])), (50, 40))
        self.assertEqual(sum(x["size"] for x in chunks if x["kind"] == "c"), 4628)
        self.assertEqual(sum(x["size"] for x in chunks if x["kind"] == "asm"),
                         0x5B8500 - 0x587370 - 4628)
        expected_off = 0x587370
        for c in chunks:
            self.assertEqual(c["rom_start"], expected_off)
            expected_off = c["rom_end"]
        self.assertEqual(expected_off, 0x5B8500)
        self.assertEqual(new.reviewed_plan(self.trial)["ordered_segments"][59:62], [
            (0x5A63F8, "asm", None), (0x5A6F30, "c", "file11_eight_callbacks"),
            (0x5A7090, "asm", None)])
        plan = new.reviewed_plan(self.trial)
        self.assertEqual((plan["chunks"], plan["c_units"], plan["asm_slices"]), (90, 50, 40))
        self.assertEqual((plan["file11_c_total"], plan["file11_c_instruction_bytes"]), (160, 4628))

    def test_new_original_symbols_and_source_fingerprint(self):
        c = new.load_fixture()["chunks"][60]
        self.assertEqual(hashlib.sha256(c["source"].encode("utf-8")).hexdigest(),
                         "7919d61ac0453f342629d51186b1ddf16f3716f527b411c93716815941122d60")
        self.assertEqual(c["original_sha256"],
                         "b1fbaa8f74fec1f63e9f3cf2d0647daf26fd008a135cba0f767e5958113dcff1")
        expected = [
            ("func_%08X_%X" % (0x801EB020 + 44*i, 0x5A6F30 + 44*i))
            for i in range(8)
        ]
        self.assertEqual([x["name"] for x in c["functions"]], expected)
        self.assertEqual([x["size"] for x in c["functions"]], [44]*8)
        self.assertEqual([x["vma"] for x in c["functions"]],
                         [0x801EB020 + 44*i for i in range(8)])
        objects = new.source_objects()
        self.assertEqual(len(objects), 90)
        self.assertEqual(sum(x[1] for x in objects), 0x5B8500 - 0x587370)
        self.assertEqual(objects[60][0].as_posix(),
                         "build/usa/src/file11_eight_callbacks.c.o")

    def test_invalid_ownership_or_payload_rejected(self):
        with self.assertRaises(ValueError):
            new.reviewed_plan(self.canonical)
        fixture = new.load_fixture()
        mutated = copy.deepcopy(fixture)
        mutated["chunks"][60]["size"] -= 4
        with mock.patch.object(new, "load_fixture", return_value=mutated):
            with self.assertRaises(ValueError):
                new.reviewed_plan(self.trial)
        mutated = copy.deepcopy(fixture)
        mutated["chunks"][60]["source"] += "\nint injected_function(void) { return 1; }\n"
        with mock.patch.object(new, "load_fixture", return_value=mutated):
            with self.assertRaises(ValueError):
                new.reviewed_plan(self.trial)
        mutated = copy.deepcopy(fixture)
        mutated["chunks"][58]["rom_start"] += 4
        with mock.patch.object(new, "load_fixture", return_value=mutated):
            with self.assertRaises(ValueError):
                new.reviewed_plan(self.trial)

    def test_source_payloads_collision_and_counts(self):
        plan = new.reviewed_plan(self.trial)
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            outputs = new.source_payloads(root, plan)
            self.assertEqual(len(outputs), 50)
            self.assertEqual(len({str(p) for p, _ in outputs}), 50)
            path = root / "src" / "file11_eight_callbacks.c"
            path.parent.mkdir()
            path.write_text("already here")
            with self.assertRaises(FileExistsError):
                new.source_payloads(root, plan)

    def test_review_acceptance_refuses_scratch_without_central_gates(self):
        trial, claims = review.candidate_manifest(self.trial)
        self.assertEqual(len(claims), 323)
        self.assertEqual(trial["overlay_file11_stage"], {"format":new.STAGE_FORMAT})
        with self.assertRaises(ValueError):
            review.verify_g2_report({
                "format":"goemon-matching-build-result-v1",
                "status":"NATIVE_SCRATCH_VERIFIED_NOT_CENTRAL",
                "stage":"complete", "comparison":{"full_rom_match":True}
            }, claims)
        with self.assertRaises(ValueError):
            review.verify_inventory_report({
                "format":"goemon-function-inventory-v1",
                "decompressed_sha1":"6ea0ed71032ce08fc2745f412d84936382197494",
                "summary":{"newly_matching_c":323}
            }, 323)


if __name__ == "__main__":
    unittest.main()
