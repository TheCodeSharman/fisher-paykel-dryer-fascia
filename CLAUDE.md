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

## Conventions

- **Millimetres**, always. No unit suffixes in names.
- The dryer is wall-mounted with the fascia horizontal along the bottom of the
  machine, and the control board sits upside-down relative to its silkscreen in
  that position. Do not assume board designators run the same way as the
  buttons on the label.
- **Coordinate system**: origin at the bottom-left corner of the panel outline
  seen from the front; +X right, +Y up, +Z out of the front face. `z = 0` is
  the back face, `z = thickness` the front. Feature positions are offsets from
  that corner so they can be taken straight off the calipers.
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

## State

Geometry is complete and builds, but almost every dimension is still a
placeholder. The next real step is filling in `reference/measurements.md` from
calipers. Open questions are listed at the bottom of that file.
