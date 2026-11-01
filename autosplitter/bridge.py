"""Goemon Any% memory-based LiveSplit bridge.

Usage:
  python -m autosplitter.bridge import-splits community.lss route.json
  python -m autosplitter.bridge monitor --route route.json
  python -m autosplitter.bridge monitor --route route.json --base 0x... --pid 1234
"""
import argparse
import json
import math
import os
import time

from .engine import load_route, make_route, save_route, segment_names, SplitEngine
from .livesplit import LiveSplit
from .memory import Rdram, WindowsProcess, discover_rdram


def find_pid():
    try: import psutil
    except ImportError: raise SystemExit("Install psutil: python -m pip install psutil")
    for p in psutil.process_iter(["pid", "name"]):
        name = (p.info["name"] or "").lower()
        if "goemon64recomp" in name:
            return p.info["pid"]
    raise RuntimeError("Goemon64Recomp process not found; start the US port first, or use --pid")


def monitor(args):
    route = load_route(args.route)
    pid = args.pid or find_pid()
    proc = WindowsProcess(pid)
    try:
        if args.base:
            base, endian = int(args.base, 0), ("wordswapped" if args.endian=="auto" else args.endian)
        else:
            base, endian = discover_rdram(proc, args.endian)
        ram = Rdram(proc, base, endian)
        sample = ram.snapshot()
        if sample["x"] is None or sample["action"] is None:
            raise RuntimeError("No player position / task at validated base; enter gameplay")
        print(f"Connected PID={pid}; RAM base=0x{base:X}; format={endian}; "
              f"initial pos=({sample['x']:.1f}, {sample['y']:.1f}, {sample['z']:.1f})")
        engine = SplitEngine(route)
        ls = LiveSplit(port=args.port)
        last_phase = ""
        verified_index = None
        last_report = 0
        while True:
            snapshot = ram.snapshot()
            try: phase = ls.phase()
            except OSError: phase = "Disconnected"
            running = phase.lower() == "running"
            if running:
                external_index=ls.split_index()
                if external_index != engine.index:
                    engine.align_index(external_index)
                    print(f"LiveSplit moved to segment {external_index+1}; synchronised.")
                if external_index != verified_index and external_index < len(route["segments"]):
                    actual=ls.current_split_name()
                    expected=route["segments"][external_index]["name"]
                    if actual != expected:
                        raise RuntimeError(f"LiveSplit segment {external_index+1} is {actual!r} but route expected {expected!r}. Load the matching .lss file.")
                    verified_index=external_index
            else:
                verified_index=None
            if phase != last_phase:
                print("LiveSplit:",phase)
                # Manual timer reset should rearm route index.
                if phase.lower() == "notrunning": engine.align_index(0)
                last_phase = phase
            result = engine.update(snapshot, running)
            if result:
                try:
                    ls.split()
                    print(f"SPLIT {result.index+1}: {result.name}")
                except OSError as e:
                    print("LiveSplit split failed, stopping to prevent desynchronisation:",e)
                    break
            if time.monotonic()-last_report > args.report:
                print(f"{engine.index}/{len(route['segments'])} | "
                      f"pos=({snapshot['x']}, {snapshot['y']}, {snapshot['z']}) "
                      f"character={snapshot['character']} action={snapshot['action']} "
                      f"loading={snapshot['loading']}")
                last_report = time.monotonic()
            time.sleep(1/max(1,args.hz))
    finally:
        proc.close()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="command",required=True)
    imp = sub.add_parser("import-splits")
    imp.add_argument("lss")
    imp.add_argument("route")
    run = sub.add_parser("monitor")
    run.add_argument("--route",required=True)
    run.add_argument("--pid",type=int)
    run.add_argument("--base",help="RDRAM host base as hex, otherwise attempt invariant scan")
    run.add_argument("--endian", choices=["auto","wordswapped","big"],default="auto")
    run.add_argument("--port",type=int,default=16834)
    run.add_argument("--hz",type=int,default=20)
    run.add_argument("--report",type=float,default=5)
    args=ap.parse_args()
    if args.command=="import-splits":
        names=segment_names(args.lss)
        save_route(make_route(names),args.route)
        print(f"Imported {len(names)} segments. Triggers are deliberately not configured.")
    else:
        monitor(args)

if __name__=="__main__": main()
