"""Every measured or chosen dimension lives here. Nothing else hard-codes a number.

Units are millimetres throughout.

Coordinate system
-----------------
Looking at the front of the panel, the side you see standing at the dryer:

    X  -> right
    Y  -> up
    Z  -> out of the machine, towards you

X and Y have their origin at the bottom-left corner of the panel outline, so
feature positions can be taken straight off the calipers as offsets from that
corner.

**z = 0 is the dryer's front face**, the surface the lip is screwed down onto.
The PCB is flush with it and the switch posts stand *proud* of it, so
everything of interest is at positive z, growing towards you.

That is what shapes the part. The plate cannot lie on the face, because the
switch posts are in the way; it is held clear of them on walls, with a lip
returning to the face to take the screws. `plate_standoff` is where the plate's
back face has to sit, and it falls out of the measurements rather than being
chosen.

Values marked PLACEHOLDER are guesses, sized so the model builds and can be
eyeballed in the viewer. Replace them with real caliper readings and record how
each one was taken in reference/measurements.md.
"""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Switch:
    """A button, positioned by the hinge line of its tab.

    `y` is the **hinge line**, not the tab centre and not the switch itself.
    The tab hangs down from there, matching the original, and the actuator sits
    `plunger_drop` below it. Measuring the hinge line is what the old fascia
    makes easy, so that is what the model asks for.
    """

    name: str
    x: float
    y: float
    #: Degrees anticlockwise. Turns which way the tab swings: 0 hangs down from
    #: a hinge along its top, 90 swings sideways. The keylock is the odd one.
    rotation: float = 0.0


@dataclass(frozen=True)
class Led:
    """An indicator LED that needs a bezel hole through the panel."""

    name: str
    x: float
    y: float
    #: Diameter of the hole the LED sits in. The visible bezel is the wider
    #: counterbore in front of it, not this.
    aperture: float = 3.3


@dataclass(frozen=True)
class ScrewHole:
    """A hole through the flange, into a hole drilled in the dryer."""

    name: str
    x: float
    y: float


# ---------------------------------------------------------------------------
# Board features, in **cluster coordinates**: x from the centre of the
# left-most tab, y from the button hinge line, +y up. Readings off the old
# fascia go in here raw; `cluster_x` and `cluster_y` place the whole group on
# the panel, so no measurement has to be converted by hand.
#
# The stack runs, top to bottom: hinge line, tabs hanging down from it, then
# the LED row below them. So tabs and LEDs both sit at negative y.
#
# Names come from the original printed label. Positions are still PLACEHOLDER.
# ---------------------------------------------------------------------------

def _row(names: tuple[str, ...], pitches: tuple[float, ...], y: float) -> tuple:
    """Lay names out along x from cumulative centre-to-centre pitches.

    Positions come from pitches rather than absolute offsets because that is
    how they are measured: the row is longer than a caliper, so each feature is
    measured from its neighbour. Storing the readings and summing them here
    keeps arithmetic out of the worksheet.
    """
    x = 0.0
    out = []
    for i, name in enumerate(names):
        if i:
            x += pitches[i - 1]
        out.append((name, x, y))
    return tuple(out)


#: Left to right in the readable frame. Not the order first assumed from the
#: label photo, which had it backwards. It is the measured 3 | 2 | 3 grouping
#: that confirms this one: wrinkle guard falls in with the temperature pair,
#: and start/pause, power and delay start make the three at the far end.
#:
#: Which of each pair is up and which is down is still a guess.
_BUTTON_NAMES = (
    "wrinkle_guard",
    "temp_up",
    "temp_down",
    "dryness_up",
    "dryness_down",
    "start_pause",
    "power",
    "delay_start",
)

#: Centre to centre along the button row, left to right. Measured opening edge
#: to opening edge, which is the same thing since every opening is identical.
#:
#: All measured. The two large values are the gaps between groups, so the row
#: runs 3 | 2 | 3, not the 3/2/2/1 the label photo suggested. The outer groups
#: share their internal spacing exactly, 20.58 then 16.98, which is a good sign
#: the readings are sound.
#:
#: The names below remain the weaker part of this: the positions are measured,
#: which button sits at each is read off a photo.
_BUTTON_PITCHES = (
    20.58,  # B1 -> B2, measured
    16.98,  # B2 -> B3, measured
    25.06,  # B3 -> B4, measured
    16.98,  # B4 -> B5, measured, same as B2 -> B3
    28.23,  # B5 -> B6, measured, across to temperature
    20.58,  # B6 -> B7, measured, same as B1 -> B2
    16.98,  # B7 -> B8, measured, same as B2 -> B3
)

_SWITCHES = tuple(
    Switch(name, x, y) for name, x, y in _row(_BUTTON_NAMES, _BUTTON_PITCHES, 0.0)
)

