r"""Solve Zadatak 2 of Vjezbe 5 -- robust stabilisation of the inverted pendulum.

The exercise sheet states the problem but carries no worked solution, so the
notes solve it with the machinery of chapter 7.  The friction coefficient b
enters the state matrix affinely, so A(b) over [b_min, b_max] is the convex hull
of the two vertex matrices.  Quadratic stability of a convex hull only needs the
LMI at the vertices (lecture 07, str. 26), and the synthesis substitution
Q = P^-1, Y = K P^-1 (str. 31-33) turns the bilinear condition into an LMI:

    Q > 0,   Q A_i' + Y' B' + A_i Q + B Y < 0,   i = 1, 2
    K = Y Q^-1

Method fidelity: this is a semidefinite program, and the exercises solve such
problems with a modelling layer on top of a solver (YALMIP in MATLAB, Vjezbe 3
str. 32).  Here the same role is played by CVXPY, so the LMIs are written down
as matrix inequalities exactly as on the slides and handed to an SDP solver.

Printed output feeds the worked solution in
poglavlja/07-dinamicki-sustavi-ljapunov-disipativnost.tex.
"""

import cvxpy as cp
import numpy as np

# --- parameters of the cart-pendulum, as given on Vjezbe 5, str. 5 ---------
M = 0.5          # kg, cart mass
m = 0.2          # kg, pendulum mass
L = 0.3          # m, distance to the pendulum centre of mass
J = 0.006        # kg m^2, pendulum inertia (called I on the slide)
G = 9.81         # m/s^2
B_MIN, B_MAX = 0.05, 0.5     # N/m/s, uncertain friction coefficient

C = 1.0 / (J * (M + m) + M * m * L**2)
N = 4


def state_matrix(b: float) -> np.ndarray:
    """A(b) of the linearised inverted pendulum."""
    return np.array([
        [0.0, 1.0, 0.0, 0.0],
        [0.0, -(J + m * L**2) * b * C, m**2 * G * L**2 * C, 0.0],
        [0.0, 0.0, 0.0, 1.0],
        [0.0, -m * L * b * C, m * G * L * (M + m) * C, 0.0],
    ])


B_VEC = np.array([[0.0], [(J + m * L**2) * C], [0.0], [m * L * C]])


def main() -> None:
    vrhovi = [state_matrix(B_MIN), state_matrix(B_MAX)]

    print("c =", round(C, 6))
    for b, A in zip((B_MIN, B_MAX), vrhovi):
        lam = np.linalg.eigvals(A)
        print(f"\nA(b={b}) =\n{np.round(A, 4)}")
        print("  svojstvene vrijednosti:",
              np.round(np.sort_complex(lam), 4))

    # --- the LMI, written exactly as on the slides -------------------------
    Q = cp.Variable((N, N), symmetric=True, name="Q")
    Y = cp.Variable((1, N), name="Y")
    eps = 1e-3

    # Q >> I instead of Q >> 0 only fixes the scale: the LMIs are homogeneous,
    # so (Q, Y) and (tQ, tY) give the same K for any t > 0.
    ogranicenja = [Q >> np.eye(N)]
    for A in vrhovi:
        Mi = Q @ A.T + Y.T @ B_VEC.T + A @ Q + B_VEC @ Y
        ogranicenja.append(Mi << -eps * np.eye(N))

    # the task asks only for a stabilising K, so this is a pure feasibility problem
    prob = cp.Problem(cp.Minimize(0), ogranicenja)
    prob.solve(solver=cp.SCS)

    print("\nstatus:", prob.status)

    Qv = Q.value
    P = np.linalg.inv(Qv)
    K = Y.value @ P

    print(f"\nQ =\n{np.round(Qv, 4)}")
    print(f"\nY = {np.round(Y.value, 4)}")
    print(f"\nP = Q^-1 =\n{np.round(P, 4)}")
    print(f"\nK = Y P = {np.round(K, 4)}")

    print("\nprovjera zatvorenog kruga na mrezi vrijednosti b:")
    for b in np.linspace(B_MIN, B_MAX, 10):
        Acl = state_matrix(b) + B_VEC @ K
        print(f"  b = {b:.3f}:  max Re(lambda) = "
              f"{np.linalg.eigvals(Acl).real.max():+.4f}")

    print("\nprovjera Ljapunovljeve nejednakosti "
          "A_cl(b)'P + P A_cl(b) < 0:")
    for b in (B_MIN, 0.5 * (B_MIN + B_MAX), B_MAX):
        Acl = state_matrix(b) + B_VEC @ K
        Mi = Acl.T @ P + P @ Acl
        print(f"  b = {b:.3f}:  max eig = "
              f"{np.linalg.eigvalsh(0.5 * (Mi + Mi.T)).max():+.6f}")


if __name__ == "__main__":
    main()
