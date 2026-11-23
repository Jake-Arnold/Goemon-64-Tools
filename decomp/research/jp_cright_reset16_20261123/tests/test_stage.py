"""ROM-free controls for stage/metadata source invariants; no user ROM needed."""
import hashlib,importlib.util,re,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('cright_reset16_stage',ROOT/'stage_and_verify.py')
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def fake_asm():
    lines=['.include "macro.inc"\n\n.set noat\n.set noreorder\n.set gp=64\n\n.section .text, "ax"\n\n']
    addr=module.ROM_OFF
    for n,(name,length) in enumerate(module.NAMES):
        lines.append(f'nonmatching {name}, 0x{length:X}\nglabel {name}\n')
        for k in range(0,length,4):
            x=addr+k
            lines.append(f'    /* {x:X} {0x80000400+x-0x1000:08X} 00000000 */  nop\n')
        lines.append(f'endlabel {name}\n\n')
        addr+=length
    assert addr==0x543C
    lines.append('    /* 543C 8000483C 00000000 */  nop\n')
    return ''.join(lines)

class NativeSourceStageTests(unittest.TestCase):
    def test_frozen_matching_source_digest(self):
        self.assertEqual(module.sha(module.read_source()),module.C_SHA)
    def test_synthetic_original_owner_has_exact_stage_topology(self):
        c,fragments=module.render_fragments(fake_asm())
        self.assertEqual(module.sha(c),module.MIX_SHA)
        self.assertEqual(len(fragments),4)
        self.assertTrue(all('nonmatching '+name in data for name,data in fragments))
    def test_reject_changed_original_function_size(self):
        original=fake_asm().replace('func_800041AC_4DAC, 0x30','func_800041AC_4DAC, 0x34',1)
        with self.assertRaises(ValueError):module.render_fragments(original)
    def test_reject_reordered_fragment(self):
        original=fake_asm().replace('func_800041AC_4DAC, 0x30','func_800041DC_4DDC, 0x30',1)
        with self.assertRaises(ValueError):module.render_fragments(original)
    def test_reject_missing_final_padding_nop(self):
        original=fake_asm().replace('    /* 543C 8000483C 00000000 */  nop\n','')
        with self.assertRaises(ValueError):module.render_fragments(original)
    def test_reject_wrong_original_address(self):
        original=fake_asm().replace('/* 4DAC 800041AC','/* 4DAC 800041B0',1)
        # Include an instruction-guest-address assertion in stage, not just ROM offset.
        with self.assertRaises(ValueError):module.render_fragments(original)
    def test_reject_unsigned_elf_metadata_edit_as_source(self):
        self.assertNotEqual(module.sha((ROOT/'source/negative_schedule_v1.c').read_bytes()),module.C_SHA)
    def test_wrong_original_rom_input_rejected(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            d=Path(tmp)/'config/japan_0';d.mkdir(parents=True)
            (d/'baserom.decompressed.z64').write_bytes(b'\0'*16)
            with self.assertRaises(ValueError):module.original(Path(tmp))

if __name__=='__main__':unittest.main()
