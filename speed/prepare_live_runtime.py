"""Prepare the pinned, startup-patched runtime for a live Windows speed toggle.

Use only an isolated checkout; this does not build or replace an executable.
"""
from __future__ import annotations
import argparse
import os
import subprocess
import tempfile
from pathlib import Path
from speed.prepare_runtime import PIN, BEFORE, AFTER, INCLUDE

ROOT = Path(__file__).resolve().parent


def replace_once(text, before, after):
    if text.count(before) != 1:
        raise ValueError('Pinned runtime source layout does not match expected anchor')
    return text.replace(before, after, 1)


def render(timer, events, header):
    timer = replace_once(timer, '#include "goemon_startup_multiplier.h"',
                         '#define GOEMON_HOST_RUNTIME 1\n#include "goemon_live_clock.h"')
    timer = replace_once(timer,
        'const uint32_t speed_multiplier = goemon_speed::startup_multiplier();',
        'static GoemonLiveClock goemon_clock;')
    timer = replace_once(timer, "const uint32_t counter_per_ms = 46'875 * speed_multiplier;",
                         "constexpr uint32_t counter_per_ms = 46'875;")
    timer = replace_once(timer, 'using Action = std::variant<AddTimerAction, RemoveTimerAction>;',
        'struct SpeedChangedAction {};\nusing Action = std::variant<AddTimerAction, RemoveTimerAction, SpeedChangedAction>;')
    timer = replace_once(timer,
        'return start_time + ticks_to_duration(ticks);',
        'return ultramodern::guest_deadline(ticks_to_duration(ticks));')
    timer = replace_once(timer,
        'return duration_to_ticks(std::chrono::high_resolution_clock::now() - start_time);',
        'return duration_to_ticks(std::chrono::microseconds(goemon_clock.now_us()));')
    timer = replace_once(timer, 'void timer_thread(RDRAM_ARG1) {',
        '#include "goemon_speed_channel.inc"\n\nvoid timer_thread(RDRAM_ARG1) {')
    timer = replace_once(timer,
        '''            // Waiting for the timer completed, so send the timer's message to its message queue
            ultramodern::enqueue_external_message''',
        '''            // A speed decrease can make an old host deadline premature.
            if (time_now() < cur_timer->timestamp) { active_timers.insert(cur_timer_); continue; }
            ultramodern::enqueue_external_message''')
    timer = replace_once(timer, '    timer_context.thread.detach();\n}',
        '    timer_context.thread.detach();\n    goemon_start_speed_channel();\n}')
    timer = replace_once(timer, '    return speed_multiplier;\n}',
        '    return static_cast<uint32_t>(goemon_clock.multiplier());\n}')
    timer = replace_once(timer, '    return std::chrono::high_resolution_clock::now() - start_time;\n}',
        '''    return std::chrono::duration_cast<std::chrono::high_resolution_clock::duration>(
        std::chrono::microseconds(goemon_clock.now_us()));
}

std::chrono::high_resolution_clock::time_point ultramodern::guest_deadline(std::chrono::microseconds target) {
    return std::chrono::high_resolution_clock::now() + std::chrono::microseconds(goemon_clock.delay_until_us(target.count()));
}''')
    events = replace_once(events,
        '        auto next = ultramodern::get_start() + (total_vis * 1000000us) / (60 * ultramodern::get_speed_multiplier());',
        '        auto target = (total_vis * 1000000us) / 60;\n        auto next = ultramodern::guest_deadline(target);')
    events = replace_once(events,
        '''        auto time_now = ultramodern::time_since_start();
        // Calculate how many VIs have passed
        uint64_t new_total_vis = (time_now * (60 * ultramodern::get_speed_multiplier()) / 1000ms) + 1;''',
        '''        auto time_now = ultramodern::time_since_start();
        // A rate decrease can make the prior host deadline premature.
        if (time_now < target) continue;
        // Calculate how many VIs have passed in continuous guest time.
        uint64_t new_total_vis = (time_now * 60 / 1000ms) + 1;''')
    header = replace_once(header, 'uint32_t get_speed_multiplier();',
        'uint32_t get_speed_multiplier();\nstd::chrono::high_resolution_clock::time_point guest_deadline(std::chrono::microseconds target);')
    return timer, events, header