#: The row sits 23.29 below the button hinge line, measured.
#: The LED row, 13 across, grouped 1 | 3 | 4 | 1 | [keylock tab] | 1 | 3, with
#: that last three sitting very close together. Named positionally on purpose:
#: which label belongs to which is still to be confirmed, and reading them off
#: a photo has already produced one wrong grouping.
_LED_NAMES = tuple(f"led{i:02d}" for i in range(1, 14))

#: Centre to centre along the row, all measured. No two groups share a
#: spacing: 11.54 inside the three, 10.91 inside the four, 5.98 inside the
#: close-set three at the end.
_LED_PITCHES = (
    19.34,  # led01 -> led02, measured, the gap after the lone first LED
    11.54,  # led02 -> led03, measured, inside the group of three
    11.54,  # led03 -> led04, measured, same as the last
    16.89,  # led04 -> led05, measured, the gap across to the group of four
    10.91,  # led05 -> led06, measured, inside the group of four
    10.91,  # led06 -> led07, measured, same again
    10.91,  # led07 -> led08, measured, closes the group of four
    28.65,  # led08 -> led09, measured, the gap to the lone LED
    20.20,  # led09 -> led10, APPROXIMATE: spans the keylock, and the hole
            # is clipped on its left edge so the reading is a guess
    8.44,  # led10 -> led11, measured, across to the close-set three
    5.0,
    5.98,  # led11 -> led12, measured, the close-set three
    5.98,  # led12 -> led13, measured, same again
)

_LEDS = tuple(
    Led(name, x, y) for name, x, y in _row(_LED_NAMES, _LED_PITCHES, -23.29)
)

#: The keylock tab sits in the LED row, between the lone LED at index 8 and the
#: one at index 9. Derived from them rather than measured separately, so it
#: cannot drift out of the row when their spacings are corrected.
#:
#: Turned on its side, the tab runs off its hinge along +x, so the hinge is set
#: back half a tab length to leave it centred in the gap. PLACEHOLDER, like the
#: spacings it comes from, and the hinge edge is still unconfirmed.
_KEYLOCK_X = (_LEDS[8].x + _LEDS[9].x) / 2 - 10.57 / 2

_SWITCHES = _SWITCHES[:8] + (
    # Hinged on its left edge, which is the one with no slot, so the tab runs
    # off to the right. Confirmed on the part.
    Switch("keylock", _KEYLOCK_X, _LEDS[8].y, rotation=90.0),
)


