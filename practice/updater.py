"""Safe, explicit mainline updates for Git-cloned Goemon toolkit installs.

Never reset, force-checkout, clean user files or switch development branches.
Fetch the canonical GitHub origin and fast-forward *only* a clean main checkout.
Git's merge protections also prevent overwriting conflicting untracked files.
"""
from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
import re
import shutil
import subprocess


CANONICAL_REPOSITORY = "Jake-Arnold/Goemon-64-Tools"
BRANCH = "main"
REMOTE = "origin"


class UpdateError(RuntimeError):
    """An update cannot be safely checked or installed."""


@dataclass(frozen=True)
class UpdateStatus:
    state: str  # current or available
    local_sha: str
    remote_sha: str

    @property
    def message(self):
        if self.state == "current":
            return f"Up to date with main ({self.local_sha[:9]})."
        return (f"Update available: main {self.local_sha[:9]} "
                f"→ {self.remote_sha[:9]}.")


def _git(root: Path, *args: str, timeout: int = 30, permit_failure=False):
    env = os.environ.copy()
    env["GIT_TERMINAL_PROMPT"] = "0"
    try:
        result = subprocess.run(
            ["git", "-C", str(root), *args],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            timeout=timeout, env=env, check=False)
    except FileNotFoundError as exc:
        raise UpdateError("Git is not installed; auto-update requires a Git checkout.") from exc
    except subprocess.TimeoutExpired as exc:
        raise UpdateError("Git operation timed out; files were not reset.") from exc
    if result.returncode and not permit_failure:
        detail = (result.stderr or result.stdout).strip()
        raise UpdateError(detail[:450] or f"Git exited {result.returncode}.")
    return result


def _trusted_origin(url: str) -> bool:
    """Only accept the official repository via HTTPS or GitHub SSH."""
    url = url.strip()
    patterns = (
        rf"(?i)https://github\.com/{CANONICAL_REPOSITORY}(?:\.git)?/?",
        rf"(?i)git@github\.com:{CANONICAL_REPOSITORY}(?:\.git)?/?",
        rf"(?i)ssh://git@github\.com/{CANONICAL_REPOSITORY}(?:\.git)?/?",
    )
    return any(re.fullmatch(pattern, url) for pattern in patterns)


def _validate_checkout(root: Path):
    root = Path(root).resolve()
    if shutil.which("git") is None:
        raise UpdateError("Git is not installed; update a source checkout manually.")
    if not (root / ".git").exists():
        raise UpdateError("Automatic updates require a Git clone, not a ZIP download.")
    top = _git(root, "rev-parse", "--show-toplevel").stdout.strip()
    if Path(top).resolve() != root:
        raise UpdateError("This toolkit folder is not the root of its Git checkout.")
    branch = _git(root, "branch", "--show-current").stdout.strip()
    if branch != BRANCH:
        raise UpdateError(
            f"Current branch is '{branch or 'detached HEAD'}'. "
            "Auto-update only works on main; development branches are left untouched.")
    url = _git(root, "remote", "get-url", REMOTE).stdout.strip()
    if not _trusted_origin(url):
        raise UpdateError("Origin does not point to the canonical Goemon toolkit repository.")
    changes = _git(root, "status", "--porcelain", "--untracked-files=no").stdout.strip()
    if changes:
        raise UpdateError("Tracked files have local changes; commit or stash them before updating.")
    return root


def _head(root: Path, ref: str) -> str:
    sha = _git(root, "rev-parse", "--verify", ref).stdout.strip()
    if not re.fullmatch(r"[0-9a-f]{40}", sha):
        raise UpdateError("Git returned an invalid commit SHA.")
    return sha


def _fetch_remote_head(root: Path) -> str:
    _git(root, "fetch", "--no-tags", REMOTE, f"refs/heads/{BRANCH}",
         timeout=45)
    return _head(root, "FETCH_HEAD")


def _is_ancestor(root: Path, before: str, after: str) -> bool:
    result = _git(root, "merge-base", "--is-ancestor", before, after,
                  permit_failure=True)
    if result.returncode not in (0, 1):
        raise UpdateError("Git could not check commit ancestry.")
    return result.returncode == 0


def check_for_updates(root: Path) -> UpdateStatus:
    """Fetch metadata/objects but never change working-tree files."""
    root = _validate_checkout(root)
    local = _head(root, "HEAD")
    remote = _fetch_remote_head(root)
    if local == remote:
        return UpdateStatus("current", local, remote)
    if not _is_ancestor(root, local, remote):
        raise UpdateError(
            "Local main is ahead or diverged from upstream main. "
            "Auto-update will not reset or overwrite local commits.")
    return UpdateStatus("available", local, remote)


def install_update(root: Path, checked: UpdateStatus) -> str:
    """Revalidate and fast-forward to the exact commit displayed to the user.

    The new version should launch *after* the current Tk window and all game
    process handles have been closed by the normal application shutdown path.
    """
    if checked.state != "available":
        raise UpdateError("No checked update to install.")
    root = _validate_checkout(root)
    if _head(root, "HEAD") != checked.local_sha:
        raise UpdateError("Local HEAD changed after the update check; check again.")
    remote = _fetch_remote_head(root)
    if remote != checked.remote_sha:
        raise UpdateError("Upstream main changed since the check; check again.")
    if not _is_ancestor(root, checked.local_sha, remote):
        raise UpdateError("Cannot fast-forward main; no files were reset.")
    _git(root, "merge", "--ff-only", remote, timeout=45)
    if _head(root, "HEAD") != remote:
        raise UpdateError("Update did not reach the expected commit.")
    return remote
