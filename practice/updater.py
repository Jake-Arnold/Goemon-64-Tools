"""Git-backed toolkit version selector: stable main, test branches, release tags.

Discover refs only from the canonical GitHub origin. Never reset, delete local
commits, switch to decomp branches or overwrite tracked changes. A selected
cross-version switch is explicit; same-branch installs are fast-forwards only.
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
SHA_PATTERN = re.compile(r"[0-9a-f]{40}\Z")
TOOLKIT_BRANCH_PATTERN = re.compile(
    r"toolkit/[a-zA-Z0-9][a-zA-Z0-9_./-]*\Z")
TAG_PATTERN = re.compile(
    r"v?\d+\.\d+\.\d+(?:[-.][0-9A-Za-z.-]+)?\Z")


class UpdateError(RuntimeError):
    """A version check or installation cannot be completed safely."""


@dataclass(frozen=True)
class VersionTarget:
    kind: str  # branch or tag
    name: str
    sha: str

    def __post_init__(self):
        if self.kind == "branch":
            if self.name != BRANCH and not TOOLKIT_BRANCH_PATTERN.fullmatch(self.name):
                raise ValueError("Not a toolkit branch")
        elif self.kind == "tag":
            if not TAG_PATTERN.fullmatch(self.name):
                raise ValueError("Not a toolkit release tag")
        else:
            raise ValueError("Unsupported update target type")
        if not SHA_PATTERN.fullmatch(self.sha):
            raise ValueError("Invalid target SHA")

    @property
    def label(self):
        if self.kind == "tag":
            return f"Release tag · {self.name}"
        if self.name == BRANCH:
            return "Stable · main"
        return f"Test · {self.name}"


@dataclass(frozen=True)
class UpdateStatus:
    state: str  # current, available, switch
    local_sha: str
    remote_sha: str
    branch: str = BRANCH  # compatibility with current updater tests
    target_kind: str = "branch"

    @property
    def message(self):
        if self.state == "current":
            return f"Already running {self.branch} ({self.local_sha[:9]})."
        if self.state == "switch":
            return (f"Switch to {self.branch} ({self.remote_sha[:9]}) "
                    f"from {self.local_sha[:9]}.")
        return (f"Update available on {self.branch}: {self.local_sha[:9]} "
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
        raise UpdateError("Git is not installed; use a Git checkout.") from exc
    except subprocess.TimeoutExpired as exc:
        raise UpdateError("Git operation timed out; changes were not reset.") from exc
    if result.returncode and not permit_failure:
        detail = (result.stderr or result.stdout).strip()
        raise UpdateError(detail[:450] or f"Git exited {result.returncode}.")
    return result


def _trusted_origin(url: str) -> bool:
    url = url.strip()
    patterns = (
        rf"(?i)https://github\.com/{CANONICAL_REPOSITORY}(?:\.git)?/?",
        rf"(?i)git@github\.com:{CANONICAL_REPOSITORY}(?:\.git)?/?",
        rf"(?i)ssh://git@github\.com/{CANONICAL_REPOSITORY}(?:\.git)?/?",
    )
    return any(re.fullmatch(pattern, url) for pattern in patterns)


def _validate_checkout(root: Path):
    """Check local Git safety; keep detached release checkouts supported."""
    root = Path(root).resolve()
    if shutil.which("git") is None:
        raise UpdateError("Git is not installed.")
    if not (root / ".git").exists():
        raise UpdateError("Version selection requires a Git clone, not a ZIP download.")
    top = _git(root, "rev-parse", "--show-toplevel").stdout.strip()
    if Path(top).resolve() != root:
        raise UpdateError("The toolkit folder is not the root Git checkout.")
    branch = _git(root, "branch", "--show-current").stdout.strip()
    if branch and branch != BRANCH and not TOOLKIT_BRANCH_PATTERN.fullmatch(branch):
        raise UpdateError(
            f"Current branch '{branch}' is not a toolkit branch. "
            "Decompilation and other research checkouts are left untouched.")
    url = _git(root, "remote", "get-url", REMOTE).stdout.strip()
    if not _trusted_origin(url):
        raise UpdateError("Origin is not the canonical Goemon toolkit repository.")
    changes = _git(root, "status", "--porcelain", "--untracked-files=no").stdout.strip()
    if changes:
        raise UpdateError(
            "Tracked files have local changes; commit or stash before switching versions.")
    return root, branch


def _head(root: Path, ref: str) -> str:
    sha = _git(root, "rev-parse", "--verify", ref).stdout.strip()
    if not SHA_PATTERN.fullmatch(sha):
        raise UpdateError("Git returned an invalid SHA.")
    return sha


def _local_branch_tip(root: Path, branch: str):
    result = _git(root, "rev-parse", "--verify", f"refs/heads/{branch}",
                  permit_failure=True)
    if result.returncode:
        return None
    sha = result.stdout.strip()
    if not SHA_PATTERN.fullmatch(sha):
        raise UpdateError("Invalid local branch SHA.")
    return sha


def _is_ancestor(root: Path, before: str, after: str) -> bool:
    result = _git(root, "merge-base", "--is-ancestor", before, after,
                  permit_failure=True)
    if result.returncode not in (0, 1):
        raise UpdateError("Git could not establish ancestry.")
    return result.returncode == 0


def _ref(target: VersionTarget) -> str:
    return ("refs/heads/" if target.kind == "branch" else "refs/tags/") + target.name


def _fetch_remote_target(root: Path, target: VersionTarget) -> str:
    _git(root, "fetch", "--no-tags", REMOTE, _ref(target), timeout=45)
    return _head(root, "FETCH_HEAD^{commit}")


def list_available_versions(root: Path):
    """List allowed stable, toolkit test branches and semver release tags."""
    root, branch = _validate_checkout(root)
    result = _git(root, "ls-remote", "--heads", "--tags", REMOTE, timeout=45)
    refs = {}
    peeled = {}
    for line in result.stdout.splitlines():
        try:
            sha, ref = line.split("\t", 1)
        except ValueError:
            continue
        if not SHA_PATTERN.fullmatch(sha):
            continue
        if ref.startswith("refs/tags/") and ref.endswith("^{}"):
            peeled[ref[:-3]] = sha
        else:
            refs[ref] = sha
    targets = []
    for ref, sha in refs.items():
        if ref.startswith("refs/heads/"):
            name = ref.removeprefix("refs/heads/")
            if name == BRANCH or TOOLKIT_BRANCH_PATTERN.fullmatch(name):
                targets.append(VersionTarget("branch", name, sha))
        elif ref.startswith("refs/tags/"):
            name = ref.removeprefix("refs/tags/")
            if TAG_PATTERN.fullmatch(name):
                targets.append(VersionTarget("tag", name, peeled.get(ref, sha)))
    if not any(t.kind == "branch" and t.name == BRANCH for t in targets):
        raise UpdateError("The official GitHub main branch was not listed.")
    stable = [t for t in targets if t.kind == "branch" and t.name == BRANCH]
    tests = sorted(
        (t for t in targets if t.kind == "branch" and t.name != BRANCH),
        key=lambda x: x.name.casefold())
    tags = sorted(
        (t for t in targets if t.kind == "tag"),
        key=lambda t: (
            tuple(int(x) for x in re.match(r"v?(\d+)\.(\d+)\.(\d+)", t.name).groups()),
            bool(re.search(r"[-]", t.name))), reverse=True)
    return tuple(stable + tests + tags)


def detect_installed_target(root: Path, targets) -> VersionTarget | None:
    """Select the matching branch or exact release when the UI opens."""
    root, branch = _validate_checkout(root)
    if branch:
        return next((t for t in targets
                     if t.kind == "branch" and t.name == branch), None)
    sha = _head(root, "HEAD")
    return next((t for t in targets
                 if t.kind == "tag" and t.sha == sha), None)


def _resolve_target(root: Path, target: VersionTarget | None, branch: str):
    if target is not None:
        if not isinstance(target, VersionTarget):
            raise ValueError("Unknown target selection")
        return target
    if not branch:
        raise UpdateError("Select a branch or release before checking updates.")
    remote = _fetch_remote_target(
        root, VersionTarget("branch", branch, "0" * 40))
    return VersionTarget("branch", branch, remote)


def check_for_updates(root: Path, target: VersionTarget | None = None) -> UpdateStatus:
    """Fetch a user-selected remote ref without changing working-tree files."""
    root, current = _validate_checkout(root)
    selected = _resolve_target(root, target, current)
    local_sha = _head(root, "HEAD")
    remote_sha = _fetch_remote_target(root, selected)
    if target is not None and remote_sha != selected.sha:
        raise UpdateError("The selected remote version changed; refresh versions.")
    selected = VersionTarget(selected.kind, selected.name, remote_sha)
    if selected.kind == "tag":
        state = "current" if not current and local_sha == remote_sha else "switch"
    elif current == selected.name:
        if local_sha == remote_sha:
            state = "current"
        elif _is_ancestor(root, local_sha, remote_sha):
            state = "available"
        else:
            raise UpdateError(
                "Local branch has diverged from GitHub; commits will not be reset.")
    else:
        local_target = _local_branch_tip(root, selected.name)
        if local_target and not _is_ancestor(root, local_target, remote_sha):
            raise UpdateError(
                "Selected local branch is ahead/diverged; branch history is protected.")
        state = "switch"
    return UpdateStatus(state, local_sha, remote_sha,
                        selected.name, selected.kind)


def install_update(root: Path, checked: UpdateStatus) -> str:
    """Install an explicitly checked ref without discarding local history.

    Any branch switch is initiated by the user in the UI. The GUI restarts
    only after its game-worker/process cleanup has completed.
    """
    if checked.state not in ("available", "switch"):
        raise UpdateError("No checked version to install.")
    root, current = _validate_checkout(root)
    if _head(root, "HEAD") != checked.local_sha:
        raise UpdateError("Local HEAD changed; check again.")
    selected = VersionTarget(checked.target_kind, checked.branch, checked.remote_sha)
    remote_sha = _fetch_remote_target(root, selected)
    if remote_sha != checked.remote_sha:
        raise UpdateError("Selected version changed since the check; check again.")
    if checked.target_kind == "tag":
        if checked.state != "switch":
            raise UpdateError("Release is already installed.")
        _git(root, "switch", "--detach", remote_sha, timeout=45)
    else:
        local_target = _local_branch_tip(root, checked.branch)
        if local_target and not _is_ancestor(root, local_target, remote_sha):
            raise UpdateError("Selected local branch diverged; no history was reset.")
        if current != checked.branch:
            if local_target is None:
                _git(root, "switch", "-c", checked.branch, remote_sha, timeout=45)
            else:
                _git(root, "switch", checked.branch, timeout=45)
        if _head(root, "HEAD") != remote_sha:
            _git(root, "merge", "--ff-only", remote_sha, timeout=45)
    if _head(root, "HEAD") != remote_sha:
        raise UpdateError("Selected version was not installed.")
    return remote_sha
