"""Replacement control-board fascia panel for a Fisher & Paykel ED55/56 dryer."""

from .panel import FLEXURE, SEPARATE, VARIANTS, make_caps, make_panel
from .params import DEFAULT, Params

__all__ = [
    "DEFAULT",
    "FLEXURE",
    "Params",
    "SEPARATE",
    "VARIANTS",
    "make_caps",
    "make_panel",
]
