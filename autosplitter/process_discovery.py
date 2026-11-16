"""Discover a running Goemon64Recompiled or Project64 process.

Standalone game process discovery; not coupled to timing or route integrations.
"""
def find_pid(target="auto"):
    if target not in ("auto", "recomp", "project64"):
        raise ValueError("Unknown connection target")
    try: import psutil
    except ImportError: raise SystemExit("Install psutil: python -m pip install psutil")
    matches = []
    for p in psutil.process_iter(["pid", "name"]):
        name = (p.info["name"] or "").lower()
        recomp = "goemon64recomp" in name
        project64 = name == "project64.exe"
        if ((target in ("auto", "recomp") and recomp) or
                (target in ("auto", "project64") and project64)):
            matches.append(p.info["pid"])
    if len(matches) == 1:
        return matches[0]
    if matches:
        raise RuntimeError(f"Multiple matching game processes: {matches}. Select a target or use --pid.")
    raise RuntimeError("Game process not found; start US Goemon in Goemon64Recomp or Project64, or use --pid")

