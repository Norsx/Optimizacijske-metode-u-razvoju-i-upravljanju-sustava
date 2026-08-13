"""Figures for the chapter on Lagrangian duality (lecture 04 + Vjezbe 3).

1. 04-primjer2-kkt.png -- Primjer 2 from Vjezbe 3: the box constraint set
   0 <= x1 <= 2, 0 <= x2 <= 1, the circular level curves of
   (x1-3)^2 + (x2-2)^2 and the KKT point (2, 1) with its two active-constraint
   gradients.

2. 04-ponuda-potraznja.png -- the aggregated supply and demand curves whose
   intersection fixes the market price lambda*, redrawing the sketch on
   Vjezbe 3, str. 15.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parents[1] / "figures"

ZELENA = "#1E6B3A"
CRVENA = "#D62728"
PLAVA = "#1F4FD8"
SIVA = "#BFBFBF"


def primjer2_kkt() -> None:
    fig, ax = plt.subplots(figsize=(6.8, 5.6))

    # feasible box
    ax.fill([0, 2, 2, 0], [0, 0, 1, 1], color=SIVA, alpha=0.6, zorder=0)
    ax.plot([0, 2, 2, 0, 0], [0, 0, 1, 1, 0], color=PLAVA, lw=2.0)

    # level curves of the objective, circles around (3, 2)
    th = np.linspace(0.0, 2.0 * np.pi, 400)
    for c in (0.5, 1.0, 2.0, 4.0, 6.0, 9.0):
        r = np.sqrt(c)
        ax.plot(3.0 + r * np.cos(th), 2.0 + r * np.sin(th),
                color="#7a7a9a", lw=0.8)
        ax.annotate(f"$f={c:g}$", xy=(3.0, 2.0 + r), fontsize=7,
                    color="#5a5a5a", ha="center", va="bottom")

    # unconstrained minimiser
    ax.plot(3.0, 2.0, marker="+", ms=13, mew=2.2, color="k")
    ax.annotate(r"$(3,2)$: min bez ograničenja", xy=(3.0, 2.0),
                xytext=(8, 8), textcoords="offset points", fontsize=9)

    # KKT point
    xs = np.array([2.0, 1.0])
    ax.plot(*xs, marker="o", ms=9, color="k", zorder=6)
    ax.annotate(r"$x^\star=(2,1)$,  $p^\star=2$", xy=xs, xytext=(-42, -30),
                textcoords="offset points", fontsize=10)

    grad_f = np.array([2 * xs[0] - 6, 2 * xs[1] - 4])          # = (-2, -2)
    ax.annotate("", xy=xs + 0.42 * grad_f, xytext=xs,
                arrowprops=dict(arrowstyle="-|>", lw=2.2, color=ZELENA))
    ax.annotate(r"$\nabla f=(-2,-2)$", xy=xs + 0.42 * grad_f, xytext=(-116, 6),
                textcoords="offset points", fontsize=9, color=ZELENA)

    # gradients of the two active constraints, scaled by their multipliers
    for g, lab, off in ((np.array([1.0, 0.0]), r"$\mu_2\nabla g_2$", (8, -14)),
                        (np.array([0.0, 1.0]), r"$\mu_4\nabla g_4$", (6, 4))):
        ax.annotate("", xy=xs + 0.42 * 2.0 * g, xytext=xs,
                    arrowprops=dict(arrowstyle="-|>", lw=2.0, color=CRVENA))
        ax.annotate(lab, xy=xs + 0.42 * 2.0 * g, xytext=off,
                    textcoords="offset points", fontsize=9, color=CRVENA)

    ax.set_xlim(-0.8, 4.6)
    ax.set_ylim(-0.9, 3.6)
    ax.set_xlabel(r"$x_1$")
    ax.set_ylabel(r"$x_2$")
    ax.set_title(r"Vježbe 3, Primjer 2: $\min\ (x_1-3)^2+(x_2-2)^2$"
                 "\n"
                 r"uz  $0\leq x_1\leq 2$,  $0\leq x_2\leq 1$")
    ax.grid(alpha=0.22)
    ax.set_aspect("equal", adjustable="box")

    fig.tight_layout()
    fig.savefig(OUT / "04-primjer2-kkt.png", dpi=160)
    plt.close(fig)


def ponuda_potraznja() -> None:
    fig, ax = plt.subplots(figsize=(6.4, 4.8))

    # aggregated curves drawn as staircases, as on the slide
    p_supply = np.array([0.0, 0.6, 0.6, 1.6, 1.6, 2.8, 2.8, 3.6, 3.6, 4.4])
    l_supply = np.array([8.0, 8.0, 14.0, 14.0, 22.0, 22.0, 33.0, 33.0, 52.0, 52.0])

    p_demand = np.array([0.0, 0.8, 0.8, 1.9, 1.9, 2.9, 2.9, 3.8, 3.8, 4.4])
    l_demand = np.array([60.0, 60.0, 44.0, 44.0, 30.0, 30.0, 18.0, 18.0, 6.0, 6.0])

    ax.plot(p_supply, l_supply, color=ZELENA, lw=2.0, label="agregirana ponuda")
    ax.plot(p_demand, l_demand, color=PLAVA, lw=2.0, label="agregirana potražnja")

    # the crossing point: both curves sit at 22 / 30 over 1.9 .. 2.8
    p_star, l_star = 2.35, 26.0
    ax.plot(p_star, l_star, marker="o", ms=9, color=CRVENA, zorder=6)
    ax.plot([0, p_star], [l_star, l_star], ls="--", lw=1.0, color=CRVENA)
    ax.plot([p_star, p_star], [0, l_star], ls="--", lw=1.0, color=CRVENA)
    ax.annotate(r"$\lambda^\star$", xy=(0, l_star), xytext=(-30, -6),
                textcoords="offset points", fontsize=12, color=CRVENA)
    ax.annotate(r"$\sum_i p_i^\star=\sum_j d_j^\star$", xy=(p_star, 0),
                xytext=(-46, -30), textcoords="offset points", fontsize=10,
                color=CRVENA)

    ax.set_xlim(0.0, 4.4)
    ax.set_ylim(0.0, 62.0)
    ax.set_xlabel("snaga / energija")
    ax.set_ylabel(r"cijena $\lambda$")
    ax.set_title("Tržišna cijena kao sjecište agregiranih krivulja")
    ax.grid(alpha=0.22)
    ax.legend(loc="upper center", fontsize=9)

    fig.tight_layout()
    fig.savefig(OUT / "04-ponuda-potraznja.png", dpi=160)
    plt.close(fig)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    primjer2_kkt()
    ponuda_potraznja()


if __name__ == "__main__":
    main()
