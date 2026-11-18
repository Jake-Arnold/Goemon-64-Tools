"""ROM-free decomp access to the single project-wide guest-data registry."""
import json
from pathlib import Path
import tempfile
import unittest

from decomp.memory_registry import (
    load_canonical_registry, validate_bidirectional_flags,
)


class CanonicalMemoryRegistryTests(unittest.TestCase):
    def setUp(self):
        self.usa = {
            "id": "story:usa:sample", "region": "usa",
            "category": "saved_event_bit", "address": "0x8015C621",
            "counterpart": "0x80161E11", "mask": "0x4",
            "confidence": "research_observed",
            "id_aliases": ["crosswalk:usa:event:sample"],
        }
        self.japan = {
            "id": "crosswalk:japan:event:sample", "region": "japan",
            "category": "saved_event_bit", "address": "0x80161E11",
            "counterpart": "0x8015C621", "mask": "0x4",
            "confidence": "candidate", "id_aliases": [],
        }

    def _load(self, entries):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp, "catalogue.json")
            path.write_text(json.dumps({
                "format": "goemon-address-catalogue-v1",
                "entries": entries}), encoding="utf-8")
            return load_canonical_registry(path)

    def test_reads_one_authority_with_two_regioned_names(self):
        view = self._load([self.usa, self.japan])
        self.assertEqual(view.flag_counts(), {"usa": 1, "japan": 1})
        self.assertIs(view.lookup("crosswalk:usa:event:sample"),
                      view.lookup("story:usa:sample"))
        self.assertEqual(
            view.lookup("crosswalk:japan:event:sample")["confidence"],
            "candidate")

    def test_rejects_absent_or_mismatched_counterpart(self):
        for bad in ([self.usa], [
                self.usa, dict(self.japan, mask="0x8")]):
            with self.subTest(bad=bad), self.assertRaisesRegex(
                    ValueError, "missing reciprocal"):
                self._load(bad)

    def test_explicit_unknown_is_not_assigned_fake_address(self):
        unknown = dict(self.usa, counterpart=None,
                       crosswalk_status="unresolved")
        view = self._load([unknown])
        self.assertIsNone(view.lookup(unknown["id"])["counterpart"])

    def test_nondata_code_identity_does_not_get_offset(self):
        code = {"id": "decomp:source_vma", "region": "usa",
                "category": "code_vma", "address": "0x80030000",
                "counterpart": None}
        view = self._load([self.usa, self.japan, code])
        self.assertIsNone(view.lookup("decomp:source_vma")["counterpart"])

    def test_duplicate_alias_fails_closed(self):
        duplicate = dict(self.japan, id_aliases=["story:usa:sample"])
        with self.assertRaisesRegex(ValueError, "Duplicate canonical"):
            self._load([self.usa, duplicate])

    def test_contract_rejects_unpaired_in_both_directions(self):
        self.assertIsNone(validate_bidirectional_flags(
            [self.usa, self.japan]))
        with self.assertRaises(ValueError):
            validate_bidirectional_flags([self.japan])


if __name__ == "__main__":
    unittest.main()
