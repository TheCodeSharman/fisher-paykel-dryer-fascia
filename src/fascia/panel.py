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

import math

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
    """The front plate, and the skirt behind it if there is one.

    A flat plate, not a tray. Its own perimeter is the flange that lands on the
    dryer skin and takes the screws, so nothing stands proud of the front face.
    Everything the panel adds -- skirt, plungers, light posts -- projects
    backwards, into the machine.
    """
    plate = _slab(p.width, p.height, p.corner_radius, p.thickness, z=-p.reach)
    if p.skirt_depth <= 0:
        return plate

    i = p.skirt_inset
    radius = max(p.corner_radius - i, 1.0)
    outer = _slab(
        p.width - 2 * i, p.height - 2 * i, radius, p.skirt_depth, z=-p.reach - p.skirt_depth
    )
    inner = _slab(
        p.width - 2 * i - 2 * p.skirt_wall,
        p.height - 2 * i - 2 * p.skirt_wall,
        max(radius - p.skirt_wall, 0.5),
        p.skirt_depth,
        z=-p.reach - p.skirt_depth,
    )
    skirt = Pos(i, i, 0) * outer - Pos(i + p.skirt_wall, i + p.skirt_wall, 0) * inner
    return plate + skirt


def label_recess(p: Params) -> Part:
    """Shallow pocket in the front face so the printed label sits flush."""
    m = p.label_recess_margin
    pocket = _slab(
        p.width - 2 * m,
        p.height - 2 * m,
        radius=max(p.corner_radius - m, 1.0),
        depth=p.label_recess_depth,
        z=-p.reach + p.thickness - p.label_recess_depth,
    )
    return Pos(m, m, 0) * pocket


def countersunk_hole(p: Params, hole: ScrewHole) -> Part:
    """Clearance hole through the flange, countersunk at its outer face."""
    shank = Pos(0, 0, -p.reach - 1) * Cylinder(
        p.screw_shank / 2, p.thickness + 2, align=_BOTTOM
    )

    # A 90-degree countersink drops 1mm for every 1mm of radius it gains.
    sink = Pos(0, 0, -p.reach + p.thickness) * Cone(
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


def _check_features_fit(p: Params) -> None:
    """Every button and LED has to land on the front plate, inside the walls.

    Easy to break by nudging the outline or the cluster offset, and the result
    is a hole cut through a wall or out across the flange, which is obvious in
    the viewer but easy to miss in a batch of exports.
    """
    x0 = y0 = p.edge_margin
    x1, y1 = p.width - x0, p.height - y0

    # Conservative and rotation-independent: the circle the tab opening fits in.
    half_w = (p.button_width + 2 * p.flexure_slot) / 2
    half_h = (p.button_height + 2 * p.flexure_slot) / 2
    tab_reach = (half_w**2 + half_h**2) ** 0.5
    post = p.led_body_bore / 2 + p.tunnel_wall

    strays = []
    for sw in p.placed_switches:
        if not (
            x0 + tab_reach <= sw.x <= x1 - tab_reach
            and y0 + tab_reach <= sw.y <= y1 - tab_reach
        ):
            strays.append(f"button {sw.name!r} at ({sw.x:.1f}, {sw.y:.1f})")
    for led in p.placed_leds:
        if not (x0 + post <= led.x <= x1 - post and y0 + post <= led.y <= y1 - post):
            strays.append(f"LED {led.name!r} at ({led.x:.1f}, {led.y:.1f})")

    if strays:
        raise ValueError(
            "these features come closer to the panel edge than edge_margin "
            "allows; the usable area spans "
            f"({x0:.1f}, {y0:.1f}) to ({x1:.1f}, {y1:.1f}): "
            + "; ".join(strays)
            + ". Widen the panel or move the cluster with cluster_x/cluster_y."
        )


def _check_no_overlaps(p: Params) -> None:
    """No LED may land in a button's opening.

    Not covered by the single-body check: an LED bored through a tab does not
    cut anything free, it just puts a hole in the tab. The result is valid
    geometry and a useless part, so it has to be tested for directly.
    """
    half_w = p.button_width / 2 + p.flexure_slot
    post = p.led_body_bore / 2 + p.tunnel_wall

    clashes = []
    for sw in p.placed_switches:
        angle = math.radians(sw.rotation)
        cos_a, sin_a = math.cos(-angle), math.sin(-angle)
        for led in p.placed_leds:
            dx, dy = led.x - sw.x, led.y - sw.y
            # Into the tab's own frame: hinge at the origin, tab down -y.
            lx = dx * cos_a - dy * sin_a
            ly = dx * sin_a + dy * cos_a
            inside_x = abs(lx) <= half_w + post
            inside_y = -(p.button_height + p.flexure_slot) - post <= ly <= p.flexure_slot / 2 + post
            if inside_x and inside_y:
                clashes.append(f"LED {led.name!r} sits in button {sw.name!r}'s opening")

    if clashes:
        raise ValueError("; ".join(clashes))


def make_panel(p: Params, variant: str = FLEXURE) -> Part:
    """Build the panel for one button strategy."""
    if variant not in VARIANTS:
        raise ValueError(f"unknown variant {variant!r}, expected one of {VARIANTS}")
    if p.reach < 0:
        raise ValueError(
            f"reach {p.reach} is negative, which would stand the plate off the "
            f"dryer skin with nothing under it"
        )
    if p.switch_gap <= p.pre_travel:
        raise ValueError(
            f"switch_gap is {p.switch_gap}: the front plate would sit on the "
            f"switches. Reduce reach ({p.reach}) or recheck skin_to_switch "
            f"({p.skin_to_switch})."
        )

    _check_features_fit(p)
    _check_no_overlaps(p)

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
    for led in p.placed_leds:
        post = light_post(p, led)
        if post is not None:
            part += post
    for led in p.placed_leds:
        part -= led_bezel(p, led)

    for sw in p.placed_switches:
        if variant == FLEXURE:
            part -= to_plate * buttons.flexure_slot(p, sw)
            relief = buttons.flexure_relief(p, sw)
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

    solids = part.solids()
    if len(solids) != 1:
        biggest = max(s.volume for s in solids)
        raise ValueError(
            f"the {variant} panel came out as {len(solids)} separate bodies, not "
            f"one. Something has been cut free: the largest is {biggest:.0f} mm3 "
            f"of {part.volume:.0f}. Usually a button tab overlapping an LED, or "
            f"a feature crossing a wall. An STL like this looks fine in a viewer "
            f"and slices into nonsense."
        )

    part.label = f"fascia-panel-{variant}"
    return part


def make_caps(p: Params) -> list[Part]:
    """The loose button caps for the `separate` variant, one per switch."""
    caps = []
    for sw in p.placed_switches:
        c = Pos(0, 0, -p.reach) * buttons.cap(p, sw)
        c.label = f"button-cap-{sw.name}"
        caps.append(c)
    return caps
