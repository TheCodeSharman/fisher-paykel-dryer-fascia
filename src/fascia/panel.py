"""The fascia panel itself.

The original fascia is discarded. This part screws straight to holes drilled in
the dryer's front face, and the PCB is flush with that face with its switch
posts standing proud of it. So the plate cannot lie on the face: it is carried
clear of the posts on walls, with a lip returning to the face for the screws.

        ______________________________  front plate, at plate_standoff
       |                              |
    ___|                              |___    walls
   |___    ____________________________   |__ lip, on the dryer face, z = 0
       |  |                            |  |
       |  |  switch posts, 8.95 proud  |  |
   ========================================== dryer front face, PCB flush

Everything the plate carries -- plungers, light posts -- hangs off its back
into that space. See `params` for the coordinate system: z = 0 is the dryer's
front face and grows towards you.
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
    """Plate, walls and lip, before any features are cut.

    Hollow: the switch posts and the LEDs live in the space the walls enclose.
    """
    plate = _slab(p.width, p.height, p.corner_radius, p.thickness, z=p.plate_standoff)

    walls = _slab(p.width, p.height, p.corner_radius, p.plate_standoff, z=0)

    lip = Pos(-p.lip_width, -p.lip_width, 0) * _slab(
        p.width + 2 * p.lip_width,
        p.height + 2 * p.lip_width,
        p.corner_radius + p.lip_width,
        p.lip_thickness,
        z=0,
    )

    hollow = Pos(p.wall, p.wall, 0) * _slab(
        p.width - 2 * p.wall,
        p.height - 2 * p.wall,
        max(p.corner_radius - p.wall, 0.5),
        p.plate_standoff,
        z=0,
    )

    return (plate + walls + lip) - hollow


def label_recess(p: Params) -> Part:
    """Shallow pocket in the front face so the printed label sits flush."""
    m = p.label_recess_margin
    pocket = _slab(
        p.width - 2 * m,
        p.height - 2 * m,
        radius=max(p.corner_radius - m, 1.0),
        depth=p.label_recess_depth,
        z=p.plate_standoff + p.thickness - p.label_recess_depth,
    )
    return Pos(m, m, 0) * pocket


def countersunk_hole(p: Params, hole: ScrewHole) -> Part:
    """Clearance hole through the lip, countersunk on the side facing out."""
    shank = Pos(0, 0, -1) * Cylinder(
        p.screw_shank / 2, p.lip_thickness + 2, align=_BOTTOM
    )

    # A 90-degree countersink drops 1mm for every 1mm of radius it gains.
    sink = Pos(0, 0, p.lip_thickness) * Cone(
        bottom_radius=p.screw_shank / 2,
        top_radius=p.screw_head / 2,
        height=(p.screw_head - p.screw_shank) / 2,
        align=_SINK,
    )
    return Pos(hole.x, hole.y, 0) * (shank + sink)


def light_post(p: Params, led: Led) -> Part | None:
    """Solid boss below one LED hole, bored out by `led_bezel` afterwards.

    Once the plate stands off the board, light from one LED washes into its
    neighbours' holes. A tube per LED keeps them apart. Built solid and drilled
    later rather than as a ready-made tube, so it shares material with the
    plate instead of meeting it on a coincident face.

    Returns None when the plate is close enough to the board not to need one.
    """
    length = p.tunnel_length
    if length <= 0:
        return None

    post = Cylinder(
        led.aperture / 2 + p.tunnel_wall, length + p.thickness, align=_BOTTOM
    )
    return Pos(led.x, led.y, p.plate_standoff - length) * post


def led_bezel(p: Params, led: Led) -> Part:
    """The hole, the counterbore in front of it, and a chamfer on that.

    Two diameters, not one: a narrow hole for the LED to sit in, opening out
    into a wider counterbore at the face. The counterbore is what is seen and
    what the label is drawn around.
    """
    face = p.plate_standoff + p.thickness
    bottom = p.plate_standoff - max(p.tunnel_length, 0.0) - 1

    bore = Pos(0, 0, bottom) * Cylinder(led.aperture / 2, face - bottom, align=_BOTTOM)

    # The counterbore is what is seen from the front; the hole behind it only
    # has to clear the LED.
    counterbore = Pos(0, 0, face) * Cylinder(
        p.led_counterbore / 2, p.led_counterbore_depth, align=_SINK
    )
    chamfer = Pos(0, 0, face) * Cone(
        bottom_radius=p.led_counterbore / 2,
        top_radius=p.led_counterbore / 2 + p.led_chamfer,
        height=p.led_chamfer,
        align=_SINK,
    )
    return Pos(led.x, led.y, 0) * (bore + counterbore + chamfer)


def _check_features_fit(p: Params) -> None:
    """Every button and LED has to land on the plate, clear of its edge.

    Easy to break by nudging the outline or the cluster offset, and the result
    is a hole cut through the border the screws land in, which is obvious in
    the viewer but easy to miss in a batch of exports.
    """
    x0 = y0 = p.wall + p.edge_margin
    x1, y1 = p.width - x0, p.height - y0

    # Conservative and rotation-independent: the circle the tab opening fits in.
    half_w = (p.button_width + 2 * p.flexure_slot) / 2
    half_h = (p.button_height + 2 * p.flexure_slot) / 2
    tab_reach = (half_w**2 + half_h**2) ** 0.5

    strays = []
    for sw in p.placed_switches:
        if not (
            x0 + tab_reach <= sw.x <= x1 - tab_reach
            and y0 + tab_reach <= sw.y <= y1 - tab_reach
        ):
            strays.append(f"button {sw.name!r} at ({sw.x:.1f}, {sw.y:.1f})")
    for led in p.placed_leds:
        post = p.led_footprint
        if not (x0 + post <= led.x <= x1 - post and y0 + post <= led.y <= y1 - post):
            strays.append(f"LED {led.name!r} at ({led.x:.1f}, {led.y:.1f})")

    if strays:
        raise ValueError(
            "these features come closer to the panel edge than edge_margin "
            f"allows; the usable area spans ({x0:.1f}, {y0:.1f}) to "
            f"({x1:.1f}, {y1:.1f}): " + "; ".join(strays)
            + ". Widen the panel or move the cluster with cluster_x/cluster_y."
        )


def _check_no_overlaps(p: Params) -> None:
    """No LED may land in a button's opening.

    Not covered by the single-body check: an LED bored through a tab does not
    cut anything free, it just puts a hole in the tab. The result is valid
    geometry and a useless part, so it has to be tested for directly.
    """
    half_w = p.button_width / 2 + p.flexure_slot

    clashes = []
    for sw in p.placed_switches:
        angle = math.radians(sw.rotation)
        cos_a, sin_a = math.cos(-angle), math.sin(-angle)
        for led in p.placed_leds:
            post = p.led_footprint
            dx, dy = led.x - sw.x, led.y - sw.y
            # Into the tab's own frame: hinge at the origin, tab down -y.
            lx = dx * cos_a - dy * sin_a
            ly = dx * sin_a + dy * cos_a
            inside_x = abs(lx) <= half_w + post
            inside_y = (
                -(p.button_height + p.flexure_slot) - post
                <= ly
                <= p.flexure_slot / 2 + post
            )
            if inside_x and inside_y:
                clashes.append(f"LED {led.name!r} sits in button {sw.name!r}'s opening")

    if clashes:
        raise ValueError("; ".join(clashes))


def make_panel(p: Params, variant: str = FLEXURE) -> Part:
    """Build the panel for one button strategy."""
    if variant not in VARIANTS:
        raise ValueError(f"unknown variant {variant!r}, expected one of {VARIANTS}")
    if p.plunger_length <= 0:
        raise ValueError(f"plunger_length {p.plunger_length} is not positive")
    if p.tunnel_length >= p.plate_standoff:
        raise ValueError(
            f"a light tunnel {p.tunnel_length} long would reach past the dryer "
            f"face, which is {p.plate_standoff} below the plate"
        )

    _check_features_fit(p)
    _check_no_overlaps(p)

    part = body(p)

    if p.label_recess_depth > 0:
        part -= label_recess(p)

    for hole in p.placed_screws:
        part -= countersunk_hole(p, hole)

    # Features in the front plate are modelled in plate-local coordinates,
    # where z runs 0 to `thickness`, then dropped to where the plate sits.
    to_plate = Pos(0, 0, p.plate_standoff)

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
            part += at * Pos(0, 0, p.plate_standoff + p.thickness) * buttons.plunger(
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
        c = Pos(0, 0, p.plate_standoff) * buttons.cap(p, sw)
        c.label = f"button-cap-{sw.name}"
        caps.append(c)
    return caps
