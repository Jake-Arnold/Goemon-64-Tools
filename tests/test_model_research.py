"""ROM-free deterministic geometry decoder tests; no game memory or N64 GPU."""
import struct
import unittest
from practice.model_research import decode_geometry, extract_rom_probe


def putcmd(data, off, op, payload, operand):
    struct.pack_into('>II', data, off, (op << 24) | payload, operand)


def triangle_word(a,b,c):
    return (a << 17) | (b << 9) | (c << 1)


def mesh_fixture():
    data=bytearray(0x200)
    for i,xyz in enumerate(((0,0,0),(100,0,0),(0,100,0))):
        struct.pack_into('>hhhHhhBBBB', data, 0x80+i*16,*xyz,0,0,0,40+i*10,80,120,255)
    putcmd(data,0,4,(3<<10)|0x2F,0x08000080)  # G_VTX n3/v0 0
    putcmd(data,8,0xBF,0,triangle_word(0,1,2))
    putcmd(data,16,0xB8,0,0)
    return data


class GeometryTests(unittest.TestCase):
    def test_rt64_f3dex_tri1_end_vertex_colors(self):
        data=mesh_fixture()
        mesh=decode_geometry(data,0,24)
        self.assertEqual(mesh.triangle_count,1)
        self.assertTrue(mesh.ended)
        self.assertEqual(mesh.commands,3)
        self.assertEqual(mesh.vertex_loads,1)
        self.assertEqual(mesh.bounds,((0,0,0),(100,100,0)))
        self.assertEqual(mesh.rgb[0],(50,80,120))
        self.assertEqual(mesh.triangles[0],((0,0,0),(100,0,0),(0,100,0)))

    def test_tri2_preserves_nonzero_vertex_slot_and_dl_return(self):
        data=mesh_fixture()
        putcmd(data,0,4,(1<<17)|(3<<10)|0x2F,0x08000080)
        putcmd(data,8,6,0,0x08000030)       # push child and resume
        putcmd(data,16,0xBF,0,triangle_word(1,2,3))
        putcmd(data,24,0xB8,0,0)
        putcmd(data,0x30,0xB1,triangle_word(1,2,3),triangle_word(3,2,1))
        putcmd(data,0x38,0xB8,0,0)
        mesh=decode_geometry(data,0,32)
        self.assertEqual(mesh.triangle_count,3)
        self.assertEqual(mesh.commands,6)
        self.assertEqual(mesh.vertex_loads,1)
        self.assertTrue(mesh.ended)

    def test_rejects_malformed_spans_and_pointer_regions(self):
        data=mesh_fixture()
        for start,end in ((0,0),(-8,24),(0,17),(4,24),(0,2048)):
            with self.subTest(start=start,end=end):
                with self.assertRaises(ValueError):decode_geometry(data,start,end)
        putcmd(data,0,4,(3<<10)|0x2F,0x09000080)
        with self.assertRaisesRegex(ValueError,'segment-08'):decode_geometry(data,0,24)
        putcmd(data,0,4,(40<<10)|0x2F,0x08000080)
        with self.assertRaisesRegex(ValueError,'vertex load'):decode_geometry(data,0,24)

    def test_fails_closed_on_cycles_and_budgets(self):
        data=mesh_fixture()
        putcmd(data,0,6,1<<16,0x08000000)  # no-push branch to self
        with self.assertRaisesRegex(ValueError,'command budget'):decode_geometry(data,0,24,max_commands=12)
        data=mesh_fixture()
        with self.assertRaisesRegex(ValueError,'triangle budget'):decode_geometry(data,0,24,max_faces=0)
        putcmd(data,8,0xB1,triangle_word(0,1,2),triangle_word(1,2,0))
        with self.assertRaisesRegex(ValueError,'Triangle budget'):decode_geometry(data,0,24,max_faces=1)

    def test_unresolved_triangles_and_incomplete_span_are_labelled(self):
        data=mesh_fixture()
        putcmd(data,8,0xBF,0,triangle_word(0,1,20))
        mesh=decode_geometry(data,0,16)
        self.assertEqual(mesh.triangle_count,0)
        self.assertFalse(mesh.ended)
        self.assertTrue(any('not loaded' in warning for warning in mesh.warnings))
        self.assertTrue(any('without G_ENDDL' in warning for warning in mesh.warnings))

    def test_unknown_region_and_file_id(self):
        with self.assertRaisesRegex(ValueError,'Unsupported region'):extract_rom_probe(b'bad','japan_1',141,0,16)
        with self.assertRaises(ValueError):decode_geometry(bytearray(16),0,16,max_depth=0)


if __name__=='__main__':unittest.main()
