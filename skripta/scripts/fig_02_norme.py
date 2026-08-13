"""Unit balls of the p-norms in R^2 -- reproduces the picture in Vjezbe 1, str. 33.

Each curve is the set {x | ||x||_p = 1} for one value of p.  For p = 1 it is a
diamond, for p = 2 the unit circle, and as p grows it inflates towards the
square of the infinity norm.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parents[1] / "figures"

PS = [1.0, 1.5, 2.0, 3.0, 6.0]
BOJE = ["#8E44AD", "#2E4A9E", "#3498DB", "#1E6B3A", "#E67E22"]


def jedinicna_kugla(p: float, n: int = 2000) -> tuple[np.ndarray, np.ndarray]:
    """Points with ||x||_p = 1, parametrised by angle."""
    th = np.linspace(0.0, 2.0 * np.pi, n)
    c, s = np.cos(th), np.sin(th)
    r = (np.abs(c) ** p + np.abs(s) ** p) ** (-1.0 / p)
    return r * c, r * s


def main() -> None:
    fig, ax = plt.subplots(figsize=(5.8, 5.8))

    for p, boja in zip(PS, BOJE):
        x, y = jedinicna_kugla(p)
        ax.plot(x, y, color=boja, lw=1.8, label=f"$p={p:g}$")

    # p = infinity: the square
    ax.plot([-1, 1, 1, -1, -1], [-1, -1, 1, 1, -1],
            color="#D62728", lw=1.8, label=r"$p=\infty$")

    ax.axhline(0, color="k", lw=0.6, alpha=0.5)
    ax.axvline(0, color="k", lw=0.6, alpha=0.5)
    ax.set_xlim(-1.35, 1.35)
    ax.set_ylim(-1.35, 1.35)
    ax.set_xlabel(r"$x_1$")
    ax.set_ylabel(r"$x_2$")
    ax.set_title(r"Jedinične kugle $\{x \mid \|x\|_p = 1\}$ u $\mathbb{R}^2$")
    ax.grid(alpha=0.25)
    ax.legend(loc="upper right", fontsize=9, framealpha=0.95)
    ax.set_aspect("equal", adjustable="box")

    OUT.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(OUT / "02-norme-jedinicne-kugle.png", dpi=160)


if __name__ == "__main__":
    main()
