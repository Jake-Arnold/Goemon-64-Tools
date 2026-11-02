"""Linux tool integration using synthetic assembly, never game instructions."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
import unittest

from decomp.batch import Queue, StageTimeout, bounded, export_matches, sha
from decomp.probe import Elf32, linker_script


@unittest.skipUnless(os.name=='posix' and shutil.which('mips-linux-gnu-as') and shutil.which('mips-linux-gnu-ld'), 'Requires Linux MIPS binutils')
class ProbeIntegrationTests(unittest.TestCase):
    def build_probe(self, root):
        asm=root/'input.s'
        asm.write_text('.set noat\n.set noreorder\n.text\n.align 4\n.globl synthetic\n.type synthetic,@function\nsynthetic:\nlui $v0,%hi(synthetic_global)\naddiu $v0,$v0,%lo(synthetic_global)\njr $ra\nnop\n.size synthetic,.-synthetic\n')
        obj=root/'input.o'
        subprocess.run(['mips-linux-gnu-as','-EB','-march=vr4300','-mabi=32',str(asm),'-o',str(obj)],check=True,capture_output=True)
        data=Elf32(obj.read_bytes())
        script=root/'input.ld';script.write_text(linker_script('synthetic',0x80000004,data.undefined(),{'synthetic_global':0x8012FFFE}))
        image=root/'probe.elf'
        subprocess.run(['mips-linux-gnu-ld','-T',str(script),'-o',str(image),str(obj)],check=True,capture_output=True)
        return image

    def test_real_relocations_and_non_sixteen_byte_entry(self):
        with tempfile.TemporaryDirectory() as folder:
            image=self.build_probe(Path(folder));elf=Elf32(image.read_bytes());symbol=elf.function('synthetic')
            self.assertEqual(symbol.value,0x80000004)
            self.assertEqual(elf.code(symbol),bytes.fromhex('3c0280132442fffe03e0000800000000'))

    def test_export_revalidates_source_and_linked_code_before_writing(self):
        with tempfile.TemporaryDirectory() as folder:
            cache=Path(folder);attempt=cache/'attempts/000001-synthetic';attempt.mkdir(parents=True)
            image=self.build_probe(attempt);data=image.read_bytes();elf=Elf32(data);expected=elf.code(elf.function('synthetic'))
            source=attempt/'candidate.c';source.write_text('/* synthetic review fixture */\n')
            original=source.read_bytes()
            queue=Queue(cache/'queue.sqlite')
            queue.register({'test':'synthetic'},[dict(name='synthetic',address=0x80000004,size=16,section='.main',source='',asm='',expected=expected,verified=0)])
            queue.meta('last_recipe','recipe')
            ident=queue.claim('synthetic','recipe')
            queue.finish(ident,dict(status='linked_match',size=16,artifacts='attempts/000001-synthetic',candidate_source='candidate.c',candidate_sha256=sha(original),linked_elf='probe.elf',linked_elf_sha256=sha(data),comparison={'actual_sha256':sha(expected)}))
            queue.close()
            result=export_matches(cache,cache/'review')
            self.assertEqual(result['newly_verified_full_rom_functions'],0)
            self.assertEqual((cache/'review/synthetic.c').read_bytes(),original)
            with self.assertRaisesRegex(ValueError,'Unknown recipe'):export_matches(cache,cache/'unknown-recipe','unknown')
            self.assertFalse((cache/'unknown-recipe').exists())
            source.write_bytes(b'changed')
            with self.assertRaisesRegex(ValueError,'source changed'):export_matches(cache,cache/'changed-source')
            self.assertFalse((cache/'changed-source').exists())
            source.write_bytes(original);image.write_bytes(data+b'changed')
            with self.assertRaisesRegex(ValueError,'ELF changed'):export_matches(cache,cache/'changed-elf')
            self.assertFalse((cache/'changed-elf').exists())

    def test_timeout_kills_descendant_process_group(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);pidfile=root/'child.pid'
            code='import subprocess,sys,time; from pathlib import Path; child=subprocess.Popen([sys.executable,"-c","import time;time.sleep(30)"]); Path(sys.argv[1]).write_text(str(child.pid)); time.sleep(30)'
            with self.assertRaises(StageTimeout):
                bounded([sys.executable,'-c',code,str(pidfile)],root,root/'log',time.monotonic()+1.5)
            self.assertTrue(pidfile.exists())
            child=int(pidfile.read_text())
            for _ in range(20):
                state=Path(f'/proc/{child}/stat')
                if not state.exists() or state.read_text().split(') ',1)[1].startswith('Z'):break
                time.sleep(.05)
            else:self.fail('Descendant survived the process-group timeout')
