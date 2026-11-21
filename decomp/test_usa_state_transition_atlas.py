"""Discover the ROM-free state atlas tests in the regular decomp test suite."""
from pathlib import Path
import sys

RESEARCH_DIR = Path(__file__).parent / 'research' / 'usa_state_transition_atlas_20261121'
if str(RESEARCH_DIR) not in sys.path:
    sys.path.insert(0, str(RESEARCH_DIR))

from test_static_atlas import StateAtlasTests  # noqa: E402,F401
