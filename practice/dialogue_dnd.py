"""Toolkit Tk root with optional native TkDND support (Linux/Windows/macOS)."""
from __future__ import annotations
import tkinter as tk


def make_toolkit_root(*, class_name='goemon-practice-toolkit'):
    """Use TkinterDnD when available; retain normal Tk as a safe fallback."""
    try:
        from tkinterdnd2 import TkinterDnD
    except ImportError:
        return tk.Tk(className=class_name)
    try:
        return TkinterDnD.Tk(className=class_name)
    except (tk.TclError,RuntimeError):
        return tk.Tk(className=class_name)
