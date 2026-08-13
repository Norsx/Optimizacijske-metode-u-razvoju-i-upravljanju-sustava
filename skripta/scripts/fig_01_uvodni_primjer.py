"""Feasible set and objective level curves of the introductory example.

Reproduces the plot on slide 15 of 01_Uvod.pdf:

    min (x1-2)^2 + (x2-1)^2   s.t.   x1^2 - x2 <= 0,  x1 + x2 - 2 <= 0

The infeasible region is filled, the feasible lens is left white, the level
curves of the objective are drawn as circles around (2, 1) and the optimum
(1, 1) is marked.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parents[1] / "figures"

X1_RANGE = (-2.0, 3.0)
X2_RANGE = (-2.0, 4.0)


def main() -> None:
    x1 = np.linspace(*X1_RANGE, 801)
    x2 = np.linspace(*X2_RANGE, 801)
    X1, X2 = np.meshgrid(x1, x2)

    g1 = X1**2 - X2
    g2 = X1 + X2 - 2
    feasible = (g1 <= 0) & (g2 <= 0)

    fig, ax = plt.subplots(figsize=(7.0, 6.4))

    # infeasible region red, feasible lens white
    ax.contourf(X1, X2, np.where(feasible, 1.0, 0.0), levels=[-0.5, 0.5, 1.5],
                colors=["#d62728", "#ffffff"])

    # constraint boundaries
    ax.plot(x1, x1**2, color="#1f77b4", lw=2.0, label=r"$g_1(x)=x_1^2-x_2=0$")
    ax.plot(x1, 2.0 - x1, color="#2ca02c", lw=2.0, label=r"$g_2(x)=x_1+x_2-2=0$")

    # level curves of the objective
    F = (X1 - 2.0) ** 2 + (X2 - 1.0) ** 2
    cs = ax.contour(X1, X2, F, levels=[0.25, 1.0, 2.0, 4.0, 6.0, 9.0],
                    colors="#3b3b8f", linewidths=0.9)
    ax.clabel(cs, fmt="%.2g", fontsize=8)

    # unconstrained minimiser and constrained optimum
    ax.plot(2.0, 1.0, marker="+", ms=12, mew=2, color="k")
    ax.annotate(r"$(2,1)$: minimum bez ograničenja", xy=(2.0, 1.0),
                xytext=(1.35, -0.9), fontsize=9,
                arrowprops=dict(arrowstyle="->", lw=0.8))
    ax.plot(1.0, 1.0, marker="o", ms=8, color="k", zorder=5)
    ax.annotate(r"$x^\star=(1,1)$,  $f(x^\star)=1$", xy=(1.0, 1.0),
                xytext=(-1.85, 2.9), fontsize=10,
                arrowprops=dict(arrowstyle="->", lw=0.8))

    ax.set_xlim(*X1_RANGE)
    ax.set_ylim(*X2_RANGE)
    ax.set_xlabel(r"$x_1$")
    ax.set_ylabel(r"$x_2$")
    ax.set_title("Dozvoljeni skup i nivo krivulje funkcije cilja")
    ax.legend(loc="upper right", fontsize=9, framealpha=0.95)
    ax.grid(alpha=0.25)
    ax.set_aspect("equal", adjustable="box")

    OUT.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(OUT / "01-uvodni-primjer.png", dpi=160)


if __name__ == "__main__":
    main()
