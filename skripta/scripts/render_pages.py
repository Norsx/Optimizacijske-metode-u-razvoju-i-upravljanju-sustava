"""Render selected PDF pages to PNG so they can be inspected as images.

Usage:  python render_pages.py <pdf-name> <page> [<page> ...]

Pages are written to the session scratchpad as <stem>_p<NN>.png and the paths are
printed.  Needed because the source slides carry a lot of content (plots, sketched
geometry, tables) that never reaches the PDF text layer.
"""

import os
import sys
from pathlib import Path

import fitz

SRC = Path(__file__).resolve().parents[2] / "data" / "sources"
OUT = Path(
    os.environ.get(
        "SCRATCH",
        r"C:\Users\ivann\AppData\Local\Temp\claude"
        r"\C--Users-ivann-Desktop-omurius"
        r"\234f717b-e83b-4009-ac62-866f26382458\scratchpad",
    )
)
ZOOM = 2.0


def main() -> None:
    name = sys.argv[1]
    pages = [int(a) for a in sys.argv[2:]]

    OUT.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(SRC / name)
    stem = Path(name).stem
    for p in pages:
        pix = doc[p - 1].get_pixmap(matrix=fitz.Matrix(ZOOM, ZOOM))
        path = OUT / f"{stem}_p{p:02d}.png"
        pix.save(path)
        print(path)
    doc.close()


if __name__ == "__main__":
    main()
