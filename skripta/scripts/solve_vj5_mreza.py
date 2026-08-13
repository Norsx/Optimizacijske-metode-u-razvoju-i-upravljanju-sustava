r"""Solve Zadatak 1 of Vjezbe 5 -- production and flow optimisation in a network.

The exercise sheet states the problem but carries no worked solution, so the
notes solve it with the machinery of chapter 5 (a QP with linear flow
constraints) and read the investment answer off the dual variables of the
capacity constraints, exactly as the sensitivity analysis of chapter 4
prescribes.

Network (arcs are directed):

        1 --> 3 --> 5
        |  \  |  /  |
        |   \ | /   |
        2 --> 4 --> 6

Producers sit at nodes 1 and 2, consumers at nodes 5 and 6.

    min  C1(p1) + C2(p2) + sum_e cost_e * f_e
    s.t. flow balance at every node
         0 <= f_e <= cap_e,  p1, p2 >= 0

with C1(p1) = 0.5 p1^2 + 2 p1 and C2(p2) = 0.3 p2^2 + 5 p2.

Printed output feeds the worked solution in poglavlja/05-lp-qp.tex.
"""

import numpy as np
from scipy.optimize import minimize

# arcs in a fixed order: variables f[0..8]
ARCS = [(1, 3), (1, 4), (2, 3), (2, 4), (3, 4), (3, 5), (4, 5), (4, 6), (5, 6)]
COST = np.array([1.0, 2.0, 1.0, 3.0, 2.0, 1.5, 2.0, 2.5, 1.0])
CAP = np.array([15.0, 15.0, 20.0, 20.0, 20.0, 30.0, 20.0, 15.0, 30.0])

D5, D6 = 30.0, 20.0

# decision vector z = [f_0 .. f_8, p1, p2]
NF = len(ARCS)
NZ = NF + 2


def balance_matrix() -> tuple[np.ndarray, np.ndarray]:
    """Rows of A_eq z = b_eq: one flow balance per node 1..6."""
    A = np.zeros((6, NZ))
    b = np.zeros(6)
    for k, (u, v) in enumerate(ARCS):
        A[u - 1, k] -= 1.0        # flow leaves u
        A[v - 1, k] += 1.0        # flow enters v
    A[0, NF] = 1.0                # p1 injected at node 1
    A[1, NF + 1] = 1.0            # p2 injected at node 2
    b[4] = D5                     # node 5 consumes d5
    b[5] = D6                     # node 6 consumes d6
    return A, b


def total_cost(z: np.ndarray) -> float:
    f, p1, p2 = z[:NF], z[NF], z[NF + 1]
    return 0.5 * p1**2 + 2.0 * p1 + 0.3 * p2**2 + 5.0 * p2 + COST @ f


def total_cost_grad(z: np.ndarray) -> np.ndarray:
    g = np.zeros(NZ)
    g[:NF] = COST
    g[NF] = z[NF] + 2.0
    g[NF + 1] = 0.6 * z[NF + 1] + 5.0
    return g


def main() -> None:
    A_eq, b_eq = balance_matrix()

    bounds = [(0.0, CAP[k]) for k in range(NF)] + [(0.0, None), (0.0, None)]
    cons = [{"type": "eq",
             "fun": lambda z: A_eq @ z - b_eq,
             "jac": lambda z: A_eq}]

    z0 = np.full(NZ, 5.0)
    res = minimize(total_cost, z0, jac=total_cost_grad, bounds=bounds,
                   constraints=cons, method="SLSQP",
                   options={"maxiter": 800, "ftol": 1e-12})

    z = res.x
    f, p1, p2 = z[:NF], z[NF], z[NF + 1]

    print("uspjeh:", res.success, "|", res.message)
    print(f"\nukupan trosak = {total_cost(z):.4f}")
    print(f"  proizvodnja: p1 = {p1:.4f}, p2 = {p2:.4f}  (zbroj {p1 + p2:.4f})")
    print(f"  trosak proizvodnje = "
          f"{0.5 * p1**2 + 2 * p1 + 0.3 * p2**2 + 5 * p2:.4f}")
    print(f"  trosak transporta  = {COST @ f:.4f}")

    print("\ntokovi po bridovima:")
    for k, (u, v) in enumerate(ARCS):
        zas = "  <-- ZASICEN" if f[k] > CAP[k] - 1e-6 else ""
        print(f"  ({u},{v}): f = {f[k]:8.4f} / {CAP[k]:5.1f}"
              f"   cijena {COST[k]:4.1f}{zas}")

    # Sensitivity to capacity: re-solve with cap_e raised by one unit and read
    # off the change in the optimal cost.  This is the numerical counterpart of
    # the dual variable of the capacity constraint (chapter 4).
    print("\nosjetljivost na povecanje kapaciteta za +1:")
    base = total_cost(z)
    for k, (u, v) in enumerate(ARCS):
        cap2 = CAP.copy()
        cap2[k] += 1.0
        b2 = [(0.0, cap2[i]) for i in range(NF)] + [(0.0, None), (0.0, None)]
        r2 = minimize(total_cost, z, jac=total_cost_grad, bounds=b2,
                      constraints=cons, method="SLSQP",
                      options={"maxiter": 800, "ftol": 1e-12})
        print(f"  ({u},{v}): delta = {total_cost(r2.x) - base:+.4f}")


if __name__ == "__main__":
    main()
