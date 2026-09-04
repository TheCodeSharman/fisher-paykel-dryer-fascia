"""The fascia panel itself.

The original fascia is discarded entirely. This part screws straight to holes
drilled in the dryer's skin, which means it has to span the distance down to
the control board on its own. So it is a shallow tray, not a plate:

    flange  -----____                    ____-----   z = 0, on the dryer skin
                     |                  |
                     | wall             | wall
                     |__________________|
                        front plate                  z = -reach

The flange lands on the skin and takes the screws. The walls carry the front
plate down into the machine by `reach`, leaving `switch_gap` between the back
of the plate and the switch tops for the plungers to cross. The label goes on
the front plate, at the bottom of the well.

See `params` for the full coordinate system and dimension chain.
"""

from build123d import (
    Align,
    Cone,
    Cylinder,
    Part,
    Pos,
    RectangleRounded,
    Sketch,
    extrude,
)

from . import buttons
from .params import Led, Params, ScrewHole

FLEXURE = "flexure"
SEPARATE = "separate"
VARIANTS = (FLEXURE, SEPARATE)

_BOTTOM = (Align.CENTER, Align.CENTER, Align.MIN)
_SINK = (Align.CENTER, Align.CENTER, Align.MAX)


def _outline(width: float, height: float, radius: float) -> Sketch:
    """A rounded rectangle sitting with its bottom-left corner on the origin."""
    return Pos(width / 2, height / 2) * RectangleRounded(width, height, radius)


def _slab(width: float, height: float, radius: float, depth: float, z: float) -> Part:
    """A rounded-rectangle slab of `depth`, its underside at `z`."""
    return Pos(0, 0, z) * extrude(_outline(width, height, radius), depth)


def body(p: Params) -> Part:
    """The tray: flange, walls and front plate, before any features are cut."""
    inner_radius = max(p.corner_radius - p.body_inset, 1.0)

    # A solid block from the front plate up through the flange, then the flange
    # spread out around it, then the well hollowed back out of the top.
    trunk = _slab(
        p.body_width,
        p.body_height,
        inner_radius,
        depth=p.reach + p.flange_thickness,
        z=-p.reach,
    )
    trunk = Pos(p.body_inset, p.body_inset, 0) * trunk

    flange = _slab(p.width, p.height, p.corner_radius, p.flange_thickness, z=0)

    well = _slab(
        p.body_width - 2 * p.wall,
        p.body_height - 2 * p.wall,
        max(inner_radius - p.wall, 0.5),
        depth=p.reach - p.thickness + p.flange_thickness + 1,
        z=-p.reach + p.thickness,
    )
    well = Pos(p.body_inset + p.wall, p.body_inset + p.wall, 0) * well

    return (trunk + flange) - well


def label_recess(p: Params) -> Part:
    """Shallow pocket in the front face so the printed label sits flush."""
    m = p.body_inset + p.wall + p.label_recess_margin
    pocket = _slab(
        p.width - 2 * m,
        p.height - 2 * m,
        radius=2.0,
        depth=p.label_recess_depth,
        z=-p.reach + p.thickness - p.label_recess_depth,
    )
    return Pos(m, m, 0) * pocket


def countersunk_hole(p: Params, hole: ScrewHole) -> Part:
    """Clearance hole through the flange, countersunk at its outer face."""
    shank = Pos(0, 0, -1) * Cylinder(
        p.screw_shank / 2, p.flange_thickness + 2, align=_BOTTOM
    )

    # A 90-degree countersink drops 1mm for every 1mm of radius it gains.
    sink = Pos(0, 0, p.flange_thickness) * Cone(
        bottom_radius=p.screw_shank / 2,
        top_radius=p.screw_head / 2,
        height=(p.screw_head - p.screw_shank) / 2,
        align=_SINK,
    )
    return Pos(hole.x, hole.y, 0) * (shank + sink)


