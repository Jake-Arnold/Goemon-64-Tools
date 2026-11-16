"""Install an Ubuntu/GNOME application launcher using the existing toolkit PNG.

No root/sudo, no system-global changes. Installs a desktop entry and a copy
of the checked-in application logo under the current user's XDG data home.
"""
from __future__ import annotations

import os
from pathlib import Path
import shutil

APP_ID = "goemon-practice-toolkit"
WINDOW_CLASS = APP_ID  # Exact Tk WM_CLASS instance / .desktop basename


def _desktop_exec_quote(value: str) -> str:
    """Quote a desktop-entry Exec argument (not shell syntax)."""
    # Exec keys need doubled escaping for the desktop-entry layer.
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    escaped = escaped.replace("$", "\\$").replace("`", "\\`")
    return f'"{escaped}"'


def install(*, repo_root=None, data_home=None) -> Path:
    root = (Path(repo_root) if repo_root else Path(__file__).resolve().parents[1]
            ).resolve(strict=True)
    launch = root / "Run-Linux.sh"
    logo = root / "assets" / "goemon_tools_logo.png"
    if not launch.is_file():
        raise FileNotFoundError(f"Missing unified Linux launcher: {launch}")
    if not logo.is_file() or logo.read_bytes()[:8] != bytes.fromhex(
            "89504e470d0a1a0a"):
        raise ValueError(f"Missing or invalid PNG app icon: {logo}")
    base = (Path(data_home) if data_home is not None else
            Path(os.environ.get("XDG_DATA_HOME") or
                 Path.home() / ".local" / "share"))
    icon = base / "icons" / f"{APP_ID}.png"
    desktop = base / "applications" / f"{APP_ID}.desktop"
    icon.parent.mkdir(parents=True, exist_ok=True)
    desktop.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(logo, icon)
    entry = (
        "[Desktop Entry]\n"
        "Type=Application\n"
        "Name=Goemon Practice Toolkit\n"
        "GenericName=Goemon Speedrun Tools\n"
        "Comment=Unified USA and Japanese Goemon practice toolkit\n"
        f"Exec=/usr/bin/env bash {_desktop_exec_quote(str(launch))}\n"
        f"Path={root}\n"
        f"Icon={icon}\n"
        "Terminal=false\n"
        "Categories=Game;Utility;\n"
        "StartupNotify=true\n"
        f"StartupWMClass={WINDOW_CLASS}\n"
    )
    desktop.write_text(entry, encoding="utf-8")
    desktop.chmod(0o644)
    return desktop


def main() -> None:
    result = install()
    print(f"Installed Goemon Practice Toolkit launcher: {result}")
    print("Close old toolkit windows; launch from Ubuntu app grid and pin to dock.")
    print("Expected WM_CLASS instance: goemon-practice-toolkit")
    print("If a cog persists, run: xprop WM_CLASS (click the toolkit window)")


if __name__ == "__main__":
    main()
