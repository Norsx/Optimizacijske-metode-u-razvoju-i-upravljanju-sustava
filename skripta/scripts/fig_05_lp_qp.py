"""Figures for the chapter on linear and quadratic programming.

1. 05-lp-geometrija.png     -- an LP over a polytope: parallel level lines of
   c'x, the descent direction -c and the optimum sitting in a vertex.
2. 05-aproksimacije.png     -- the same data fitted in the 2-, infinity- and
   1-norm, showing how the choice of norm changes the fit.
3. 05-rekonstrukcija.png    -- Primjer 4 of Vjezbe 4: a noisy signal
   reconstructed by quadratic regularisation for three values of delta.
4. 05-mreza.png             -- the transport network of Vjezbe 5, Zadatak 1,
   annotated with the optimal flows.
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


def lp_geometrija() -> None:
    fig, ax = plt.subplots(figsize=(6.4, 5.4))

    vrhovi = np.array([[0.0, 0.0], [4.0, 0.0], [5.5, 2.0],
                       [4.0, 4.5], [1.2, 4.0]])
    ax.fill(vrhovi[:, 0], vrhovi[:, 1], color=SIVA, alpha=0.65, zorder=0)
    ax.plot(np.append(vrhovi[:, 0], vrhovi[0, 0]),
            np.append(vrhovi[:, 1], vrhovi[0, 1]), color=PLAVA, lw=2.0)
    ax.annotate(r"$\mathcal{P}$", xy=(2.8, 2.0), fontsize=16)

    c = np.array([1.0, 0.6])
    t = np.linspace(-1.5, 7.0, 50)
    for val in np.arange(-1.0, 7.5, 1.0):
        # c1*x1 + c2*x2 = val  ->  x2 = (val - c1*x1)/c2
        ax.plot(t, (val - c[0] * t) / c[1], ls="--", lw=0.8, color="#8a8a8a")

    # optimum: the vertex minimising c'x is the origin here
    xs = vrhovi[np.argmin(vrhovi @ c)]
    ax.plot(*xs, marker="o", ms=10, color="k", zorder=6)
    ax.annotate(r"$x^\star$", xy=xs, xytext=(10, -18),
                textcoords="offset points", fontsize=13)
    ax.annotate("", xy=xs - 1.4 * c, xytext=xs,
                arrowprops=dict(arrowstyle="-|>", lw=2.2, color=CRVENA))
    ax.annotate(r"$-c$", xy=xs - 1.4 * c, xytext=(-30, -6),
                textcoords="offset points", fontsize=13, color=CRVENA)

    ax.set_xlim(-2.2, 7.0)
    ax.set_ylim(-2.2, 5.6)
    ax.set_xlabel(r"$x_1$")
    ax.set_ylabel(r"$x_2$")
    ax.set_title(r"Geometrija LP problema:  $\min_{x\in\mathcal{P}} c^\top x$")
    ax.grid(alpha=0.2)
    ax.set_aspect("equal", adjustable="box")

    fig.tight_layout()
    fig.savefig(OUT / "05-lp-geometrija.png", dpi=160)
    plt.close(fig)


def aproksimacije() -> None:
    """Fit the same data with the 2-, infinity- and 1-norm."""
    from scipy.optimize import linprog

    rng = np.random.default_rng(3)
    N = 40
    xs = np.linspace(0.0, 10.0, N)
    ys = 1.0 + 0.6 * xs + rng.normal(0.0, 0.5, N)
    ys[7] += 6.0          # two outliers, to separate the three norms
    ys[28] -= 5.0

    A = np.column_stack([np.ones(N), xs])       # basis {1, x}

    # 2-norm: normal equations
    c2 = np.linalg.solve(A.T @ A, A.T @ ys)

    # infinity-norm as an LP in (c0, c1, t)
    n = A.shape[1]
    c_lp = np.concatenate([np.zeros(n), [1.0]])
    A_ub = np.block([[A, -np.ones((N, 1))],
                     [-A, -np.ones((N, 1))]])
    b_ub = np.concatenate([ys, -ys])
    r = linprog(c_lp, A_ub=A_ub, b_ub=b_ub, bounds=[(None, None)] * (n + 1))
    cinf = r.x[:n]

    # 1-norm as an LP in (c0, c1, y_1..y_N)
    c_lp = np.concatenate([np.zeros(n), np.ones(N)])
    A_ub = np.block([[A, -np.eye(N)],
                     [-A, -np.eye(N)]])
    b_ub = np.concatenate([ys, -ys])
    r = linprog(c_lp, A_ub=A_ub, b_ub=b_ub, bounds=[(None, None)] * (n + N))
    c1 = r.x[:n]

    fig, ax = plt.subplots(figsize=(6.8, 4.8))
    ax.plot(xs, ys, "o", ms=5, color="#4a4a4a", label="podaci")
    grid = np.linspace(-0.3, 10.3, 100)
    for coef, boja, lab in ((c2, PLAVA, r"$\|\cdot\|_2$ (najmanji kvadrati)"),
                            (cinf, CRVENA, r"$\|\cdot\|_\infty$ (Chebyshev)"),
                            (c1, ZELENA, r"$\|\cdot\|_1$")):
        ax.plot(grid, coef[0] + coef[1] * grid, lw=2.0, color=boja, label=lab)

    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$y$")
    ax.set_title("Ista podatkovna serija, tri norme")
    ax.grid(alpha=0.22)
    ax.legend(loc="upper left", fontsize=9)

    fig.tight_layout()
    fig.savefig(OUT / "05-aproksimacije.png", dpi=160)
    plt.close(fig)


def rekonstrukcija() -> None:
    """Primjer 4 of Vjezbe 4: quadratic regularisation of a noisy signal."""
    rng = np.random.default_rng(1)
    n = 220
    t = np.linspace(0.0, 1.0, n)
    x = (0.6 * np.sin(2.5 * np.pi * t) + 0.4 * np.sign(np.sin(6.0 * np.pi * t))
         * 0.5)
    x_cor = x + rng.normal(0.0, 0.22, n)

    D = np.zeros((n - 1, n))
    for i in range(n - 1):
        D[i, i] = -1.0
        D[i, i + 1] = 1.0

    fig, axs = plt.subplots(3, 1, figsize=(6.8, 6.6), sharex=True)
    for ax, delta in zip(axs, (1.0, 20.0, 400.0)):
        xhat = np.linalg.solve(np.eye(n) + delta * D.T @ D, x_cor)
        ax.plot(t, x_cor, lw=0.8, color="#9a9a9a", label=r"$x_{\mathrm{cor}}$")
        ax.plot(t, xhat, lw=2.0, color=PLAVA, label=r"$\hat x^\star$")
        ax.set_ylabel(r"$x$")
        ax.set_title(rf"$\delta = {delta:g}$", fontsize=10)
        ax.grid(alpha=0.22)
    axs[0].legend(loc="upper right", fontsize=8, ncol=2)
    axs[-1].set_xlabel(r"$i/n$")

    fig.suptitle(r"Rekonstrukcija signala: "
                 r"$\min_{\hat x}\ \|\hat x - x_{\mathrm{cor}}\|_2^2"
                 r" + \delta\|D\hat x\|_2^2$", fontsize=11)
    fig.tight_layout()
    fig.savefig(OUT / "05-rekonstrukcija.png", dpi=160)
    plt.close(fig)


def mreza() -> None:
    """Transport network of Vjezbe 5, Zadatak 1, with the optimal flows."""
    poz = {1: (0.0, 1.0), 2: (0.0, 0.0),
           3: (1.6, 1.0), 4: (1.6, 0.0),
           5: (3.2, 1.0), 6: (3.2, 0.0)}
    # (from, to, cost, capacity, optimal flow, label position along the arc)
    bridovi = [(1, 3, 1.0, 15, 10.00, 0.50), (1, 4, 2.0, 15, 11.25, 0.74),
               (2, 3, 1.0, 20, 20.00, 0.26), (2, 4, 3.0, 20, 8.75, 0.50),
               (3, 4, 2.0, 20, 0.00, 0.50), (3, 5, 1.5, 30, 30.00, 0.50),
               (4, 5, 2.0, 20, 5.00, 0.50), (4, 6, 2.5, 15, 15.00, 0.50),
               (5, 6, 1.0, 30, 5.00, 0.50)]

    fig, ax = plt.subplots(figsize=(7.4, 3.8))

    for u, v, cost, cap, f, s in bridovi:
        x0, y0 = poz[u]
        x1, y1 = poz[v]
        zasicen = f > cap - 1e-6
        ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                    arrowprops=dict(arrowstyle="-|>",
                                    lw=2.6 if zasicen else 1.4,
                                    color=CRVENA if zasicen else "#4a4a4a",
                                    shrinkA=16, shrinkB=16))
        mx, my = x0 + s * (x1 - x0), y0 + s * (y1 - y0)
        ax.text(mx, my + 0.09, f"{f:g}/{cap:g}", fontsize=8, ha="center",
                color=CRVENA if zasicen else "#2a2a2a",
                bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none"))

    for k, (x, y) in poz.items():
        ax.plot(x, y, "o", ms=26, color="white", mec="k", mew=1.6, zorder=5)
        ax.text(x, y, str(k), ha="center", va="center", fontsize=12, zorder=6)

    ax.annotate(r"$p_1=21{,}25$", xy=poz[1], xytext=(-92, -6),
                textcoords="offset points", fontsize=10, color=ZELENA)
    ax.annotate(r"$p_2=28{,}75$", xy=poz[2], xytext=(-92, -6),
                textcoords="offset points", fontsize=10, color=ZELENA)
    ax.annotate(r"$d_5=30$", xy=poz[5], xytext=(24, -6),
                textcoords="offset points", fontsize=10, color=PLAVA)
    ax.annotate(r"$d_6=20$", xy=poz[6], xytext=(24, -6),
                textcoords="offset points", fontsize=10, color=PLAVA)

    ax.set_xlim(-1.5, 4.6)
    ax.set_ylim(-0.55, 1.55)
    ax.axis("off")
    ax.set_title("Optimalni tokovi (oznaka: tok/kapacitet); "
                 "crveno = zasićen brid", fontsize=10)

    fig.tight_layout()
    fig.savefig(OUT / "05-mreza.png", dpi=160)
    plt.close(fig)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    lp_geometrija()
    aproksimacije()
    rekonstrukcija()
    mreza()


if __name__ == "__main__":
    main()
