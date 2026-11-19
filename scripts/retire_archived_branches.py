"""SHA-leased cleanup for merged, allowlisted historical archive PRs only."""
import json
import os
from pathlib import Path
import subprocess
import urllib.error
import urllib.parse
import urllib.request

REPO = "Jake-Arnold/Goemon-64-Tools"
BASE = "chatgptweb/decomp"

def need(value, message):
    if not value:
        raise RuntimeError("BRANCH RETIREMENT REFUSED: " + message)

def api(path, missing=False):
    request = urllib.request.Request(
        "https://api.github.com/repos/" + REPO + "/" + path,
        headers={"Authorization": "Bearer " + os.environ["GH_TOKEN"],
                 "Accept": "application/vnd.github+json",
                 "X-GitHub-Api-Version": "2022-11-28"})
    try:
        with urllib.request.urlopen(request, timeout=30) as reply:
            return json.load(reply)
    except urllib.error.HTTPError as error:
        if missing and error.code == 404:
            return None
        raise

def all_open_heads():
    heads = set()
    for page in range(1, 22):
        rows = api(f"pulls?state=open&per_page=100&page={page}")
        for row in rows:
            head = row.get("head") or {}
            if (head.get("repo") or {}).get("full_name") == REPO:
                heads.add(head.get("ref"))
        if len(rows) < 100:
            return heads
    need(False, "too many open PR pages")

def execute():
    need(os.environ["GITHUB_REPOSITORY"] == REPO, "wrong repository")
    event = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text())
    pull = event.get("pull_request") or {}
    number = str(pull.get("number", ""))
    plan = json.loads(Path("decomp/research/branch_archive/RETIREMENT_PLAN_20261119.json").read_text())
    need(plan["format"] == "goemon-retire-archived-branches-v1", "wrong plan format")
    if event.get("action") != "closed" or not pull.get("merged") or number not in plan["prs"]:
        print("Not an allowlisted merged archive PR; nothing deleted")
        return
    record = plan["prs"][number]
    head = pull.get("head") or {}
    need((pull.get("base") or {}).get("ref") == BASE
         and head.get("ref") == record["head"]
         and (head.get("repo") or {}).get("full_name") == REPO,
         "archive PR identity changed")
    latest = api("pulls/" + number)
    merged = latest.get("merge_commit_sha")
    need(latest.get("merged_at") and merged and merged == pull.get("merge_commit_sha"),
         "merge not authenticated")
    prefix = "decomp/research/branch_archive/" + record["archive"]
    for page in range(1, 22):
        files = api(f"pulls/{number}/files?per_page=100&page={page}")
        for file in files:
            name = file["filename"]
            need(name == "PROGRESS.md" or name.startswith(prefix + "/"),
                 "unreviewed change in archive PR: " + name)
        if len(files) < 100:
            break
    else:
        need(False, "PR file list unexpectedly long")
    tree = api(f"git/trees/{merged}?recursive=1")
    need(not tree.get("truncated"), "truncated tree")
    roots = [item for item in tree.get("tree", []) if item.get("path") == prefix and item.get("type") == "tree"]
    need(len(roots) == 1 and roots[0]["sha"] == record["tree"],
         "archive subtree differs from original approved source blobs")
    current = api("git/ref/heads/" + BASE)["object"]["sha"]
    need(api(f"compare/{merged}...{current}")["status"] in ("identical", "ahead"),
         "archive merge absent from current canon")
    active = all_open_heads()
    pending = []
    for branch, pinned in record["branches"].items():
        need(branch not in ("main", BASE, record["head"]) and branch not in active,
             "source ref still in use: " + branch)
        path = "git/ref/heads/" + urllib.parse.quote(branch, safe="/")
        remote = api(path, missing=True)
        if remote is None:
            print("Already absent:", branch)
            continue
        need(remote["object"]["sha"] == pinned, "source ref moved: " + branch)
        pending.append((branch, pinned))
    print("Verified merged archive #" + number + "; retiring " + str(len(pending)) + " pinned refs")
    for branch, pinned in pending:
        subprocess.run(["git", "push",
                        "--force-with-lease=refs/heads/" + branch + ":" + pinned,
                        "origin", ":refs/heads/" + branch], check=True)
        need(api("git/ref/heads/" + urllib.parse.quote(branch, safe="/"), missing=True) is None,
             "delete unconfirmed: " + branch)
        print("Retired:", branch)

if __name__ == "__main__":
    execute()
