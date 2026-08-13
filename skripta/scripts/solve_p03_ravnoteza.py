r"""Equilibrium by minimisation of potential energy -- lecture 03, str. 64-68.

Those five slides are pictures only: the sketches are drawn but no formulas are
written, because the derivations were done on the blackboard.  The notes
therefore set each of them up and solve them with the apparatus of chapter 3,
in the order the slides present them:

    str. 64  mass on a spring                      -> unconstrained, grad V = 0
    str. 65  slider on a vertical guide            -> equality constraint, Lagrange
    str. 66-67  contour plot of V with gradients   -> geometry of the same case
    str. 68  mass above an inclined plane          -> inequality constraint, KKT

The potential energy is the one used in lecture 01, str. 40:

    V(x, y) = m g y + (k/2) (sqrt(x^2 + y^2) - L0)^2

Numerical values are a concrete illustration (the slides give none) and are
declared as such in the notes.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import brentq, fsolve

OUT = Path(__file__).resolve().parents[1] / "figures"

M, GRAV, K, L0 = 1.0, 9.81, 100.0, 0.30      # kg, m/s^2, N/m, m
X0 = 0.20                                     # m, guide offset (str. 65)
A_NAG, B_ODS = 0.5, -0.35                     # incline y = a x + b (str. 68)


def V(x: float, y: float) -> float:
    r = np.hypot(x, y)
    return M * GRAV * y + 0.5 * K * (r - L0) ** 2


def dV(x: float, y: float) -> tuple[float, float]:
    r = np.hypot(x, y)
    zajed = K * (r - L0) / r
    return zajed * x, M * GRAV + zajed * y


def primjer_1() -> tuple[float, float]:
    """str. 64: free mass on a spring -> grad V = 0."""
    y = -(L0 + M * GRAV / K)
    print("--- str. 64: uteg na opruzi (bez ogranicenja) ---")
    print(f"  analiticki:  x* = 0,  y* = -(L0 + mg/k) = {y:.4f} m")
    print(f"  produljenje opruge mg/k = {M * GRAV / K:.4f} m")
    print(f"  provjera gradijenta: {np.round(dV(0.0, y), 9)}")
    return 0.0, y


def primjer_2() -> tuple[float, float, float]:
    """str. 65: slider constrained to the vertical guide x = -x0."""
    def stac(y: float) -> float:
        return dV(-X0, y)[1]                  # dV/dy = 0 with x fixed

    y = brentq(stac, -2.0, -1e-6)
    r = np.hypot(X0, y)
    lam = -dV(-X0, y)[0]                      # grad V + lambda * grad h = 0
    print("\n--- str. 65: klizac na vertikalnoj vodilici x = -x0 ---")
    print(f"  x* = {-X0:.4f} m  (nametnuto vodilicom)")
    print(f"  y* = {y:.4f} m,  duljina opruge r = {r:.4f} m")
    print(f"  dV/dy u optimumu = {stac(y):.3e}")
    print(f"  lambda = {lam:.4f} N   <- vodoravna reakcija vodilice")
    print(f"  V(x*,y*) = {V(-X0, y):.4f} J")
    return -X0, y, lam


def primjer_5() -> tuple[float, float, float]:
    """str. 68: mass above the incline  y >= a x + b, i.e. g = a x + b - y <= 0."""
    x_slob, y_slob = 0.0, -(L0 + M * GRAV / K)
    g_slob = A_NAG * x_slob + B_ODS - y_slob
    print("\n--- str. 68: uteg iznad kose podloge y = a x + b ---")
    print(f"  slobodni optimum (0, {y_slob:.4f});  "
          f"g = {g_slob:+.4f}  ->  "
          f"{'ogranicenje AKTIVNO' if g_slob > 0 else 'ogranicenje neaktivno'}")

    def kkt(v: np.ndarray) -> list[float]:
        x, y, mu = v
        gx, gy = dV(x, y)
        return [gx + mu * A_NAG,               # dL/dx
                gy + mu * (-1.0),              # dL/dy
                A_NAG * x + B_ODS - y]         # g = 0 (active)

    x, y, mu = fsolve(kkt, [0.0, B_ODS, 1.0], full_output=False)
    print(f"  x* = {x:.4f} m,  y* = {y:.4f} m,  mu = {mu:.4f} N")
    print(f"  provjera mu >= 0: {mu >= 0};  ostatak KKT-a: "
          f"{np.round(kkt([x, y, mu]), 9)}")
    print(f"  V(x*,y*) = {V(x, y):.4f} J   (slobodni V = {V(0.0, y_slob):.4f} J)")
    return x, y, mu


def slika(klizac: tuple[float, float, float]) -> None:
    """str. 66-67: contour plot of V with the two gradients at the optimum."""
    xs, ys, lam = klizac

    gx = np.linspace(-0.55, 0.35, 400)
    gy = np.linspace(-0.75, 0.15, 400)
    X, Y = np.meshgrid(gx, gy)
    Z = M * GRAV * Y + 0.5 * K * (np.hypot(X, Y) - L0) ** 2

    fig, ax = plt.subplots(figsize=(6.6, 5.8))
    cs = ax.contour(X, Y, Z, levels=25, colors="#7a7a9a", linewidths=0.8)
    ax.clabel(cs, cs.levels[::4], fmt="%.2f", fontsize=6)

    ax.axvline(-X0, color="#1F4FD8", lw=2.2,
               label=r"vodilica  $h(x,y)=x+x_0=0$")
    ax.plot(0.0, 0.0, marker="s", ms=8, color="k")
    ax.annotate("objesište", xy=(0, 0), xytext=(8, 6),
                textcoords="offset points", fontsize=9)

    ax.plot(xs, ys, marker="o", ms=10, color="#D62728", zorder=6)
    ax.annotate(rf"$(x^\star,y^\star)=({xs:.2f},\ {ys:.3f})$", xy=(xs, ys),
                xytext=(14, -20), textcoords="offset points", fontsize=10,
                color="#D62728")

    gV = np.array(dV(xs, ys))
    s = 0.16 / max(np.linalg.norm(gV), 1e-9)
    ax.annotate("", xy=(xs + s * gV[0], ys + s * gV[1]), xytext=(xs, ys),
                arrowprops=dict(arrowstyle="-|>", lw=2.4, color="#1E6B3A"))
    ax.annotate(r"$\nabla V$", xy=(xs + s * gV[0], ys + s * gV[1]),
                xytext=(6, 4), textcoords="offset points", fontsize=11,
                color="#1E6B3A")
    ax.annotate("", xy=(xs + 0.16, ys), xytext=(xs, ys),
                arrowprops=dict(arrowstyle="-|>", lw=2.4, color="#B35C00"))
    ax.annotate(r"$\nabla h$", xy=(xs + 0.16, ys), xytext=(4, -14),
                textcoords="offset points", fontsize=11, color="#B35C00")

    ax.set_xlim(-0.55, 0.35)
    ax.set_ylim(-0.75, 0.15)
    ax.set_xlabel(r"$x$  [m]")
    ax.set_ylabel(r"$y$  [m]")
    ax.set_title("Nivo krivulje potencijalne energije $V(x,y)$\n"
                 "i ravnoteža klizača na vodilici", fontsize=11)
    ax.grid(alpha=0.2)
    ax.legend(loc="lower right", fontsize=8)
    ax.set_aspect("equal", adjustable="box")

    OUT.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(OUT / "03-ravnoteza-klizac.png", dpi=160)
    plt.close(fig)


def main() -> None:
    print(f"parametri: m={M} kg, g={GRAV} m/s^2, k={K} N/m, "
          f"L0={L0} m, x0={X0} m, kosina y={A_NAG}x{B_ODS:+g}\n")
    primjer_1()
    klizac = primjer_2()
    primjer_5()
    slika(klizac)


if __name__ == "__main__":
    main()
