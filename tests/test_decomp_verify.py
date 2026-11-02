import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from decomp.verify import load_manifest,apply_units,parse_symbols,compare_images

ROOT=Path(__file__).resolve().parents[1]


class DecompVerificationTests(unittest.TestCase):
    def test_manifest_bounds_and_symbol_identity(self):
        manifest=load_manifest(ROOT/'decomp/manifest.json')
        self.assertEqual(sum(len(u['functions']) for u in manifest['units']),24)
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'bad.json'
            bad=copy.deepcopy(manifest);bad['units'][0]['source']='../other.c'
            path.write_text(json.dumps(bad))
            with self.assertRaisesRegex(ValueError,'source'):load_manifest(path)
            bad=copy.deepcopy(manifest);bad['units'][0]['functions'][0]['rom_offset']+=4
            path.write_text(json.dumps(bad))
            with self.assertRaises(ValueError):load_manifest(path)

    def test_symbol_parsing_and_tampered_matching_evidence(self):
        data=b'\x11'*16
        manifest={'decompressed_sha1':hashlib.sha1(data).hexdigest(),
                  'units':[{'rom_end':16,'functions':[{'name':'func_80000000_0','rom_offset':0,'size':8}]}]}
        # Synthetic symbols preserve the same guest/ROM relation used by verifier.
        manifest['units'][0]['functions'][0]['name']='func_7FFFF400_0'
        symbols=parse_symbols('7ffff400 T func_7FFFF400_0\n         U external\n')
        result=compare_images(data,data,manifest,symbols)
        self.assertTrue(result['full_rom_match']);self.assertEqual(result['matched_functions'],1)
        changed=data[:9]+b'\x22'+data[10:]
        result=compare_images(data,changed,manifest,symbols)
        self.assertFalse(result['full_rom_match']);self.assertEqual(result['matched_functions'],1)
        result=compare_images(data,b'\x22'+data[1:],manifest,symbols)
        self.assertEqual(result['matched_functions'],0)
        symbols['func_7FFFF400_0.NON_MATCHING']=0x7FFFF400
        self.assertEqual(compare_images(data,data,manifest,symbols)['matched_functions'],0)
        del symbols['func_7FFFF400_0.NON_MATCHING'];symbols['func_7FFFF400_0']+=4
        self.assertEqual(compare_images(data,data,manifest,symbols)['matched_functions'],0)
        with self.assertRaisesRegex(ValueError,'identity'):compare_images(b'other',data,manifest,symbols)

    def test_apply_only_expected_anchor_preserves_existing_files_on_failure(self):
        with tempfile.TemporaryDirectory() as folder:
            checkout=Path(folder)/'candidate';(checkout/'config/usa').mkdir(parents=True)
            (checkout/'src').mkdir();sources=Path(folder)/'sources';sources.mkdir()
            config=checkout/'config/usa/splat.yaml';config.write_text('before [0x10, asm] after\n')
            (sources/'unit.c').write_text('void function(void) {}\n')
            manifest={'units':[{'source':'unit.c','splat_original':'[0x10, asm]',
                                'splat_replacement':'[0x10, c, unit]'}]}
            apply_units(checkout,manifest,sources)
            self.assertIn('before [0x10, c, unit] after',config.read_text())
            (checkout/'src/unit.c').write_text('user work')
            config.write_text('before [0x10, asm] after\n');before=config.read_bytes()
            with self.assertRaises(ValueError):apply_units(checkout,manifest,sources)
            self.assertEqual((checkout/'src/unit.c').read_text(),'user work')
            self.assertEqual(config.read_bytes(),before)

    def test_shared_flag_functions_have_no_assembly_placeholders(self):
        for unit in load_manifest(ROOT/'decomp/manifest.json')['units']:
            source=(ROOT/'decomp'/unit['source']).read_text()
            self.assertEqual(source.count('GLOBAL_ASM'),len(unit.get('assembly_functions',[])))
            for fn in unit['functions']:
                self.assertNotIn('/'+fn['name']+'.s',source)
            self.assertNotIn('__asm__',source)

    def test_assembly_retention_cannot_claim_a_reconstructed_function(self):
        manifest=load_manifest(ROOT/'decomp/manifest.json')
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'manifest.json'
            manifest['units'][0]['assembly_functions']=[manifest['units'][0]['functions'][0]['name']]
            path.write_text(json.dumps(manifest))
            with self.assertRaisesRegex(ValueError,'assembly placeholder'):load_manifest(path)

    def test_undeclared_placeholder_rejected_without_partial_application(self):
        with tempfile.TemporaryDirectory() as folder:
            checkout=Path(folder)/'candidate';(checkout/'config/usa').mkdir(parents=True)
            (checkout/'src').mkdir();sources=Path(folder)/'sources';sources.mkdir()
            config=checkout/'config/usa/splat.yaml';config.write_text('[0x10, asm]\n')
            (sources/'unit.c').write_text('#pragma GLOBAL_ASM("asm/func_80000000_0.s")\n')
            manifest={'units':[{'source':'unit.c','splat_original':'[0x10, asm]',
                                'splat_replacement':'[0x10, c, unit]'}]}
            with self.assertRaisesRegex(ValueError,'Undeclared'):apply_units(checkout,manifest,sources)
            self.assertFalse((checkout/'src/unit.c').exists())
            self.assertEqual(config.read_text(),'[0x10, asm]\n')
