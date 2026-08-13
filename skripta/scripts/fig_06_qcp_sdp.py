"""Figures for the chapter on conic quadratic and semidefinite programming.

1. 06-konus.png          -- the second-order cone in R^3, the set whose
   membership defines a CQP constraint.
2. 06-klasifikacija.png  -- linear classification: the separating hyperplane,
   the two margin hyperplanes H1 and H2, and the margin 2/||a||_2 that the
   robust classifier maximises.
3. 06-robusni-lp.png     -- an ellipsoidal uncertainty set around a_i and the
   worst-case constraint it produces.
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


def konus() -> None:
    fig = plt.figure(figsize=(5.8, 5.2))
    ax = fig.add_subplot(111, projection="3d")

    th = np.linspace(0.0, 2.0 * np.pi, 90)
    h = np.linspace(0.0, 1.0, 40)
    TH, H = np.meshgrid(th, h)
    X = H * np.cos(TH)
    Y = H * np.sin(TH)

    ax.plot_surface(X, Y, H, alpha=0.55, color="#7ba7e8",
                    linewidth=0, antialiased=True)
    ax.plot(np.cos(th), np.sin(th), np.ones_like(th), color=PLAVA, lw=1.6)

    ax.set_xlabel(r"$x_1$")
    ax.set_ylabel(r"$x_2$")
    ax.set_zlabel(r"$x_3$")
    ax.set_title(r"Konus drugog stupnja:  $x_3 \geq \sqrt{x_1^2+x_2^2}$",
                 fontsize=11)
    ax.view_init(elev=18, azim=-58)
    ax.set_box_aspect((1.0, 1.0, 0.85))

    fig.tight_layout()
    fig.savefig(OUT / "06-konus.png", dpi=160)
    plt.close(fig)


def klasifikacija() -> None:
    rng = np.random.default_rng(7)
    X = rng.normal([2.6, 2.6], 0.62, size=(18, 2))     # class "x"
    Y = rng.normal([0.5, 0.6], 0.62, size=(18, 2))     # class "y"

    # a separating direction chosen so both margins are respected
    a = np.array([1.0, 1.0])
    # pick b so that min over X of a'x + b == 1 and max over Y == -1 (scale a)
    lo = (X @ a).min()
    hi = (Y @ a).max()
    scale = 2.0 / (lo - hi)
    a = a * scale
    b = 1.0 - (X @ a).min()

    fig, ax = plt.subplots(figsize=(6.4, 5.4))
    ax.plot(X[:, 0], X[:, 1], "o", ms=7, color=PLAVA, label=r"$x_i$")
    ax.plot(Y[:, 0], Y[:, 1], "s", ms=7, color=CRVENA, label=r"$y_j$")

    t = np.linspace(-1.6, 4.8, 50)
    for c, boja, stil, lab in ((1.0, PLAVA, "--", r"$H_1:\ a^\top z+b=1$"),
                               (0.0, "k", "-", r"$a^\top z+b=0$"),
                               (-1.0, CRVENA, "--", r"$H_2:\ a^\top z+b=-1$")):
        ax.plot(t, (c - b - a[0] * t) / a[1], stil, lw=1.8, color=boja,
                label=lab)

    # margin arrow between H1 and H2, drawn along a / ||a||
    n = a / np.linalg.norm(a)
    sirina = 2.0 / np.linalg.norm(a)
    p0 = np.array([1.6, ( -b - a[0] * 1.6) / a[1]])
    ax.annotate("", xy=p0 + sirina * n, xytext=p0 - 0.0 * n,
                arrowprops=dict(arrowstyle="<->", lw=2.0, color=ZELENA))
    ax.annotate(r"$\dfrac{2}{\|a\|_2}$", xy=p0 + 0.5 * sirina * n,
                xytext=(14, -6), textcoords="offset points",
                fontsize=13, color=ZELENA)

    ax.set_xlim(-1.4, 4.6)
    ax.set_ylim(-1.4, 4.6)
    ax.set_xlabel(r"$z_1$")
    ax.set_ylabel(r"$z_2$")
    ax.set_title("Robusna linearna klasifikacija: maksimizacija margine")
    ax.grid(alpha=0.22)
    ax.legend(loc="lower right", fontsize=8, framealpha=0.95)
    ax.set_aspect("equal", adjustable="box")

    fig.tight_layout()
    fig.savefig(OUT / "06-klasifikacija.png", dpi=160)
    plt.close(fig)


def robusni_lp() -> None:
    fig, ax = plt.subplots(figsize=(6.2, 5.0))

    a_bar = np.array([1.0, 0.7])
    P = np.array([[0.34, 0.10], [0.10, 0.20]])

    th = np.linspace(0.0, 2.0 * np.pi, 300)
    U = np.vstack([np.cos(th), np.sin(th)])
    E = a_bar[:, None] + P @ U
    ax.fill(E[0], E[1], color=SIVA, alpha=0.7, zorder=0)
    ax.plot(E[0], E[1], color=PLAVA, lw=1.8,
            label=r"$\mathcal{E}_i=\{\bar a_i+P_iu \mid \|u\|_2\leq1\}$")
    ax.plot(*a_bar, marker="o", ms=8, color=PLAVA, zorder=5)
    ax.annotate(r"$\bar a_i$", xy=a_bar, xytext=(8, 6),
                textcoords="offset points", fontsize=12, color=PLAVA)

    # worst-case direction: the point of E maximising a'x for a fixed x
    x = np.array([1.0, 0.35])
    x = x / np.linalg.norm(x)
    u_worst = (P.T @ x) / np.linalg.norm(P.T @ x)
    a_worst = a_bar + P @ u_worst
    ax.plot(*a_worst, marker="*", ms=16, color=CRVENA, zorder=6)
    ax.annotate(r"najgori $a_i$", xy=a_worst, xytext=(8, -18),
                textcoords="offset points", fontsize=10, color=CRVENA)
    ax.annotate("", xy=a_bar + 0.9 * x, xytext=a_bar,
                arrowprops=dict(arrowstyle="-|>", lw=2.0, color=ZELENA))
    ax.annotate(r"smjer $x$", xy=a_bar + 0.9 * x, xytext=(4, 8),
                textcoords="offset points", fontsize=10, color=ZELENA)

    ax.set_xlim(0.1, 2.3)
    ax.set_ylim(0.0, 1.6)
    ax.set_xlabel(r"$(a_i)_1$")
    ax.set_ylabel(r"$(a_i)_2$")
    ax.set_title(r"Elipsoidna nesigurnost:  "
                 r"$\sup_{a_i\in\mathcal{E}_i} a_i^\top x"
                 r" = \bar a_i^\top x + \|P_i^\top x\|_2$", fontsize=10)
    ax.grid(alpha=0.22)
    ax.legend(loc="upper right", fontsize=8)
    ax.set_aspect("equal", adjustable="box")

    fig.tight_layout()
    fig.savefig(OUT / "06-robusni-lp.png", dpi=160)
    plt.close(fig)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    konus()
    klasifikacija()
    robusni_lp()


if __name__ == "__main__":
    main()
