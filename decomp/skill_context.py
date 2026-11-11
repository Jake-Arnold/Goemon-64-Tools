"""Compact Goemon task packets from stored plan/proof. Does not run the verifier."""
from __future__ import annotations
import argparse
from collections import Counter
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
TASK_RE = re.compile(r"G64-(\d{3})\Z")


def load(root=ROOT):
    read = lambda p: json.loads(p.read_text(encoding="utf-8"))
    tasks = read(root / "plans" / "TASKS_100.json")["tasks"]
    result = read(root / "results" / "combined.json")
    summary = read(root / "results" / "inventory.json")["summary"]
    c = result["comparison"]
    return {"tasks": tasks, "proof": {
        "status": result.get("status"), "full_rom_match": c.get("full_rom_match"),
        "matched": c.get("matched_functions"), "claimed": c.get("claimed_functions"),
        "bytes": c.get("matched_function_bytes"), "rom_size": c.get("rom_size"),
        "sha1": c.get("candidate_sha1"), "c_total": summary.get("current_unmarked_entries"),
        "asm_total": summary.get("remaining_assembly_entries"),
        "identified": summary.get("identified_function_entries"),
        "new_c": summary.get("newly_matching_c"),
    }}


def validate(data):
    tasks = data["tasks"]
    ids = [t.get("id") for t in tasks]
    errors = []
    if ids != [f"G64-{i:03}" for i in range(1, 101)]:
        errors.append("Task IDs must be exactly G64-001..G64-100")
    for i, task in enumerate(tasks, 1):
        for dep in task.get("depends_on", []):
            match = TASK_RE.fullmatch(dep)
            if dep not in ids or not match or int(match.group(1)) >= i:
                errors.append("Invalid dependency " + str(dep))
    p = data["proof"]
    if p["status"] != "matched" or p["full_rom_match"] is not True:
        errors.append("Recorded ROM proof is not matched")
    if p["matched"] != p["claimed"] or p["claimed"] != p["new_c"]:
        errors.append("Proof/inventory claim counts disagree")
    if p["c_total"] + p["asm_total"] != p["identified"]:
        errors.append("Inventory C/ASM totals disagree")
    if p["rom_size"] != 33554432:
        errors.append("Original-ROM size differs")
    return errors


def task_brief(data, task_id, detail=False):
    entries = {t["id"]: t for t in data["tasks"]}
    if task_id not in entries:
        raise ValueError("Unknown task: " + task_id)
    t = entries[task_id]
    payload = {"task": task_id, "status": t.get("status"),
               "title": t.get("title"), "phase": t.get("phase"),
               "dependencies": [{"id": d, "status": entries[d].get("status")}
                                for d in t.get("depends_on", []) if d in entries],
               "focus_files": t.get("focus_files", []),
               "intent": t.get("architecture_design"),
               "acceptance": t.get("explicit_acceptance"),
               "phase_file": f"decomp/plans/phases/PHASE_{t['phase']:02}.md",
               "stored_proof": data["proof"]}
    if detail:
        payload.update(steps=t.get("implementation_sequence", []),
                       tests=t.get("focused_testing"),
                       negative=t.get("negative_control"),
                       stop=t.get("stop_or_recovery"),
                       evidence=t.get("evidence_requirements", []),
                       optional_rea=t.get("optional_reverse_engineering_assist"))
    return payload


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--task")
    mode.add_argument("--phase", type=int, choices=range(1, 11))
    mode.add_argument("--status", action="store_true")
    mode.add_argument("--validate", action="store_true")
    parser.add_argument("--detail", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    data = load()
    errors = validate(data)
    if errors:
        parser.error("; ".join(errors))
    if args.task:
        result = task_brief(data, args.task, args.detail)
    elif args.phase:
        result = {"phase": args.phase, "tasks": [
            {"task": t["id"], "status": t.get("status"), "title": t.get("title")}
            for t in data["tasks"] if t.get("phase") == args.phase]}
    elif args.status:
        result = {"stored_proof": data["proof"],
                  "statuses": dict(sorted(Counter(t.get("status", "UNKNOWN") for t in data["tasks"]).items())),
                  "first_planned": next((t["id"] for t in data["tasks"] if t.get("status") == "PLANNED"), None),
                  "notice": "Stored reports; no fresh original-ROM build performed"}
    else:
        result = {"status": "CONSISTENT_STORED_REPORTS", "task_count": len(data["tasks"]),
                  "notice": "No new verifier run"}
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif args.task:
        print(f"{result['task']} [{result['status']}] {result['title']}")
        print(f"Phase: {result['phase_file']}")
        if result["dependencies"]:
            print("Deps: " + ", ".join(f"{r['id']}={r['status']}" for r in result["dependencies"]))
        print("Files: " + ", ".join(result["focus_files"]))
        print("Do: " + str(result["intent"]))
        print("Accept: " + str(result["acceptance"]))
        p = result["stored_proof"]
        print(f"STORED proof: {p['matched']}/{p['claimed']} C, {p['bytes']} bytes; C/ASM={p['c_total']}/{p['asm_total']}")
        if args.detail:
            for i, step in enumerate(result["steps"], 1):
                print(f"{i}. {step}")
            print("Tests:", result["tests"])
            print("Stop:", result["stop"])
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
