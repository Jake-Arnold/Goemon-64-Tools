"""Tag-first SHA-leased cleanup of pinned historical branch refs; fail closed."""
import json
import os
from pathlib import Path
import subprocess
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import Request, urlopen

BASE = "https://api.github.com/repos/Jake-Arnold/Goemon-64-Tools/"
ALLOWED = {"PROGRESS.md", ".github/workflows/goemon-retire-archived-research.yml",
           "scripts/retire_legacy_branches.py",
           "decomp/research/branch_archive/RETIREMENT_BATCH_20261119.json",
           "decomp/research/branch_archive/REVIEW_20261119.md"}

def need(ok, reason):
    if not ok:
        raise RuntimeError("RETIREMENT REFUSED: " + reason)

def api(path, data=None, absent=False):
    payload = json.dumps(data).encode() if data is not None else None
    req = Request(BASE + path, data=payload,
                  method="POST" if payload is not None else "GET",
                  headers={"Authorization": "Bearer " + os.environ["GH_TOKEN"],
                           "Accept": "application/vnd.github+json",
                           "Content-Type": "application/json"})
    try:
        with urlopen(req, timeout=40) as res:
            return json.load(res)
    except HTTPError as exc:
        if absent and exc.code == 404:
            return None
        raise

def ref(kind, name):
    obj = api("git/ref/" + kind + "/" + quote(name, safe="/"), absent=True)
    return obj["object"]["sha"] if obj else None

def ancestor(older, newer):
    return api("compare/" + older + "..." + newer).get("status") in ("identical", "ahead")

def open_heads(repo):
    result = set()
    for page in range(1, 22):
        rows = api("pulls?state=open&per_page=100&page=" + str(page))
        for row in rows:
            h = row.get("head") or {}
            if (h.get("repo") or {}).get("full_name") == repo:
                result.add(h.get("ref"))
        if len(rows) < 100:
            return result
    need(False, "open PR list truncated")

def execute():
    repo = os.environ.get("GITHUB_REPOSITORY")
    need(repo == "Jake-Arnold/Goemon-64-Tools", "repository mismatch")
    event = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text())
    p = event.get("pull_request") or {}
    h = p.get("head") or {}
    trigger = "ops/retire-legacy-branches-20261119"
    if event.get("action") != "closed" or not p.get("merged") or h.get("ref") != trigger:
        print("Not the dedicated merged retirement PR; skip")
        return
    plan = json.loads(Path("decomp/research/branch_archive/RETIREMENT_BATCH_20261119.json").read_text())
    need(plan["format"] == "goemon-legacy-retirement-v1" and plan["repo"] == repo
         and plan["base"] == "chatgptweb/decomp" and plan["trigger"] == trigger,
         "invalid plan")
    need((p.get("base") or {}).get("ref") == plan["base"]
         and (h.get("repo") or {}).get("full_name") == repo, "wrong PR base/repo")
    pr_number = p["number"]
    latest = api("pulls/" + str(pr_number))
    merge = latest.get("merge_commit_sha")
    need(latest.get("merged_at") and merge == p.get("merge_commit_sha")
         and (latest.get("head") or {}).get("sha") == h.get("sha"), "PR merge identity changed")
    changed = set()
    for page in range(1, 22):
        rows = api("pulls/" + str(pr_number) + "/files?per_page=100&page=" + str(page))
        changed.update(x["filename"] for x in rows)
        if len(rows) < 100:
            break
    else:
        need(False, "PR files truncated")
    need(changed == ALLOWED, "unexpected retirement PR changes")
    current = ref("heads", plan["base"])
    need(current and ancestor(merge, current), "merge absent from current canon")
    fixed = plan["branches"]
    need(len(fixed) == 25 and set(fixed) == set(plan["anchors"]) | set(plan["merged_prs"]),
         "incomplete 25-branch manifest")
    need(not set(fixed) & set(plan["excluded"]), "protected ref in plan")
    active = open_heads(repo)
    need(not (set(fixed) | {trigger}) & active, "branch has open PR")
    for num in set(plan["merged_prs"].values()):
        old = api("pulls/" + str(num))
        need(old.get("merged_at") and old.get("merge_commit_sha")
             and (old.get("base") or {}).get("ref") == plan["base"]
             and ancestor(old["merge_commit_sha"], current), "unmerged evidence PR #" + str(num))
    for name, proof in plan["anchors"].items():
        for branch in (name, proof["target"]):
            r = api("contents/" + quote(proof["path"], safe="/") + "?ref=" + quote(branch, safe=""))
            need(r.get("sha") == proof["sha"], "research SHA mismatch: " + name)
    refs = dict(fixed)
    refs[trigger] = h["sha"]
    for name, expected in refs.items():
        need(name not in plan["excluded"] and name not in active, "unsafe source ref")
        current_sha = ref("heads", name)
        saved_sha = ref("tags", plan["tag_prefix"] + name)
        need(current_sha in (None, expected) and saved_sha in (None, expected),
             "moved branch/tag: " + name)
        need(current_sha is not None or saved_sha == expected,
             "missing unarchived branch: " + name)
    # Create and verify every lightweight archival tag BEFORE deleting any branch.
    for name, expected in refs.items():
        tag = plan["tag_prefix"] + name
        if ref("tags", tag) is None:
            api("git/refs", {"ref": "refs/tags/" + tag, "sha": expected})
        need(ref("tags", tag) == expected, "tag creation not verified: " + name)
    for name, expected in refs.items():
        actual = ref("heads", name)
        if actual is None:
            continue
        need(actual == expected, "branch advanced after preflight: " + name)
        subprocess.run(["git", "push", "--force-with-lease=refs/heads/" + name +
                        ":" + expected, "origin", ":refs/heads/" + name], check=True)
        need(ref("heads", name) is None, "deletion not verified: " + name)
        print("Retired:", name)

if __name__ == "__main__":
    execute()
