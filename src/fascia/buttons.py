"""Button geometry, in two flavours.

`flexure` replicates the original Fisher & Paykel design seen in
reference/photos/04: an inverted-U slot cuts a tab free on three sides, leaving
it joined along its bottom edge so it swings like a trapdoor. The printed label
bridges the slot, sealing it and providing the cushion. The hinge is thinned
from the back so the tab moves without dragging the panel with it.

`separate` drops a loose printed cap through a round aperture. The cap has a
flange behind the panel so it cannot fall out the front; it is held captive
between the panel and the control board.

Both end in a plunger that reaches down towards the tactile switch, stopping
`pre_travel` short of it so the switches are not held half-pressed at rest.
"""

from build123d import (
    Align,
    Axis,
    Box,
    Cylinder,
    GeomType,
    Part,
    Pos,
    Rectangle,
    RectangleRounded,
    Sketch,
    extrude,
    fillet,
)

from .params import Params, Switch

_BOTTOM = (Align.CENTER, Align.CENTER, Align.MIN)
_TOP = (Align.CENTER, Align.CENTER, Align.MAX)


def plunger(p: Params, sw: Switch, deduct: float = 0.0) -> Part:
    """The boss reaching from the back of the panel towards the switch.

    `deduct` accounts for anything already standing between the back face and
    the start of the boss, such as a button cap's flange.
    """
    length = sw.standoff - p.pre_travel - deduct
    if length <= 0:
        raise ValueError(
            f"switch {sw.name!r}: a standoff of {sw.standoff} leaves no room for "
            f"a plunger once {p.pre_travel} of pre-travel and {deduct} of "
            f"anything else are taken out"
        )
    return Cylinder(p.plunger / 2, length, align=_TOP)


# ---------------------------------------------------------------------------
# flexure variant: the original trapdoor tab
# ---------------------------------------------------------------------------


def _tab_outline(p: Params, grow: float = 0.0) -> Sketch:
    return RectangleRounded(
        p.button_width + 2 * grow,
        p.button_height + 2 * grow,
        p.button_radius + grow,
    )


def flexure_slot(p: Params, sw: Switch) -> Part:
    """The inverted-U slot that frees the tab on its left, top and right.

    The ring of material between the tab and the panel is trimmed back to the
    hinge line, so the bottom edge stays joined.
    """
    s = p.flexure_slot
    ring = _tab_outline(p, grow=s) - _tab_outline(p)

    # Keep only the part of the ring at or above the hinge line, which sits at
    # the bottom edge of the tab.
    above_hinge = Pos(0, s / 2) * Rectangle(
        p.button_width + 2 * s + 2, p.button_height + s
    )

    solid = extrude(ring & above_hinge, p.thickness + 2)
    return Pos(sw.x, sw.y, -1) * solid


def flexure_hinge_relief(p: Params, sw: Switch) -> Part | None:
    """Thinning cut across the hinge line, taken from the back face."""
    depth = p.thickness - p.hinge_thickness
    if depth <= 0:
        return None
    relief = Box(p.button_width, p.hinge_band, depth, align=_BOTTOM)
    return Pos(sw.x, sw.y - p.button_height / 2, 0) * relief


def flexure_pad(p: Params, sw: Switch) -> Part | None:
    """Bump raised on the tab so the button can be found through the label."""
    if p.flexure_pad_rise <= 0:
        return None
    pad = extrude(_tab_outline(p, grow=-p.flexure_pad_inset), p.flexure_pad_rise)
    pad = fillet(
        pad.edges().group_by(Axis.Z)[-1], radius=min(0.4, p.flexure_pad_rise / 2.5)
    )
    return Pos(sw.x, sw.y, p.thickness) * pad


# ---------------------------------------------------------------------------
# separate variant: loose caps
# ---------------------------------------------------------------------------


def cap_aperture(p: Params, sw: Switch) -> Part:
    """Through-hole in the panel that a loose cap slides in."""
    bore = p.button_width + 2 * p.cap_clearance
    return Pos(sw.x, sw.y, -1) * Cylinder(bore / 2, p.thickness + 2, align=_BOTTOM)


def cap(p: Params, sw: Switch) -> Part:
    """One loose button cap, modelled in place relative to the panel."""
    flange_d = p.button_width + 2 * p.cap_flange_width
    flange = Cylinder(flange_d / 2, p.cap_flange_thickness, align=_TOP)

    shaft = Cylinder(p.button_width / 2, p.thickness + p.cap_rise, align=_BOTTOM)
    top = shaft.edges().filter_by(GeomType.CIRCLE).sort_by(Axis.Z)[-1]
    shaft = fillet(top, radius=0.5)

    boss = Pos(0, 0, -p.cap_flange_thickness) * plunger(
        p, sw, deduct=p.cap_flange_thickness
    )

    return Pos(sw.x, sw.y, 0) * (flange + shaft + boss)
