"""ROM-free source identity and no-false-promotion tests for file_11 wave 6."""
import hashlib,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"decomp/research/file11_wave6_four_sources.json"
class Wave6Identity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.d=json.loads(DATA.read_text())
    def test_unique_and_pinned(self):
        a=self.d["functions"]
        self.assertEqual(len(a),4)
        self.assertEqual(sum(r["size"] for r in a),152)
        self.assertEqual(len({r["off"] for r in a}),4)
        for r in a:
            self.assertEqual(r["vma"],0x801CB460+r["off"]-0x587370)
            self.assertEqual(hashlib.sha256(r["source"].encode()).hexdigest(),r["source_sha256"])
    def test_claims_research_only(self):
        self.assertEqual(self.d["base_usa_verified_functions"],342)
        self.assertEqual(self.d["pending_pr23_unique_unpromoted"],82)
        self.assertEqual(self.d["central_346_g2"],"NOT_RUN")
        self.assertFalse(self.d["canonical_manifest_modified"])
if __name__=="__main__":unittest.main()
