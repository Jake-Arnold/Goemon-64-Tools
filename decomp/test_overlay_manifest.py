"""Synthetic schema checks for explicit overlay and provenance mappings."""
from copy import deepcopy
import unittest

try:
    from .overlay_manifest import validate_overlay_manifest
except ImportError:
    from overlay_manifest import validate_overlay_manifest


def sample_manifest():
    digest = "a" * 64
    return {
        "format": "goemon-overlay-manifest-v1",
        "reference_rom_sha1": "b" * 40,
        "overlays": [{
            "id": "file_43",
            "exclusive_ram_id": "tlb_overlay",
            "rom_start": 0x1000,
            "rom_end": 0x1100,
            "vma_start": 0x08000000,
            "vma_end": 0x08000100,
            "alignment": 16,
            "sections": [
                {"name": "text", "rom_start": 0x1000, "rom_end": 0x1080,
                 "vma_start": 0x08000000, "vma_end": 0x08000080,
                 "alignment": 16, "sha256": digest},
                {"name": "rodata", "rom_start": 0x1080, "rom_end": 0x1100,
                 "vma_start": 0x08000080, "vma_end": 0x08000100,
                 "alignment": 16, "sha256": digest},
            ],
            "functions": [{
                "name": "func_08000010_1000",
                "section": "text",
                "rom_offset": 0x1000,
                "vma": 0x08000010,
                "size": 8,
                "source_owner": "decomp/candidates/key_spawn_gate.c",
                "source_sha256": digest,
                "object_sha256": digest,
                "relocation_sha256": digest,
                "original_sha256": digest,
            }],
        }],
    }


