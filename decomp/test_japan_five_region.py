"""Region verification supports historic four-C and current five-C stages."""
from __future__ import annotations
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from decomp import region_verify as rv
from decomp import japan_five_c as jp


class JapanStageSelectionTests(unittest.TestCase):
    def test_manifests_keep_historical_and_current_claims_separate(self):
        old=rv.load_manifest(rv.ROOT / 'regions/japan_0_four_c.json')
        middle=rv.load_manifest(rv.ROOT / 'regions/japan_0_five_c.json')
        new=rv.load_manifest()
        self.assertEqual(tuple(len(x['units']) for x in (old,middle,new)),(2,3,4))
        self.assertEqual(tuple(sum(len(u['functions']) for u in x['units']) for x in (old,middle,new)),(4,5,6))

    def test_reject_stage_crossed_sources(self):
        item=rv.load_manifest()
        item['splat_candidate']='config/japan_0/splat_four_c.local.yaml'
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'manifest.json'
            path.write_text(json.dumps(item))
            with self.assertRaisesRegex(ValueError,'source units'):
                rv.load_manifest(path)

    def test_five_c_stage_uses_distinct_config_and_preserves_four_c(self):
        base='    - [0x122F0, asm, main_122F0]\n    - [0x16DF0, c, jp_bit_array]\n    - [0x38620, c, jp_main_38620]\n'
        # Require no mutation of the input four-C text.
        before=base
        rendered=jp.render_config(base)
        self.assertIn('[0x12D60, c, jp_motion_12D60]', rendered)
        self.assertNotIn('[0x12D60, c, jp_motion_12D60]', base)
        self.assertEqual(before,base)


if __name__=='__main__':unittest.main()
