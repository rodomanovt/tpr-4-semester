from fractions import Fraction

def simplex_max(c_list, A_list, b_list):
    """Maximization simplex method (canonical form with slack variables)."""
    n_orig = len(c_list)
    n_slack = len(b_list)
    n = n_orig + n_slack

    c = [Fraction(x) for x in c_list] + [Fraction(0)] * n_slack
    A = [[Fraction(x) for x in row] + [Fraction(1 if i==j else 0)
          for j in range(n_slack)]
         for i, row in enumerate(A_list)]
    b = [Fraction(x) for x in b_list]
    basis = list(range(n_orig, n))

    for _ in range(100):
        CB = [c[basis[i]] for i in range(n_slack)]
        nb = [j for j in range(n) if j not in basis]
        deltas = {j: sum(CB[i]*A[i][j] for i in range(n_slack)) - c[j]
                  for j in nb}
        Q = sum(CB[i]*b[i] for i in range(n_slack))
        neg = {j: d for j, d in deltas.items() if d < 0}
        if not neg:
            x = [Fraction(0)] * n
            for i, bv in enumerate(basis):
                x[bv] = b[i]
            return float(Q), [float(xi) for xi in x]
        entering = min(neg, key=lambda j: neg[j])
        ratios = {i: b[i]/A[i][entering]
                  for i in range(n_slack) if A[i][entering] > 0}
        if not ratios:
            return None, None  # unbounded
        lr = min(ratios, key=lambda i: ratios[i])
        piv = A[lr][entering]
        new_A = [row[:] for row in A]
        new_b = b[:]
        new_A[lr] = [A[lr][j]/piv for j in range(n)]
        new_b[lr] = b[lr]/piv
        for i in range(n_slack):
            if i != lr:
                f = A[i][entering]
                for j in range(n):
                    new_A[i][j] = (A[i][j]*piv - A[lr][j]*f) / piv
                new_b[i] = (b[i]*piv - b[lr]*f) / piv
                print(new_b[i])
        A, b, basis[lr] = new_A, new_b, entering


if __name__ == "__main__":
    c  = [8, 6, 0.5, 8, 6, 0.5]
    A  = [[1/20, 1/30, 1/50, 0,    0,    0   ],
        [0,    0,    0,    1/45, 1/30, 1/60]]
    b  = [12, 8]
    Q, x = simplex_max(c, A, b)
    print(f"f_max = {Q}")
    print(f"x = {x}")