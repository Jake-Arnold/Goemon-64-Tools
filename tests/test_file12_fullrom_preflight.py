import importlib.util, unittest, struct
from pathlib import Path
spec=importlib.util.spec_from_file_location('fullrom', str(Path(__file__).resolve().parents[1] / 'decomp/research/file12_spatial/integrate_fullrom.py'))
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

def synthetic_text(code=b'\x01\x02\x03\x04', padded=b'\x00\x00\x00\x00'):
    s=b'\x00.text\x00.shstrtab\x00'
    data=bytearray(b'\x00'*0x180)
    data[:16]=b'\x7fELF\x01\x02\x01'+b'\x00'*9
    struct.pack_into('>HHI',data,16,1,8,1)
    struct.pack_into('>I',data,32,0x100)
    struct.pack_into('>HHH',data,46,40,3,2)
    data[0x40:0x40+len(code+padded)]=code+padded
    data[0x80:0x80+len(s)]=s
    # section name=1, type=progbits, flags=ALLOC|EXEC, offset=0x40, size=8, align16
    struct.pack_into('>IIIIIIIIII',data,0x128,1,1,6,0,0x40,len(code+padded),0,0,16,0)
    struct.pack_into('>IIIIIIIIII',data,0x150,7,3,0,0,0x80,len(s),0,0,1,0)
    return bytes(data)

class IntegratedChecks(unittest.TestCase):
    def test_exact_layout(self):
        self.assertEqual(sum(y-x for _,_,x,y in mod.LAYOUT),0x5E3C90-0x5C8770)
        self.assertEqual(sum(sz for _,_,_,sz,_ in mod.FUNCTIONS),420)
    def test_padding_rewrite(self):
        out,e=mod.elf_text_trim_align(synthetic_text(),4)
        self.assertEqual(e['zero_padding_removed'],4)
        self.assertEqual(struct.unpack_from('>I',out,0x128+20)[0],4)
        self.assertEqual(struct.unpack_from('>I',out,0x128+32)[0],4)
    def test_reject_nonzero_padding(self):
        with self.assertRaisesRegex(ValueError,'nonzero'):
            mod.elf_text_trim_align(synthetic_text(padded=b'\x01\x00\x00\x00'),4)
    def test_reject_bad_elf(self):
        with self.assertRaises(ValueError):mod.elf_text_trim_align(b'',4)
    def test_fail_closed_source_anchor(self):
        with self.assertRaises(ValueError):mod.fail_same('unknown','missing','new')
        self.assertEqual(mod.fail_same('foo\n', 'foo','bar'),'bar\n')
    def test_source_hashes_are_pinned(self):
        self.assertTrue(all(len(f[-1])==64 for f in mod.FUNCTIONS))

if __name__=='__main__':unittest.main()
