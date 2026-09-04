# Measurements

The source of truth for real numbers. Anything still marked `PLACEHOLDER` in
`src/fascia/params.py` is a guess and needs a row here.

Record **how** each reading was taken, not just the value. "Panel width 187.4"
is much less useful in six months than "panel width 187.4, outside to outside
across the opening, measured at the middle not the corners".

## Datum

The original fascia is discarded, so its outline is not a useful reference.
Measure the button and LED cluster against itself:

- **X = 0** at the left edge of the left-most button tab
- **Y = 0** at the hinge line of the button row
- **z = 0** at the dryer's outer skin, the surface the flange screws onto,
  with +Z out of the machine towards you

The cluster is what has to be right; the panel outline around it is ours to
choose, and `params.py` shifts the cluster into panel coordinates once that
outline is settled.

Screw positions do not need measuring. The printed panel is its own drilling
template: offer it up with the plungers over the switches, mark through the
flange holes, drill. They only have to land on solid metal.

The dryer is wall-mounted and the fascia runs horizontally along the bottom of
the machine as it hangs. The board silkscreen reads upside-down in that
position. Decide once which way "up" is for the panel and the label, and stay
with it &mdash; see the open questions below.

The fascia is currently off the machine, which is the easy time to measure it.

## The machine

| What | Value | How taken |
|---|---|---|
| Cabinet width | 550 mm | as the machine stands upright, off-machine nominal |
| Cabinet height | 760 mm | " |
| Cabinet depth | 520 mm | " |
| Door outside diameter | 425 mm | across the outer rim of the door surround |
| Door window diameter | 255 mm | across the glass |
| Bottom of cabinet to door | 90 mm | cabinet edge to the door surround; note the fascia end is the bottom as hung |

Control board: `PCB ED55/56 Dryer`, F&P part `3470428-C`, 1997.
EPROM: `ED56 427318270820`.

## The opening to be filled

| What | Value | How taken |
|---|---|---|
| Opening width | | across the gap in the old fascia, at the middle |
| Opening height | | |
| Overlap onto sound fascia | | how far the new panel laps over the old on each side |
| Panel thickness | | thickness of the original fascia beside the break |
| Depth from fascia face to board | | sets `Switch.standoff` |

## Screw positions

Drilled into what is left of the original fascia. Note what the screw bites
into &mdash; solid moulding or a thin skin.

| Name | X | Y | Notes |
|---|---|---|---|
| bl | | | |
| br | | | |
| tl | | | |
| tr | | | |

Screw type used: ______  Pilot hole drilled: ______

## Switches

Eight buttons, read off the original label left to right. Board designators run
`S1`&ndash;`S9`, so one switch on the board is not brought out to a button;
confirm which.

Nine buttons, so every board switch `S1`-`S9` is brought out after all. X is
the tab centre, Y the hinge line, both in cluster coordinates.

Positions come from centre-to-centre pitches, measured opening edge to
opening edge along the row, since it is longer than a caliper.

| Pitch | Value | |
|---|---|---|
| B1 -> B2 | 20.58 | |
| B2 -> B3 | 16.98 | |
| B3 -> B4 | 25.06 | **group gap** |
| B4 -> B5 | 16.98 | |
| B5 -> B6 | 28.23 | **group gap** |
| B6 -> B7 | 20.58 | |
| B7 -> B8 | 16.98 | |

So the row groups **3 | 2 | 3** and spans 145.39 centre to centre. The first
and last groups share their internal spacing exactly. Cross-check G, first
opening's left edge to last opening's right edge, should read **156.02**.

| Button | Board ref | X | Y | Rotation |
|---|---|---|---|---|
| delay_start | | 0.00 | 0 | |
| power | | 20.58 | 0 | |
| start_pause | | 37.56 | 0 | |
| dryness_down | | 62.62 | 0 | |
| dryness_up | | 79.60 | 0 | |
| temp_down | | 107.83 | 0 | |
| temp_up | | 128.41 | 0 | |
| wrinkle_guard | | 145.39 | 0 | |
| keylock | | | | turned on its side; **which edge is the hinge?** |

Names are read off the label photo, not measured. The 3 | 2 | 3 grouping fits
the label if Wrinkle Guard sits alongside the Temperature pair rather than
apart from it &mdash; worth confirming against the label fragments.

The keylock sits down among the LEDs at the bottom right rather than on the
button line, running `tab, LED, gap, 3 LEDs`. Its tab is the same size as the
others; only the printed button on the label is smaller, which is an artwork
matter and not a geometry one.

Also needed: tactile switch actuator diameter, and its travel and force if you
can feel it, since that sets how stiff the hinge can be.

