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


def plunger(p: Params, deduct: float = 0.0, overlap: float = 0.0) -> Part:
    """The boss reaching from the back of the front plate towards a switch.

    Its free length comes from the depth chain in `Params`: whatever
    `switch_gap` leaves once `pre_travel` and `deduct` are taken out. `deduct`
    accounts for anything standing between the plate and the start of the boss,
    such as a button cap's flange.

    `overlap` extends the boss further back into the part it grows from, so the
    two share solid material rather than meeting on a single coincident face.
    Touching faces make for fragile booleans and multi-body STLs.
    """
    length = p.plunger_length - deduct
    if length <= 0:
        raise ValueError(
            f"a switch_gap of {p.switch_gap} (skin_to_switch {p.skin_to_switch} "
            f"less reach {p.reach}) leaves no room for a plunger once "
            f"{p.pre_travel} of pre-travel and {deduct} of anything else are "
            f"taken out. Either reach less deep or check the measurements."
        )
    return Cylinder(p.plunger / 2, length + overlap, align=_TOP)


# ---------------------------------------------------------------------------
# flexure variant: the original trapdoor tab
# ---------------------------------------------------------------------------


def _tab_outline(p: Params, grow: float = 0.0) -> Sketch:
    """The tab profile, optionally grown or shrunk all round by `grow`.

    The radius is clamped to what the rectangle can actually carry. The tabs
    are narrow, so a radius that suits the full outline will not survive being
    shrunk for the raised pad, and `RectangleRounded` will not accept a radius
    of half the side or more.
    """
    width = p.button_width + 2 * grow
    height = p.button_height + 2 * grow
    if width <= 0 or height <= 0:
        raise ValueError(
            f"a tab of {p.button_width} x {p.button_height} cannot be grown by "
            f"{grow}: that leaves {width} x {height}"
        )
    radius = min(p.button_radius + grow, width / 2 - 0.01, height / 2 - 0.01)
    return RectangleRounded(width, height, max(radius, 0.01))


def _tab_at(p: Params, grow: float = 0.0) -> Sketch:
    """The tab profile placed relative to its hinge line, which is at y = 0.

    The tab hangs *down* from the hinge, matching the original, so it occupies
    negative y. Growing the outline pushes it above the hinge line too; the
    slot trims that part off.
    """
    return Pos(0, -p.button_height / 2) * _tab_outline(p, grow)


def switch_point(p: Params, sw: Switch) -> Pos:
    """Where the plunger lands: below the hinge line by `plunger_drop`.

    Not the same as the tab centre in general. How far the actuator sits from
    the hinge sets the leverage, so it is a parameter rather than an assumption.
    """
    return Pos(sw.x, sw.y - p.plunger_drop, 0)


def flexure_slot(p: Params, sw: Switch) -> Part:
    """The U-shaped slot that frees the tab on its left, bottom and right.

    The ring of material around the tab is trimmed back to the hinge line, so
    the top edge stays joined and the tab swings from there.
    """
    s = p.flexure_slot
    ring = _tab_at(p, grow=s) - _tab_at(p)

    # Keep only the part of the ring at or below the hinge line at y = 0.
    below_hinge = Pos(0, -(p.button_height + s) / 2) * Rectangle(
        p.button_width + 2 * s + 2, p.button_height + s
    )

    solid = extrude(ring & below_hinge, p.thickness + 2)
    return Pos(sw.x, sw.y, -1) * solid


def flexure_hinge_relief(p: Params, sw: Switch) -> Part | None:
    """Thinning cut across the hinge line, taken from the back face."""
    depth = p.thickness - p.hinge_thickness
    if depth <= 0:
        return None
    relief = Box(p.button_width, p.hinge_band, depth, align=_BOTTOM)
    return Pos(sw.x, sw.y, 0) * relief


def flexure_pad(p: Params, sw: Switch) -> Part | None:
    """Bump raised on the tab so the button can be found through the label."""
    if p.flexure_pad_rise <= 0:
        return None
    pad = extrude(_tab_at(p, grow=-p.flexure_pad_inset), p.flexure_pad_rise)
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
    at = switch_point(p, sw)
    return at * Pos(0, 0, -1) * Cylinder(bore / 2, p.thickness + 2, align=_BOTTOM)


def cap(p: Params, sw: Switch) -> Part:
    """One loose button cap, modelled in place relative to the panel."""
    flange_d = p.button_width + 2 * p.cap_flange_width
    flange = Cylinder(flange_d / 2, p.cap_flange_thickness, align=_TOP)

    shaft = Cylinder(p.button_width / 2, p.thickness + p.cap_rise, align=_BOTTOM)
    top = shaft.edges().filter_by(GeomType.CIRCLE).sort_by(Axis.Z)[-1]
    shaft = fillet(top, radius=0.5)

    boss = Pos(0, 0, -p.cap_flange_thickness) * plunger(
        p, deduct=p.cap_flange_thickness
    )

    return switch_point(p, sw) * (flange + shaft + boss)
