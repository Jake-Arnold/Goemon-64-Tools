"""Explicit OS permission adjustment for attaching to an already-running Linux game.

Never runs the toolkit as root. Only an explicit GUI action can invoke the
system-installed polkit utility to change a Linux Yama setting.
"""
from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess
import sys

YAMA_SCOPE = Path('/proc/sys/kernel/yama/ptrace_scope')


def ptrace_scope(path=YAMA_SCOPE):
    """Return the active Yama setting; None when unavailable."""
    try:
        return int(path.read_text(encoding='ascii').strip())
    except (OSError, ValueError):
        return None


def external_pid_hint(pid, scope=None):
    if scope is None:
        scope=ptrace_scope()
    if scope is None:
        return (f'PID {pid}: process memory access denied. Check ownership, '
                'sandbox limits and Linux ptrace permissions.')
    if scope == 0:
        return (f'PID {pid}: ptrace_scope=0 already permits normal same-user '
                'attachment; check process ownership and sandbox restrictions.')
    return (f'PID {pid}: kernel.yama.ptrace_scope={scope} restricts access to '
            'independently launched processes. Use the Connection panel '
            'permission control for an authenticated, temporary system setting '
            'change, or launch the game as a toolkit child.')


def change_ptrace_scope(value):
    """Use trusted OS binaries with polkit; caller must obtain user approval.

    Does not modify persistent configuration files. Setting 0 affects all
    same-user processes and must be restored explicitly.
    """
    if sys.platform != 'linux':
        raise OSError('Linux PID permissions are only available on Linux')
    if value not in (0, 1, 2):
        raise ValueError('Invalid Linux ptrace restriction value')
    pkexec=shutil.which('pkexec')
    sysctl=shutil.which('sysctl')
    if not pkexec or not sysctl:
        raise OSError('pkexec/sysctl not installed. On Ubuntu: install policykit-1; '
                      'otherwise configure kernel.yama.ptrace_scope manually.')
    command=[str(Path(pkexec).resolve()),str(Path(sysctl).resolve()),
             '-w',f'kernel.yama.ptrace_scope={value}']
    result=subprocess.run(command,stdin=subprocess.DEVNULL,
                          capture_output=True,text=True,timeout=120,check=False)
    if result.returncode:
        message=(result.stderr or result.stdout).strip()
        raise PermissionError(message or
              'Administrator authorization was cancelled or ptrace scope change was denied')
    observed=ptrace_scope()
    if observed is not None and observed != value:
        raise OSError(f'Linux still reports ptrace_scope={observed}; expected {value}')
    return observed
