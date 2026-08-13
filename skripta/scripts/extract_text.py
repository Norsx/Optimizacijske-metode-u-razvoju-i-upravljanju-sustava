"""Extract the text layer of a lecture/exercise PDF, page by page.

Usage:  python extract_text.py <pdf-name> [first] [last]

Beamer footers (author / course title / date / slide counter) are dropped, and
pages that carry no usable text layer are flagged so they can be read as images
instead.  This is only the first pass over a source: any page whose mathematics
comes out ambiguous is still opened as an image.
"""

import re
import sys
from pathlib import Path

import fitz

SRC = Path(__file__).resolve().parents[2] / "data" / "sources"

FOOTER = re.compile(
    r"^(Andrej Joki|Optimizacijske metode u razvoju|Vježbe|\d+\s*/\s*\d+$"
    r"|\d+\.\s*\w+\s*20\d\d\.$)"
)


def clean(text: str) -> str:
    lines = [ln for ln in text.splitlines() if not FOOTER.match(ln.strip())]
    while lines and not lines[-1].strip():
        lines.pop()
    return "\n".join(lines).strip()


def main() -> None:
    name = sys.argv[1]
    first = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    last = int(sys.argv[3]) if len(sys.argv) > 3 else 10**6

    doc = fitz.open(SRC / name)
    for i in range(first - 1, min(last, doc.page_count)):
        page = doc[i]
        body = clean(page.get_text("text"))
        n_img = len(page.get_images(full=True)) + len(page.get_drawings())
        flag = "  [MALO TEKSTA -> pogledaj sliku]" if len(body) < 40 else ""
        print(f"\n===== str. {i + 1} | crteza: {n_img}{flag} =====")
        print(body)
    doc.close()


if __name__ == "__main__":
    main()
