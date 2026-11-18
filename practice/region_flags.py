"""Tk-native small raster flags, independent of emoji fonts and Pillow."""
from __future__ import annotations

import math
import tkinter as tk


def make_region_flag_images(master):
    """Return USA/Japan 48x32 PhotoImages; caller holds references."""
    width, height = 48, 32
    usa = tk.PhotoImage(master=master, width=width, height=height)
    for index in range(13):
        top, bottom = index * height // 13, (index + 1) * height // 13
        if bottom > top:
            usa.put('#B22234' if index % 2 == 0 else '#FFFFFF',
                    to=(0, top, width, bottom))
    usa.put('#3C3B6E', to=(0, 0, 21, 18))
    for row in range(7):
        for col in range(6 if row % 2 == 0 else 5):
            x = 2 + col * 3 + (row % 2)
            y = 2 + row * 2
            if x < 21:
                usa.put('#FFFFFF', to=(x, y, x + 1, y + 1))

    japan = tk.PhotoImage(master=master, width=width, height=height)
    japan.put('#FFFFFF', to=(0, 0, width, height))
    for y in range(6, 27):
        half = int(math.sqrt(max(0, 100 - (y - 16) ** 2)))
        japan.put('#BC002D', to=(24 - half, y, 25 + half, y + 1))
    return {'usa': usa, 'japan': japan}
