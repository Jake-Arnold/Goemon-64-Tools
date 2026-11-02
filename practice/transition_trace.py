"""High-frequency, read-only trace of ORIGINAL in-game area transitions.

No guest memory writes, raw RDRAM dumps or PC host pointer addresses are exported.
Use a normal door/scene transition to capture how the game starts and commits a warp.
"""
from __future__ import annotations
from datetime import datetime, timezone
import threading
import time

BASE = 0x800C7A94
BLOCK_END = 0x800C7E64
FIELDS = (
    ('state', 0x800C7A94, 1),
    ('phase', 0x800C7A9E, 1),
    ('exit_request', 0x800C7A9F, 1),
    ('category_or_submode', 0x800C7AA4, 1),
    ('stage_offset', 0x800C7AB4, 2),
    ('current_map', 0x800C7AB2, 2),
    ('previous_map', 0x800C7ABC, 2),
    ('pending_map', 0x800C7CA0, 2),
    ('menu_entry_pointer', 0x800C7E60, 4),
    ('loading_flag', 0x8015C5D4, 4),
    ('active_character', 0x8015C5DC, 4),
)


def read_transition_sample(ram):
    system = ram.read_guest(BASE, BLOCK_END-BASE)
    live = ram.read_guest(0x8015C5D4, 12)
    if len(system) != BLOCK_END-BASE or len(live) != 12:
        raise OSError('Incomplete guest RAM snapshot')
    result = {}
    for name, address, width in FIELDS:
        if BASE <= address < BLOCK_END:
            raw = system[address-BASE:address-BASE+width]
        else:
            raw = live[address-0x8015C5D4:address-0x8015C5D4+width]
        result[name] = int.from_bytes(raw,'big')
    return result


class TransitionTrace:
    def __init__(self, ram, *, duration=30.0, interval=0.02):
        self.ram=ram
        self.duration=float(duration)
        self.interval=float(interval)
        self.stop_event=threading.Event()
        self.thread=None
        self.events=[]
        self.samples_trace=[]
        self.error=None
        self.start_utc=None
        self.end_utc=None
        self.samples=0
        self._lock=threading.Lock()

    def start(self):
        if self.thread is not None:
            raise RuntimeError('Trace already started')
        self.thread=threading.Thread(target=self._capture,daemon=True,name='N64-transition-trace')
        self.thread.start()

    def _capture(self):
        self.start_utc=datetime.now(timezone.utc).isoformat()
        start=time.monotonic()
        prev=None
        try:
            while not self.stop_event.is_set():
                now=time.monotonic()
                if now-start >= self.duration:
                    break
                values=read_transition_sample(self.ram)
                self.samples += 1
                changes={} if prev is None else {k:[prev[k],v] for k,v in values.items() if prev[k]!=v}
                sample={'elapsed_ms':round((now-start)*1000), 'values':values}
                if changes:
                    sample['changed']=changes
                with self._lock:
                    self.samples_trace.append(sample)
                    if prev is None or changes:
                        self.events.append(sample)
                prev=values
                self.stop_event.wait(self.interval)
        except (OSError,ValueError,RuntimeError) as exc:
            self.error=str(exc)
        finally:
            self.end_utc=datetime.now(timezone.utc).isoformat()

    def stop(self):
        self.stop_event.set()
        if self.thread is not None:
            self.thread.join(timeout=2.0)

    def report(self):
        with self._lock:
            events=list(self.events)
            samples_trace=list(self.samples_trace)
        return {
            'format':'mnsg-usa-in-game-transition-trace-v1',
            'start_utc':self.start_utc,
            'end_utc':self.end_utc,
            'interval_requested_ms':round(self.interval*1000),
            'samples':self.samples,
            'observed_changes':max(0,len(events)-1),
            'error':self.error,
            'fields':{name:f'0x{address:08X}' for name,address,_ in FIELDS},
            'events':events,
            'samples_trace':samples_trace,
            'notes':'READ ONLY. Move through a REAL in-game door during the capture. '
                    'The export now includes every sampled frame in samples_trace, '
                    'plus the compact change-only event list. No game assets or RAM dumps.'
        }
