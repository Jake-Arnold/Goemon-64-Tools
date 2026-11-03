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
        self.assertEqual(sum(len(u['functions']) for u in manifest['units']),78)
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

    def test_jump_label_override_is_narrow_and_candidate_only(self):
        manifest=load_manifest(ROOT/'decomp/manifest.json')
        self.assertEqual(manifest['splat_options'],{'asm_jtbl_label_macro':'glabel'})
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'manifest.json'
            bad=copy.deepcopy(manifest);bad['splat_options']={'arbitrary':'setting'}
            path.write_text(json.dumps(bad))
            with self.assertRaisesRegex(ValueError,'Splat'):load_manifest(path)
            checkout=Path(folder)/'candidate';(checkout/'config/usa').mkdir(parents=True)
            (checkout/'src').mkdir();sources=Path(folder)/'sources';sources.mkdir()
            config=checkout/'config/usa/splat.yaml';config.write_text('options:\n  compiler: IDO\n[0x10, asm]\n')
            (sources/'unit.c').write_text('void function(void) {}\n')
            small={'splat_options':{'asm_jtbl_label_macro':'glabel'},'units':[{
                'source':'unit.c','splat_original':'[0x10, asm]','splat_replacement':'[0x10, c, unit]'}]}
            apply_units(checkout,small,sources)
            self.assertIn('options:\n  asm_jtbl_label_macro: glabel\n  compiler: IDO',config.read_text())

    def test_reference_comparator_is_excluded_from_matching_c_count(self):
        manifest=load_manifest(ROOT/'decomp/manifest.json')
        vm=next(unit for unit in manifest['units'] if unit['source']=='script_vm.c')
        self.assertEqual(len(vm['functions']),49)
        self.assertEqual(len(vm['assembly_functions']),20)
        name='func_8003D9B8_3E5B8'
        self.assertIn(name,vm['assembly_functions'])
        self.assertIn('func_8003DE80_3EA80',vm['assembly_functions'])
        self.assertNotIn(name,{fn['name'] for fn in vm['functions']})
    def test_vm_layout_preset_rejects_other_values_and_missing_handler(self):
        manifest=load_manifest(ROOT/'decomp/manifest.json')
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'manifest.json'
            for value in (False,1,'yes',{}):
                bad=copy.deepcopy(manifest);bad['vm_assignment_table_layout']=value
                path.write_text(json.dumps(bad))
                with self.assertRaisesRegex(ValueError,'layout preset'):load_manifest(path)
            bad=copy.deepcopy(manifest)
            vm=next(u for u in bad['units'] if u['source']=='script_vm.c')
            vm['functions']=[f for f in vm['functions'] if f['name']!='func_8003DB0C_3E70C']
            path.write_text(json.dumps(bad))
            with self.assertRaisesRegex(ValueError,'pinned assignment'):load_manifest(path)

    def test_vm_layout_changes_only_selected_main_header_and_table(self):
        with tempfile.TemporaryDirectory() as folder:
            checkout=Path(folder)/'candidate';(checkout/'config/usa').mkdir(parents=True)
            (checkout/'src').mkdir();sources=Path(folder)/'sources';sources.mkdir()
            config=checkout/'config/usa/splat.yaml'
            original=('    start: 0x1050\n    vram: 0x80000450\n    subalign: 16\n    subsegments:\n'
                '    - [0x10, asm]\n    - [0x7B6F0, rodata, main_continued]\n'
                '  - name: other\n    subalign: 16\n')
            config.write_text(original);(checkout/'Makefile').write_text('all:\n\ttrue\n')
            (sources/'unit.c').write_text('void function(void) {}\n')
            manifest={'vm_assignment_table_layout':True,'units':[{'source':'unit.c',
                'splat_original':'[0x10, asm]','splat_replacement':'[0x10, c, unit]'}]}
            apply_units(checkout,manifest,sources)
            updated=config.read_text()
            self.assertIn('    - [0x7DC2C, .rodata, script_vm]\n    - [0x7DC68, rodata, main_continued_after_vm_store]',updated)
            self.assertIn('  - name: other\n    subalign: 16',updated)
            self.assertEqual(updated.count('    subalign: 4'),1)
            self.assertIn('main_continued.rodata.s.o: ASFLAGS += --no-pad-sections',(checkout/'Makefile').read_text())
            # An ambiguous anchor must fail without copying a C file or modifying either build file.
            (checkout/'src/unit.c').unlink()
            config.write_text(original.replace('    subalign: 16\n    subsegments:', '    subalign: 8\n    subsegments:'))
            before=config.read_bytes();make_before=(checkout/'Makefile').read_bytes()
            with self.assertRaisesRegex(ValueError,'subalignment'):apply_units(checkout,manifest,sources)
            self.assertEqual(config.read_bytes(),before)
            self.assertEqual((checkout/'Makefile').read_bytes(),make_before)
            self.assertFalse((checkout/'src/unit.c').exists())
    def test_current_sources_and_manifest_have_matching_build_evidence(self):
        manifest=load_manifest(ROOT/'decomp/manifest.json')
        result=json.loads((ROOT/'decomp/results/combined.json').read_text())
        self.assertEqual(result['status'],'matched')
        self.assertEqual(result['upstream_commit'],manifest['upstream_commit'])
        self.assertTrue(result['comparison']['full_rom_match'])
        expected={f['name']:f for u in manifest['units'] for f in u['functions']}
        actual={f['name']:f for f in result['comparison']['functions']}
        self.assertEqual(set(expected),set(actual))
        self.assertEqual(result['comparison']['matched_function_bytes'],sum(f['size'] for f in expected.values()))
        for name,fn in actual.items():
            self.assertTrue(fn['matched'],name)
            self.assertEqual(fn['size'],expected[name]['size'])
            self.assertEqual(int(fn['rom_offset'],16),expected[name]['rom_offset'])
            self.assertEqual(fn['candidate_sha256'],fn['expected_sha256'])
        sources={u['source'] for u in manifest['units']}|set(manifest['support_headers'])
        self.assertEqual(set(result['sources_sha256_lf']),sources)
        for name in sources:
            data=(ROOT/'decomp'/name).read_bytes().replace(b'\r\n',b'\n')
            self.assertEqual(hashlib.sha256(data).hexdigest(),result['sources_sha256_lf'][name],name)
        self.assertEqual(result['object_layout']['payload_bytes_changed'],0)
        self.assertTrue(result['assignment_table']['matched'])
