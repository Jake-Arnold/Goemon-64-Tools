"""Quirk-indexed minimal task-packet builder for Orchestrator/Executor runs.

Distills target metadata, disassembly, m2c draft, first mismatch, and only the
1-2 relevant snippets from decomp/COMPILER_QUIRKS.md into a 4-8 KB JSON packet
with a strict attempt_ledger ceiling so cheap executors never drag 75-965 KB of
history/prose into every compile loop.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
QUIRKS_PATH = ROOT / "COMPILER_QUIRKS.md"

# Keyword buckets mapping MIPS/mismatch patterns to relevant quirk topics.
TOPIC_KEYWORDS: dict[str, tuple[str, ...]] = {
    "float": ("float", "f32", "f64", "lwc1", "swc1", "mtc1", "mfc1", "cvt.", "add.s", "mul.s", "sub.s", "div.s", "c.lt.s", "c.eq.s", "bc1", "pool", "literal"),
    "jump_table": ("jr ", "jtbl", "rodata", "jump-table", "switch", "case "),
    "abs_metadata": ("abs", "notype", "object", "st_info", "d_3", "0x3a", "0x3b", "relocation"),
    "loop_schedule": ("loop", "increment", "pointer", "countdown", "bne", "bltz", "bgtz", "bnez", "register", "scheduling"),
    "mask_cast": ("andi", "0xffff", "0xff", "mask", "unsigned", "u8", "u16", "s16", "cast", "sign"),
    "padding_size": ("nop", "padding", "endlabel", "size", "global_asm", "alignment"),
    "line_order": ("source-line", "initializer", "order", "prologue", "copy", "struct"),
    "sdk_flags": ("-o1", "-g3", "libultra", "os", "al", "gu", "sdk"),
}


def parse_quirks_index(quirks_path: Path = QUIRKS_PATH) -> list[dict]:
    """Parse COMPILER_QUIRKS.md into compact indexed sections."""
    text = quirks_path.read_text(encoding="utf-8")
    sections: list[dict] = []
    current_title: str | None = None
    buf: list[str] = []

    def flush() -> None:
        if current_title is None:
            return
        body = "\n".join(buf).strip()
        if not body or current_title.startswith("Entry template"):
            return
        lower = (current_title + "\n" + body).lower()
        tags = sorted(topic for topic, kws in TOPIC_KEYWORDS.items() if any(kw in lower for kw in kws))
        sections.append({
            "title": current_title,
            "tags": tags,
            "excerpt": body[:700] + ("..." if len(body) > 700 else ""),
        })

    for line in text.splitlines():
        m = re.match(r"^#{2,3}\s+(.+)$", line)
        if m:
            flush()
            current_title = m.group(1).strip()
            buf = []
        elif current_title is not None:
            buf.append(line)
    flush()
    return sections


def select_relevant_quirks(
    asm_text: str,
    first_mismatch: str = "",
    *,
    quirks_path: Path = QUIRKS_PATH,
    max_snippets: int = 2,
    max_chars: int = 1600,
) -> list[dict]:
    """Select only the top 1-2 relevant quirk snippets for a target function."""
    sections = parse_quirks_index(quirks_path)
    probe = (asm_text + "\n" + first_mismatch).lower()
    active_tags = {topic for topic, kws in TOPIC_KEYWORDS.items() if any(kw in probe for kw in kws)}
    if not active_tags:
        return []
    scored = []
    for sec in sections:
        overlap = len(active_tags & set(sec["tags"]))
        if overlap:
            # Prefer verified/concrete entries over generic headers
            bonus = 1 if ("verified" in sec["title"].lower() or "quirk" in sec["title"].lower()) else 0
            scored.append((overlap, bonus, sec))
    scored.sort(key=lambda item: (item[0], item[1]), reverse=True)
    chosen: list[dict] = []
    used_chars = 0
    for _, _, sec in scored:
        if len(chosen) >= max_snippets:
            break
        cost = len(sec["title"]) + len(sec["excerpt"])
        if used_chars + cost > max_chars and chosen:
            break
        chosen.append(sec)
        used_chars += cost
    return chosen


def should_escalate(attempt_scores: list[int], max_non_improving: int = 3) -> bool:
    """Return True when a worker hits max_non_improving attempts without reducing diff count."""
    if len(attempt_scores) < max_non_improving:
        return False
    best = attempt_scores[0]
    stale = 0
    for score in attempt_scores[1:]:
        if score < best:
            best = score
            stale = 0
        else:
            stale += 1
            if stale >= max_non_improving - 1:
                return True
    return len(attempt_scores) >= max_non_improving and best == attempt_scores[0]


def build_task_packet(
    *,
    region: str,
    name: str,
    rom_offset: int,
    vma: int,
    size: int,
    owner: str,
    asm_text: str,
    m2c_draft: str,
    first_mismatch: str,
    diff_words: int,
    flags: list[str],
    quirks_path: Path = QUIRKS_PATH,
    max_attempts: int = 3,
) -> dict:
    """Build a compact 4-8 KB JSON task packet for a fast executor."""
    ledger_sha = hashlib.sha256(quirks_path.read_bytes()).hexdigest()
    quirks = select_relevant_quirks(asm_text, first_mismatch, quirks_path=quirks_path)
    tier = "executor_fast" if diff_words <= 6 and size <= 256 else "architect_frontier"
    return {
        "format": "goemon-executor-task-packet-v1",
        "recommended_tier": tier,
        "region": region,
        "name": name,
        "rom_offset": f"0x{rom_offset:X}",
        "vma": f"0x{vma:08X}",
        "original_bytes": size,
        "owner": owner,
        "flags": flags,
        "ledger_sha256": ledger_sha,
        "diff_words": diff_words,
        "first_mismatch": first_mismatch,
        "attempt_budget": {
            "max_attempts": max_attempts,
            "escalate_after_non_improving": max_attempts,
            "required_outcome_tags": [
                "EXISTING_QUIRK_REPRODUCED",
                "EXISTING_QUIRK_NOT_APPLICABLE",
                "NEW_REPRODUCIBLE_QUIRK",
                "NO_NEW_COMPILER_FINDING",
            ],
        },
        "relevant_quirks": quirks,
        "asm": asm_text,
        "m2c_draft": m2c_draft,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--index", action="store_true", help="Print summary of parsed COMPILER_QUIRKS index")
    parser.add_argument("--query", default="", help="Select relevant quirks for a snippet/keyword")
    args = parser.parse_args()
    if args.index:
        idx = parse_quirks_index()
        print(json.dumps({"quirk_sections": len(idx), "topics": sorted(TOPIC_KEYWORDS)}, indent=2))
    else:
        print(json.dumps(select_relevant_quirks(args.query), indent=2))


if __name__ == "__main__":
    main()
