"""ROM-free structure, provenance, mutation and deterministic-source gates."""
import copy
import json
import tempfile
import unittest
from pathlib import Path

from decomp import japan_noop_port as port


class JapaneseUSANoopPort(unittest.TestCase):
    def test_canonical_manifest(self):
        m=port.load_manifest()
        self.assertEqual((m['total_c_functions'],m['total_c_bytes']),(329,5356))
        self.assertEqual(len(m['parents']),81)
        self.assertEqual(sum(len(x['c']) for x in m['parents']),290)

    def test_provenance_both_forms(self):
        m=port.load_manifest()
        by_form={form:[] for form in port.FORM}
        for parent in m['parents']:
            for name,form in parent['c']:
                by_form[form].append(name)
        self.assertEqual((len(by_form['P']),len(by_form['Z'])),(236,54))
        self.assertIn('void *a0, void *a1',port.source_text(by_form['P'][0],'P'))
        self.assertIn('(void)',port.source_text(by_form['Z'][0],'Z'))
        self.assertNotIn('GLOBAL_ASM',port.source_text(by_form['P'][0],'P'))

    def mutate_and_reject(self,change):
        m=json.loads(port.MANIFEST.read_text())
        change(m)
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'manifest.json'
            path.write_text(json.dumps(m))
            with self.assertRaises((ValueError,AssertionError,KeyError)):
                port.load_manifest(path)

    def test_missing_candidate_rejected(self):
        self.mutate_and_reject(lambda m:m['parents'][0]['c'].pop())

    def test_duplicate_function_rejected(self):
        self.mutate_and_reject(lambda m:m['parents'][0]['c'].__setitem__(1,m['parents'][0]['c'][0]))

    def test_wrong_region_rejected(self):
        self.mutate_and_reject(lambda m:m.__setitem__('region','usa'))

    def test_stale_original_hash_rejected(self):
        self.mutate_and_reject(lambda m:m.__setitem__('original_retail_sha1','bad'))

    def test_illegal_parent_size_rejected(self):
        self.mutate_and_reject(lambda m:m['parents'][0].__setitem__('size',1))

    def test_zero_arg_stubs_retain_native_eight_bytes(self):
        m=port.load_manifest()
        counts={f:0 for f in port.FORM}
        for parent in m['parents']:
            for name,form in parent['c']:
                counts[form]+=port.FORM[form]['size']
        self.assertEqual(sum(counts.values()),3264)
        self.assertEqual(counts,{'P':2832,'Z':432})

    def test_no_private_rom_or_asm_assets_in_port_inputs(self):
        for p in [port.MANIFEST,port.HERE/'japan_noop_port.py',port.HERE/'build_japan_noop_port_329.sh']:
            self.assertTrue(p.exists())
            self.assertLess(p.stat().st_size,40000)
        manifest=port.MANIFEST.read_text()
        self.assertNotIn('baserom.z64',manifest)
        self.assertNotIn('.NON_MATCHING',manifest)

if __name__=='__main__':unittest.main()