## The old fascia

Discarded, but it is the jig for the button and LED layout. Measure an intact
tab near the middle, away from the cracks.

| # | What | Value | How taken |
|---|---|---|---|
| F3 | Face thickness | 2.73 mm | **on the wrap-around return edge, not the face.** Assumed equal to the face; confirm at the crack that runs through the face |
| F4 | Tab width | 5.63 mm | across the tab, inside the slot |
| F5 | Tab height | 10.57 mm | hinge line to the free end. **The hinge is at the top and the tab hangs down**, so the tab occupies negative Y |
| F6 | Slot width | 2.41 mm | uniform all round, tab edge to hole edge. Cross-checked: whole opening 10.63, so ~2.50 a side. Wide because moulding needs steel there |
| F7 | Tab corner radius | semicircular | so half the tab width, 2.815 |
| F8 | Tab face | flush, with a 5.25 circle | pad flush with the panel face, tab's flat recessed around it. The pad is as wide as the tab, and sits **low on it, not centred** |
| F11 | Hinge line to pad centre | | wanted: sets the leverage and where the plunger lands. Currently guessed at 7.3 |
| F9 | Hinge line to top edge | 41.14 mm | above the hinge line |
| F10 | Hinge line to bottom edge | 55.58 mm | below the hinge line, past the LED row |

Vertical stack in this frame, top to bottom: top of fascia, hinge line, tabs
hanging down from it, LED row, bottom of fascia. Tabs and LEDs are both at
negative y.

So the old fascia stood 96.72 tall, with the cluster high in it: 41.14 above
the hinge, 55.58 below. The new panel takes those proportions provisionally,
but it only has to cover the board opening, so the machine measurements govern.

Chosen for the print, and why they differ from the measurements:

- front plate `thickness` 2.8 &mdash; F3 rounded up to 14 layers at 0.2
- `flexure_slot` 1.2 &mdash; three nozzle widths, rather than copying F6's 2.41.
  That figure is a moulding constraint we do not share; ours only has to
  separate on the bed and be bridgeable by the label. Widen it towards 2.41 if
  the tabs print fused to the panel.

## LEDs

Around twelve, in a row above the buttons. **Confirm the count and the order
against the board** &mdash; the names below are read off the printed label and
the grouping is not certain.

| LED | Board ref | X | Y | Colour |
|---|---|---|---|---|
| delay_9hr | | | | |
| delay_6hr | | | | |
| delay_3hr | | | | |
| keylock | | | | |
| power | | | | |
| dry_timed | | | | |
| dry_light | | | | |
| dry_extra | | | | |
| temp_airing | | | | |
| temp_low | | | | |
| temp_reg | | | | |
| wrinkle_guard | | | | |

Also needed: LED body diameter, and how far the LED tips stand above the board.

## Other features in the old fascia

The label-off photo shows features beyond the buttons and LEDs: a large round
hole and a rectangular cut-out at one end, two long rectangular slots, and
several small square holes. Work out which of these are inside the replacement
area and what each one does &mdash; board retaining clips, light guides, or
nothing that matters any more.

## Open questions

1. ~~Label orientation.~~ Settled. The machine was hung the way it is to put
   the buttons within reach, and since the cabinet is symmetric that left the
   *original* label upside down. So the readable orientation is the flipped
   one, which is the same frame these measurements are taken in: hinge line at
   the top, tabs hanging down, LED row below them. Model, measurements and new
   label artwork all share that frame, and nothing needs rotating at the end.
2. **How much to replace.** Does the new panel stop at the board opening, or
   run further along the fascia to a natural line?
3. ~~Which board switch has no button.~~ None: the ninth is the keylock,
   turned on its side down in the LED row. All of `S1`-`S9` are used.
4. ~~Printer and material.~~ Settled: PETG on FDM, panel printed flat with the
   front face on the bed.
5. **The hinge does not match the original and does not look workable.**
   Deferred to test prints rather than redesigned blind. What is there now is a
   band across the top of the tab, thinned from behind to `hinge_thickness`
   over `hinge_band`, which is a guess and not a copy. Worth measuring on the
   original before printing: how thick the material actually is at the hinge,
   whether it is thinned at all or just flexes the full 2.73, and how far back
   from the slot ends the thinning runs. Print a strip of tabs at a few
   thicknesses and pick by feel.
6. **Flange overhang.** Printed face down, the flange is a lip cantilevered off
   the top of the walls by `body_inset`. Depending on how deep `reach` turns
   out, that may want a taper down to 45 degrees so it self-supports. Not worth
   solving until the depth is measured.
