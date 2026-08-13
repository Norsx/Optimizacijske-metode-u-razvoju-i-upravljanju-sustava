"""Figures for the chapter on optimality conditions (lecture 03).

1. 03-sedlo-disk.png     -- min x1^2 - x2^2 on the unit disc: level curves,
   the two boundary points examined on slides 10-18, their gradients and the
   cones of feasible directions.

2. 03-jednakost-krug.png -- min x1 + x2 subject to x1^2 + x2^2 = 2, redrawing
   slide 26: -grad f (green), grad h (red) and the feasible directions (blue)
   tangent to the circle.

3. 03-nejednakost-krug.png -- the same objective with the constraint relaxed to
   x1^2 + x2^2 - 2 <= 0 (slide 41), showing the feasible disc and the optimum.
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


def sedlo_disk() -> None:
    fig, ax = plt.subplots(figsize=(6.4, 6.0))

    t = np.linspace(-1.5, 1.5, 500)
    X1, X2 = np.meshgrid(t, t)
    F = X1**2 - X2**2

    cs = ax.contour(X1, X2, F, levels=np.linspace(-2.0, 2.0, 17),
                    colors="#7a7a9a", linewidths=0.7)
    ax.clabel(cs, cs.levels[::4], fmt="%.1f", fontsize=7)

    th = np.linspace(0.0, 2.0 * np.pi, 400)
    ax.fill(np.cos(th), np.sin(th), color=SIVA, alpha=0.45, zorder=0)
    ax.plot(np.cos(th), np.sin(th), color=CRVENA, lw=2.0,
            label=r"rub: $x_1^2+x_2^2=1$")

    # candidate 1: (0, 1) -- a local minimum
    p1 = np.array([0.0, 1.0])
    g1 = np.array([0.0, -2.0])                       # grad f = (2x1, -2x2)
    ax.plot(*p1, marker="o", ms=8, color="k", zorder=6)
    ax.annotate("", xy=p1 + 0.36 * g1, xytext=p1,
                arrowprops=dict(arrowstyle="-|>", lw=2.2, color=ZELENA))
    ax.annotate(r"$x^*=(0,1)$" "\n" r"$\nabla f=(0,-2)$", xy=p1,
                xytext=(-98, 16), textcoords="offset points", fontsize=9)

    # candidate 2: (1, 0) -- not a minimum
    p2 = np.array([1.0, 0.0])
    g2 = np.array([2.0, 0.0])
    ax.plot(*p2, marker="s", ms=8, color="k", zorder=6)
    ax.annotate("", xy=p2 + 0.36 * g2, xytext=p2,
                arrowprops=dict(arrowstyle="-|>", lw=2.2, color=ZELENA))
    ax.annotate(r"$x^*=(1,0)$" "\n" r"$\nabla f=(2,0)$", xy=p2,
                xytext=(-20, -46), textcoords="offset points", fontsize=9)

    # cones of feasible directions, drawn as short blue arrows
    for base, dirs in ((p1, [(-1, 0), (1, 0), (-0.7, -0.7), (0.7, -0.7), (0, -1)]),
                       (p2, [(0, 1), (0, -1), (-0.7, 0.7), (-0.7, -0.7), (-1, 0)])):
        for d in dirs:
            d = np.array(d, dtype=float)
            d /= np.linalg.norm(d)
            ax.annotate("", xy=base + 0.28 * d, xytext=base,
                        arrowprops=dict(arrowstyle="-|>", lw=1.2, color=PLAVA))

    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_xlabel(r"$x_1$")
    ax.set_ylabel(r"$x_2$")
    ax.set_title(r"$\min\ x_1^2-x_2^2$  uz  $x_1^2+x_2^2 \leq 1$")
    ax.grid(alpha=0.22)
    ax.legend(loc="lower left", fontsize=8, framealpha=0.95)
    ax.set_aspect("equal", adjustable="box")

    fig.tight_layout()
    fig.savefig(OUT / "03-sedlo-disk.png", dpi=160)
    plt.close(fig)


def jednakost_krug() -> None:
    fig, ax = plt.subplots(figsize=(6.4, 6.2))

    r = np.sqrt(2.0)
    th = np.linspace(0.0, 2.0 * np.pi, 400)
    ax.plot(r * np.cos(th), r * np.sin(th), color=PLAVA, lw=1.8,
            label=r"ograničenje  $x_1^2+x_2^2=2$")

    # level curves of f = x1 + x2 are parallel lines
    t = np.linspace(-2.4, 2.4, 100)
    for c in (-3, -2, -1, 0, 1, 2, 3):
        ax.plot(t, c - t, color="#8a8a8a", lw=0.7)

    # arrows at sample points on the circle
    for a in np.linspace(0.0, 2.0 * np.pi, 16, endpoint=False):
        p = r * np.array([np.cos(a), np.sin(a)])
        grad_h = np.array([2.0 * p[0], 2.0 * p[1]])       # h = x1^2+x2^2-2
        grad_h = grad_h / np.linalg.norm(grad_h)
        tang = np.array([-grad_h[1], grad_h[0]])
        minus_grad_f = -np.array([1.0, 1.0]) / np.sqrt(2.0)

        ax.annotate("", xy=p + 0.42 * grad_h, xytext=p,
                    arrowprops=dict(arrowstyle="-|>", lw=1.5, color=CRVENA))
        for s in (+1.0, -1.0):
            ax.annotate("", xy=p + 0.30 * s * tang, xytext=p,
                        arrowprops=dict(arrowstyle="-|>", lw=1.3, color=PLAVA))
        ax.annotate("", xy=p + 0.42 * minus_grad_f, xytext=p,
                    arrowprops=dict(arrowstyle="-|>", lw=1.5, color=ZELENA))

    # the optimum
    xs = np.array([-1.0, -1.0])
    ax.plot(*xs, marker="o", ms=9, color="k", zorder=6)
    ax.annotate(r"$x^\star=(-1,-1)$", xy=xs, xytext=(-30, -34),
                textcoords="offset points", fontsize=10)

    ax.plot([], [], color=ZELENA, lw=1.8, label=r"zeleno: $-\nabla f(x)$")
    ax.plot([], [], color=CRVENA, lw=1.8, label=r"crveno: $\nabla h(x)$")
    ax.plot([], [], color=PLAVA, lw=1.4,
            label=r"plavo: dozvoljeni smjerovi $d$")

    ax.set_xlim(-2.4, 2.4)
    ax.set_ylim(-2.4, 2.4)
    ax.set_xlabel(r"$x_1$")
    ax.set_ylabel(r"$x_2$")
    ax.set_title(r"$\min\ x_1+x_2$  uz  $x_1^2+x_2^2=2$")
    ax.grid(alpha=0.22)
    ax.legend(loc="upper right", fontsize=8, framealpha=0.95)
    ax.set_aspect("equal", adjustable="box")

    fig.tight_layout()
    fig.savefig(OUT / "03-jednakost-krug.png", dpi=160)
    plt.close(fig)


def nejednakost_krug() -> None:
    fig, ax = plt.subplots(figsize=(6.4, 6.0))

    r = np.sqrt(2.0)
    th = np.linspace(0.0, 2.0 * np.pi, 400)
    ax.fill(r * np.cos(th), r * np.sin(th), color=SIVA, alpha=0.5, zorder=0)
    ax.plot(r * np.cos(th), r * np.sin(th), color=PLAVA, lw=1.9,
            label=r"$g(x)=x_1^2+x_2^2-2=0$")

    t = np.linspace(-2.4, 2.4, 100)
    for c in (-3, -2, -1, 0, 1, 2, 3):
        ax.plot(t, c - t, color="#8a8a8a", lw=0.7)
        if -2.3 < c / 2.0 < 2.3:
            ax.annotate(f"$f={c}$", xy=(c / 2.0, c / 2.0), fontsize=7,
                        color="#5a5a5a", rotation=-45,
                        ha="center", va="bottom")

    xs = np.array([-1.0, -1.0])
    grad_f = np.array([1.0, 1.0])
    grad_g = np.array([2.0 * xs[0], 2.0 * xs[1]])       # = (-2, -2)

    ax.plot(*xs, marker="o", ms=9, color="k", zorder=6)
    ax.annotate("", xy=xs + 0.5 * grad_f, xytext=xs,
                arrowprops=dict(arrowstyle="-|>", lw=2.2, color=ZELENA))
    ax.annotate(r"$\nabla f=(1,1)$", xy=xs + 0.5 * grad_f, xytext=(6, -4),
                textcoords="offset points", fontsize=9, color=ZELENA)
    ax.annotate("", xy=xs + 0.25 * grad_g, xytext=xs,
                arrowprops=dict(arrowstyle="-|>", lw=2.2, color=CRVENA))
    ax.annotate(r"$\nabla g=(-2,-2)$", xy=xs + 0.25 * grad_g, xytext=(-118, -16),
                textcoords="offset points", fontsize=9, color=CRVENA)
    ax.annotate(r"$x^\star=(-1,-1)$", xy=xs, xytext=(10, 12),
                textcoords="offset points", fontsize=10)

    ax.set_xlim(-2.4, 2.4)
    ax.set_ylim(-2.4, 2.4)
    ax.set_xlabel(r"$x_1$")
    ax.set_ylabel(r"$x_2$")
    ax.set_title(r"$\min\ x_1+x_2$  uz  $x_1^2+x_2^2-2 \leq 0$")
    ax.grid(alpha=0.22)
    ax.legend(loc="upper right", fontsize=8, framealpha=0.95)
    ax.set_aspect("equal", adjustable="box")

    fig.tight_layout()
    fig.savefig(OUT / "03-nejednakost-krug.png", dpi=160)
    plt.close(fig)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sedlo_disk()
    jednakost_krug()
    nejednakost_krug()


if __name__ == "__main__":
    main()
