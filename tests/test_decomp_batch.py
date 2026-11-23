import json
import os
from pathlib import Path
import sqlite3
import struct
import subprocess
import sys
import tempfile
import time
import unittest

from decomp.batch import Queue, StageTimeout, bounded, draft_issue, assembly_index, report_cache, local_storage
from decomp.probe import Elf32, linker_script, compare_code


def fixture(extra_data=False, second_function=False):
    names = b'\0.text\0.symtab\0.strtab\0.shstrtab\0.rodata\0'
    strings = b'\0function\0external\0other\0absolute\0'
    data = bytearray(52)
    sections = [(0,)*10]
    def add(name, kind, flags, payload, address=0, link=0, info=0, align=4, entry=0):
        start = len(data); data.extend(payload)
        sections.append((names.index(name+b'\0'), kind, flags, address, start, len(payload), link, info, align, entry))
    add(b'.text', 1, 6, b'\x11\x22\x33\x44')
    symbols = bytes(16)
    for name, value, size, info, section in [
        (b'function',0,4,0x12,1),(b'external',0,0,0x10,0),(b'absolute',0x1234,0,0x10,0xFFF1)]:
        symbols += struct.pack('>IIIBBH', strings.index(name+b'\0'), value, size, info, 0, section)
    if second_function:
        symbols += struct.pack('>IIIBBH', strings.index(b'other\0'),0,4,0x12,0,1)
    add(b'.symtab',2,0,symbols,link=3,entry=16)
    add(b'.strtab',3,0,strings,align=1)
    add(b'.shstrtab',3,0,names,align=1)
    if extra_data: add(b'.rodata',1,2,b'ABCD')
    shoff=len(data)
    for header in sections: data.extend(struct.pack('>10I',*header))
    data[:16]=b'\x7fELF\x01\x02\x01'+bytes(9)
    struct.pack_into('>HHIIIIIHHHHHH',data,16,1,8,1,0,0,shoff,0,52,0,0,40,len(sections),4)
    return bytes(data)


def function(name, size=8, verified=0):
    return dict(name=name,address=0x80000004,size=size,section='.main',source='asm/usa/unit.s',asm='glabel '+name+'\nendlabel '+name+'\n',expected=b'\x11'*size,verified=verified)


class ProbeTests(unittest.TestCase):
    def test_reads_actual_function_extent_globals_and_undefined(self):
        elf=Elf32(fixture())
        symbol=elf.function('function')
        self.assertEqual(elf.code(symbol), b'\x11\x22\x33\x44')
        self.assertEqual(elf.undefined(), {'external'})
        self.assertEqual(elf.globals()['absolute'],0x1234)
        self.assertIsNone(elf.layout_reason('function'))
        with self.assertRaises(ValueError):elf.function('missing')

    def test_generated_data_and_additional_functions_require_layout_review(self):
        self.assertEqual(Elf32(fixture(extra_data=True)).layout_reason('function'),'generated_allocated_data:.rodata')
        self.assertEqual(Elf32(fixture(second_function=True)).layout_reason('function'),'additional_functions_or_text_layout')

    def test_common_storage_requires_layout_review(self):
        data=bytearray(fixture());elf=Elf32(data)
        symbols=elf.sections[2][4]
        struct.pack_into('>H',data,symbols+3*16+14,0xFFF2)
        self.assertEqual(Elf32(data).layout_reason('function'),'generated_common_data')

    def test_invalid_elf_rejected(self):
        for value in (b'',fixture()[:20],b'BAD!'+fixture()[4:],fixture()[:-1]):
            with self.subTest(value=len(value)):
                with self.assertRaises(ValueError):Elf32(value)
        value=bytearray(fixture());value[5]=1
        with self.assertRaises(ValueError):Elf32(value)

    def test_link_script_preserves_four_byte_entries_and_checks_symbols(self):
        script=linker_script('function',0x80000004,{'external'},{'external':0x80001000})
        self.assertIn('.text 0x80000004 : SUBALIGN(4)',script)
        self.assertIn('external = 0x80001000;',script)
        for name in ('bad; injected','../outside'):
            with self.assertRaises(ValueError):linker_script(name,0,[],{})
        with self.assertRaisesRegex(ValueError,'Unresolved'):linker_script('function',0,{'missing'},{})
        with self.assertRaises(ValueError):linker_script('function',0,{'bad-name'},{'bad-name':1})

    def test_comparison_never_ignores_length_or_changed_words(self):
        self.assertEqual(compare_code(b'1234',b'1234')['word_differences'],0)
        self.assertEqual(compare_code(b'1234',b'12345')['byte_differences'],1)
        self.assertEqual(compare_code(b'12345678',b'1234xxxx')['word_differences'],1)
        comparison=compare_code(b'12345678',b'1234xxxx')
        self.assertEqual(comparison['word_mismatch_offsets'],[4])
        self.assertEqual(comparison['first_mismatch_offset'],4)


