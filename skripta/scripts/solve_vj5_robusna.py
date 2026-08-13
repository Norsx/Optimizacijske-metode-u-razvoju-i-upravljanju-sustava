r"""Solve Zadatak 2 of Vjezbe 5 -- robust stabilisation of the inverted pendulum.

The exercise sheet states the problem but carries no worked solution, so the
notes solve it with the machinery of chapter 7: the friction coefficient b
enters the state matrix affinely, so A(b) for b in [b_min, b_max] is the convex
hull of the two vertex matrices A(b_min), A(b_max).  Quadratic stability of a
convex hull only needs the LMI at the vertices (slide 26), and the synthesis
substitution Q = P^-1, Y = K P^-1 (slides 31-33) turns the bilinear condition
into an LMI:

    Q > 0,   Q A_i' + Y' B' + A_i Q + B Y < 0,   i = 1, 2
    K = Y Q^-1

The LMI is solved here without a dedicated SDP solver: the feasibility problem
is written as minimisation of the largest eigenvalue over the free entries of
(Q, Y), normalised by trace(Q) = n to remove the homogeneous scaling.

Printed output feeds the worked solution in
poglavlja/07-dinamicki-sustavi-ljapunov-disipativnost.tex.
"""

import numpy as np
from scipy.optimize import minimize

# --- parameters of the cart-pendulum, as given on Vjezbe 5, str. 5 ---------
M = 0.5          # kg, cart mass
m = 0.2          # kg, pendulum mass
L = 0.3          # m, distance to the pendulum centre of mass
J = 0.006        # kg m^2, pendulum inertia (called I on the slide)
G = 9.81         # m/s^2
B_MIN, B_MAX = 0.05, 0.5     # N/m/s, uncertain friction coefficient

C = 1.0 / (J * (M + m) + M * m * L**2)

N = 4            # states
NQ = N * (N + 1) // 2        # free entries of a symmetric Q
NY = N                       # Y is 1 x n


def state_matrix(b: float) -> np.ndarray:
    """A(b) of the linearised inverted pendulum."""
    return np.array([
        [0.0, 1.0, 0.0, 0.0],
        [0.0, -(J + m * L**2) * b * C, m**2 * G * L**2 * C, 0.0],
        [0.0, 0.0, 0.0, 1.0],
        [0.0, -m * L * b * C, m * G * L * (M + m) * C, 0.0],
    ])


B_VEC = np.array([[0.0], [(J + m * L**2) * C], [0.0], [m * L * C]])


def unpack(z: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    Q = np.zeros((N, N))
    iu = np.triu_indices(N)
    Q[iu] = z[:NQ]
    Q = Q + Q.T - np.diag(np.diag(Q))
    Y = z[NQ:].reshape(1, N)
    return Q, Y


def worst_eig(z: np.ndarray, vrhovi: list[np.ndarray]) -> float:
    """Largest eigenvalue over -Q and the closed-loop LMI at every vertex."""
    Q, Y = unpack(z)
    vals = [np.linalg.eigvalsh(-Q).max()]
    for A in vrhovi:
        Mi = Q @ A.T + Y.T @ B_VEC.T + A @ Q + B_VEC @ Y
        vals.append(np.linalg.eigvalsh(0.5 * (Mi + Mi.T)).max())
    return max(vals)


def main() -> None:
    vrhovi = [state_matrix(B_MIN), state_matrix(B_MAX)]

    print("c =", round(C, 6))
    for b, A in zip((B_MIN, B_MAX), vrhovi):
        lam = np.linalg.eigvals(A)
        print(f"\nA(b={b}) =\n{np.round(A, 4)}")
        print("  svojstvene vrijednosti:", np.round(np.sort_complex(lam), 4))

    cons = [{"type": "eq", "fun": lambda z: np.trace(unpack(z)[0]) - N}]

    best, best_val = None, np.inf
    rng = np.random.default_rng(0)
    for _ in range(60):
        z0 = np.concatenate([
            np.eye(N)[np.triu_indices(N)] + 0.1 * rng.normal(size=NQ),
            rng.normal(scale=5.0, size=NY),
        ])
        r = minimize(worst_eig, z0, args=(vrhovi,), constraints=cons,
                     method="SLSQP", options={"maxiter": 2000, "ftol": 1e-10})
        if r.success and worst_eig(r.x, vrhovi) < best_val:
            best_val, best = worst_eig(r.x, vrhovi), r.x

    Q, Y = unpack(best)
    P = np.linalg.inv(Q)
    K = Y @ P

    print(f"\nnajveca svojstvena vrijednost u LMI-jevima: {best_val:.4f}"
          f"   ({'DOPUSTIVO' if best_val < 0 else 'NIJE DOPUSTIVO'})")
    print(f"\nQ =\n{np.round(Q, 4)}")
    print(f"\nY = {np.round(Y, 4)}")
    print(f"\nP = Q^-1 =\n{np.round(P, 4)}")
    print(f"\nK = Y P = {np.round(K, 4)}")

    print("\nprovjera zatvorenog kruga na mrezi vrijednosti b:")
    for b in np.linspace(B_MIN, B_MAX, 10):
        Acl = state_matrix(b) + B_VEC @ K
        lam = np.linalg.eigvals(Acl)
        print(f"  b = {b:.3f}:  max Re(lambda) = {lam.real.max():+.4f}")

    print("\nprovjera Ljapunovljeve nejednakosti A(b)'P + P A(b) < 0 "
          "za zatvoreni krug:")
    for b in (B_MIN, 0.5 * (B_MIN + B_MAX), B_MAX):
        Acl = state_matrix(b) + B_VEC @ K
        Mi = Acl.T @ P + P @ Acl
        print(f"  b = {b:.3f}:  max eig = "
              f"{np.linalg.eigvalsh(0.5 * (Mi + Mi.T)).max():+.4f}")


if __name__ == "__main__":
    main()
