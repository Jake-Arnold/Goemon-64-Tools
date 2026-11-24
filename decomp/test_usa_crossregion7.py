"""ROM-free checks for new original USA matching-C ownership and integrity.

No test here substitutes for native IDO, combined 32 MiB ROM, ELF or CI gates.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from decomp import usa_crossregion7 as stage
from decomp import overlay_isolated233 as splice
from decomp.verify import claimed_functions, load_manifest

ROOT=Path(__file__).resolve().parent

class Crossregion7StageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.current=load_manifest(ROOT/'results/manifest_2325_before_consolidated29_20261124.json')
        cls.current.pop('usa_transition_final_promotion',None)
        cls.current.pop('usa_transition1_promotion',None)
        cls.current.pop('usa_cright4_promotion',None)  # Preserve USA2079 checkpoint
        cls.current.pop('usa_script_vm_dual_reference',None)  # Preserve USA2079 checkpoint
        cls.current.pop('usa_script_vm440_promotion',None)  # Preserve USA2079 checkpoint
        cls.current.pop('usa_native151_promotion',None)  # Preserve USA2079 checkpoint
        cls.current.pop('usa_script_vm436_promotion',None)  # prior 2079 stage is immutable
        # Historical checkpoint projection: post2090 functions were not yet accepted.
        cls.current.pop('overlay_usa_opening_new2_stage',None)
        cls.current.pop('overlay_usa_short72_stage',None)
        cls.current.pop('overlay_mini_selector_stage',None)  # Preserve USA2079 checkpoint
        cls.current.pop('overlay_mini10_stage',None)  # Preserve USA2079 checkpoint
        cls.fixture=stage.validate_predecessor(cls.current)
        cls.old={k:v for k,v in cls.current.items() if k!='overlay_crossregion7_stage'}

    def test_reviewed_original_boundaries_are_additive(self):
        prior=claimed_functions(self.old)
        final=claimed_functions(self.current)
        self.assertEqual((len(prior),sum(f['size'] for f in prior)),(2072,92492))
        self.assertEqual((len(final),sum(f['size'] for f in final)),(2079,93016))
        known={f['name'] for f in prior}
        novel=[f for f in final if f['name'] not in known]
        self.assertEqual({f['name'] for f in novel},
                         {f['name'] for f in self.fixture['functions']})
        self.assertEqual(sum(x['size'] for x in novel),524)
        spans=sorted((f['rom_offset'],f['rom_offset']+f['size']) for f in final)
        self.assertTrue(all(a[1]<=b[0] for a,b in zip(spans,spans[1:])))

    def test_all_native_sources_and_headers_are_content_pinned(self):
        self.assertEqual(len(self.fixture['functions']),7)
        self.assertEqual(len(self.fixture['headers']),2)
        for f in self.fixture['functions']:
            with self.subTest(name=f['name']):
                p=stage.SRC/(f['source']+'.c')
                self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),f['source_sha256'])
                self.assertNotIn(b'GLOBAL_ASM',p.read_bytes())
                self.assertEqual(f['vma'],int(f['name'].split('_')[1],16))
                self.assertEqual(f['rom_offset'],int(f['name'].split('_')[2],16))
                self.assertTrue(f['jp_name'] is None or f['jp_name'].startswith('func_'))

    def test_no_disguised_or_duplicate_stage(self):
        missing=dict(self.old)
        with self.assertRaises(ValueError):stage.validate_predecessor(missing)
        wrong=dict(self.current)
        wrong['overlay_crossregion7_stage']={'format':'unreviewed'}
        with self.assertRaises(ValueError):stage.validate_predecessor(wrong)
        shifted=dict(self.current)
        shifted['splat_options']={'noncanonical':True}
        with self.assertRaises(ValueError):stage.validate_predecessor(shifted)

    def test_source_context_preserves_previous_accepted_embedded_sources(self):
        preserved=dict(splice.EMBEDDED)
        self.assertNotIn('func_800363F4_36FF4',preserved)
        with stage.source_context():
            self.assertEqual(splice.EMBEDDED,{'func_800363F4_36FF4':'object_flags.c'})
        self.assertEqual(splice.EMBEDDED,preserved)

    def test_mixed_owner_header_rewrite_is_exact_and_fails_closed(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            (root/'src').mkdir()
            owner=root/'src/object_flags.c'
            anchor='/* Original native C for func_800363F4_36FF4 */\n#include "probe_common.h"'
            owner.write_text('preamble\n'+anchor+'\nclosing\n')
            stage.resolve_embedded_owner_header(root)
            output=owner.read_text()
            self.assertIn('#include "m2c_macros.h"',output)
            self.assertNotIn('probe_common.h',output)
            self.assertTrue(output.startswith('preamble\n'))
            with self.assertRaises(ValueError):stage.resolve_embedded_owner_header(root)

    def test_forged_source_hash_and_candidate_range_rejected(self):
        # The real fixture is hash-pinned before individual entries are read.
        data=stage.MANIFEST.read_bytes()
        with patch.object(stage,'FIXTURE_SHA256','0'*64):
            with self.assertRaisesRegex(ValueError,'manifest hash changed'):
                stage.fixture()
        self.assertEqual(hashlib.sha256(data).hexdigest(),stage.FIXTURE_SHA256)
        self.assertEqual(stage.ROM_SHA1,'6ea0ed71032ce08fc2745f412d84936382197494')


    def test_each_original_c_source_host_sanitizer_syntax(self):
        gcc=shutil.which('gcc')
        if not gcc:self.skipTest('No host GCC')
        for f in self.fixture['functions']:
            source=stage.SRC/(f['source']+'.c')
            with self.subTest(function=f['name']):
                cmd=[gcc,'-std=gnu89','-fsyntax-only','-fsanitize=address,undefined',
                     '-Wno-int-to-pointer-cast','-Wno-pointer-to-int-cast',
                     '-Wno-implicit-function-declaration','-Wno-incompatible-pointer-types',
                     '-Wno-int-conversion',str(source)]
                result=subprocess.run(cmd,capture_output=True,timeout=15)
                self.assertEqual(result.returncode,0,result.stderr.decode(errors='replace')[:1000])

    def test_actual_move_to_front_c_relinks_nodes_with_host_sanitizers(self):
        gcc=shutil.which('gcc')
        if not gcc:self.skipTest('No host GCC')
        # Original N64 pointer fields at 0x74 are 4-byte aligned. The host is
        # LP64; disable only UBSan's host-pointer alignment subcheck while
        # retaining address and all other UB sanitizers. The actual original
        # IDO/ELF ABI is separately validated by the complete native verifier.
        # Offset by 4 to align the 64-bit host pointer inside the object.
        body=r'''#include <stddef.h>
#include <stdio.h>
#include <stdint.h>
extern int func_800363F4_36FF4(void*,void*);
static unsigned char a[160] __attribute__((aligned(16)));
static unsigned char b[160] __attribute__((aligned(16)));
static unsigned char c[160] __attribute__((aligned(16)));
static void set_next(void *p,void *v){*(void **)((char*)p+0x74)=v;}
static void *get_next(void *p){return *(void **)((char*)p+0x74);}
int main(void){
  void *pa=a+4,*pb=b+4,*pc=c+4;
  fprintf(stderr,"pa=%p pa.field=%p pb=%p pb.field=%p pc=%p pc.field=%p\n",pa,(char*)pa+0x74,pb,(char*)pb+0x74,pc,(char*)pc+0x74);
  if(((uintptr_t)((char*)pa+0x74)%8)!=0||((uintptr_t)((char*)pb+0x74)%8)!=0||((uintptr_t)((char*)pc+0x74)%8)!=0)return 7;
  set_next(pa,pb);set_next(pb,pc);set_next(pc,0);
  if(func_800363F4_36FF4(0,pc)!=0)return 1;
  if(func_800363F4_36FF4(pa,0)!=0)return 2;
  if(func_800363F4_36FF4(pa,pc)!=1)return 3;
  if(get_next(pa)!=pc||get_next(pc)!=pb||get_next(pb)!=0)return 4;
  if(func_800363F4_36FF4(pa,pb)!=1)return 5;
  if(get_next(pa)!=pb||get_next(pb)!=pc||get_next(pc)!=0)return 6;
  return 0;
}
'''
        with tempfile.TemporaryDirectory() as path:
            root=Path(path)
            c=root/'move_to_front.c';exe=root/'move_to_front'
            c.write_text(body)
            src=stage.SRC/'xreg7_000.c'
            cmd=[gcc,'-std=gnu11','-O1','-g','-fsanitize=address,undefined',
                 '-fno-omit-frame-pointer','-fno-sanitize=alignment',
                 '-o',str(exe),str(c),str(src)]
            compile_=subprocess.run(cmd,capture_output=True,timeout=30)
            self.assertEqual(compile_.returncode,0,compile_.stderr.decode(errors='replace')[:1200])
            run=subprocess.run([str(exe)],capture_output=True,timeout=20)
            self.assertEqual(run.returncode,0,run.stderr.decode(errors='replace')[:1400])

if __name__=='__main__':unittest.main()
