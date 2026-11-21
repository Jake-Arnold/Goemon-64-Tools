"""Read, validate and checkpoint the curated Goemon task queue (stdlib only).

This is planning metadata, NOT a compiler/ROM/CI acceptance gate.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import sys
from datetime import datetime, timezone

REGISTRY = Path(__file__).resolve().parent / "tasks" / "registry.json"
STATUSES = {"pending", "in_progress", "blocked_external", "blocked_input", "blocked_rebase", "blocked_verification", "done", "superseded"}
ACTIVE = STATUSES - {"done", "superseded"}
WORKSTREAMS = {"japan-glitch", "japan-decomp", "usa-decomp", "cross-region", "maintenance"}
REGIONS = {"japan_0", "usa", "both", "none"}
ID_PATTERN = re.compile(r"^GQ-[A-Z0-9]+-[0-9]{3}$")
SHA_PATTERN = re.compile(r"^[a-f0-9]{40}$")


def read_registry(path: Path = REGISTRY) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path = REGISTRY) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate(data: dict) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["registry root must be an object"]
    if data.get("format") != "goemon-task-registry-v1":
        errors.append("format must be goemon-task-registry-v1")
    if data.get("branch") != "chatgptweb/decomp":
        errors.append("branch must remain chatgptweb/decomp")
    head = data.get("reconciled_head", "")
    if not isinstance(head, str) or not SHA_PATTERN.fullmatch(head):
        errors.append("reconciled_head must be a 40-character SHA")
    tasks = data.get("tasks")
    if not isinstance(tasks, list):
        return errors + ["tasks must be an array"]
    seen = set()
    for index, t in enumerate(tasks):
        ident = t.get("id", "") if isinstance(t, dict) else ""
        prefix = f"tasks[{index}] {ident!r}"
        if not isinstance(t, dict):
            errors.append(f"{prefix}: task must be an object")
            continue
        if not isinstance(ident, str) or not ID_PATTERN.fullmatch(ident):
            errors.append(f"{prefix}: invalid ID")
        if isinstance(ident, str):
            if ident in seen:
                errors.append(f"{prefix}: duplicate ID")
            seen.add(ident)
        for key in ("title", "summary", "proof_tier", "next_step", "acceptance", "last_reviewed"):
            if not isinstance(t.get(key), str) or not t[key].strip():
                errors.append(f"{prefix}: missing {key}")
        for key, valid in (("status", STATUSES), ("workstream", WORKSTREAMS), ("region", REGIONS)):
            value = t.get(key)
            if not isinstance(value, str) or value not in valid:
                errors.append(f"{prefix}: invalid {key}")
        if type(t.get("priority")) is not int or t["priority"] not in (1, 2, 3):
            errors.append(f"{prefix}: priority must be 1, 2 or 3")
        for key in ("requires", "evidence", "conflicts_with", "history"):
            if not isinstance(t.get(key), list):
                errors.append(f"{prefix}: {key} must be an array")
        for ref in t.get("evidence", []) if isinstance(t.get("evidence"), list) else []:
            if not isinstance(ref, str) or not (ref.startswith("https://github.com/Jake-Arnold/Goemon-64-Tools/") or ref.startswith("decomp/")):
                errors.append(f"{prefix}: unsupported evidence reference {ref!r}")
        if t.get("status") == "done" and not t.get("completion_proof"):
            errors.append(f"{prefix}: done requires completion_proof")
        for c in t.get("history", []) if isinstance(t.get("history"), list) else []:
            if not isinstance(c, dict) or not all(k in c for k in ("at", "status", "note")):
                errors.append(f"{prefix}: invalid history checkpoint")
    for t in tasks:
        if not isinstance(t, dict):
            continue
        for c in t.get("conflicts_with", []) if isinstance(t.get("conflicts_with"), list) else []:
            if not isinstance(c, str) or c not in seen or c == t.get("id"):
                errors.append(f"{t.get('id')}: invalid conflict {c!r}")
    return errors


def ordered(data: dict, *, status: str | None = None, region: str | None = None,
            workstream: str | None = None, all_tasks: bool = False) -> list[dict]:
    tasks = [t for t in data["tasks"] if all_tasks or status is not None or t["status"] in ACTIVE]
    if status:
        tasks = [t for t in tasks if t["status"] == status]
    if region:
        tasks = [t for t in tasks if t["region"] in (region, "both")]
    if workstream:
        tasks = [t for t in tasks if t["workstream"] == workstream]
    return sorted(tasks, key=lambda t: (t["priority"], t["id"]))


def get_task(data: dict, ident: str) -> dict:
    for t in data["tasks"]:
        if t["id"] == ident:
            return t
    raise ValueError(f"Unknown task {ident}")


def write_checkpoint(path: Path, data: dict, task_id: str, *, status: str, note: str,
                     next_step: str | None, evidence: list[str], expected: str) -> str:
    if not re.fullmatch(r"[a-f0-9]{64}", expected):
        raise ValueError("checkpoint requires --expected-sha256 from fingerprint")
    if digest(path) != expected:
        raise ValueError("registry changed since fingerprint; re-read and reconcile")
    if status not in STATUSES:
        raise ValueError(f"invalid status: {status}")
    if not note.strip():
        raise ValueError("checkpoint note is mandatory")
    t = get_task(data, task_id)
    if status == "done":
        raise ValueError("done requires reviewed acceptance proof and an agent-edited completion_proof; no CLI auto-promotion")
    if t["status"] == "done" and status != "done":
        raise ValueError("completed task cannot be silently reopened")
    for url in evidence:
        if not url.startswith("https://github.com/Jake-Arnold/Goemon-64-Tools/"):
            raise ValueError("checkpoint evidence must be a repository GitHub URL")
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    t["status"] = status
    if next_step:
        t["next_step"] = next_step
    for url in evidence:
        if url not in t["evidence"]:
            t["evidence"].append(url)
    t["history"].append({"at": now, "status": status, "note": note, "evidence": evidence})
    if validate(data):
        raise ValueError("checkpoint would invalidate registry: " + "; ".join(validate(data)))
    # Recheck before replace; updates must still be committed and reviewed in Git.
    if digest(path) != expected:
        raise ValueError("registry changed during checkpoint; abort")
    candidate = path.with_name(path.name + ".tmp")
    try:
        candidate.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        os.replace(candidate, path)
    finally:
        candidate.unlink(missing_ok=True)
    return now


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, default=REGISTRY, help=argparse.SUPPRESS)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("validate", help="Validate registry schema, links, IDs and conflicts")
    sub.add_parser("fingerprint", help="Print sha256 for guarded checkpoint updates")
    listing = sub.add_parser("list", help="List pending and blocked tasks (default excludes done)")
    listing.add_argument("--all", action="store_true")
    listing.add_argument("--status", choices=sorted(STATUSES))
    listing.add_argument("--region", choices=("usa", "japan_0"))
    listing.add_argument("--workstream", choices=sorted(WORKSTREAMS))
    listing.add_argument("--json", action="store_true")
    for name in ("show", "resume"):
        p = sub.add_parser(name, help=("Show full task record" if name == "show" else "Print a safe task-execution handoff"))
        p.add_argument("id")
    cp = sub.add_parser("checkpoint", help="Write a guarded, evidence-preserving progress note (not a Git commit)")
    cp.add_argument("id")
    cp.add_argument("--status", required=True, choices=sorted(STATUSES))
    cp.add_argument("--note", required=True)
    cp.add_argument("--next-step")
    cp.add_argument("--evidence", action="append", default=[])
    cp.add_argument("--expected-sha256", required=True)
    args = parser.parse_args(argv)
    try:
        data = read_registry(args.registry)
        errors = validate(data)
        if errors:
            for e in errors:
                print("INVALID: " + e, file=sys.stderr)
            return 2
        if args.command == "validate":
            print(f"VALID: {len(data['tasks'])} tasks, source HEAD {data['reconciled_head']}")
            return 0
        if args.command == "fingerprint":
            print(digest(args.registry))
            return 0
        if args.command == "list":
            tasks = ordered(data, status=args.status, region=args.region,
                            workstream=args.workstream, all_tasks=args.all)
            if args.json:
                print(json.dumps(tasks, indent=2))
            else:
                for t in tasks:
                    print(f"{t['id']:19} P{t['priority']} {t['status']:20} {t['region']:8} {t['title']}")
                print(f"{len(tasks)} task(s); branch={data['branch']} last_reconciled={data['reconciled_head'][:12]}")
            return 0
        if args.command in ("show", "resume"):
            t = get_task(data, args.id)
            if args.command == "show":
                print(json.dumps(t, indent=2))
                return 0
            print(f"TASK {t['id']} — {t['title']}\nStatus: {t['status']} ({t['proof_tier']})")
            print(f"Summary: {t['summary']}\nNeeds: {', '.join(t['requires']) or 'none'}")
            print(f"Next: {t['next_step']}\nAcceptance: {t['acceptance']}")
            print(f"Potential conflicts: {', '.join(t['conflicts_with']) or 'none explicitly listed'}")
            print("Evidence: " + ", ".join(t["evidence"]))
            print("HANDOFF: Re-fetch the current chatgptweb/decomp HEAD and open PRs/issues; dedupe original function offsets and overlapping promotion owners before edits. Do not infer acceptance from the registry or historical reports.")
            if t["status"].startswith("blocked_"):
                print("BLOCKED: Perform only independent research and evidence preparation until prerequisites are met. Do not invent live results.")
            print("For C promotion: native original-address IDO+complete ROM, ELF/relocation, strict inventory and full local_ci must pass; update PROGRESS.md in same commit and verify GitHub ref.")
            return 0
        if args.command == "checkpoint":
            now = write_checkpoint(args.registry, data, args.id, status=args.status, note=args.note,
                                   next_step=args.next_step, evidence=args.evidence,
                                   expected=args.expected_sha256)
            print(f"CHECKPOINT WRITTEN {args.id} at {now}. Commit registry.json + PROGRESS.md together; no remote push or verification occurred.")
            return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 1


if __name__ == "__main__":
    raise SystemExit(main())