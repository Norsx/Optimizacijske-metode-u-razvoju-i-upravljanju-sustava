r"""Solve Zadatak 1 of Vjezbe 5 -- production and flow optimisation in a network.

The exercise sheet states the problem but carries no worked solution, so the
notes solve it with the machinery of chapter 5: a QP with linear flow
constraints.

Method fidelity: the exercises solve such problems with a modelling layer on
top of a solver (YALMIP + quadprog, Vjezbe 3, str. 32-33) and read the optimal
dual variables straight off the solver as a by-product -- `mu_opt.ineqlin` in
MATLAB, `constraint.dual_value` here.  The investment question is then answered
by the sensitivity result of chapter 4,

    d p* / d v_j = - mu_j*,

so the capacity multipliers rank the arcs directly.  No constraint is perturbed
and nothing is re-solved.

Network (arcs are directed):

        1 --> 3 --> 5
        |  \  |  /  |
        |   \ | /   |
        2 --> 4 --> 6

Printed output feeds the worked solution in poglavlja/05-lp-qp.tex.
"""

import cvxpy as cp
import numpy as np

ARCS = [(1, 3), (1, 4), (2, 3), (2, 4), (3, 4), (3, 5), (4, 5), (4, 6), (5, 6)]
COST = np.array([1.0, 2.0, 1.0, 3.0, 2.0, 1.5, 2.0, 2.5, 1.0])
CAP = np.array([15.0, 15.0, 20.0, 20.0, 20.0, 30.0, 20.0, 15.0, 30.0])

D5, D6 = 30.0, 20.0
NF = len(ARCS)


def balance() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Node balance  Af f + Ap p = b, one row per node 1..6."""
    Af = np.zeros((6, NF))
    Ap = np.zeros((6, 2))
    b = np.zeros(6)
    for k, (u, v) in enumerate(ARCS):
        Af[u - 1, k] -= 1.0          # flow leaves u
        Af[v - 1, k] += 1.0          # flow enters v
    Ap[0, 0] = 1.0                   # p1 injected at node 1
    Ap[1, 1] = 1.0                   # p2 injected at node 2
    b[4] = D5                        # node 5 consumes d5
    b[5] = D6                        # node 6 consumes d6
    return Af, Ap, b


def main() -> None:
    Af, Ap, b = balance()

    f = cp.Variable(NF, name="f")
    p = cp.Variable(2, name="p")

    trosak_proizvodnje = 0.5 * cp.square(p[0]) + 2.0 * p[0] \
        + 0.3 * cp.square(p[1]) + 5.0 * p[1]
    trosak_transporta = COST @ f
    cilj = cp.Minimize(trosak_proizvodnje + trosak_transporta)

    c_balans = Af @ f + Ap @ p == b
    c_kapacitet = f <= CAP
    c_f_nenegativan = f >= 0
    c_p_nenegativan = p >= 0

    prob = cp.Problem(cilj, [c_balans, c_kapacitet,
                             c_f_nenegativan, c_p_nenegativan])
    prob.solve(solver=cp.CLARABEL)

    print("status:", prob.status)
    print(f"\nukupan trosak p* = {prob.value:.4f}")
    print(f"  proizvodnja: p1 = {p.value[0]:.4f}, p2 = {p.value[1]:.4f}"
          f"  (zbroj {p.value.sum():.4f})")
    print(f"  trosak proizvodnje = {trosak_proizvodnje.value:.4f}")
    print(f"  trosak transporta  = {trosak_transporta.value:.4f}")

    mu = c_kapacitet.dual_value          # multipliers of  f <= cap
    print("\ntokovi i dualne varijable kapaciteta:")
    for k, (u, v) in enumerate(ARCS):
        zas = "ZASICEN" if f.value[k] > CAP[k] - 1e-6 else "       "
        print(f"  ({u},{v}): f = {f.value[k]:8.4f} / {CAP[k]:5.1f}  {zas}"
              f"   mu = {mu[k]:7.4f}   dp*/dv = {-mu[k]:+7.4f}")

    lam = c_balans.dual_value
    print("\ndualne varijable balansa po vrhovima (cijena goriva u vrhu):")
    for i, l in enumerate(lam, start=1):
        print(f"  vrh {i}: lambda = {l:8.4f}")

    k_best = int(np.argmax(mu))
    print(f"\ninvesticija -> brid {ARCS[k_best]}, "
          f"dobitak {mu[k_best]:.4f} po jedinici kapaciteta")

    # marginal production costs, for the interpretation in the notes
    print(f"\nmarginalni troskovi: C1'(p1) = {p.value[0] + 2.0:.4f}, "
          f"C2'(p2) = {0.6 * p.value[1] + 5.0:.4f}")


if __name__ == "__main__":
    main()
