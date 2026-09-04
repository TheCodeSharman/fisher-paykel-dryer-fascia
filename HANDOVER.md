# Handover

Where this project has got to, what is settled, and what is not. Read
`README.md` for what the thing is and `CLAUDE.md` for how to work on it.

## State in one line

The cluster &mdash; every button and LED, and the depth chain that decides
whether the buttons reach the switches &mdash; is fully measured off the
original fascia. **The panel outline is not.** Nothing can be printed to fit
until it is.

## What is measured, and therefore settled

| | |
|---|---|
| Buttons | 9, positions from measured pitches, names confirmed against the part |
| LEDs | 13, all 12 pitches measured, grouped 1 &#124; 3 &#124; 4 &#124; 1 &#124; keylock &#124; 1 &#124; 3 |
| Tab | 5.75 &times; 10.57, semicircular free end, 1.2 slot, 1.0 thick |
| Bump | as wide as the tab, on its end cap, flush with the face |
| LED hole | 3.3, behind a 5.94 counterbore |
| Switch posts | 8.95 proud of the dryer's front face |
| Prong | 3.19, so `plate_standoff` is 12.64 |
| Light tunnel | 2.64 |

## What is still a placeholder

Only three numbers matter, and they are all the same job: **the outline**.

- `width`, `height` &mdash; currently 240 &times; 96.72, arbitrary
- `cluster_x`, `cluster_y` &mdash; where the measured cluster sits on that outline

These need the machine, not the fascia: how much flat metal surrounds the
opening for the lip to land on and take screws. Everything else about the part
is determined.

Smaller ones: `led_counterbore_depth` (1.0, guessed), and the keylock's X, which
is currently derived as centred between its neighbouring LEDs. The original is
plainly not centred &mdash; it clips the LED beside it &mdash; so a direct
reading is wanted before printing.

## Decisions that are not obvious from the code

- **`flexure` is the design.** `separate` stays as a fallback and comparison
  print. Do not delete it, but new work goes into `flexure`.
- **PETG, printed flat, front face down.** That orientation constrains the front
  face: nothing may stand proud of it, and no broad shallow pocket may be cut
  into it. That rule has already killed a raised pad and a label recess.
  Exports come out already turned the right way up.
- **The slot is 1.2, where the original is 2.41.** The original's width is a
  moulding constraint; ours only has to separate on the bed and be bridgeable by
  the label. This is not an oversight, and it is what buys the clearance that
  lets the keylock miss the LED the original clips.
- **The plate is held clear of the switch posts on walls, with a lip returning
  to the dryer face for the screws.** The posts stand proud of the mounting
  surface, so a flat plate lying on that surface is not possible.

## Traps that have already cost time

- **Anything read off `photos/03` or `04` comes out backwards.** They show the
  fascia as its label was printed, 180 degrees from the frame used here, because
  the machine hangs inverted. The button names were assigned from those photos
  and ran the wrong way down the entire row. The LED labels are still unmapped
  and the label artwork is still undrawn; both will meet the same rotation.
- **Do not extrapolate a pitch from an apparent pattern.** It was tried twice on
  the button row and was wrong twice.
- **Measure off counterbore edges, not hole edges.** Calipers seat against a
  counterbore. The first LED pass used hole edges and ran long by about 0.4 a
  time, which would have accumulated into millimetres along the row.
- **The build refuses to produce a part that is wrong in ways a viewer hides.**
  It checks the panel is a single body, that features clear the walls, and that
  no LED lands in a button's opening. All three have caught real faults.

## What to do next

1. Measure the opening on the machine and set the outline. That is the only
   thing standing between here and a first print.
2. Print a strip of tabs at a few thicknesses either side of 1.0 and pick the
   hinge by feel. This is the one part of the design that reasoning cannot
   settle.
3. Decide the lip: printed face down it overhangs, so either taper it to 45
   degrees or accept support on a face that is not the mounting surface.
4. Map the LED labels and draw the artwork &mdash; watching the rotation.

The full list of open questions, with the reasoning behind each, is at the
bottom of `reference/measurements.md`.
