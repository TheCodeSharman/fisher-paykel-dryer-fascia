# Measurements

The source of truth for real numbers. Anything still marked `PLACEHOLDER` in
`src/fascia/params.py` is a guess and needs a row here.

Record **how** each reading was taken, not just the value. "Panel width 187.4"
is much less useful in six months than "panel width 187.4, outside to outside
across the opening, measured at the middle not the corners".

## Datum

Origin is the **bottom-left corner of the new panel outline**, viewed from the
front, with the panel held the way the label reads. +X right, +Y up, +Z out of
the front face towards you.

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

## Button tabs

Measure a surviving tab on the old fascia rather than guessing.

| What | Value |
|---|---|
| Tab width | |
| Tab height | |
| Tab corner radius | |
| Slot width around the tab | |
| Panel thickness at the hinge | |
| Tab standing proud of the face | |

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
4. **Printer and material** &mdash; the flexure hinge thickness and slot width
   depend on both.
