"""Observed original debug-menu categories; MAIN occupies value zero.

The order comes from the user's live menu screenshot. Two blurry lower row
labels retain explicit question marks pending clearer verification.
"""
from __future__ import annotations

NATIVE_MENU_CATEGORIES = (
    'MAIN', 'SIRO', 'DOUCHU', 'MACHI', 'SHOP', 'OBOMBER',
    'SIDO??', 'DATMAP', 'OPENING', 'GOPENING', 'BOSS3D.OP',
    'DIARY', 'G?TERM', 'GAMEOVER',
)

def native_menu_category(value: int) -> str:
    return NATIVE_MENU_CATEGORIES[value] if 0 <= value < len(NATIVE_MENU_CATEGORIES) else 'UNKNOWN'

SCENE_FAMILY_CATEGORY_INDEX = {'SIRO': 1, 'DOUCHU': 2, 'MACHI': 3, 'SHOP': 4}
