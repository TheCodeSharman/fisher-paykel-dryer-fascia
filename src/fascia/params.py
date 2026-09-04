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

**z = 0 is the dryer's outer skin**, the surface the flange is screwed down
onto. Everything inside the machine is negative, so the control board sits at
negative z and `skin_to_switch` is a positive number measured inwards.

The part is a tray, not a plate. It screws to holes drilled in the dryer and
must itself span the distance down to the switches, so `reach` and
`skin_to_switch` together decide whether the buttons touch. See `switch_gap`.

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
    #: Diameter of the light aperture at the front face.
    aperture: float = 2.5


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


_BUTTON_NAMES = (
    "delay_start",
    "power",
    "start_pause",
    "dryness_down",
    "dryness_up",
    "temp_down",
    "temp_up",
    "wrinkle_guard",
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
) + (
    # Turned on its side and sitting down among the LEDs rather than on the
    # button line. Same tab size as the rest. PLACEHOLDER position, and the
    # rotation sign still needs settling: which edge is its hinge?
    Switch("keylock", 140.0, -16.0, rotation=90.0),
)

_LEDS = (
    Led("delay_9hr", -1.0, -16.0),
    Led("delay_6hr", 6.0, -16.0),
    Led("delay_3hr", 13.0, -16.0),
    Led("keylock", 25.0, -16.0),
    Led("power", 38.0, -16.0),
    Led("dry_timed", 55.0, -16.0),
    Led("dry_light", 69.0, -16.0),
    Led("dry_extra", 83.0, -16.0),
    Led("temp_airing", 101.0, -16.0),
    Led("temp_low", 115.0, -16.0),
    Led("temp_reg", 129.0, -16.0),
    Led("wrinkle_guard", 152.8, -16.0),
)


@dataclass(frozen=True)
class Params:
    # ------------------------------------------------------------------
    # Outline. The flange footprint is what you see from outside.
    # ------------------------------------------------------------------
    #: PLACEHOLDER. Provisionally the original fascia's height, F9 + F10, so
    #: the preview is proportioned like the real thing. What actually bounds
    #: the outline is the flat metal around the opening on the machine.
    width: float = 200.0  # PLACEHOLDER
    height: float = 96.72  # PLACEHOLDER, = 41.14 + 55.58
    corner_radius: float = 4.0

    #: The front plate that carries the buttons, LEDs and label. The original
    #: measured 2.73 on its return edge; rounded up to 14 layers at 0.2 so the
    #: slicer is not left with a part layer to fudge.
    thickness: float = 2.8
    #: The lip that lands on the dryer skin and takes the screws.
    flange_thickness: float = 2.4
    #: Side walls of the tray, joining the front plate up to the flange.
    wall: float = 2.0
    #: How far the tray body sits inside the flange edge, leaving a landing
    #: strip of flange around it for the screws.
    body_inset: float = 10.0

    # ------------------------------------------------------------------
    # Depth. The chain that decides whether the buttons reach the switches.
    #
    #   skin_to_switch   how far the switch tops are below the dryer skin
    #   reach            how far the front plate sits below the dryer skin
    #   switch_gap       what is left for the plunger  (= the difference)
    #
    # `reach` is ours to choose; `skin_to_switch` has to be measured on the
    # machine with the board in place.
    # ------------------------------------------------------------------
    skin_to_switch: float = 18.0  # PLACEHOLDER
    skin_to_led: float = 20.0  # PLACEHOLDER
    #: PLACEHOLDER. Deeper keeps the plungers short, but sinks the buttons
    #: down a well. See `plunger_tip_sweep` for what shallow costs.
    reach: float = 6.0

    # ------------------------------------------------------------------
    # Label
    # ------------------------------------------------------------------
    #: Shallow recess in the front face so the printed label sits flush.
    #: Set to 0.0 to omit it.
    label_recess_depth: float = 0.4
    label_recess_margin: float = 2.0  # bare plastic left inside the well

    # ------------------------------------------------------------------
    # Fasteners: through the flange into holes drilled in the dryer
    # ------------------------------------------------------------------
    screw_shank: float = 3.4  # clearance hole for an M3 / #6 self-tapper
    screw_head: float = 6.4  # countersunk head diameter at the front face
    screws: tuple[ScrewHole, ...] = field(
        default_factory=lambda: (  # PLACEHOLDER positions, must sit on the flange
            ScrewHole("bl", 5.0, 5.0),
            ScrewHole("br", 185.0, 5.0),
            ScrewHole("tl", 5.0, 55.0),
            ScrewHole("tr", 185.0, 55.0),
        )
    )

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
    led_body_bore: float = 5.2
    led_aperture_land: float = 0.8
    tunnel_wall: float = 1.0
    #: Clearance left between the end of a tunnel and the tip of its LED.
    tunnel_gap: float = 1.5

    # ------------------------------------------------------------------
    # Buttons: shared
    # ------------------------------------------------------------------
    button_width: float = 5.63  # measured, F4
    button_height: float = 10.57  # measured, F5
    #: Confirmed semicircular (F7), so this is half the width. `_tab_outline`
    #: clamps it just under that, since RectangleRounded will not take exactly
    #: half a side.
    button_radius: float = 2.815
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
    #: PLACEHOLDER until the actuator position under the tab is known.
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
    hinge_band: float = 2.0
    hinge_thickness: float = 0.8
    #: The pressed pad is a circle on the tab, measured at 5.25 across (F8).
    flexure_pad_diameter: float = 5.25
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
    def body_width(self) -> float:
        return self.width - 2 * self.body_inset

    @property
    def body_height(self) -> float:
        return self.height - 2 * self.body_inset

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
    def plunger_drop(self) -> float:
        """Distance from the hinge line down to the plunger centre."""
        if self.plunger_offset is not None:
            return self.plunger_offset
        return self.button_height / 2

    @property
    def switch_gap(self) -> float:
        """Clear distance from the back of the front plate to the switch tops.

        The single number that decides whether the buttons work. The plunger
        fills all but `pre_travel` of it.
        """
        return self.skin_to_switch - self.reach

    @property
    def plunger_length(self) -> float:
        return self.switch_gap - self.pre_travel

    @property
    def plunger_tip_sweep(self) -> float:
        """How far the plunger tip slides sideways over a full press.

        The tab swings on its hinge, so the plunger swings with it and the tip
        travels an arc rather than straight down. A long plunger amplifies a
        small rotation into real sideways movement, and if it exceeds the
        actuator's radius the plunger walks off the switch. That is the price
        of a shallow `reach`.
        """
        angle = self.switch_travel / self.plunger_drop  # radians, small
        return self.plunger_length * angle

    @property
    def tunnel_length(self) -> float:
        """How far a light tunnel drops before it reaches its LED."""
        return self.skin_to_led - self.reach - self.tunnel_gap


DEFAULT = Params()
