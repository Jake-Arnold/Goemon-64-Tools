"""Dark Japanese-inspired Tk/ttk styling for the Goemon tools.

Presentation-only module: no game state access or memory writes.
"""
from __future__ import annotations

from tkinter import ttk

PALETTE = {
    'background': '#111317',
    'surface': '#1a1d23',
    'surface_alt': '#22262e',
    'line': '#3c3a39',
    'gold': '#edbf6b',
    'red': '#8c3030',
    'red_hover': '#aa4040',
    'teal': '#60cdbb',
    'foreground': '#f3eee5',
    'muted': '#b8b4ad',
    'warning': '#f0b778',
    'invalid': '#5d3030',
    'changed': '#254f49',
}


def apply_theme(root) -> None:
    """Apply app styling without requiring external theme libraries."""
    c = PALETTE
    root.configure(bg=c['background'])
    style = ttk.Style(root)
    style.theme_use('clam')
    style.configure('.', font=('Segoe UI', 10), background=c['background'], foreground=c['foreground'])
    style.configure('TFrame', background=c['background'])
    style.configure('Card.TFrame', background=c['surface'], relief='flat', borderwidth=0)
    style.configure('Header.TFrame', background=c['surface'])
    style.configure('TLabel', background=c['background'], foreground=c['foreground'])
    style.configure('Card.TLabel', background=c['surface'], foreground=c['foreground'])
    style.configure('Muted.TLabel', background=c['background'], foreground=c['muted'])
    style.configure('CardMuted.TLabel', background=c['surface'], foreground=c['muted'])
    style.configure('Header.TLabel', background=c['surface'], foreground=c['gold'], font=('Segoe UI Semibold', 18))
    style.configure('HeaderSub.TLabel', background=c['surface'], foreground=c['muted'], font=('Segoe UI', 9))
    style.configure('Heading.TLabel', background=c['surface'], foreground=c['gold'], font=('Segoe UI Semibold', 11))
    style.configure('AccentValue.TLabel', background=c['surface'], foreground=c['teal'], font=('Consolas', 10, 'bold'))
    style.configure('TLabelFrame', background=c['surface'], bordercolor=c['line'], borderwidth=1, relief='solid')
    style.configure('TLabelFrame.Label', background=c['surface'], foreground=c['gold'], font=('Segoe UI Semibold', 11))
    style.configure('TButton', background=c['surface_alt'], foreground=c['foreground'],
                    bordercolor=c['line'], padding=(10, 7), relief='flat', focusthickness=0)
    style.map('TButton', background=[('disabled', c['surface']), ('active', '#343a45')],
              foreground=[('disabled', '#777b82')])
    style.configure('Accent.TButton', background=c['red'], foreground='#ffffff',
                    padding=(11, 8), bordercolor=c['red'])
    style.map('Accent.TButton', background=[('active', c['red_hover']), ('disabled', '#503535')])
    style.configure('Gold.TButton', background='#644522', foreground='#fff3d6', bordercolor='#9a703c')
    style.map('Gold.TButton', background=[('active', '#805c31')])
    # Dense event-flag rows use unified card backgrounds instead of a
    # Card.TLabel drawn on a plain dark frame (which made text look patched).
    style.configure('FlagRow.TFrame', background=c['surface_alt'])
    style.configure('FlagGroup.TFrame', background=c['surface'])
    style.configure('FlagName.TLabel', background=c['surface_alt'],
                    foreground='#ffffff', font=('Segoe UI Semibold', 10))
    style.configure('FlagMeta.TLabel', background=c['surface_alt'],
                    foreground='#cbd1d9', font=('Segoe UI', 9))
    style.configure('FlagAddress.TLabel', background=c['surface_alt'],
                    foreground='#d4c5aa', font=('Consolas', 10))
    style.configure('FlagState.TLabel', background=c['surface_alt'],
                    foreground='#d3dce4', font=('Segoe UI Semibold', 10))
    style.configure('FlagGroup.TLabel', background=c['surface'],
                    foreground=c['gold'], font=('Segoe UI Semibold', 11))
    style.configure('Flag.TButton', background='#39424e', foreground='#f1f5fa',
                    bordercolor='#586574', padding=(8, 5),
                    font=('Segoe UI Semibold', 10), relief='flat')
    style.map('Flag.TButton',
              background=[('disabled', '#303741'), ('active', '#4b5968')],
              foreground=[('disabled', '#b4becb')])
    style.configure('FlagOn.TButton', background='#245b52',
                    foreground='#f6fffb', bordercolor='#4caa96',
                    padding=(8, 5), font=('Segoe UI Semibold', 10))
    style.map('FlagOn.TButton',
              background=[('disabled', '#314d48'), ('active', '#307567')],
              foreground=[('disabled', '#d5e8e2')])
    style.configure('FlagOff.TButton', background='#66502e',
                    foreground='#fff8e8', bordercolor='#ba955e',
                    padding=(8, 5), font=('Segoe UI Semibold', 10))
    style.map('FlagOff.TButton',
              background=[('disabled', '#4c4233'), ('active', '#80653b')],
              foreground=[('disabled', '#f0ddbc')])
    style.configure('TEntry', fieldbackground=c['surface_alt'], foreground=c['foreground'],
                    insertcolor=c['foreground'], bordercolor=c['line'], lightcolor=c['gold'],
                    padding=(6, 5))
    style.configure('TCombobox', fieldbackground=c['surface_alt'], background=c['surface_alt'],
                    foreground=c['foreground'], arrowcolor=c['gold'], bordercolor=c['line'], padding=4)
    style.map('TCombobox', fieldbackground=[('readonly', c['surface_alt'])],
              foreground=[('readonly', c['foreground'])],
              selectforeground=[('readonly', c['foreground'])],
              selectbackground=[('readonly', c['surface_alt'])])
    style.configure('TCheckbutton', background=c['background'], foreground=c['foreground'], padding=3)
    style.map('TCheckbutton', background=[('active', c['background'])], foreground=[('active', c['gold'])])
    style.configure('TNotebook', background=c['background'], borderwidth=0, tabmargins=(8, 6, 0, 0))
    style.configure('TNotebook.Tab', background=c['surface_alt'], foreground=c['muted'],
                    borderwidth=0, padding=(16, 10))
    style.map('TNotebook.Tab', background=[('selected', c['red']), ('active', '#343039')],
              foreground=[('selected', '#ffffff'), ('active', c['foreground'])])
    style.configure('Treeview', background=c['surface'], fieldbackground=c['surface'],
                    foreground=c['foreground'], borderwidth=0, rowheight=26)
    style.map('Treeview', background=[('selected', '#6d292b')], foreground=[('selected', '#ffffff')])
    style.configure('Treeview.Heading', background=c['surface_alt'], foreground=c['gold'],
                    font=('Segoe UI Semibold', 9), relief='flat', borderwidth=0, padding=6)
    style.map('Treeview.Heading', background=[('active', '#343a45')])
    style.configure('TScrollbar', background=c['surface_alt'], troughcolor=c['surface'],
                    arrowcolor=c['gold'], bordercolor=c['surface'], gripcount=0)
    style.configure('TSeparator', background=c['line'])
    # Pop-downs use Tk listbox colours separate from ttk styles.
    try:
        root.option_add('*TCombobox*Listbox.background', c['surface_alt'])
        root.option_add('*TCombobox*Listbox.foreground', c['foreground'])
        root.option_add('*TCombobox*Listbox.selectBackground', c['red'])
    except Exception:
        pass
