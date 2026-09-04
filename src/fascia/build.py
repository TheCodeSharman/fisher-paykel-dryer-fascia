"""Export the model to STL.

    uv run fascia-build                 # every variant
    uv run fascia-build --variant flexure
"""

import argparse
from pathlib import Path

from build123d import Part, Pos, export_stl

from .panel import FLEXURE, SEPARATE, VARIANTS, make_caps, make_panel
from .params import DEFAULT, Params

EXPORTS = Path(__file__).resolve().parents[2] / "exports"


def _on_the_bed(part: Part) -> Part:
    """Drop a part so its lowest point sits on z = 0, ready to slice."""
    return Pos(0, 0, -part.bounding_box().min.Z) * part


def _write(part: Part, path: Path, tolerance: float) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    export_stl(part, str(path), tolerance=tolerance, angular_tolerance=0.1)
    print(f"  {path.relative_to(EXPORTS.parent)}  ({len(part.faces())} faces)")


def build(variant: str, p: Params, out: Path, tolerance: float) -> None:
    print(f"{variant}:")
    _write(_on_the_bed(make_panel(p, variant)), out / f"panel-{variant}.stl", tolerance)

    if variant == SEPARATE:
        caps = make_caps(p)
        together = caps[0]
        for c in caps[1:]:
            together += c
        _write(_on_the_bed(together), out / "button-caps.stl", tolerance)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--variant",
        choices=VARIANTS,
        action="append",
        help="button strategy to build; repeatable, defaults to all",
    )
    ap.add_argument("--out", type=Path, default=EXPORTS, help="output directory")
    ap.add_argument(
        "--tolerance",
        type=float,
        default=0.02,
        help="STL chordal deviation in mm; lower is smoother and slower",
    )
    args = ap.parse_args()

    for variant in args.variant or [FLEXURE, SEPARATE]:
        build(variant, DEFAULT, args.out, args.tolerance)


if __name__ == "__main__":
    main()
