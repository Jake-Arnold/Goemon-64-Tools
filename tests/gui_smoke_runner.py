"""Run Tk smoke tests without invisible modal dialog deadlocks."""
from contextlib import ExitStack, contextmanager
import sys
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
import tkinter.simpledialog as simpledialog
import unittest
from unittest.mock import patch

_DIALOG_FUNCTIONS = (
    (messagebox, (
        "askyesno", "askokcancel", "askquestion", "askretrycancel",
        "askyesnocancel", "showinfo", "showwarning", "showerror",
    )),
    (filedialog, (
        "askopenfilename", "askopenfilenames", "asksaveasfilename",
        "askopenfile", "askopenfiles", "asksaveasfile", "askdirectory",
    )),
    (simpledialog, ("askstring", "askinteger", "askfloat")),
)

@contextmanager
def reject_unexpected_modals():
    """Raise an actionable error instead of waiting on a hidden dialog."""
    with ExitStack() as stack:
        for module, functions in _DIALOG_FUNCTIONS:
            for function in functions:
                stack.enter_context(patch.object(
                    module, function,
                    side_effect=AssertionError(
                        f"Unexpected modal dialog: {module.__name__}.{function}"
                    ),
                ))
        yield

def main(modules=None):
    arguments = sys.argv[1:] if modules is None else modules
    # Existing Bash smoke scripts pass the standard unittest -v flag.
    names = [name for name in arguments if name not in ('-v', '--verbose')]
    if not names:
        print("Usage: python -m tests.gui_smoke_runner TEST_MODULE [...]", file=sys.stderr)
        return 2
    with reject_unexpected_modals():
        suite = unittest.defaultTestLoader.loadTestsFromNames(names)
        result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1

if __name__ == "__main__":
    raise SystemExit(main())
