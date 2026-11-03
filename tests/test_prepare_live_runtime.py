import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from speed.prepare_runtime import PIN, BEFORE, AFTER, INCLUDE
from speed.prepare_live_runtime import prepare_live_runtime, render

TIMER = '''#include "ultramodern/ultra64.h"
constexpr uint32_t speed_multiplier = 1;
constexpr uint32_t counter_per_ms = 46'875 * speed_multiplier;
using Action = std::variant<AddTimerAction, RemoveTimerAction>;
return start_time + ticks_to_duration(ticks);
return duration_to_ticks(std::chrono::high_resolution_clock::now() - start_time);
void timer_thread(RDRAM_ARG1) {
            // Waiting for the timer completed, so send the timer's message to its message queue
            ultramodern::enqueue_external_message
    timer_context.thread.detach();
}
    return speed_multiplier;
}
    return std::chrono::high_resolution_clock::now() - start_time;
}
'''
EVENTS = '''        auto next = ultramodern::get_start() + (total_vis * 1000000us) / (60 * ultramodern::get_speed_multiplier());
        auto time_now = ultramodern::time_since_start();
        // Calculate how many VIs have passed
        uint64_t new_total_vis = (time_now * (60 * ultramodern::get_speed_multiplier()) / 1000ms) + 1;
'''
HEADER = 'uint32_t get_speed_multiplier();\n'
PATHS = ('ultramodern/src/timer.cpp','ultramodern/src/events.cpp',
         'ultramodern/include/ultramodern/ultramodern.hpp')

class PrepareLiveRuntimeTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        self.originals=dict(zip(PATHS,(TIMER,EVENTS,HEADER)))
        startup=TIMER.replace(INCLUDE,INCLUDE+'\n#include "goemon_startup_multiplier.h"').replace(BEFORE,AFTER).replace(
            "constexpr uint32_t counter_per_ms = 46'875 * speed_multiplier;",
            "const uint32_t counter_per_ms = 46'875 * speed_multiplier;")
        self.expected=dict(zip(PATHS,(startup,EVENTS,HEADER)))
        for name,data in self.expected.items():
            path=self.root/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(data,encoding='utf-8')
        header=self.root/'ultramodern/src/goemon_startup_multiplier.h'
        header.write_bytes((Path(__file__).resolve().parents[1]/'speed/startup_multiplier.h').read_bytes())
    def git_output(self, cmd, **kwargs):
        if cmd[-2:]==['rev-parse','HEAD']:return PIN+'\n'
        if 'status' in cmd:return ' M ultramodern/src/timer.cpp\n?? ultramodern/src/goemon_startup_multiplier.h\n'
        if 'show' in cmd:return self.originals[cmd[-1][5:]]
        raise AssertionError(cmd)
    def test_applies_all_timing_and_wakeup_changes(self):
        with patch('speed.prepare_live_runtime.subprocess.check_output',side_effect=self.git_output):
            prepare_live_runtime(self.root)
        timer=(self.root/PATHS[0]).read_text(encoding='utf-8')
        events=(self.root/PATHS[1]).read_text(encoding='utf-8')
        self.assertIn('SpeedChangedAction',timer)
        self.assertIn('time_now() < cur_timer->timestamp',timer)
        self.assertIn('goemon_start_speed_channel()',timer)
        self.assertIn('if (time_now < target) continue;',events)
        self.assertTrue((self.root/'ultramodern/src/goemon_speed_channel.inc').is_file())
    def test_refuses_dirty_or_unexpected_source_without_changes(self):
        with patch('speed.prepare_live_runtime.subprocess.check_output',side_effect=lambda cmd,**kw: PIN+'\n' if 'rev-parse' in cmd else ' M other.cpp\n'):
            with self.assertRaises(ValueError):prepare_live_runtime(self.root)
        self.assertEqual((self.root/PATHS[0]).read_text(encoding='utf-8'),self.expected[PATHS[0]])
        with self.assertRaises(ValueError):render('unexpected',EVENTS,HEADER)
    def test_failure_rolls_back_replaced_sources(self):
        import os
        real_replace=os.replace;calls=0
        def fail_second(a,b):
            nonlocal calls
            calls+=1
            if calls==2:raise OSError('simulated failure')
            return real_replace(a,b)
        with patch('speed.prepare_live_runtime.subprocess.check_output',side_effect=self.git_output), patch('speed.prepare_live_runtime.os.replace',side_effect=fail_second):
            with self.assertRaises(OSError):prepare_live_runtime(self.root)
        for name,data in self.expected.items():self.assertEqual((self.root/name).read_text(encoding='utf-8'),data)
        self.assertFalse((self.root/'ultramodern/src/goemon_live_clock.h').exists())