class QueueTests(unittest.TestCase):
    def setUp(self):
        self.folder=tempfile.TemporaryDirectory()
        self.path=Path(self.folder.name)/'queue.sqlite'
        self.queue=Queue(self.path)
        self.identity={'elf':'one'}
        self.queue.register(self.identity,[function('first'),function('second',12),function('verified',8,1)])

    def tearDown(self):
        self.queue.close();self.folder.cleanup()

    def test_resume_context_changes_and_retry_limits(self):
        selected=self.queue.select('recipe',10,64,scope='all')
        self.assertEqual([r['name'] for r in selected],['first','second'])
        ident=self.queue.claim('first','recipe')
        self.queue.finish(ident,dict(status='mismatch'))
        self.assertEqual([r['name'] for r in self.queue.select('recipe',10,64,scope='all')],['second'])
        self.assertEqual([r['name'] for r in self.queue.select('recipe',10,64,scope='all',retry=True,max_attempts=2)],['first','second'])
        second=self.queue.claim('first','recipe');self.queue.finish(second,dict(status='mismatch'))
        self.assertEqual([r['name'] for r in self.queue.select('recipe',10,64,scope='all',retry=True,max_attempts=2)],['second'])
        self.assertEqual(len(self.queue.select('new_context',10,64,scope='all')),2)
        self.queue.close();self.queue=Queue(self.path)
        self.assertEqual(len(self.queue.results('recipe')),1)
        self.assertEqual(self.queue.db.execute('SELECT COUNT(*) FROM attempts').fetchone()[0],2)

    def test_running_attempt_recovers_without_erasing_history(self):
        ident=self.queue.claim('first','recipe')
        self.queue.recover()
        self.assertEqual(self.queue.db.execute('SELECT status FROM attempts WHERE id=?',(ident,)).fetchone()[0],'interrupted')
        self.assertEqual(len(self.queue.select('recipe',10,64,scope='all')),1)

    def test_baseline_drift_and_invalid_names_are_rejected_atomically(self):
        with self.assertRaisesRegex(ValueError,'identity'):self.queue.register({'elf':'two'},[])
        changed=function('first');changed['expected']=b'X'*8
        with self.assertRaisesRegex(ValueError,'contents'):self.queue.register(self.identity,[function('new'),changed])
        self.assertIsNone(self.queue.db.execute("SELECT name FROM functions WHERE name='new'").fetchone())
        with self.assertRaises(ValueError):self.queue.register(self.identity,[function('../outside')])

    def test_verified_updates_do_not_destroy_attempts(self):
        ident=self.queue.claim('first','recipe');self.queue.finish(ident,dict(status='mismatch'))
        self.queue.register(self.identity,[function('first',verified=1)])
        self.assertEqual([r['name'] for r in self.queue.select('new',10,64,scope='all')],['second'])
        self.assertEqual(len(self.queue.results('recipe')),1)

    def test_reports_keep_probe_matches_separate_from_full_rom_proof(self):
        self.queue.meta('reference',dict(newly_verified=1))
        ident=self.queue.claim('first','recipe')
        self.queue.finish(ident,dict(status='linked_match',size=8,candidate_sha256='a',comparison={'actual_sha256':'b'}))
        ident=self.queue.claim('second','recipe')
        self.queue.finish(ident,dict(status='failed',reason=self.folder.name))
        result=report_cache(self.queue,'recipe')
        self.assertEqual(result['newly_verified_full_rom_functions'],0)
        self.assertEqual(result['linked_probe_bytes'],8)
        self.assertEqual(result['statuses'],{'linked_match':1,'failed':1})
        self.assertNotIn(self.folder.name,json.dumps(result))
        self.assertEqual(len(self.queue.select('recipe',10,64,scope='all',retry=True,max_attempts=9)),1)

    def test_run_history_is_persistent(self):
        ident=self.queue.start_run('recipe',dict(workers=2),2)
        self.queue.end_run(ident,1.2345)
        result=report_cache(self.queue,'recipe')
        self.assertEqual(result['runs'][0]['selected'],2)
        self.assertEqual(result['runs'][0]['elapsed'],1.234)

    def test_generated_and_overlay_filters_are_independent(self):
        overlay=function('func_overlay');overlay['section']='.overlay'
        self.queue.register(self.identity,[function('func_main'),overlay])
        self.assertEqual([r['name'] for r in self.queue.select('new',10,64,region='main')],['func_main'])
        self.assertEqual([r['name'] for r in self.queue.select('new',10,64,region='overlays')],['func_overlay'])

    def test_completed_attempts_cannot_be_rewritten(self):
        ident=self.queue.claim('first','recipe');self.queue.finish(ident,dict(status='mismatch'))
        with self.assertRaisesRegex(ValueError,'not running'):self.queue.finish(ident,dict(status='linked_match'))
        self.assertEqual(self.queue.results('recipe')[0]['status'],'mismatch')


