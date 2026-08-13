r"""Figures for the chapter on robust optimisation (lecture 08).

Reproduces Primjer 1 and Primjer 2: the nominal LP, the robust counterpart, and
the shrinking of the feasible set caused by the uncertainty.  The three panels
match slides 8, 9 and 17-19.

    min  c'x = [-50, 10] x
    s.t. A x <= b,   A = [[-1,-1],[1,-1],[1,1],[-1,1]],  b = [-10,10,30,10]

Primjer 1: every element of A varies independently by +-5 %.
Primjer 2: the same two relative perturbations delta1, delta2 act on x1 and x2
           in all constraints, i.e. A(I + Delta) x <= b.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import linprog

OUT = Path(__file__).resolve().parents[1] / "figures"

A = np.array([[-1.0, -1.0], [1.0, -1.0], [1.0, 1.0], [-1.0, 1.0]])
B = np.array([-10.0, 10.0, 30.0, 10.0])
Cvec = np.array([-50.0, 10.0])

ZELENA = "#1E6B3A"
CRVENA = "#D62728"
PLAVA = "#1F4FD8"
SIVA = "#BFBFBF"


def nominalno() -> np.ndarray:
    r = linprog(Cvec, A_ub=A, b_ub=B, bounds=[(None, None)] * 2)
    return r.x


def robusno_primjer1(rel: float = 0.05) -> np.ndarray:
    """Independent +-rel perturbation of every element of A.

    sup over the box of a'x equals nominal'x + rel * sum_j |a_j| |x_j|, so the
    robust constraint is written with auxiliary variables t_j >= |x_j|.
    Variables: (x1, x2, t1, t2).
    """
    n = 2
    c = np.concatenate([Cvec, np.zeros(n)])
    rows, rhs = [], []
    for i in range(A.shape[0]):
        rows.append(np.concatenate([A[i], rel * np.abs(A[i])]))
        rhs.append(B[i])
    for j in range(n):                      # t_j >= x_j and t_j >= -x_j
        e = np.zeros(2 * n)
        e[j], e[n + j] = 1.0, -1.0
        rows.append(e.copy())
        rhs.append(0.0)
        e[j] = -1.0
        rows.append(e.copy())
        rhs.append(0.0)
    r = linprog(c, A_ub=np.array(rows), b_ub=np.array(rhs),
                bounds=[(None, None)] * (2 * n))
    return r.x[:n]


def robusno_primjer2(d1: float = 0.05, d2: float = 0.05,
                     cvec: np.ndarray | None = None) -> np.ndarray:
    """A (I + Delta) x <= b at every vertex of the Delta box."""
    if cvec is None:
        cvec = Cvec
    rows, rhs = [], []
    for s1 in (-d1, d1):
        for s2 in (-d2, d2):
            Delta = np.diag([s1, s2])
            for i, row in enumerate(A @ (np.eye(2) + Delta)):
                rows.append(row)
                rhs.append(B[i])
    r = linprog(cvec, A_ub=np.array(rows), b_ub=np.array(rhs),
                bounds=[(None, None)] * 2)
    return r.x


def _nacrtaj_skup(ax, matrice: list[np.ndarray], boja: str, lw: float,
                  fill: bool, label: str | None) -> None:
    """Shade {x | M x <= b for every M} on a grid, and draw its boundary."""
    g = np.linspace(-2.0, 34.0, 700)
    X1, X2 = np.meshgrid(g, g)
    ok = np.ones_like(X1, dtype=bool)
    for M in matrice:
        for i in range(M.shape[0]):
            ok &= (M[i, 0] * X1 + M[i, 1] * X2 <= B[i] + 1e-12)
    if fill:
        ax.contourf(X1, X2, ok.astype(float), levels=[0.5, 1.5],
                    colors=[boja], alpha=0.35)
    ax.contour(X1, X2, ok.astype(float), levels=[0.5], colors=[boja],
               linewidths=lw)
    if label:
        ax.plot([], [], color=boja, lw=lw, label=label)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    x_nom = nominalno()
    x_r1 = robusno_primjer1()
    x_r2 = robusno_primjer2()
    x_r2b = robusno_primjer2(0.05, 0.15)
    x_r2c = robusno_primjer2(0.05, 0.15, np.array([0.0, -50.0]))

    print("nominalno        x* =", np.round(x_nom, 4),
          " c'x =", round(float(Cvec @ x_nom), 4))
    print("Primjer 1 robust x* =", np.round(x_r1, 4),
          " c'x =", round(float(Cvec @ x_r1), 4))
    print("Primjer 2 robust x* =", np.round(x_r2, 4),
          " c'x =", round(float(Cvec @ x_r2), 4))
    print("Primjer 2, d2=0.15  x* =", np.round(x_r2b, 4))
    print("Primjer 2, c=[0,-50] x* =", np.round(x_r2c, 4))

    vrhovi2 = [A @ (np.eye(2) + np.diag([s1, s2]))
               for s1 in (-0.05, 0.05) for s2 in (-0.05, 0.05)]

    fig, axs = plt.subplots(1, 2, figsize=(10.4, 4.9))

    # --- left: nominal problem -------------------------------------------
    ax = axs[0]
    _nacrtaj_skup(ax, [A], PLAVA, 2.0, True, "nominalni dozvoljeni skup")
    for val in (-1200, -900, -600, -300, 0):
        t = np.linspace(-2, 34, 20)
        ax.plot(t, (val - Cvec[0] * t) / Cvec[1], ls="--", lw=0.8,
                color="#8a8a8a")
    ax.plot(*x_nom, marker="o", ms=10, color=CRVENA, zorder=6)
    ax.annotate(rf"$x^\star=({x_nom[0]:.4g},\ {x_nom[1]:.4g})$", xy=x_nom,
                xytext=(-140, 14), textcoords="offset points", fontsize=10,
                color=CRVENA)
    ax.set_title("Nominalno rješenje", fontsize=11)

    # --- right: robust problem -------------------------------------------
    ax = axs[1]
    _nacrtaj_skup(ax, [A], PLAVA, 1.4, False, "nominalni skup")
    _nacrtaj_skup(ax, vrhovi2, ZELENA, 2.0, True, "robusni skup (presjek)")
    for val in (-1200, -900, -600, -300, 0):
        t = np.linspace(-2, 34, 20)
        ax.plot(t, (val - Cvec[0] * t) / Cvec[1], ls="--", lw=0.8,
                color="#8a8a8a")
    ax.plot(*x_nom, marker="o", ms=8, color=PLAVA, alpha=0.6, zorder=5)
    ax.plot(*x_r2, marker="o", ms=10, color=CRVENA, zorder=6)
    ax.annotate(rf"$x^\star=({x_r2[0]:.4f},\ {x_r2[1]:.4g})$", xy=x_r2,
                xytext=(-150, 14), textcoords="offset points", fontsize=10,
                color=CRVENA)
    ax.set_title("Robusno rješenje ($\\pm5\\,\\%$)", fontsize=11)

    for ax in axs:
        ax.set_xlim(-2.0, 34.0)
        ax.set_ylim(-2.0, 34.0)
        ax.set_xlabel(r"$x_1$")
        ax.set_ylabel(r"$x_2$")
        ax.grid(alpha=0.22)
        ax.legend(loc="upper right", fontsize=8)
        ax.set_aspect("equal", adjustable="box")

    fig.tight_layout()
    fig.savefig(OUT / "08-robusni-lp.png", dpi=160)
    plt.close(fig)


if __name__ == "__main__":
    main()
