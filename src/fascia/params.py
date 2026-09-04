"""Every measured or chosen dimension lives here. Nothing else hard-codes a number.

Units are millimetres throughout.

Coordinate system
-----------------
Looking at the *front* of the panel (the side you see standing at the dryer):

    X  -> right
    Y  -> up
    Z  -> out of the panel, towards you

The origin is the **bottom-left corner of the panel outline**, so every feature
position can be taken straight off the calipers as an offset from that corner.
z = 0 is the back face (against the control board); z = `thickness` is the
front face the printed label is stuck to.

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
    #: Distance from the back face of the panel to the switch actuator once the
    #: panel is screwed in place. Sets the plunger length.
    standoff: float = 4.0


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
    # Panel outline
    # ------------------------------------------------------------------
    width: float = 190.0  # PLACEHOLDER
    height: float = 60.0  # PLACEHOLDER
    thickness: float = 2.4  # PLACEHOLDER
    corner_radius: float = 4.0

    # Shallow recess in the front face that the printed label drops into, so
    # the label sits flush instead of proud. Set depth to 0.0 to omit it.
    label_recess_depth: float = 0.4
    label_recess_margin: float = 3.0  # border of bare plastic around the label

    # ------------------------------------------------------------------
    # Fasteners: self-tappers through the new panel into the old fascia
    # ------------------------------------------------------------------
    screw_shank: float = 3.4  # clearance hole for an M3 / #6 self-tapper
    screw_head: float = 6.4  # countersunk head diameter at the front face
    screws: tuple[ScrewHole, ...] = field(
        default_factory=lambda: (  # PLACEHOLDER positions
            ScrewHole("bl", 8.0, 8.0),
            ScrewHole("br", 182.0, 8.0),
            ScrewHole("tl", 8.0, 52.0),
            ScrewHole("tr", 182.0, 52.0),
        )
    )

    # ------------------------------------------------------------------
    # Board features
    # ------------------------------------------------------------------
    switches: tuple[Switch, ...] = field(default_factory=lambda: _SWITCHES)
    leds: tuple[Led, ...] = field(default_factory=lambda: _LEDS)

    # ------------------------------------------------------------------
    # LED bezels
    # ------------------------------------------------------------------
    #: Front-face chamfer around each aperture, so the light spreads and the
    #: hole does not look like a raw drilling.
    led_chamfer: float = 0.6
    #: The bore is opened out behind the aperture to clear the LED body.
    led_body_bore: float = 5.2
    #: Material left at the aperture. The rest of the thickness is bored out.
    led_aperture_land: float = 0.8

    # ------------------------------------------------------------------
    # Buttons: shared
    # ------------------------------------------------------------------
    button_width: float = 11.0  # PLACEHOLDER
    button_height: float = 13.0  # PLACEHOLDER
    button_radius: float = 4.0  # corner radius of the button outline
    #: Boss on the back of the button that reaches down to the switch.
    plunger: float = 4.0
    #: Gap left between the plunger tip and the switch actuator at rest, so the
    #: panel does not hold the switches half-pressed. Subtracted from standoff.
    pre_travel: float = 0.5

    # ------------------------------------------------------------------
    # Buttons: "flexure" variant, which replicates the original F&P design.
    #
    # A tab is cut free on three sides by an inverted-U slot and stays joined
    # along its bottom edge, so it swings like a trapdoor. The printed label
    # bridges the slot and doubles as the seal and the cushion.
    # ------------------------------------------------------------------
    #: Width of the slot cut around the tab. Must clear the nozzle comfortably.
    flexure_slot: float = 0.9
    #: The hinge is thinned from the back over this band so the tab swings
    #: without the whole panel flexing with it.
    hinge_band: float = 2.0
    hinge_thickness: float = 0.8
    #: How far the tab stands proud of the front face, giving a bump to find
    #: under the label. 0.0 leaves it flush, as the original is.
    flexure_pad_rise: float = 0.6
    #: The raised pad is inset from the tab outline so the slot stays clear.
    flexure_pad_inset: float = 1.0

    # ------------------------------------------------------------------
    # Buttons: "separate" variant, loose printed caps in through-apertures
    # ------------------------------------------------------------------
    #: Gap between the cap and the aperture it slides in. Tune to your printer.
    cap_clearance: float = 0.35
    #: Flange behind the panel that stops the cap falling out the front.
    cap_flange_width: float = 2.0
    cap_flange_thickness: float = 1.2
    #: How far the cap stands proud of the front face at rest.
    cap_rise: float = 1.5

    # ------------------------------------------------------------------
    # Print settings the geometry depends on
    # ------------------------------------------------------------------
    nozzle: float = 0.4
    layer_height: float = 0.2


DEFAULT = Params()
