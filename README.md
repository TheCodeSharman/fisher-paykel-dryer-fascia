# Fisher & Paykel dryer fascia

A 3D-printable replacement for the control-panel section of the fascia on an
old Fisher & Paykel wall-mounted dryer. The original moulding went brittle and
broke away around the buttons, leaving the control board open to the room.

The original fascia is being discarded, not repaired. This part covers the
control board and **screws straight to holes drilled in the dryer's skin**, so
it has to span the distance down to the board itself. It is a shallow tray
rather than a flat plate:

```
flange  -----____                    ____-----   z = 0, on the dryer skin
                 |                  |
                 | wall             | wall
                 |__________________|
                    front plate                  z = -reach
```

The flange lands on the skin and takes the screws; the walls carry the front
plate down into the machine by `reach`, leaving `switch_gap` for the plungers
to cross. Get that one number wrong and the buttons either miss the switches or
hold them permanently pressed, so it is the measurement to take most carefully.

Because the front plate now stands off the board, each LED gets a light tunnel
dropping towards it. Without them the LEDs wash into each other's apertures
across the gap.

| | |
|---|---|
| Control board | `PCB ED55/56 Dryer`, F&P part `3470428-C`, dated 1997 |
| Firmware | EPROM labelled `ED56 427318270820` |
| Buttons | 8 &mdash; Delay Start, Power, Start/Pause, Dryness &times;2, Temperature &times;2, Wrinkle Guard |
| Indicators | ~12 LEDs (count to be confirmed against the board) |

The dryer is wall-mounted, and the fascia runs **horizontally along the
bottom** of the machine as it hangs. The board silkscreen reads upside-down in
that position, so which way up the printed label should read is a decision
still to be made rather than something to copy from the original.

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
