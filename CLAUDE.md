# CLAUDE.md

3D-printable replacement fascia panel for the control board of an old Fisher &
Paykel wall-mounted dryer. Read `README.md` first for what the thing is.

## Toolchain

- **uv** manages the environment. Python is pinned to 3.12 (`.python-version`)
  because `cadquery-ocp` wheels do not reach 3.13 yet.
- **build123d** for the geometry, written in the **algebra API** (`+`, `-`,
  `&`, `Pos(...) * shape`), not the builder-context API. Keep it that way; do
  not mix the two styles in one module.
- **ocp_vscode** drives the OCP CAD Viewer extension, which the user has
  installed.

```sh
uv sync
uv run fascia-build                     # all variants -> exports/*.stl
uv run fascia-build --variant flexure
uv run python -m fascia.preview flexure # push to the OCP viewer
```

In VS Code the run button on `src/fascia/preview.py` does the same thing, and
F5 offers both variants plus the STL build. That is why `preview.py` alone uses
absolute imports &mdash; the run button executes it as a script, not as a module,
so relative imports fail there. Leave them absolute.

Always run the build after changing geometry. A model that imports fine can
still fail to produce a solid.

## Layout

| Path | What it holds |
|---|---|
| `src/fascia/params.py` | **Every** dimension. Nothing else hard-codes a number. |
| `src/fascia/panel.py` | The plate: outline, label recess, screw holes, LED bezels. |
| `src/fascia/buttons.py` | Button geometry for both variants, plus the plunger. |
| `src/fascia/build.py` | STL export CLI. |
| `src/fascia/preview.py` | Viewer entry point. |
| `reference/photos/` | Photos of the board, the broken fascia and the dryer. |
| `reference/measurements.md` | Caliper worksheet; the source of truth for real numbers. |
| `labels/` | Artwork for the printed label that covers the face. |
| `exports/` | Build output, git-ignored. |
| `.vscode/` | Interpreter, launch configurations, extension recommendations. |

## Conventions

- **Millimetres**, always. No unit suffixes in names.
- The dryer is wall-mounted with the fascia horizontal along the bottom of the
  machine, hung that way to bring the buttons within reach. The cabinet is
  symmetric, so that left the original label upside down. Everything &mdash;
  model, measurements, new label artwork &mdash; uses the **readable** frame:
  hinge line at the top, tabs hanging down, LED row below them. The board
  silkscreen runs the other way; do not assume its designators follow the
  buttons.
- **Anything read off `photos/03` or `04` comes out backwards.** Those show the
  fascia the way its label was printed, which is 180 degrees from the frame
  everything here uses, because the machine hangs inverted. The button names
  were assigned from that photo and ran the wrong way the whole length of the
  row. The LED labels are still unmapped and will trip on exactly the same
  thing; so will the label artwork.
- Button and LED positions are stored in **cluster coordinates** (x from the
  left-most tab's left edge, y from the hinge line, both growing away from it
  so tabs and LEDs are at negative y), and placed on the panel by `cluster_x`
  and `cluster_y`. Caliper readings go in raw; use `placed_switches` and
  `placed_leds` when building geometry.
- **Coordinate system**: +X right, +Y up, +Z out of the machine towards you.
  X and Y start at the bottom-left corner of the panel outline, so feature
  positions can be taken straight off the calipers. **`z = 0` is the dryer's
  outer skin**, the surface the flange screws down onto, so everything inside
  the machine is negative and the front plate sits at `z = -reach`.
- The part is a **flat plate**, and its own perimeter is the flange that takes
  the screws. Everything it adds projects *backwards*: skirt, plungers, light
  posts. Nothing may stand proud of the front face, which is the label surface
  and goes on the print bed.
- `switch_gap` (`skin_to_switch - reach`) decides whether the buttons work;
  `make_panel` refuses to build if it goes non-positive.
- `make_panel` also refuses if the panel comes out as more than one body, or if
  an LED lands in a button's opening. Both have happened; neither is obvious in
  a viewer.
- Features in the front plate are modelled in **plate-local** coordinates, where
  `z` runs `0` to `thickness`, then translated by `Pos(0, 0, -reach)`. Keep new
  front-plate features in that convention.
- **Never let added geometry merely touch the part it grows from.** Plungers and
  light posts overlap into the plate, and posts are added solid and drilled
  afterwards. Coincident faces give fragile booleans and multi-body STLs; the
  build prints the solid count, which must stay 1.
- Dimensions that have not been measured yet are marked `PLACEHOLDER` in
  `params.py`. Do not quietly drop that marker &mdash; it is how we tell a real
  reading from a guess. When a real measurement arrives, remove the marker and
  record it in `reference/measurements.md`.
- Prefer building features from explicit primitives (cones for countersinks and
  chamfers) over edge-selection `chamfer()` / `fillet()` calls on booleaned
  solids, which break as soon as a neighbouring dimension changes.
- Print-driven dimensions (slot widths, hinge thickness, wall counts) should be
  expressed against `nozzle` and `layer_height` where it matters.

## Working agreements

- **Commit straight to `main`.** No feature branches, no PRs on this repo.
- The repo is public and deliberately so; someone else with a dying ED55/56 may
  find it. Keep the README honest about what is measured and what is guessed.

## Decisions made

- **`flexure` is the design being taken forward.** `separate` stays in the tree
  as a fallback and a comparison print; do not delete it, but new work goes
  into `flexure`.
- **PETG on FDM.** Tougher in fatigue than PLA and happy near a warm appliance,
  which is what the hinge needs. `hinge_thickness` of 0.8 is four layers at
  0.2, and `flexure_slot` of 0.9 is a gap the 0.4 nozzle can bridge cleanly.
  Both assume PETG; revisit them if the material changes.
- **Print the panel flat, front face down.** The bed gives a smooth face for
  the label, the plungers and light posts rise as self-supporting cylinders,
  and the hinge bends along the layers rather than trying to peel them apart.
  `fascia-build` exports already turned that way up, so it is not a step
  anyone has to remember.
- That orientation constrains the front face: **nothing may stand proud of it,
  and no broad shallow pocket may be cut into it.** A pocket leaves the first
  layers as its border alone and asks the whole area to bridge in one go, which
  is what retired `label_recess_depth`. The tab recess is fine because it is
  small and lands on the bump at its far end.
- The tab is recessed from the *front* to `tab_thickness` and left flush with
  the panel on the back, as the original is. The bump is not added on top; it
  is what remains when the recess is cut around it.

## State

Geometry is complete and builds valid solids, but almost every dimension is
still a placeholder. The next real step is filling in
`reference/measurements.md` from calipers, on the fascia while it is off the
machine. Open questions are listed at the bottom of that file; the label
orientation one is the only one that could force a geometry change.