def prepare_live_runtime(root: Path):
    root = root.resolve(strict=True)
    def git(*args):
        return subprocess.check_output(['git', '-C', str(root), *args], text=True).replace('\r\n', '\n')
    if git('rev-parse', 'HEAD').strip() != PIN:
        raise ValueError('Runtime checkout is not at the verified commit')
    status = set(git('status', '--porcelain', '--untracked-files=all').splitlines())
    allowed = {' M ultramodern/src/timer.cpp', '?? ultramodern/src/goemon_startup_multiplier.h'}
    if status != allowed:
        raise ValueError('Runtime checkout must contain only the verified startup patch')
    def original(path):
        return git('show', 'HEAD:'+path)
    timer_path = 'ultramodern/src/timer.cpp'
    event_path = 'ultramodern/src/events.cpp'
    header_path = 'ultramodern/include/ultramodern/ultramodern.hpp'
    original_timer = original(timer_path)
    expected_timer = replace_once(original_timer, INCLUDE, INCLUDE+'\n#include "goemon_startup_multiplier.h"')
    expected_timer = replace_once(expected_timer, BEFORE, AFTER)
    expected_timer = replace_once(expected_timer, "constexpr uint32_t counter_per_ms = 46'875 * speed_multiplier;",
                                   "const uint32_t counter_per_ms = 46'875 * speed_multiplier;")
    source_paths = [timer_path, event_path, header_path]
    expected = [expected_timer, original(event_path), original(header_path)]
    for path, data in zip(source_paths, expected):
        if (root/path).read_text(encoding='utf-8') != data:
            raise ValueError(f'Unexpected changes in {path}; use an isolated startup-patched checkout')
    installed = root/'ultramodern/src/goemon_startup_multiplier.h'
    if not installed.is_file() or installed.read_bytes() != (ROOT/'startup_multiplier.h').read_bytes():
        raise ValueError('Missing or altered startup-speed header')
    copied = {'ultramodern/src/goemon_live_clock.h': ROOT/'live_clock.h',
              'ultramodern/src/goemon_virtual_clock.h': ROOT/'virtual_clock.h',
              'ultramodern/src/goemon_speed_channel.inc': ROOT/'runtime_channel.inc'}
    if any((root/name).exists() for name in copied):
        raise ValueError('A live-speed target file already exists')
    rendered = render(*expected)
    staged = [(root/path, data.encode('utf-8')) for path,data in zip(source_paths,rendered)]
    staged += [(root/name, src.read_bytes()) for name,src in copied.items()]
    temporary = []
    original_bytes = {dest: dest.read_bytes() if dest.exists() else None for dest, _ in staged}
    replaced = []
    try:
        for dest, data in staged:
            with tempfile.NamedTemporaryFile(dir=dest.parent, prefix='.goemon-live-', suffix='.tmp', delete=False) as f:
                f.write(data)
                temporary.append((dest, Path(f.name)))
        for dest, temp in temporary:
            os.replace(temp, dest)
            replaced.append(dest)
    except Exception:
        # Restore only paths this operation replaced; keep unrelated files intact.
        for dest in reversed(replaced):
            previous = original_bytes[dest]
            if previous is None:
                dest.unlink(missing_ok=True)
            else:
                with tempfile.NamedTemporaryFile(dir=dest.parent, prefix='.goemon-restore-', suffix='.tmp', delete=False) as f:
                    f.write(previous)
                    restore = Path(f.name)
                try:
                    os.replace(restore, dest)
                finally:
                    restore.unlink(missing_ok=True)
        raise
    finally:
        for _, temp in temporary:
            temp.unlink(missing_ok=True)


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('runtime',type=Path)
    args=parser.parse_args(argv)
    prepare_live_runtime(args.runtime)
    print('Prepared live-speed runtime; rebuild the recomp before use.')

if __name__ == '__main__':
    main()
