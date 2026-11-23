"""ROM-free source and original-checkpoint fail-closed validation."""
import hashlib, json, unittest
from pathlib import Path
from decomp import overlay_checkpoint500 as native
from decomp.verify import claimed_functions,load_manifest

# This suite proves its historical promotion checkpoint, not subsequent stages.
_historical_load_manifest = load_manifest

def load_manifest(*args, **kwargs):
    manifest = _historical_load_manifest(*args, **kwargs)
    # The 2090-C Mini stages postdate this fixed historical test checkpoint.
    manifest.pop('overlay_mini10_stage', None)
    manifest.pop('overlay_mini_selector_stage', None)
    manifest.pop('overlay_native49_stage', None)
    manifest.pop('overlay_native51_stage', None)
    # The 233-C batch is newer than this frozen historical checkpoint.
    manifest.pop('overlay_isolated233_stage', None)
    manifest.pop('overlay_reconcile108_stage', None)  # Preserve this historical acceptance checkpoint
    manifest.pop('overlay_crossregion7_stage', None)  # Historical stage projection
    return manifest


class Checkpoint500(unittest.TestCase):
    def test_fixture_and_source_hash(self):
        f=native.load_fixture()
        self.assertEqual(len(native.functions(f)),1)
        self.assertEqual(native.functions(f)[0]['rom_offset'],0x34910)
        self.assertEqual(native.functions(f)[0]['size'],48)
        source=(native.SOURCE_BASE/'checkpoint500_000.c').read_bytes()
        self.assertEqual(hashlib.sha256(source).hexdigest(),f['units'][0]['source_sha256'])
        self.assertEqual(source, (native.ROOT/'research/archived_116_20261119/checkpoint500/func_80033D10_34910.c').read_bytes())

    def test_claim_is_unique_and_after_1617(self):
        m=load_manifest(Path(__file__).resolve().parent/'manifest.json')
        m.pop('overlay_rediscovery5_stage',None)
        previous=claimed_functions({k:v for k,v in m.items() if k not in ('overlay_checkpoint500_stage','overlay_rediscovery5_stage')})
        self.assertEqual(len(previous),1617)
        accepted=claimed_functions(m)
        self.assertEqual(len(accepted),1618)
        self.assertNotIn(0x34910,{f['rom_offset'] for f in previous})
        self.assertEqual([f['name'] for f in accepted if f['rom_offset']==0x34910],['func_80033D10_34910'])