class OverlayManifestTests(unittest.TestCase):
    def test_accepts_independent_rom_and_vma_mappings(self):
        result = validate_overlay_manifest(sample_manifest())
        self.assertEqual(result["overlay_count"], 1)
        self.assertEqual(result["function_count"], 1)
        self.assertIn("explicit layout", result["proof_level"])

    def test_rejects_main_segment_formula_vma(self):
        manifest = sample_manifest()
        manifest["overlays"][0]["functions"][0]["name"] = "func_80000400_1000"
        manifest["overlays"][0]["functions"][0]["vma"] = 0x80000400
        with self.assertRaisesRegex(ValueError, "name disagrees|outside its section"):
            validate_overlay_manifest(manifest)

    def test_rejects_unknown_formula_fields(self):
        manifest = sample_manifest()
        manifest["overlays"][0]["rom_to_vma_offset"] = 0x7FFFF400
        with self.assertRaisesRegex(ValueError, "overlay fields"):
            validate_overlay_manifest(manifest)

    def test_rejects_duplicate_overlay_ids_and_overlapping_rom_segments(self):
        manifest = sample_manifest()
        manifest["overlays"].append(deepcopy(manifest["overlays"][0]))
        with self.assertRaisesRegex(ValueError, "duplicate overlay ID"):
            validate_overlay_manifest(manifest)

        second = deepcopy(sample_manifest()["overlays"][0])
        second["id"] = "file_44"
        second["rom_start"] = 0x1080
        second["rom_end"] = 0x1180
        second["vma_start"] = 0x08100000
        second["vma_end"] = 0x08100100
        second["sections"] = [
            {"name": "text", "rom_start": 0x1080, "rom_end": 0x1100,
             "vma_start": 0x08100000, "vma_end": 0x08100080,
             "alignment": 16, "sha256": "a" * 64},
            {"name": "rodata", "rom_start": 0x1100, "rom_end": 0x1180,
             "vma_start": 0x08100080, "vma_end": 0x08100100,
             "alignment": 16, "sha256": "a" * 64},
        ]
        second["functions"] = []
        manifest = sample_manifest()
        manifest["overlays"].append(second)
        with self.assertRaisesRegex(ValueError, "overlay ROM segments overlap"):
            validate_overlay_manifest(manifest)

        second["rom_start"] = 0x1200
        second["rom_end"] = 0x1300
        second["vma_start"] = 0x08000080
        second["vma_end"] = 0x08000180
        second["sections"] = [
            {"name": "text", "rom_start": 0x1200, "rom_end": 0x1280,
             "vma_start": 0x08000080, "vma_end": 0x08000100,
             "alignment": 16, "sha256": "a" * 64},
            {"name": "rodata", "rom_start": 0x1280, "rom_end": 0x1300,
             "vma_start": 0x08000100, "vma_end": 0x08000180,
             "alignment": 16, "sha256": "a" * 64},
        ]
        manifest = sample_manifest()
        manifest["overlays"].append(second)
        with self.assertRaisesRegex(ValueError, "overlay VMA segments overlap"):
            validate_overlay_manifest(manifest)

    def test_rejects_negative_or_mismatched_ranges(self):
        manifest = sample_manifest()
        manifest["overlays"][0]["rom_start"] = -4
        with self.assertRaisesRegex(ValueError, "overlay ROM range"):
            validate_overlay_manifest(manifest)
        manifest = sample_manifest()
        manifest["overlays"][0]["sections"][0]["rom_start"] += 4
        with self.assertRaisesRegex(ValueError, "section ROM and VMA extents differ"):
            validate_overlay_manifest(manifest)

        manifest = sample_manifest()
        manifest["overlays"][0]["sections"][1]["vma_start"] = 0x08000070
        manifest["overlays"][0]["sections"][1]["vma_end"] = 0x080000F0
        with self.assertRaisesRegex(ValueError, "sections overlap in VMA"):
            validate_overlay_manifest(manifest)

    def test_rejects_section_and_function_overlap(self):
        manifest = sample_manifest()
        manifest["overlays"][0]["sections"][1]["rom_start"] = 0x1070
        manifest["overlays"][0]["sections"][1]["vma_start"] = 0x08000070
        with self.assertRaisesRegex(ValueError, "sections overlap"):
            validate_overlay_manifest(manifest)

        manifest = sample_manifest()
        second = deepcopy(manifest["overlays"][0]["functions"][0])
        second["name"] = "func_08000040_1004"
        second["rom_offset"] = 0x1004
        second["vma"] = 0x08000040
        second["size"] = 4
        manifest["overlays"][0]["functions"].append(second)
        with self.assertRaisesRegex(ValueError, "functions overlap in ROM"):
            validate_overlay_manifest(manifest)

        manifest = sample_manifest()
        second = deepcopy(manifest["overlays"][0]["functions"][0])
        second["name"] = "func_08000014_100C"
        second["rom_offset"] = 0x100C
        second["vma"] = 0x08000014
        second["size"] = 4
        manifest["overlays"][0]["functions"].append(second)
        with self.assertRaisesRegex(ValueError, "functions overlap in VMA"):
            validate_overlay_manifest(manifest)

    def test_bss_is_vma_only_and_functions_must_belong_to_text(self):
        manifest = sample_manifest()
        manifest["overlays"][0]["vma_end"] = 0x08000120
        manifest["overlays"][0]["sections"].append({
            "name": "bss", "vma_start": 0x08000100, "vma_end": 0x08000120,
            "alignment": 16,
        })
        self.assertEqual(validate_overlay_manifest(manifest)["function_count"], 1)

        manifest["overlays"][0]["functions"][0]["section"] = "rodata"
        with self.assertRaisesRegex(ValueError, "unknown section"):
            validate_overlay_manifest(manifest)

    def test_rejects_missing_hash_and_unsafe_source_owner(self):
        manifest = sample_manifest()
        del manifest["overlays"][0]["functions"][0]["relocation_sha256"]
        with self.assertRaisesRegex(ValueError, "function fields"):
            validate_overlay_manifest(manifest)
        manifest = sample_manifest()
        manifest["overlays"][0]["functions"][0]["source_owner"] = "../private.c"
        with self.assertRaisesRegex(ValueError, "source owner"):
            validate_overlay_manifest(manifest)


if __name__ == "__main__":
    unittest.main()
