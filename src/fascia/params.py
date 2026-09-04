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
    """A tactile switch on the control board that a button has to press."""

    name: str
    x: float
    y: float


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
# Board features, read off reference/photos/03 and 04. Names come from the
# original printed label; positions are still PLACEHOLDER.
# ---------------------------------------------------------------------------

_SWITCHES = (
    Switch("delay_start", 18.0, 22.0),
    Switch("power", 36.0, 22.0),
    Switch("start_pause", 54.0, 22.0),
    Switch("dryness_down", 80.0, 22.0),
    Switch("dryness_up", 98.0, 22.0),
    Switch("temp_down", 124.0, 22.0),
    Switch("temp_up", 142.0, 22.0),
    Switch("wrinkle_guard", 168.0, 22.0),
)

_LEDS = (
    Led("delay_9hr", 14.0, 40.0),
    Led("delay_6hr", 21.0, 40.0),
    Led("delay_3hr", 28.0, 40.0),
    Led("keylock", 40.0, 40.0),
    Led("power", 54.0, 40.0),
    Led("dry_timed", 70.0, 40.0),
    Led("dry_light", 84.0, 40.0),
    Led("dry_extra", 98.0, 40.0),
    Led("temp_airing", 116.0, 40.0),
    Led("temp_low", 130.0, 40.0),
    Led("temp_reg", 144.0, 40.0),
    Led("wrinkle_guard", 168.0, 40.0),
)


@dataclass(frozen=True)
class Params:
    # ------------------------------------------------------------------
    # Outline. The flange footprint is what you see from outside.
    # ------------------------------------------------------------------
    width: float = 190.0  # PLACEHOLDER
    height: float = 60.0  # PLACEHOLDER
    corner_radius: float = 4.0

    #: The front plate that carries the buttons, LEDs and label.
    thickness: float = 2.4
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
    reach: float = 12.0  # PLACEHOLDER

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
    button_width: float = 11.0  # PLACEHOLDER
    button_height: float = 13.0  # PLACEHOLDER
    button_radius: float = 4.0
    #: Boss on the back of the button that reaches down to the switch.
    plunger: float = 4.0
    #: Gap left between the plunger tip and the switch actuator at rest, so the
    #: panel does not hold the switches half-pressed.
    pre_travel: float = 0.5

    # ------------------------------------------------------------------
    # Buttons: "flexure" variant, replicating the original F&P design.
    #
    # A tab is cut free on three sides by an inverted-U slot and stays joined
    # along its bottom edge, so it swings like a trapdoor. The printed label
    # bridges the slot and doubles as the seal and the cushion.
    # ------------------------------------------------------------------
    flexure_slot: float = 0.9
    hinge_band: float = 2.0
    hinge_thickness: float = 0.8
    flexure_pad_rise: float = 0.6
    flexure_pad_inset: float = 1.0

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
    def tunnel_length(self) -> float:
        """How far a light tunnel drops before it reaches its LED."""
        return self.skin_to_led - self.reach - self.tunnel_gap


DEFAULT = Params()
