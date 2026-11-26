"""ROM-free tests for quirk-indexed task-packet generation and escalation caps."""
from __future__ import annotations

import json
import unittest

from decomp import task_packet as tp


class TaskPacketTests(unittest.TestCase):
    def test_quirks_index_parses_live_ledger(self):
        idx = tp.parse_quirks_index()
        self.assertGreater(len(idx), 15)
        self.assertTrue(all(sec["title"] and sec["excerpt"] for sec in idx))

    def test_relevant_quirks_compact_and_targeted(self):
        quirks = tp.select_relevant_quirks("lwc1 $f0, 0($a0)\nadd.s $f2, $f0, $f4\nswc1 $f2, 0($a0)")
        self.assertTrue(1 <= len(quirks) <= 2)
        total_chars = sum(len(q["title"]) + len(q["excerpt"]) for q in quirks)
        self.assertLessEqual(total_chars, 2000)

    def test_packet_stays_compact_and_assigns_tier(self):
        pkt = tp.build_task_packet(
            region="usa",
            name="func_80001000_1C00",
            rom_offset=0x1C00,
            vma=0x80001000,
            size=48,
            owner="main.s",
            asm_text="glabel func_80001000_1C00\n  jr $ra\n  nop\n",
            m2c_draft="void func_80001000_1C00(void) {}\n",
            first_mismatch="word 2: expected addiu $v0,$zero,1 got ori $v0,$zero,1",
            diff_words=2,
            flags=["-O2", "-mips2"],
        )
        encoded = json.dumps(pkt)
        self.assertLess(len(encoded), 8192)
        self.assertEqual(pkt["recommended_tier"], "executor_fast")
        self.assertEqual(pkt["attempt_budget"]["max_attempts"], 3)

        hard_pkt = tp.build_task_packet(
            region="japan_0",
            name="func_80002000_2C00",
            rom_offset=0x2C00,
            vma=0x80002000,
            size=400,
            owner="main.s",
            asm_text="jr $t0\n",
            m2c_draft="void func_80002000_2C00(void) {}\n",
            first_mismatch="jump table mismatch",
            diff_words=15,
            flags=["-O2", "-mips2"],
        )
        self.assertEqual(hard_pkt["recommended_tier"], "architect_frontier")

    def test_escalation_ceiling(self):
        self.assertFalse(tp.should_escalate([5]))
        self.assertFalse(tp.should_escalate([5, 3]))
        self.assertFalse(tp.should_escalate([5, 3, 1]))
        self.assertTrue(tp.should_escalate([5, 5, 5]))
        self.assertTrue(tp.should_escalate([5, 3, 3, 3]))


if __name__ == "__main__":
    unittest.main()