@dataclass(frozen=True)
class Params:
    # ------------------------------------------------------------------
    # Outline. The flange footprint is what you see from outside.
    # ------------------------------------------------------------------
    #: PLACEHOLDER. Provisionally the original fascia's height, F9 + F10, so
    #: the preview is proportioned like the real thing. What actually bounds
    #: the outline is the flat metal around the opening on the machine.
    width: float = 240.0  # PLACEHOLDER
    height: float = 96.72  # PLACEHOLDER, = 41.14 + 55.58
    corner_radius: float = 4.0

    #: The front plate that carries the buttons, LEDs and label. The original
    #: measured 2.73 on its return edge; rounded up to 14 layers at 0.2 so the
    #: slicer is not left with a part layer to fudge.
    thickness: float = 2.8
    #: How close a feature may come to the inside of the walls.
    edge_margin: float = 4.0
    #: The walls carrying the plate clear of the switch posts.
    wall: float = 2.5
    #: The lip at their base, lying on the dryer's front face and taking the
    #: screws. It stands out beyond the panel so a screwdriver can reach.
    lip_width: float = 9.0
    lip_thickness: float = 2.4

    # ------------------------------------------------------------------
    # Depth. All three measured, so the standoff is not a judgement call.
    #
    #   switch_height   the switch posts, proud of the dryer's front face
    #   plunger_length  the prong on the back of each tab
    #   plate_standoff  where the plate's back face lands (derived)
    # ------------------------------------------------------------------
    #: The PCB is flush with the dryer's front face and the switch posts stand
    #: this far proud of it.
    switch_height: float = 8.95
    #: The prong on the back of each tab, taken from the original.
    plunger_length: float = 3.19
    #: How far a light tunnel stands off the back of the plate, also from the
    #: original. Shorter than the prongs, not longer as the photo suggested.
    tunnel_length: float = 2.64

    # ------------------------------------------------------------------
    # Label
    # ------------------------------------------------------------------
    #: Shallow recess in the front face so the printed label sits flush.
    #:
    #: Zero, and it has to be. The front face prints on the bed, so a pocket
    #: across it would leave the first layers as nothing but the border, and
    #: the whole label area would then try to bridge that span in one go. A
    #: printed label is a couple of tenths thick and can simply sit proud.
    #: Only revisit this if the part is ever printed face up.
    label_recess_depth: float = 0.0
    label_recess_margin: float = 2.0  # bare plastic left inside the well

    # ------------------------------------------------------------------
    # Fasteners: through the flange into holes drilled in the dryer
    # ------------------------------------------------------------------
    screw_shank: float = 3.4  # clearance hole for an M3 / #6 self-tapper
    screw_head: float = 6.4  # countersunk head diameter at the front face
    #: Empty means the four derived below. Positions are in panel coordinates,
    #: so the lip band is at negative x/y and beyond width/height.
    screws: tuple[ScrewHole, ...] = ()

    # ------------------------------------------------------------------
    # Board features
    # ------------------------------------------------------------------
    switches: tuple[Switch, ...] = field(default_factory=lambda: _SWITCHES)
    leds: tuple[Led, ...] = field(default_factory=lambda: _LEDS)

    #: Where the cluster datum (left-most tab's left edge, on the hinge line)
    #: sits in panel coordinates. Slides the whole group about without
    #: disturbing a single measurement. PLACEHOLDER.
    cluster_x: float = 25.0  # PLACEHOLDER
    cluster_y: float = 55.58  # puts the hinge line 41.14 below the top, as F9

    # ------------------------------------------------------------------
    # LED bezels and light tunnels
    #
    # Once the front plate stands off the board, light from one LED will wash
    # into its neighbours' apertures. A tube per LED, dropping from the back of
    # the front plate down towards the board, keeps them separate.
    # ------------------------------------------------------------------
    led_chamfer: float = 0.6
    tunnel_wall: float = 1.0
    #: A counterbore in the front face, wider than the hole behind it. This is
    #: what reads as the bezel, and mistaking the hole for it is what made the
    #: gaps between LEDs look too wide.
    led_counterbore: float = 5.66
    #: PLACEHOLDER: how deep that counterbore goes.
    led_counterbore_depth: float = 1.0

    # ------------------------------------------------------------------
    # Buttons: shared
    # ------------------------------------------------------------------
    button_width: float = 5.75  # measured, F4 refined
    button_height: float = 10.57  # measured, F5
    #: Boss on the back of the button that reaches down to the switch. It has
    #: to fit inside a tab only 5.63 wide, and land on the switch actuator, so
    #: check it against both. PLACEHOLDER until the actuator is measured.
    plunger: float = 3.5
    #: Gap left between the plunger tip and the switch actuator at rest, so the
    #: panel does not hold the switches half-pressed.
    pre_travel: float = 0.5
    #: How far the switch actuator moves to click. PLACEHOLDER: typical for a
    #: tactile switch, but this one is from 1997 and should be measured.
    switch_travel: float = 0.25
    #: How far below the hinge line the plunger sits. Further down means more
    #: leverage and a lighter press. None puts it at the middle of the tab.
    #:
    #: None puts it at the centre of the tab's lower end cap, which is where
    #: the original's bump sits: same radius as the tab, tangent to the free
    #: end. Set a number to override.
    plunger_offset: float | None = None

    # ------------------------------------------------------------------
    # Buttons: "flexure" variant, replicating the original F&P design.
    #
    # A tab is cut free on three sides by a U-shaped slot and stays joined
    # along its top edge, so it swings down like a trapdoor. The printed label
    # bridges the slot and doubles as the seal and the cushion.
    # ------------------------------------------------------------------
    #: Width of the slot cut around the tab.
    #:
    #: The original measures 2.41 (F6), which is an injection-moulding
    #: constraint: the tool needs steel of some thickness between tab and
    #: panel. Printing has no such constraint, only that the gap separates
    #: reliably on the bed and that the label can bridge it, so this is three
    #: nozzle widths instead. Open it back out towards 2.41 if the tabs come
    #: off the bed fused to the panel.
    flexure_slot: float = 1.2
    #: What the tab is thinned to, over its whole length. This is the flexure:
    #: the original's tab flat sits 1.73 below a bump that is flush with the
    #: face, so on a 2.73 panel the tab is about 1.0 thick. A full-thickness
    #: tab with one thinned line across it forces all the bending into that
    #: line; the original spreads it along a thin tab.
    #:
    #: Recessed from the *front*, as the original is, so the label spans the
    #: recess and touches only the panel face and the bump. The recess depth
    #: falls out as `thickness - tab_thickness`, and what is left standing in
    #: the middle is the bump.
    tab_thickness: float = 1.0
    #: How far the thinning runs past the hinge line into the panel.
    #:
    #: Zero: the relief stops at the hinge. Carrying it into the panel thins
    #: the very material that has to hold the hinge still, so the panel flexes
    #: along with the tab and the press goes soft. The original does the
    #: opposite and leaves that area full thickness. Kept as a knob because a
    #: little relief may yet prove to soften the action usefully.
    hinge_band: float = 0.0
    #: Thickness across the hinge band itself. None keeps it the same as the
    #: tab, which is what the original does. Thinner is a softer action, and is
    #: the first knob to turn if the test prints feel stiff.
    hinge_thickness: float | None = None
    #: The pressed pad is a circle as wide as the tab itself, sitting low on
    #: it. Since the tab ends in a semicircle of the same radius, the pad is
    #: exactly that end cap. None follows the tab width rather than repeating
    #: it, so refining `button_width` carries the pad with it.
    flexure_pad_diameter: float | None = None
    #: How far that pad stands proud of the front face.
    #:
    #: Zero, and deliberately. The original is flush at the top, and the front
    #: face goes on the bed, so anything proud would have to print below it.
    #: The original also recesses the tab's flat *around* the pad; printed face
    #: down that flat becomes an unsupported annulus hanging off the pad, and
    #: the label covers it anyway. Flush costs nothing and prints clean.
    flexure_pad_rise: float = 0.0

    # ------------------------------------------------------------------
    # Buttons: "separate" variant, loose printed caps in through-apertures
    # ------------------------------------------------------------------
    cap_clearance: float = 0.35
    cap_flange_width: float = 2.0
    cap_flange_thickness: float = 1.2
    cap_rise: float = 1.5

    # ------------------------------------------------------------------
    # Print settings the geometry depends on
    # ------------------------------------------------------------------
    nozzle: float = 0.4
    layer_height: float = 0.2

    # ------------------------------------------------------------------
    # Derived
    # ------------------------------------------------------------------
    @property
    def placed_switches(self) -> tuple[Switch, ...]:
        """The switches in panel coordinates rather than cluster coordinates."""
        return tuple(
            Switch(s.name, s.x + self.cluster_x, s.y + self.cluster_y, s.rotation)
            for s in self.switches
        )

    @property
    def placed_leds(self) -> tuple[Led, ...]:
        """The LEDs in panel coordinates rather than cluster coordinates."""
        return tuple(
            Led(led.name, led.x + self.cluster_x, led.y + self.cluster_y, led.aperture)
            for led in self.leds
        )

    @property
    def hinge_gauge(self) -> float:
        """Thickness across the hinge band, defaulting to the tab's own."""
        if self.hinge_thickness is not None:
            return self.hinge_thickness
        return self.tab_thickness

    @property
    def led_footprint(self) -> float:
        """Radius an LED needs kept clear: the wider of counterbore and post."""
        return max(
            self.led_counterbore / 2,
            max(led.aperture for led in self.leds) / 2 + self.tunnel_wall,
        )

    @property
    def tab_end_radius(self) -> float:
        """The tab's free end is a semicircle, so half its width (F7).

        Derived rather than stored: the two cannot then drift apart, and the
        hinge end is square, so there is no second radius to keep track of.
        """
        return self.button_width / 2

    @property
    def pad_diameter(self) -> float:
        """The pressed pad is as wide as the tab unless told otherwise."""
        if self.flexure_pad_diameter is not None:
            return self.flexure_pad_diameter
        return self.button_width

    @property
    def plunger_drop(self) -> float:
        """Distance from the hinge line down to the plunger centre.

        Defaults to the centre of the tab's lower end cap, where the original
        puts its bump, rather than the middle of the tab.
        """
        if self.plunger_offset is not None:
            return self.plunger_offset
        return self.button_height - self.tab_end_radius

    @property
    def placed_screws(self) -> tuple[ScrewHole, ...]:
        """Screw positions, defaulting to four in the lip band.

        Kept away from the corners, where the lip is turning through its
        radius and there is least meat around a hole.
        """
        if self.screws:
            return self.screws
        mid = self.lip_width / 2
        return (
            ScrewHole("bl", self.width * 0.2, -mid),
            ScrewHole("br", self.width * 0.8, -mid),
            ScrewHole("tl", self.width * 0.2, self.height + mid),
            ScrewHole("tr", self.width * 0.8, self.height + mid),
        )

    @property
    def plate_standoff(self) -> float:
        """Where the plate's back face sits above the dryer's front face.

        Derived, not chosen: the switch posts fix the floor, the prong fixes
        its own length, and `pre_travel` keeps the plunger off the switch at
        rest. Getting this wrong either misses the switches or holds them
        permanently pressed.
        """
        return self.switch_height + self.pre_travel + self.plunger_length

    @property
    def plunger_tip_sweep(self) -> float:
        """How far the plunger tip slides sideways over a full press.

        The tab swings on its hinge, so the plunger swings with it and the tip
        travels an arc rather than straight down. A long plunger amplifies a
        small rotation into real sideways movement, and if it exceeds the
        actuator's radius the plunger walks off the switch. That is the price
        the price of standing the plate a long way off the board.
        """
        angle = self.switch_travel / self.plunger_drop  # radians, small
        return self.plunger_length * angle



DEFAULT = Params()