def light_post(p: Params, led: Led) -> Part | None:
    """Solid boss below one LED aperture, drilled out by `led_bezel` later.

    Once the tray stands the front plate off the board, light from one LED
    washes into its neighbours' apertures. A tube per LED keeps them separate.
    Built solid and drilled afterwards rather than as a ready-made tube, so it
    shares material with the plate instead of meeting it on a coincident face.

    Returns None when the plate is close enough to the board not to need one.
    """
    length = p.tunnel_length
    if length <= 0:
        return None

    post = Cylinder(
        p.led_body_bore / 2 + p.tunnel_wall, length + p.thickness, align=_BOTTOM
    )
    return Pos(led.x, led.y, -p.reach - length) * post


def led_bezel(p: Params, led: Led) -> Part:
    """Bore through the front plate and its light post: clearance, aperture,
    chamfer.

    The land of material left at the aperture keeps the hole reading as a bezel
    rather than a raw drilling.
    """
    face = -p.reach + p.thickness  # outer face of the front plate
    bore_top = face - p.led_aperture_land
    bore_bottom = -p.reach - max(p.tunnel_length, 0.0) - 1

    body_bore = Pos(0, 0, bore_bottom) * Cylinder(
        p.led_body_bore / 2, bore_top - bore_bottom, align=_BOTTOM
    )
    aperture = Pos(0, 0, bore_top) * Cylinder(
        led.aperture / 2, p.led_aperture_land + 1, align=_BOTTOM
    )
    chamfer = Pos(0, 0, face) * Cone(
        bottom_radius=led.aperture / 2,
        top_radius=led.aperture / 2 + p.led_chamfer,
        height=p.led_chamfer,
        align=_SINK,
    )
    return Pos(led.x, led.y, 0) * (body_bore + aperture + chamfer)


def make_panel(p: Params, variant: str = FLEXURE) -> Part:
    """Build the panel for one button strategy."""
    if variant not in VARIANTS:
        raise ValueError(f"unknown variant {variant!r}, expected one of {VARIANTS}")
    if p.reach < p.thickness:
        raise ValueError(
            f"reach {p.reach} is less than the front plate thickness {p.thickness}"
        )
    if p.switch_gap <= p.pre_travel:
        raise ValueError(
            f"switch_gap is {p.switch_gap}: the front plate would sit on the "
            f"switches. Reduce reach ({p.reach}) or recheck skin_to_switch "
            f"({p.skin_to_switch})."
        )

    part = body(p)

    if p.label_recess_depth > 0:
        part -= label_recess(p)

    for hole in p.screws:
        part -= countersunk_hole(p, hole)

    # Features in the front plate are modelled in plate-local coordinates,
    # where z runs 0 to `thickness`, then dropped to where the plate sits.
    to_plate = Pos(0, 0, -p.reach)

    # Posts go on solid, then every LED is drilled through plate and post in
    # one go, so no boolean ever has to resolve two coincident cylinders.
    for led in p.leds:
        post = light_post(p, led)
        if post is not None:
            part += post
    for led in p.leds:
        part -= led_bezel(p, led)

    for sw in p.switches:
        if variant == FLEXURE:
            part -= to_plate * buttons.flexure_slot(p, sw)
            relief = buttons.flexure_hinge_relief(p, sw)
            if relief is not None:
                part -= to_plate * relief
            pad = buttons.flexure_pad(p, sw)
            if pad is not None:
                part += to_plate * pad
            at = buttons.switch_point(p, sw)
            part += at * Pos(0, 0, -p.reach + p.thickness) * buttons.plunger(
                p, overlap=p.thickness
            )
        else:
            part -= to_plate * buttons.cap_aperture(p, sw)

    part.label = f"fascia-panel-{variant}"
    return part


def make_caps(p: Params) -> list[Part]:
    """The loose button caps for the `separate` variant, one per switch."""
    caps = []
    for sw in p.switches:
        c = Pos(0, 0, -p.reach) * buttons.cap(p, sw)
        c.label = f"button-cap-{sw.name}"
        caps.append(c)
    return caps
