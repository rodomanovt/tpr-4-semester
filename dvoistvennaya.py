from fractions import Fraction

def dual_from_primal(c_list, A_list, b_list, basis_indices, CB_list):
    """
    Вычисляет оптимальное решение двойственной задачи из оптимального
    решения прямой задачи по формуле: y* = CB * D^-1
    
    basis_indices: индексы базисных переменных в оптимальном плане
    CB_list: коэффициенты целевой функции для базисных переменных
    """
    n_constraints = len(b_list)
    
    # Формируем матрицу D из столбцов базисных переменных
    D = [[Fraction(A_list[i][j]) for j in basis_indices]
         for i in range(n_constraints)]
    
    # Находим обратную матрицу D^-1 методом Гаусса-Жордана
    n = len(D)
    aug = [D[i][:] + [Fraction(1 if i==j else 0) for j in range(n)]
           for i in range(n)]
    
    for col in range(n):
        # Найти ведущий элемент
        pivot_row = max(range(col, n), key=lambda r: abs(aug[r][col]))
        aug[col], aug[pivot_row] = aug[pivot_row], aug[col]
        pivot = aug[col][col]
        aug[col] = [x / pivot for x in aug[col]]
        for row in range(n):
            if row != col:
                factor = aug[row][col]
                aug[row] = [aug[row][k] - factor * aug[col][k]
                            for k in range(2*n)]
    
    D_inv = [[aug[i][n+j] for j in range(n)] for i in range(n)]
    
    # Вычисляем y* = CB * D^-1
    CB = [Fraction(x) for x in CB_list]
    y_star = [sum(CB[i] * D_inv[i][j] for i in range(n)) for j in range(n)]
    
    # Вычисляем g_min
    b = [Fraction(x) for x in b_list]
    g_min = sum(b[i] * y_star[i] for i in range(n_constraints))
    
    return y_star, g_min, D_inv


def stability_intervals(D_inv, x_basis, b):
    """
    Вычисляет интервалы устойчивости двойственных оценок.
    """
    m = len(b)
    results = []
    for i in range(m):
        col = [D_inv[j][i] for j in range(len(x_basis))]
        pos = [(x_basis[j], col[j]) for j in range(len(col)) if col[j] > 0]
        neg = [(x_basis[j], col[j]) for j in range(len(col)) if col[j] < 0]
        
        delta_H = min(xj/dji for xj, dji in pos) if pos else float('inf')
        delta_B = min(abs(xj/dji) for xj, dji in neg) if neg else float('inf')
        
        results.append({
            'resource': i+1, 'b': b[i],
            'delta_H': delta_H, 'delta_B': delta_B,
            'interval': (float(b[i]) - float(delta_H),
                         float(b[i]) + float(delta_B))
        })
    return results


c  = [8, 6, Fraction(1,2), 8, 6, Fraction(1,2)]
A  = [[Fraction(1,20), Fraction(1,30), Fraction(1,50), 0, 0, 0],
      [0, 0, 0, Fraction(1,45), Fraction(1,30), Fraction(1,60)]]
b  = [12, 8]

# Из решения прямой задачи: базис = {x2, x4}, CB = [6, 8]
basis_idx = [1, 3]   # x2 -> index 1, x4 -> index 3
CB        = [6, 8]

y_star, g_min, D_inv = dual_from_primal(c, A, b, basis_idx, CB)
print(f"y* = {[float(y) for y in y_star]}")
print(f"g_min = {g_min} = {float(g_min)}")

x_basis = [Fraction(360), Fraction(360)]  # x2*, x4*
intervals = stability_intervals(D_inv, x_basis, b)
for r in intervals:
    print(f"Ресурс {r['resource']}: b={r['b']}, "
          f"Δb ∈ (-{r['delta_H']}, {'+inf' if r['delta_B']==float('inf') else r['delta_B']}), "
          f"интервал = ({r['interval'][0]}, +inf)")
