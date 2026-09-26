"""Stable registry of 28 computational reasoning slots."""
from dataclasses import dataclass
from typing import Tuple

@dataclass(frozen=True)
class ThoughtMode:
    mode_id: str
    ordinal: int
    operation: str
    description: str

_OPERATIONS = ("identity","reverse","rotate","pairwise","difference","sum",
               "intersection","union","projection","expansion","reduction",
               "permutation","combination","cartesian")

THOUGHT_MODES_28: Tuple[ThoughtMode,...] = tuple(
    ThoughtMode(f"TM-{i:02d}", i, _OPERATIONS[(i-1)%len(_OPERATIONS)],
                f"Formal reasoning slot {i}; operator binding is configuration-driven.")
    for i in range(1,29)
)

def get_mode(mode_id: str) -> ThoughtMode:
    for mode in THOUGHT_MODES_28:
        if mode.mode_id == mode_id:
            return mode
    raise KeyError(f"unknown thought mode: {mode_id}")
