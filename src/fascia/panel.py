"""The fascia panel itself.

Only the strip around the control board is replaced, not the whole dryer
fascia. The panel is a flat plate that covers the opening, is screwed into the
remains of the original fascia, carries the buttons and LED bezels, and has a
flat front for a printed label.

See `params` for the coordinate system: origin at the bottom-left corner of the
panel, +Z out of the front face.
"""

from build123d import Align, Axis, Box, Cone, Cylinder, Part, Pos, fillet

from . import buttons
from .params import Led, Params, ScrewHole

FLEXURE = "flexure"
SEPARATE = "separate"
VARIANTS = (FLEXURE, SEPARATE)

_CORNER = (Align.MIN, Align.MIN, Align.MIN)
_BOTTOM = (Align.CENTER, Align.CENTER, Align.MIN)
_SINK = (Align.CENTER, Align.CENTER, Align.MAX)


def blank(p: Params) -> Part:
    """The plate with its corners rounded, before any features are cut."""
    plate = Box(p.width, p.height, p.thickness, align=_CORNER)
    return fillet(plate.edges().filter_by(Axis.Z), radius=p.corner_radius)


def label_recess(p: Params) -> Part:
    """Shallow pocket in the front face so the printed label sits flush."""
    m = p.label_recess_margin
    pocket = Box(p.width - 2 * m, p.height - 2 * m, p.label_recess_depth, align=_CORNER)
    pocket = fillet(
        pocket.edges().filter_by(Axis.Z), radius=max(p.corner_radius - m, 0.5)
    )
    return Pos(m, m, p.thickness - p.label_recess_depth) * pocket


def countersunk_hole(p: Params, hole: ScrewHole) -> Part:
    """Clearance hole with a countersink opening out at the front face."""
    shank = Pos(0, 0, -1) * Cylinder(p.screw_shank / 2, p.thickness + 2, align=_BOTTOM)

    # A 90-degree countersink drops 1mm for every 1mm of radius it gains.
    sink = Pos(0, 0, p.thickness) * Cone(
        bottom_radius=p.screw_shank / 2,
        top_radius=p.screw_head / 2,
        height=(p.screw_head - p.screw_shank) / 2,
        align=_SINK,
    )
    return Pos(hole.x, hole.y, 0) * (shank + sink)


def led_bezel(p: Params, led: Led) -> Part:
    """Bore for one LED: body clearance behind, a small aperture, a chamfer.

    The land of material left at the aperture keeps the hole reading as a bezel
    rather than a raw drilling, and stops the LED poking through.
    """
    bore_depth = p.thickness - p.led_aperture_land
    body = Pos(0, 0, -1) * Cylinder(p.led_body_bore / 2, bore_depth + 1, align=_BOTTOM)

    aperture = Pos(0, 0, bore_depth) * Cylinder(
        led.aperture / 2, p.led_aperture_land + 1, align=_BOTTOM
    )

    chamfer = Pos(0, 0, p.thickness) * Cone(
        bottom_radius=led.aperture / 2,
        top_radius=led.aperture / 2 + p.led_chamfer,
        height=p.led_chamfer,
        align=_SINK,
    )
    return Pos(led.x, led.y, 0) * (body + aperture + chamfer)


def make_panel(p: Params, variant: str = FLEXURE) -> Part:
    """Build the panel for one button strategy."""
    if variant not in VARIANTS:
        raise ValueError(f"unknown variant {variant!r}, expected one of {VARIANTS}")

    part = blank(p)

    if p.label_recess_depth > 0:
        part -= label_recess(p)

    for hole in p.screws:
        part -= countersunk_hole(p, hole)

    for led in p.leds:
        part -= led_bezel(p, led)

    for sw in p.switches:
        if variant == FLEXURE:
            part -= buttons.flexure_slot(p, sw)
            relief = buttons.flexure_hinge_relief(p, sw)
            if relief is not None:
                part -= relief
            pad = buttons.flexure_pad(p, sw)
            if pad is not None:
                part += pad
            part += Pos(sw.x, sw.y, 0) * buttons.plunger(p, sw)
        else:
            part -= buttons.cap_aperture(p, sw)

    part.label = f"fascia-panel-{variant}"
    return part


def make_caps(p: Params) -> list[Part]:
    """The loose button caps for the `separate` variant, one per switch."""
    caps = []
    for sw in p.switches:
        c = buttons.cap(p, sw)
        c.label = f"button-cap-{sw.name}"
        caps.append(c)
    return caps
