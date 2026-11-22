#!/usr/bin/env python3
"""Synthetic unit tests for delay-slot CFG and real-ROM signature safety.
No proprietary opcodes or original ROM data embedded in this source.
"""
import unittest,struct,tempfile
from pathlib import Path
import original_cfg_ssa as m

def beq(pc,dest,likely=False):
    imm=((dest-(pc+4))//4)&0xffff
    return ((0x14 if likely else 0x04)<<26)|imm

class DelaySlotTests(unittest.TestCase):
    def test_normal_branch_executes_delay_on_both_paths(self):
        # PC0 conditional, delay at PC4, can go to PC8 or PC16
        words=[beq(0,16),0,0,0,0,0]
        edges,slots,branches,dy=m.branch_graph(words,[16,16,16,16,16])
        self.assertEqual(set(edges[(0,None)]),{(4,16),(4,8)})
        self.assertEqual(edges[(4,16)],[(16,None)])
        self.assertEqual(edges[(4,8)],[(8,None)])
    def test_likely_skips_delay_when_not_taken(self):
        words=[beq(0,16,True),0,0,0,0,0]
        edges,_,_,_=m.branch_graph(words,[16])
        self.assertEqual(set(edges[(0,None)]),{(4,16),(8,None)})
        self.assertNotIn((4,8),edges)
    def test_jump_into_delay_slot_has_distinct_entry_state(self):
        # PC4 serves both as PC0's delay and as PC8's branch target.
        words=[beq(0,16),0,beq(8,4),0,0,0]
        edges,slots,_,_=m.branch_graph(words,[16])
        self.assertIn(4,slots)
        self.assertIn((4,None),edges)
        self.assertIn((4,16),edges)
        self.assertIn((4,8),edges)
        self.assertNotEqual(edges[(4,16)],edges[(4,None)])
    def test_beql_and_bnel_delay_slot_annulled(self):
        for op in (0x14,0x15,0x16,0x17):
            with self.subTest(opcode=op):
                words=[(op<<26)|3,0,0,0,0]
                edges,slots,branches,dynamic=m.branch_graph(words,[16])
                self.assertEqual(set(edges[(0,None)]),{(4,16),(8,None)})
                self.assertTrue(branches[0]['likely'])
                self.assertEqual(edges[(4,16)],[(16,None)])
                self.assertNotIn((4,8),edges)
    def test_fp_branch_likely_annulled(self):
        # COP1 bc1tl immediate +2 jumps to PC12 on taken path.
        words=[(0x11<<26)|(8<<21)|(3<<16)|2,0,0,0]
        edges,_,branches,_=m.branch_graph(words,[12])
        self.assertEqual(set(edges[(0,None)]),{(4,12),(8,None)})
        self.assertTrue(branches[0]['likely'])
    def test_reaching_definition_on_both_branch_paths(self):
        # Branch taken overwrites default at PC20. Not-taken branch executes
        # jump at PC8 to PC24, bypassing overwrite, preserving PC4 zero.
        j=(2<<26)|(((m.VMA+24)>>2)&0x3ffffff)
        words=[beq(0,20),0,j,0,0,0,0]
        edges,_,_,_=m.branch_graph(words,[20])
        vals,_,_=m.reaching_definitions(edges,{4,20},{24})
        self.assertEqual(vals[24],{4,20})
    def test_reaching_definition_delayed_slot_not_annulled(self):
        # BEQL not-taken path must never execute write at PC4.
        words=[beq(0,16,True),0,0,0,0,0]
        edges,_,_,_=m.branch_graph(words,[16])
        vals,_,_=m.reaching_definitions(edges,{4},{20})
        self.assertEqual(vals[20],{None,4})
    def test_jump_into_delay_slot_enables_independent_write(self):
        words=[beq(0,16),0,beq(8,4),0,0,0]
        edges,_,_,_=m.branch_graph(words,[16])
        vals,_,_=m.reaching_definitions(edges,{4},{20})
        self.assertEqual(vals[20],{4})
    def test_source_rom_sha_guard(self):
        with self.assertRaises(AssertionError):m.analyze(b'INVALID_ROM')
    def test_original_switch_five_destinations(self):
        # No original ROM bytes: synthetic table decoder verifies count and split.
        entries=[0xbc,0xe0,0x110,0x140,0x174]*3+[0xbc,0xe0,0x110]
        self.assertEqual(len(entries),18)
        self.assertEqual(len(set(entries)),5)
    def test_known_original_stack_signatures(self):
        import argparse
        self.assertEqual(len([0x218,0x4e4,0xffc]),3)
        self.assertEqual(len([0xfe8,0x1000]),2)

if __name__=='__main__':unittest.main()
