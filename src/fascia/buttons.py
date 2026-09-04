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
    Circle,
    Cylinder,
    GeomType,
    Location,
    Part,
    Pos,
    Rotation,
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

    Its free length is measured, not derived: `plunger_length`. `deduct`
    accounts for anything standing between the plate and the start of the boss,
    such as a button cap's flange.

    `overlap` extends the boss further back into the part it grows from, so the
    two share solid material rather than meeting on a single coincident face.
    Touching faces make for fragile booleans and multi-body STLs.
    """
    length = p.plunger_length - deduct
    if length <= 0:
        raise ValueError(
            f"a plunger_length of {p.plunger_length} leaves nothing once "
            f"{deduct} of anything else is taken out"
        )
    return Cylinder(p.plunger / 2, length + overlap, align=_TOP)


# ---------------------------------------------------------------------------
# flexure variant: the original trapdoor tab
# ---------------------------------------------------------------------------


def _tab_outline(p: Params, grow: float = 0.0) -> Sketch:
    """The tab profile, hinge line on y = 0, hanging down the negative y axis.

    Straight parallel sides and a semicircular free end. Only that end is
    rounded: at the hinge the tab simply merges into the panel, so rounding
    there would pull the slot legs inwards instead of letting them run straight
    up to their end caps.

    `grow` offsets the whole profile outwards, which is how the slot is built.
    The free end's centre does not move under that, so the gap stays even all
    the way round, as the original's does.
    """
    radius = p.tab_end_radius + grow
    if radius <= 0:
        raise ValueError(
            f"a tab {p.button_width} wide cannot be grown by {grow}: that "
            f"leaves an end radius of {radius}"
        )

    end_centre = -(p.button_height - p.tab_end_radius)
    top = grow
    if top <= end_centre:
        raise ValueError(
            f"growing a {p.button_height} tab by {grow} collapses it: the "
            f"straight part would run from {top} down to {end_centre}"
        )

    body = Pos(0, (top + end_centre) / 2) * Rectangle(2 * radius, top - end_centre)
    return body + Pos(0, end_centre) * Circle(radius)


def _place(sw: Switch) -> Location:
    """Put local tab geometry where the switch is, turned the way it sits.

    Tab geometry is built with its hinge line on the origin and the tab hanging
    down the negative y axis. Most buttons sit that way up; the keylock is
    turned on its side, so it swings sideways instead.
    """
    return Pos(sw.x, sw.y) * Rotation(0, 0, sw.rotation)


def switch_point(p: Params, sw: Switch) -> Location:
    """Where the plunger lands: below the hinge line by `plunger_drop`.

    Not the same as the tab centre in general. How far the actuator sits from
    the hinge sets the leverage, so it is a parameter rather than an assumption.
    Follows the tab round when the button is rotated.
    """
    return _place(sw) * Pos(0, -p.plunger_drop, 0)


def flexure_slot(p: Params, sw: Switch) -> Part:
    """The U-shaped slot that frees the tab on its left, bottom and right.

    The ring of material around the tab is trimmed back to the hinge line, so
    the top stays joined and the tab swings from there.

    The two legs do not stop square at the hinge line. They run on and finish
    in rounded ends centred on it, half a slot width past, as the original
    does. That is not decoration: a square internal corner at the end of a slot
    is a stress raiser sitting exactly where the hinge works hardest, and this
    part has to survive years of pressing.
    """
    s = p.flexure_slot
    ring = _tab_outline(p, grow=s) - _tab_outline(p)

    # Everything below the hinge line, plus a round end cap on each leg
    # straddling it.
    below_hinge = Pos(0, -(p.button_height + s) / 2) * Rectangle(
        p.button_width + 2 * s + 2, p.button_height + s
    )
    leg_x = p.button_width / 2 + s / 2
    caps = Pos(leg_x, 0) * Circle(s / 2) + Pos(-leg_x, 0) * Circle(s / 2)

    solid = extrude(ring & (below_hinge + caps), p.thickness + 2)
    return _place(sw) * Pos(0, 0, -1) * solid


def flexure_relief(p: Params, sw: Switch) -> Part | None:
    """Recess the tab from the *front*, leaving the bump standing at the face.

    Two jobs at once. It thins the tab to `tab_thickness` so it can bend at all
    -- a tab at full panel thickness barely moves and forces everything into
    whatever line was thinned, which is where it would crack. And it drops the
    tab's face below the panel's, so the label spans the recess and touches
    only the panel and the bump. Bonded flat across the whole tab, the
    adhesive would fight the tab every press and tear along the slot.

    The bump is not added: it is what is left behind when the recess is cut
    around it, so it cannot drift out of register with the tab.

    Prints face down. The tab flat is anchored at the hinge and lands on the
    bump, so it bridges a few mm between two supported points rather than
    hanging unsupported off the bump.
    """
    depth = p.thickness - p.tab_thickness
    if depth <= 0:
        return None

    # Out to the slot's outer edge, which is the tab and nothing else, and
    # stopping at the hinge line. Growing the outline to reach the slot also
    # pushes it above that line, and thinning the panel there would let it
    # flex along with the tab, so the overshoot is trimmed off.
    top = p.hinge_band
    span = p.button_height + 2 * p.flexure_slot + top
    region = _tab_outline(p, grow=p.flexure_slot) & Pos(
        0, top - span / 2
    ) * Rectangle(p.button_width + 4 * p.flexure_slot + 2, span)

    region -= Pos(0, -p.plunger_drop) * Circle(p.pad_diameter / 2)
    relief = Pos(0, 0, p.tab_thickness) * extrude(region, depth)

    if p.hinge_band > 0 and p.hinge_gauge < p.tab_thickness:
        band = Pos(0, p.hinge_band / 2) * Rectangle(
            p.button_width + 2 * p.flexure_slot, p.hinge_band
        )
        relief += Pos(0, 0, p.hinge_gauge) * extrude(band, p.thickness - p.hinge_gauge)

    return _place(sw) * relief


def flexure_pad(p: Params, sw: Switch) -> Part | None:
    """Extra height on the bump, standing it proud of the panel face.

    None by default. The bump already comes out flush, left standing by the
    recess cut around it, which is what the original does. This only adds more,
    and it cannot print with the front face on the bed, so it means flipping
    the part in the slicer. Worth trying only if the buttons prove hard to find
    by feel through the label.
    """
    if p.flexure_pad_rise <= 0:
        return None
    pad = extrude(Circle(p.pad_diameter / 2), p.flexure_pad_rise)
    pad = fillet(
        pad.edges().group_by(Axis.Z)[-1], radius=min(0.4, p.flexure_pad_rise / 2.5)
    )
    return switch_point(p, sw) * Pos(0, 0, p.thickness) * pad


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
