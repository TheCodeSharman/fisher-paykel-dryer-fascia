"""Push the model to the OCP CAD Viewer.

Start the viewer from the VS Code command palette ("OCP CAD Viewer: Open
viewer"), then run this file with the extension's "Run in interactive Python"
or simply:

    uv run python -m fascia.preview flexure
"""

import sys

from ocp_vscode import Camera, set_defaults, show

from .panel import FLEXURE, SEPARATE, VARIANTS, make_caps, make_panel
from .params import DEFAULT


def main() -> None:
    variant = sys.argv[1] if len(sys.argv) > 1 else FLEXURE
    if variant not in VARIANTS:
        sys.exit(f"unknown variant {variant!r}, expected one of {VARIANTS}")

    set_defaults(reset_camera=Camera.KEEP, black_edges=True)

    parts = [make_panel(DEFAULT, variant)]
    if variant == SEPARATE:
        parts += make_caps(DEFAULT)

    show(*parts, names=[p.label for p in parts])


if __name__ == "__main__":
    main()
