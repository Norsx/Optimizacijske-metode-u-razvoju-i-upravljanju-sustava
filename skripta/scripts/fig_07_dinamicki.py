r"""Figures for the chapter on dynamic systems, Lyapunov and dissipativity.

1. 07-ljapunov.png   -- level sets of V(x) = x'Px together with trajectories of
   the system on slide 12, showing that every level set is invariant.
2. 07-pendulum.png   -- closed-loop response of the inverted pendulum under the
   robust gain K computed in solve_vj5_robusna.py, for several values of the
   uncertain friction coefficient b.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

OUT = Path(__file__).resolve().parents[1] / "figures"

ZELENA = "#1E6B3A"
CRVENA = "#D62728"
PLAVA = "#1F4FD8"


def ljapunov() -> None:
    """Slide 12: A = [[-1, 2], [-3, -4]], P as printed on the slide."""
    A = np.array([[-1.0, 2.0], [-3.0, -4.0]])
    P = np.array([[0.6777, 0.0584], [0.0584, 0.3223]])

    Mi = A.T @ P + P @ A
    print("  provjera A'P + PA:", np.round(np.linalg.eigvalsh(Mi), 4))

    fig, ax = plt.subplots(figsize=(6.2, 5.6))

    t = np.linspace(-2.2, 2.2, 400)
    X1, X2 = np.meshgrid(t, t)
    V = (P[0, 0] * X1**2 + 2.0 * P[0, 1] * X1 * X2 + P[1, 1] * X2**2)
    cs = ax.contour(X1, X2, V, levels=[0.15, 0.4, 0.8, 1.4, 2.2],
                    colors=PLAVA, linewidths=1.3)
    ax.clabel(cs, fmt=r"$V=%.2g$", fontsize=7)

    # vector field
    s = np.linspace(-2.1, 2.1, 17)
    S1, S2 = np.meshgrid(s, s)
    D1 = A[0, 0] * S1 + A[0, 1] * S2
    D2 = A[1, 0] * S1 + A[1, 1] * S2
    ax.quiver(S1, S2, D1, D2, color="#9a9a9a", alpha=0.75, width=0.0032)

    # a few trajectories
    for x0 in ([2.0, 1.4], [-2.0, -1.4], [1.2, -1.9], [-1.2, 1.9]):
        sol = solve_ivp(lambda tt, x: A @ x, (0.0, 6.0), x0,
                        dense_output=True, rtol=1e-8)
        tt = np.linspace(0.0, 6.0, 600)
        xt = sol.sol(tt)
        ax.plot(xt[0], xt[1], lw=2.0, color=CRVENA)
        ax.plot(*x0, marker="o", ms=5, color=CRVENA)

    ax.plot(0, 0, marker="*", ms=14, color="k", zorder=6)
    ax.set_xlim(-2.2, 2.2)
    ax.set_ylim(-2.2, 2.2)
    ax.set_xlabel(r"$x_1$")
    ax.set_ylabel(r"$x_2$")
    ax.set_title(r"Nivo skupovi $V(x)=x^\top Px$ i trajektorije "
                 r"$\dot x = Ax$", fontsize=11)
    ax.grid(alpha=0.2)
    ax.set_aspect("equal", adjustable="box")

    fig.tight_layout()
    fig.savefig(OUT / "07-ljapunov.png", dpi=160)
    plt.close(fig)


def pendulum() -> None:
    """Closed loop of the inverted pendulum with the robust gain."""
    M, m, L, J, G = 0.5, 0.2, 0.3, 0.006, 9.81
    c = 1.0 / (J * (M + m) + M * m * L**2)
    K = np.array([[1.2049, 9.3029, -16.1561, -11.1823]])
    Bv = np.array([[0.0], [(J + m * L**2) * c], [0.0], [m * L * c]])

    def A_of(b: float) -> np.ndarray:
        return np.array([
            [0.0, 1.0, 0.0, 0.0],
            [0.0, -(J + m * L**2) * b * c, m**2 * G * L**2 * c, 0.0],
            [0.0, 0.0, 0.0, 1.0],
            [0.0, -m * L * b * c, m * G * L * (M + m) * c, 0.0],
        ])

    fig, axs = plt.subplots(2, 1, figsize=(6.8, 5.6), sharex=True)
    x0 = np.array([0.0, 0.0, 0.20, 0.0])          # 0.2 rad initial tilt
    boje = plt.cm.viridis(np.linspace(0.1, 0.85, 5))

    for b, boja in zip(np.linspace(0.05, 0.5, 5), boje):
        Acl = A_of(b) + Bv @ K
        sol = solve_ivp(lambda tt, x: Acl @ x, (0.0, 60.0), x0,
                        dense_output=True, rtol=1e-9)
        tt = np.linspace(0.0, 60.0, 1200)
        xt = sol.sol(tt)
        axs[0].plot(tt, xt[2], lw=1.7, color=boja, label=rf"$b={b:.3g}$")
        axs[1].plot(tt, (K @ xt).ravel(), lw=1.7, color=boja)

    axs[0].set_ylabel(r"$\varphi$  [rad]")
    axs[0].set_title("Zatvoreni krug s robusnim pojačanjem $K$, "
                     "za pet vrijednosti $b$", fontsize=11)
    axs[0].grid(alpha=0.22)
    axs[0].legend(fontsize=8, ncol=5, loc="upper right")
    axs[1].set_ylabel(r"$F = Kx$  [N]")
    axs[1].set_xlabel(r"$t$  [s]")
    axs[1].grid(alpha=0.22)

    fig.tight_layout()
    fig.savefig(OUT / "07-pendulum.png", dpi=160)
    plt.close(fig)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    ljapunov()
    pendulum()


if __name__ == "__main__":
    main()
