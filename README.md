# Fisher & Paykel dryer fascia

A 3D-printable replacement for the control-panel section of the fascia on an
old Fisher & Paykel wall-mounted dryer. The original moulding went brittle and
broke away around the buttons, leaving the control board open to the room.

This replaces **only the strip around the control board**, not the whole
fascia. The new panel screws into what is left of the original.

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
- **`separate`** &mdash; loose printed caps dropped through round apertures,
  each with a flange behind the panel so it cannot fall out the front. More
  parts and more tolerance-chasing, but the feel is adjustable without
  reprinting the panel.

## Building

Needs [uv](https://docs.astral.sh/uv/). Everything else it installs itself.

```sh
uv sync
uv run fascia-build                    # writes exports/*.stl
uv run fascia-build --variant flexure  # just the one
```

To see it in the OCP CAD Viewer, open the viewer from the VS Code command
palette, then:

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
