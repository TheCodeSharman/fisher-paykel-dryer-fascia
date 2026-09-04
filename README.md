# Fisher & Paykel dryer fascia

A 3D-printable replacement for the control-panel section of the fascia on an
old Fisher & Paykel wall-mounted dryer. The original moulding went brittle and
broke away around the buttons, leaving the control board open to the room.

The original fascia is being discarded, not repaired. This part covers the
control board and **screws straight to holes drilled in the dryer's skin**, so
it has to span the distance down to the board itself.

It is a flat plate whose own perimeter is the flange: it lies on the skin,
takes the screws around its border, and everything it adds projects backwards
into the machine. Nothing stands proud of the front face.

```
   front face, outermost
  ______________________________________
 |______________________________________|  <- plate, screwed through its border
      |          |            |
      | plunger  | light post |             everything projects back
      v          v            v
  ------------------------------------      control board
```

`skin_to_switch` is the measurement everything hangs off: get it wrong and the
buttons either miss the switches or hold them permanently pressed.

Because the plate stands off the board, each LED gets a light tunnel dropping
towards it. Without them the LEDs wash into each other's apertures across the
gap.

## Button design

Two strategies, both built from the same measurements:

- **`flexure`** &mdash; replicates the original. An inverted-U slot cuts a tab
  free on three sides, leaving it joined along its bottom edge so it swings
  like a trapdoor. A boss on the back presses the tactile switch. The printed
  label bridges the slot, sealing it and cushioning the press. This is what the
  original does; see `reference/photos/04-fascia-front-label-off.jpg`.
  Printed in PETG, flat with the front face on the bed, so the hinge bends
  along the layers instead of peeling them apart. This is the design being
  taken forward.
- **`separate`** &mdash; loose printed caps dropped through round apertures,
  each with a flange behind the panel so it cannot fall out the front. More
  parts and more tolerance-chasing, but the feel is adjustable without
  reprinting the panel. Kept as a fallback and a comparison print.

## Building

Needs [uv](https://docs.astral.sh/uv/). Everything else it installs itself.

```sh
uv sync
uv run fascia-build                    # writes exports/*.stl
uv run fascia-build --variant flexure  # just the one
```

To see it in the OCP CAD Viewer: open `src/fascia/preview.py` and press the
run button, which shows the `flexure` variant. F5 offers "Preview: flexure",
"Preview: separate" and "Build all STLs" instead. The viewer starts itself; if
it does not, open it from the command palette with "OCP CAD Viewer: Open
viewer".

From a terminal, the same thing:

```sh
uv run python -m fascia.preview flexure
```

## Measurements

Every dimension lives in [`src/fascia/params.py`](src/fascia/params.py) and
nothing else hard-codes a number. Values marked `PLACEHOLDER` are guesses,
sized so the model builds and can be eyeballed; they are not measured yet.
[`reference/measurements.md`](reference/measurements.md) is the worksheet for
replacing them.

## Licence

Public domain, do what you like with it. If it helps you rescue an old
appliance from landfill, that was the point.
