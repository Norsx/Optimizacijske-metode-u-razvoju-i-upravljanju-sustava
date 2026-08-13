"""Level curves of a linear function -- Zadatak 2 from Vjezbe 1.

f(x) = a^T x with a = (2, 1)^T.  Every level curve is a straight line
2*x1 + x2 = c, all parallel, and a itself is perpendicular to them and points
in the direction of increasing c.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parents[1] / "figures"

A = np.array([2.0, 1.0])
LEVELS = [-4, -2, 0, 2, 4, 6, 8]


def main() -> None:
    fig, ax = plt.subplots(figsize=(6.6, 5.6))

    x1 = np.linspace(-3.0, 4.0, 200)
    for c in LEVELS:
        x2 = c - 2.0 * x1                       # 2*x1 + x2 = c
        ax.plot(x1, x2, color="#3b3b8f", lw=1.2)
        # label each line low down, where nothing else competes for the space
        ok = (x2 > -3.2) & (x2 < 1.2)
        if ok.any():
            i = int(np.flatnonzero(ok)[len(np.flatnonzero(ok)) // 2])
            ax.annotate(f"$c={c}$", xy=(x1[i], x2[i]), fontsize=8,
                        color="#3b3b8f", rotation=-63,
                        rotation_mode="anchor",
                        ha="center", va="bottom",
                        xytext=(0, 3), textcoords="offset points")

    # the vector a, drawn from the origin
    ax.annotate("", xy=(A[0], A[1]), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", lw=2.4, color="#d62728"))
    ax.annotate(r"$a=\binom{2}{1}$", xy=(A[0], A[1]), xytext=(8, -14),
                textcoords="offset points", fontsize=11, color="#d62728")

    # right angle marker between a and the level line through the origin
    d = np.array([1.0, -2.0]) / np.sqrt(5.0)    # direction along a level line
    u = A / np.linalg.norm(A)
    s = 0.32
    corner = np.array([0.0, 0.0]) + s * (u + d)
    ax.plot([s * u[0], corner[0], s * d[0]], [s * u[1], corner[1], s * d[1]],
            color="#d62728", lw=1.1)

    ax.axhline(0, color="k", lw=0.8)
    ax.axvline(0, color="k", lw=0.8)
    ax.set_xlim(-3.0, 4.0)
    ax.set_ylim(-3.4, 4.4)
    ax.set_xlabel(r"$x_1$")
    ax.set_ylabel(r"$x_2$")
    ax.set_title(r"Nivo krivulje od $f(x)=a^\top x$" "\n"
                 r"za $a=(2,1)^\top$", pad=10)
    ax.grid(alpha=0.25)
    ax.set_aspect("equal", adjustable="box")

    OUT.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(OUT / "02-nivo-krivulje-linearne.png", dpi=160)


if __name__ == "__main__":
    main()
