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
| Switch posts proud of the dryer face | 8.95 mm | the PCB is flush with the dryer's front face and the posts stand this far off it |

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
| wrinkle_guard | | 0.00 | 0 | all eight hinge lines confirmed colinear |
| temp_up | | 20.58 | 0 | which of the pair is up is a guess |
| temp_down | | 37.56 | 0 | |
| dryness_up | | 62.62 | 0 | likewise |
| dryness_down | | 79.60 | 0 | |
| start_pause | | 107.83 | 0 | |
| power | | 128.41 | 0 | |
| delay_start | | 145.39 | 0 | |
| keylock | | | | hinged on its **left** edge, the one with no slot, so the tab runs to the right |

Names confirmed against the part, and they run the opposite way to the first
reading off the label photo &mdash; which is the same 180 degree rotation as
everything else here, since that photo shows the fascia as its label was
printed and the machine hangs inverted. The LED names will trip on it too. The measured 3 | 2 | 3 grouping corroborates it:
wrinkle guard falls in with the temperature pair, and start/pause, power and
delay start make the three at the far end. Which of each pair is up and which
is down is still a guess, and only matters for the label artwork.

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
| F4 | Tab width | 5.75 mm | across the tab, inside the slot. Cross-checks: 5.75 + 2 x 2.41 = 10.57 against a measured opening of 10.63 |
| F5 | Tab height | 10.57 mm | hinge line to the free end. **The hinge is at the top and the tab hangs down**, so the tab occupies negative Y |
| F6 | Slot width | 2.41 mm | uniform all round, tab edge to hole edge. Cross-checked: whole opening 10.63, so ~2.50 a side. Wide because moulding needs steel there |
| F7 | Tab end radius | semicircular | **the free end only.** The hinge end is square, the sides straight, so the slot legs run parallel up to their end caps. Derived as half the tab width |
| F8 | Tab face | flush, with a 5.25 circle | pad flush with the panel face, tab's flat recessed around it. The pad is as wide as the tab, and sits **low on it, not centred** |
| F13 | Prong length | 3.19 mm | how far the plunger stands off the back face. Since the tab's back is flush with the panel's, this is the whole depth chain: the switch sits 3.69 down once pre-travel is allowed |
| F14 | Light cup depth | 2.64 mm | how far a light tunnel stands off the back. **Shorter than the prongs**, not longer as the underside photo suggested |
| F12 | Bump height above the tab flat | 1.73 mm | so on a 2.73 panel the tab flat is about 1.0 thick. **This is the flexure**: the tab is thin over its whole length with a boss to press on, not a full-thickness slab |
| F11 | Hinge line to pad centre | derived | the pad is as wide as the tab and sits on its semicircular free end, so it is that end cap: `button_height - tab_end_radius` = 7.695. Worth confirming |
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

Thirteen, grouped **1 | 3 | 4 | 1 | [keylock tab] | 1 | 3**, that last three
very close together. Named positionally until the label mapping is confirmed.

**The rows are tied**: `led01` sits on the centreline of the tab above it, so
it shares the cluster datum with `delay_start` at x = 0. Nothing else registers
the LED row against the button row, so without this the whole row could be
right in its spacings and still sit sideways of where it belongs.

Pitches are centre to centre, measured left edge to left edge, which is the
same thing only while every hole is one diameter.

**The keylock gap is the tight spot.** `led09` to `led10` measures about 20.20,
and that has to hold the keylock's tab and slot (12.97) plus half a light post
at each end. With the placeholder post size that comes to 20.17, leaving a
hundredth of a millimetre at each side, which is arithmetic rather than design.
Two things resolve it: **D**, since a smaller LED means smaller posts and real
clearance, and a better reading of the 20.20 itself, which is a guess because
that hole is clipped on its left edge. If it stays this tight, the posts near
the keylock can be trimmed or dropped. The span from `led09` to
`led10` is taken in two parts, either side of the keylock opening, so it gives
the keylock's position at the same time.

| LED | Pitch from previous | X | Note |
|---|---|---|---|
| led01 | &mdash; | 0.00 | on the centreline of `delay_start` |
| led02 | 19.34 | 19.34 | gap after the lone first LED |
| led03 | 11.54 | 30.88 | |
| led04 | 11.54 | 42.42 | |
| led05 | 16.89 | 59.31 | gap |
| led06 | 10.91 | 70.22 | |
| led07 | 10.91 | 81.13 | |
| led08 | 10.91 | 92.04 | |
| led09 | 28.65 | 120.69 | gap to the lone LED |
| *keylock* | | | *tab, not an LED* |
| led10 | 20.20 | 140.89 | **approximate**, spans the keylock and the hole is clipped |
| led11 | 8.44 | 149.33 | |
| led12 | 5.98 | 154.33 | the close-set three |
| led13 | 5.98 | 160.31 | |

