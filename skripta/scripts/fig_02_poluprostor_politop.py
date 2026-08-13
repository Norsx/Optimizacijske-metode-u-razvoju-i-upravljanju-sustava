"""Half-space and polytope figures for Zadaci 3 and 4 of Vjezbe 1.

The slides state both tasks but the shaded pictures were drawn on the blackboard,
so the source PDF carries no figure and no worked solution.  These two plots are
therefore concrete examples built from the definitions given in the same
exercise deck, and the script is flagged as such in the notes.

Half-space:  2*x1 + 3*x2 <= 6
Polytope:    -x1 <= 0, -x2 <= 0, x1 + x2 <= 4, x1 <= 3
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parents[1] / "figures"

SIVA = "#BFBFBF"
PLAVA = "#1F3864"
CRVENA = "#D62728"


def poluprostor() -> None:
    fig, ax = plt.subplots(figsize=(6.2, 5.4))

    a = np.array([2.0, 3.0])
    b = 6.0

    x1 = np.linspace(-2.0, 5.0, 400)
    x2_granica = (b - a[0] * x1) / a[1]

    ax.fill_between(x1, -2.5, x2_granica, color=SIVA, alpha=0.85, zorder=0)
    ax.plot(x1, x2_granica, color=PLAVA, lw=2.2,
            label=r"$a^\top x = b$:  $2x_1+3x_2=6$")

    # the normal vector a, drawn from a point on the boundary
    x0 = np.array([1.5, 1.0])           # 2*1.5 + 3*1 = 6, on the boundary
    ax.plot(*x0, marker="o", ms=6, color=PLAVA, zorder=5)
    ax.annotate(r"$x_0$", xy=x0, xytext=(-22, -14), textcoords="offset points",
                fontsize=11, color=PLAVA)
    ax.annotate("", xy=x0 + 0.42 * a, xytext=x0,
                arrowprops=dict(arrowstyle="-|>", lw=2.4, color=CRVENA))
    ax.annotate(r"$a=\binom{2}{3}$", xy=x0 + 0.42 * a, xytext=(8, 0),
                textcoords="offset points", fontsize=11, color=CRVENA)

    ax.text(-0.6, -1.4, r"$a^\top x \leq b$" "\n" "(osjenčano)", fontsize=11)
    ax.text(3.0, 2.6, r"$a^\top x \geq b$", fontsize=11)

    ax.axhline(0, color="k", lw=0.8)
    ax.axvline(0, color="k", lw=0.8)
    ax.set_xlim(-2.0, 5.0)
    ax.set_ylim(-2.5, 4.0)
    ax.set_xlabel(r"$x_1$")
    ax.set_ylabel(r"$x_2$")
    ax.set_title(r"Poluprostor $\{x \mid a^\top x \leq b\}$")
    ax.grid(alpha=0.25)
    ax.legend(loc="upper right", fontsize=9)
    ax.set_aspect("equal", adjustable="box")

    fig.tight_layout()
    fig.savefig(OUT / "02-poluprostor.png", dpi=160)
    plt.close(fig)


def politop() -> None:
    fig, ax = plt.subplots(figsize=(6.2, 5.4))

    vrhovi = np.array([[0.0, 0.0], [3.0, 0.0], [3.0, 1.0], [0.0, 4.0]])
    ax.fill(vrhovi[:, 0], vrhovi[:, 1], color=SIVA, alpha=0.85, zorder=0)

    t = np.linspace(-1.5, 5.5, 200)
    linije = [
        (t, np.zeros_like(t), r"$-x_2 \leq 0$"),                # x2 = 0
        (np.zeros_like(t), t, r"$-x_1 \leq 0$"),                # x1 = 0
        (t, 4.0 - t, r"$x_1 + x_2 \leq 4$"),                    # x1 + x2 = 4
        (3.0 * np.ones_like(t), t, r"$x_1 \leq 3$"),            # x1 = 3
    ]
    boje = ["#2CA02C", "#9467BD", "#1F3864", "#B35C00"]
    for (xx, yy, lab), boja in zip(linije, boje):
        ax.plot(xx, yy, lw=1.9, color=boja, label=lab)

    for v in vrhovi:
        ax.plot(*v, marker="o", ms=6, color="k", zorder=5)
    for v, dx, dy in zip(vrhovi, (-26, 8, 8, -30), (-16, -16, 6, 6)):
        ax.annotate(f"$({v[0]:.0f},{v[1]:.0f})$", xy=v, xytext=(dx, dy),
                    textcoords="offset points", fontsize=9)

    ax.set_xlim(-1.5, 5.0)
    ax.set_ylim(-1.5, 5.0)
    ax.set_xlabel(r"$x_1$")
    ax.set_ylabel(r"$x_2$")
    ax.set_title(r"Politop $\{x \mid Ax \leq b\}$")
    ax.grid(alpha=0.25)
    ax.legend(loc="upper right", fontsize=9)
    ax.set_aspect("equal", adjustable="box")

    fig.tight_layout()
    fig.savefig(OUT / "02-politop.png", dpi=160)
    plt.close(fig)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    poluprostor()
    politop()


if __name__ == "__main__":
    main()