class BatchInputTests(unittest.TestCase):
    def test_unknown_types_are_deferred_without_rewriting(self):
        for draft in ('? function(void);','extern ? global;','void function(? arg1) {}','void function(void *arg) { arg->unk8=0; }'):
            with self.subTest(draft=draft):self.assertIsNotNone(draft_issue(draft))
        self.assertIsNone(draft_issue('long f(long x) { return x ? call() : other(); }'))
        self.assertEqual(draft_issue('void f(void) { __asm__("nop"); }'),'inline_assembly')

    def test_function_extraction_does_not_include_neighbors(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);(root/'asm/usa').mkdir(parents=True)
            (root/'asm/usa/unit.s').write_text('glabel first\n nop\nendlabel first\nglabel second\n nop\nendlabel second\n')
            result=assembly_index(root,{'first'})
            self.assertIn('endlabel first',result['first'][1])
            self.assertNotIn('second',result['first'][1])

    def test_raw_artifacts_cannot_enter_tracked_source_directories(self):
        from decomp.batch import ROOT
        with self.assertRaises(ValueError):local_storage(ROOT/'results/raw')
        self.assertEqual(local_storage(ROOT/'local'),(ROOT/'local').resolve())

    def test_process_timeout_is_bounded_and_stage_is_preserved(self):
        with tempfile.TemporaryDirectory() as folder:
            start=time.monotonic()
            with self.assertRaises(StageTimeout) as raised:
                bounded([sys.executable,'-c','import time;time.sleep(30)'],folder,Path(folder)/'log',start+.2,stage='test')
            self.assertEqual(raised.exception.stage,'test')
            self.assertLess(time.monotonic()-start,5)

    def test_process_errors_are_not_matches(self):
        with tempfile.TemporaryDirectory() as folder:
            self.assertEqual(bounded([sys.executable,'-c','raise SystemExit(7)'],folder,Path(folder)/'log',time.monotonic()+5),7)

    def test_non_finite_budgets_are_rejected_before_running(self):
        from decomp.batch import run
        with tempfile.TemporaryDirectory() as folder:
            for seconds,search in ((float('nan'),0),(float('inf'),0),(10,float('nan')),(10,float('inf'))):
                with self.subTest(seconds=seconds,search=search):
                    with self.assertRaises(ValueError):run(folder,seconds=seconds,search_seconds=search)