The row spans 160.31, running further right than the buttons' 145.39. No two
groups share a spacing: 11.54 inside the three, 10.91 inside the four, 5.98
inside the close-set three.

Still needed: **D**, the hole diameter and whether they all match, and how far
the LED tips stand above the board.

D at 3.35 clears up both worries the placeholder had created. The close-set
three keep 2.63 of wall between bores and their posts stay 0.63 apart, and the
keylock has 0.94 to the nearest post instead of a hundredth.

It also changes what the hole is. At 3.35 it is a clearance hole for a 3mm LED
to sit in, so there is no window with material left across it and nothing to
leave a land on. The bezel is now a straight bore with the front edge broken.

## What the underside shows

`photos/09-fascia-underside.jpg`, and it settles a few things.

- **Light tunnels are real.** The original stands a row of cups off the back,
  one per LED, which is what the model builds. They are tapered rather than
  straight tubes, which will be draft for the mould rather than anything
  optical.
- **The plunger sits on the tab's free end**, over the bump, as modelled.
- **The plungers are ribbed, not solid.** A cross-section rather than a plain
  post. That is a moulding requirement, keeping the wall thin so the surface
  does not sink; printing has no such constraint and a solid cylinder is
  stronger, so ours stays solid.
- **The plungers are short**, a few mm at most. Since the old fascia *was* the
  outer skin, `skin_to_switch` should be close to that plus whatever our plate
  sits proud by. The 18 placeholder is very likely far too big, which would
  make the current 17.5 plunger nonsense. One to settle in round 3 before
  anything is printed.
- A raised feature runs across the back near the hinge line, reading as a small
  triangle at each tab but apparently continuous left to right. **Not
  modelled**, and no purpose assumed: a continuous rib is more likely
  stiffening or a moulding flow feature than anything per-button, and inventing
  a function for it would only put geometry in the way. Worth another look if
  the tabs misbehave.

  It does say one thing clearly though: the original leaves the panel *full
  thickness* past the hinge, where the model had been thinning it.

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
5. ~~Root fillet at the hinge.~~ Not a thing. The close-up,
   `photos/07-button-tab-closeup.jpg`, shows the slot legs running parallel and
   simply stopping in semicircular caps of the slot's own width. That rounded
   end was what looked like an inverse radius. The model already builds it.

   So there is no fillet needing room, and no reason to widen `flexure_slot`
   back towards the original's 2.41 on that account.

6. ~~The hinge does not match the original.~~ It now does, near enough. The
   tab is recessed from the front to leave `tab_thickness` of material, with
   the bump left standing at the panel face by cutting the recess around it.
   That is the original's arrangement: a thin tab over its whole length, a boss
   to press, and the label spanning the recess so it touches only the panel and
   the bump.

   Still to settle by test print: whether 1.0 is the right gauge in PETG, and
   whether the hinge wants any relief past the tab (`hinge_band`, currently
   nothing). Print a strip of tabs at a few thicknesses and pick by feel.

7. **The LED holes look bigger than 3.35.** `photos/10-fascia-front-holes.jpg`
   scaled against the button openings, which are a known 10.57, puts them
   around 4.5 to 5. The ratio is the clearer tell: in the photo the pitch is
   roughly 2.2 hole diameters, where 3.35 against a 10.91 pitch gives 3.26.
   That is what makes the gaps between bezels read as too wide.

   5.48 was the first answer given, then corrected to 3.35. The photo favours
   the first. Possibly the two are the front opening and a bore behind it.
   Worth one careful reading across a hole in the middle of a group, away from
   the damage.

   The pitches are not in doubt: the group of three is visibly wider-spaced
   than the group of four in the photo, which is 11.54 against 10.91.

8. **The right-hand LEDs hang off one uncertain reading.** `led09` to `led10`
   was taken as 20.20 and flagged a guess, because the tab clips that hole's
   left edge and there is no edge left to measure from. Everything right of it
   inherits the error. It wants an independent tie: from the left edge of the
   `delay_start` button opening down to `led11`, say, which is undamaged.

   The original's tab does clip that LED. Ours may not have to: the slot here
   is 1.2 against the original's 2.41, so the keylock tab spans 12.97 along x
   where the original spans 15.39.

9. **The lip overhangs when printed.** Front face down, the lip ends up at the
   top of the print, standing `lip_width` out beyond the walls with nothing
   under it. Either it wants a taper down to 45 degrees so it self-supports, or
   it gets printed with support. Support would touch the side that faces the
   room rather than the mounting face, so it is cosmetic rather than serious.
   Worth settling once the outline is fixed, since the lip changes with it.

10. **Does the recess extend past the slot?** The model recesses the tab and its
   slot. The close-up looks like a wider rounded rectangle reaching a little
   way into the panel around each tab. If so it is presumably there so the
   label is not dragged over the slot's edge. Worth a reading of how far out it
   goes, and how deep.
