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

| Button | Board ref | X | Y | Standoff |
|---|---|---|---|---|
| delay_start | | | | |
| power | | | | |
| start_pause | | | | |
| dryness_down | | | | |
| dryness_up | | | | |
| temp_down | | | | |
| temp_up | | | | |
| wrinkle_guard | | | | |

Also needed: tactile switch actuator diameter, and its travel and force if you
can feel it, since that sets how stiff the hinge can be.

## The old fascia

Discarded, but it is the jig for the button and LED layout. Measure an intact
tab near the middle, away from the cracks.

| # | What | Value | How taken |
|---|---|---|---|
| F3 | Face thickness | 2.73 mm | **on the wrap-around return edge, not the face.** Assumed equal to the face; confirm at the crack that runs through the face |
| F4 | Tab width | | across the tab, inside the slot |
| F5 | Tab height | | hinge line to the top of the tab |
| F6 | Slot width | | the gap itself |
| F7 | Tab corner radius | | |
| F8 | Tab proud of the face | | up, flush or dished |

Chosen for the print: front plate `thickness` 2.8, which is F3 rounded up to
14 layers at 0.2.

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

1. **Label orientation.** The board sits upside-down relative to its
   silkscreen in the machine's hung position. Confirm which way the finished
   label should read, and therefore whether the button and LED rows are
   mirrored end-for-end relative to the board.
2. **How much to replace.** Does the new panel stop at the board opening, or
   run further along the fascia to a natural line?
3. **Which board switch has no button** (`S1`&ndash;`S9` is nine, the label
   shows eight).
4. ~~Printer and material.~~ Settled: PETG on FDM, panel printed flat with the
   front face on the bed.