class PublishedBatchEvidenceTests(unittest.TestCase):
    def test_benchmarks_bind_current_pipeline_and_preserve_promotion_boundary(self):
        import hashlib
        from decomp.batch import ROOT
        validation=json.loads((ROOT/'results/batch_validation.json').read_text())
        for name,expected in validation['pipeline_sources_sha256_lf'].items():
            # Historical benchmark hashes are evidence about their own run; they
            # must not be rewritten to match the current pipeline implementation.
            self.assertRegex(expected,r'^[0-9a-f]{64}$',name)
        current=json.loads((ROOT/'results/combined.json').read_text())
        self.assertEqual(current['status'],'matched')
        self.assertTrue(current['comparison']['full_rom_match'])
        # Live canonical original-address matching C, including eleven Mini C promotions.
        self.assertEqual(current['comparison']['matched_functions'],2164)
        self.assertEqual(current['comparison']['matched_function_bytes'],99604)
        preserved1723=json.loads((ROOT/'results/combined_1723_pre_isolated233_20261120.json').read_text())
        self.assertEqual((preserved1723['comparison']['matched_functions'],
                          preserved1723['comparison']['matched_function_bytes']), (1723,69344))
        prior1225=json.loads((ROOT/'results/combined_1225_before_227_expansion_20261118.json').read_text())
        self.assertEqual((prior1225['comparison']['matched_functions'],prior1225['comparison']['matched_function_bytes']),(1225,52028))
        accepted1119=json.loads((ROOT/'results/combined_1119_before_wide109_20261118.json').read_text())
        self.assertEqual((accepted1119['comparison']['matched_functions'],accepted1119['comparison']['matched_function_bytes']),(1119,50828))
        previous=json.loads((ROOT/'results/combined_987_before_wide132_20261118.json').read_text())
        self.assertEqual((previous['comparison']['matched_functions'],previous['comparison']['matched_function_bytes']),(987,42640))
        preserved782=json.loads((ROOT/'results/combined_782_20261117.json').read_text())
        self.assertEqual((preserved782['comparison']['matched_functions'],preserved782['comparison']['matched_function_bytes']),(782,34392))
        preserved779=json.loads((ROOT/'results/combined_779_20261117.json').read_text())
        self.assertEqual((preserved779['comparison']['matched_functions'],preserved779['comparison']['matched_function_bytes']),(779,34288))
        preserved732=json.loads((ROOT/'results/combined_732_20261117.json').read_text())
        self.assertEqual((preserved732['comparison']['matched_functions'],preserved732['comparison']['matched_function_bytes']),(732,32068))
        preserved731=json.loads((ROOT/'results/combined_731_20261117.json').read_text())
        self.assertEqual(preserved731['comparison']['matched_functions'],731)
        self.assertEqual(preserved731['comparison']['matched_function_bytes'],31932)
        # Historical canonical 720-C proof preserved intact, not rewritten.
        preserved720=json.loads((ROOT/'results/combined_720_20261117.json').read_text())
        self.assertEqual(preserved720['comparison']['matched_functions'],720)
        self.assertEqual(preserved720['comparison']['matched_function_bytes'],31184)
        # Preserve the exact canonical 346-C report from before the file12 promotion.
        preserved346=json.loads((ROOT/'results/combined_346_20261117.json').read_text())
        self.assertEqual(preserved346['status'],'matched')
        self.assertTrue(preserved346['comparison']['full_rom_match'])
        self.assertEqual(preserved346['comparison']['matched_functions'],346)
        self.assertEqual(preserved346['comparison']['matched_function_bytes'],17720)
        self.assertEqual(preserved346['verifier_source_sha256_lf'],
                         '182f0596aeba9229ffef403473201bf79c91c03b9fc9697d59cb3194b2d29190')
        previous_inventory=json.loads((ROOT/'results/inventory_346_20261117.json').read_text())
        self.assertEqual(previous_inventory['summary']['newly_matching_c'],346)
        preserved342=json.loads((ROOT/'results/combined_342_20261117.json').read_text())
        self.assertEqual(preserved342['comparison']['matched_functions'],342)
        self.assertEqual(preserved342['comparison']['matched_function_bytes'],17568)
        self.assertEqual(preserved342['verifier_source_sha256_lf'],
                         '512dcb943e7fbe3c5ecdaf715aff9e8b499fa4dbb96f4d94810833d112b7aa3e')
        preserved315=json.loads((ROOT/'results/combined_315_preserved_20261116.json').read_text())
        self.assertEqual(preserved315['comparison']['matched_functions'],315)
        self.assertEqual(preserved315['comparison']['matched_function_bytes'],16660)
        historical307=json.loads((ROOT/'results/combined_307_20261116.json').read_text())
        self.assertEqual(historical307['comparison']['matched_functions'],307)
        self.assertEqual(historical307['comparison']['matched_function_bytes'],16344)
        self.assertEqual(historical307['verifier_source_sha256_lf'],
                         '607fc38152d04ce555ed38a1a16c24fb2e76104833c7c765a5933cb212c1b8ab')
        historic306=json.loads((ROOT/'results/combined_306_20261116.json').read_text())
        self.assertEqual(historic306['comparison']['matched_functions'],306)
        self.assertEqual(historic306['comparison']['matched_function_bytes'],16292)
        self.assertEqual(historic306['verifier_source_sha256_lf'],
                         '876390a62891188161c2e32744abb8543a9598e3e7c61fffce04d2eb1a0cda79')
        historic303=json.loads((ROOT/'results/combined_303_20261116.json').read_text())
        self.assertEqual(historic303['comparison']['matched_functions'],303)
        self.assertEqual(historic303['comparison']['matched_function_bytes'],16180)
        self.assertEqual(historic303['verifier_source_sha256_lf'],
                         '0b4556a01128510da5a23ef36e6e55094339e69a7bb070b5b45c213128231769')
        self.assertEqual(current['verifier_source_sha256_lf'],
                         hashlib.sha256((ROOT/'verify.py').read_bytes().replace(b'\r\n',b'\n')).hexdigest())
        self.assertEqual(preserved315['verifier_source_sha256_lf'],
                         '93e91fa551668a51fbc45e24ba39c73c2c60cc4e2a854d43040c4f0b209d7737')
        # The certified historical 210-C proof retains its original hash.
        historic = json.loads((ROOT/'results/combined_210_20261116.json').read_text())
        self.assertEqual(historic['verifier_source_sha256_lf'],
                         '1c60206c7007b9e499250fc2512851bfa2c1d07f5743e607b90938196bd4280b')
        current_sha = hashlib.sha256((ROOT/'verify.py').read_bytes().replace(b'\r\n',b'\n')).hexdigest()
        # The VM residual ledger records the unmodified USA2090 predecessor.
        historical=json.loads((ROOT/'results/combined_2090_pre_opening_new2_20261123.json').read_text())
        verified_prior_sha=json.loads((ROOT/'results/vm_residual_inventory.json').read_text())['current_sources']['verifier_sha256']
        self.assertEqual(historical['verifier_source_sha256_lf'],verified_prior_sha)
        self.assertEqual(current_sha,current['verifier_source_sha256_lf'])
        for name in ('batch_pilot.json','batch_search_pilot.json','batch_entrance_followup.json','batch_ui_followup.json','batch_autonomous_main_v1.json'):
            result=json.loads((ROOT/'results'/name).read_text())
            self.assertEqual(result['newly_verified_full_rom_functions'],0)
            self.assertEqual(sum(result['statuses'].values()),result['latest_attempts'])
            self.assertGreater(len(result['linked_probe_matches']),0)
            self.assertEqual(result['linked_probe_bytes'],sum(fn['size'] for fn in result['linked_probe_matches']))
            for file,expected in result['recipe_evidence']['source_hashes'].items():
                self.assertRegex(expected,r'^[0-9a-f]{64}$',file)
        self.assertTrue(validation['fresh_gate']['full_rom_match'])
        self.assertTrue(validation['cached_reviewed_bundle_gate']['full_rom_match'])
        self.assertTrue(validation['cached_reviewed_bundle_gate']['baseline_cache_used'])
        self.assertEqual(validation['resume_selected'],0)
        self.assertEqual(validation['newly_promoted_functions'],0)
