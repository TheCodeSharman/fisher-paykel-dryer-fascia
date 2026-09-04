"""Push the model to the OCP CAD Viewer.

Open the viewer first: command palette, "OCP CAD Viewer: Open viewer". Then
either press the run button with this file open, hit F5 and pick one of the
"Preview" configurations, or from a terminal:

    uv run python -m fascia.preview flexure

With no argument it shows the `flexure` variant.

Imports here are absolute rather than relative, unlike the rest of the package,
so that VS Code's run button can execute this file directly as a script.
"""

import sys

from ocp_vscode import Camera, set_defaults, show

from fascia.panel import FLEXURE, SEPARATE, VARIANTS, make_caps, make_panel
from fascia.params import DEFAULT


def main() -> None:
    variant = sys.argv[1] if len(sys.argv) > 1 else FLEXURE
    if variant not in VARIANTS:
        sys.exit(f"unknown variant {variant!r}, expected one of {VARIANTS}")

    parts = [make_panel(DEFAULT, variant)]
    if variant == SEPARATE:
        parts += make_caps(DEFAULT)

    set_defaults(reset_camera=Camera.KEEP, black_edges=True)

    try:
        show(*parts, names=[p.label for p in parts])
    except (ConnectionError, OSError) as exc:
        sys.exit(
            "Could not reach the OCP CAD Viewer. Open it from the command "
            f"palette with 'OCP CAD Viewer: Open viewer', then try again.\n({exc})"
        )


if __name__ == "__main__":
    main()
