def calc_w(matrix: list[list[float]], autocode=False, level=3, crit="") -> tuple[list, list]:
    """по любой матрице сравнений находим Vi и Wi"""
    V = []
    W = []
    for i in range(len(matrix)):
        if autocode: print(f"Строка №{i+1}\nV{i+1} = (", end='')

        row_product = 1
        for el in matrix[i]:
            row_product *= el
            if autocode: print(f"{round(el, 3)} x ", end='')
        V.append(round(row_product ** 0.2, 3))
        if autocode: print(f") ^ 1/5 = {round(row_product ** 0.2, 3)}")

    svi = sum(V)
    W = [V[i]/svi for i in range(len(V))]

    if autocode:
        print(f"Проведена нормализация полученных чисел. Для этого определен нормирующий коэффициент ∑V{crit}i.")
        print(f"∑V{crit}i = V{crit}1 + V{crit}2 + V{crit}3 + V{crit}4 + V{crit}5 = {V[0]} + {V[1]} + {V[2]} + {V[3]} + {V[4]} = {sum(V)}")
        print(f"Найдена важность приоритетов W{level}{crit}i, для этого каждое из чисел V{crit}i разделено на ∑V{crit}i.")
        for i in range(len(V)):
            print(f"Строка №{i+1}")
            print(f"W{level}{crit}{i+1} = {V[i]}/∑V{crit}i = {round(V[i]/svi, 3)}")
        print("В результате получен вектор приоритетов:")
        print(f"W{level}{crit}i = ({"; ".join([str(round(el, 3)) for el in W])}), где индекс {level} означает, что вектор приоритетов относится к {level} уровню иерархии")

    return V, W


def print_arrays(V: list[float], W: list[float]):
    print(f"\nV = ", round(V[0], 3))
    for i in range(1, len(V)):
        print(f'     {round(V[i], 3)}')
    print(f"\nW = ", round(W[0], 3))
    for i in range(1, len(W)):
        print(f'     {round(W[i], 3)}')

    print(f"sum = {sum(V)}")


def calc_coherence(matrix: list[list[float]], W: list[float], autocode=False, level=3, crit="") -> float:
    if autocode: print("Определена сумма каждого столбца матрицы суждений.")
    si = []
    pi = []

    for i in range(len(matrix)):
        col = [matrix[j][i] for j in range(len(matrix[i]))]
        s = round(sum(col), 3)
        p = round(s * W[i], 3)
        si.append(s)
        pi.append(p)

        if autocode: 
            print(f"S{i+1}{crit} = {" + ".join([str(round(col[x], 3)) for x in range(len(col))])} = {s};")
    
    lambdamax = sum(pi)
    n = len(matrix)
    i_s = round((lambdamax - n)/(n-1), 3)
    o_s = round(i_s / 1.12, 3)

    if autocode:
        print("Затем полученный результат умножен на компоненту нормализованного вектора приоритетов.")
        for i in range(len(matrix)):
            print(f"P{i+1}{crit}{level} = S{i+1} x W{level}{crit}{i+1} = {pi[i]};")
        print("Найдена пропорциональность предпочтений.")
        print(f"λmax {crit} = Р1{crit} + Р2{crit} + Р3{crit} + Р4{crit} + Р5{crit} = {lambdamax}")
        print("Отклонение от согласованности выражается индексом согласованности.")
        print(f"ИС {crit} = (λmax {crit} - n)/(n - 1) = {i_s}")
        print("Найдено отношение согласованности ОС.")
        print(f"ОС {crit} = ИС/СИ = {o_s}")
        print(f"Значение ОС меньше или равное 0.10 считается приемлемым, значит матрица {crit} согласована.")

    return o_s


def alternative_synthesis(w2i: list[float], w3k_list: list[list[float]], autocode=False) -> list[tuple[float, str]]:
    if autocode: 
        print(f"W2i = ({"; ".join([str(round(el, 2)) for el in w2i])})")
        for num, w in enumerate(w3k_list, 1):
            print(f"W3k{num}i = ({"; ".join([str(round(el, 2)) for el in w])})")
            
    prios = []

    for i in range(len(w2i)):
        w = sum(w2i[j] * w3k_list[j][i] for j in range(len(w2i)))
        prios.append(round(w, 3))

    return zip(prios, ["A", "B", "C", "D", "E"])

    




def main():
    # матрица парного сравнения критериев
    criteria_matrix = [
        [1, 3, 3, 5, 9],
        [1/3, 1, 2, 3, 7],
        [1/3, 1/2, 1, 2, 5],
        [1/5, 1/3, 1/2, 1, 3],
        [1/9, 1/7, 1/5, 1/3, 1]
    ]

    # Матрица К1: Цена
    matrix_K1 = [
        [1, 1/2, 4, 3, 1/2],
        [2, 1, 5, 3, 1],
        [1/4, 1/5, 1, 1/3, 1/5],
        [1/3, 1/3, 3, 1, 1/3],
        [2, 1, 5, 3, 1]
    ]

    # Матрица К2: Мощность процессора
    matrix_K2 = [
        [1, 3, 1, 3, 9],
        [1/3, 1, 1/3, 1, 5],
        [1, 3, 1, 3, 9],
        [1/3, 1, 1/3, 1, 5],
        [1/9, 1/5, 1/9, 1/5, 1]
    ]

    # Матрица К3: Время работы от батареи
    matrix_K3 = [
        [1, 2, 1/3, 1, 2],
        [1/2, 1, 1/5, 1/2, 1],
        [3, 5, 1, 3, 5],
        [1, 2, 1/3, 1, 2],
        [1/2, 1, 1/5, 1/2, 1]
    ]

    # Матрица К4: Вес устройства
    matrix_K4 = [
        [1, 3, 1, 3, 3],
        [1/3, 1, 1/3, 1, 1],
        [1, 3, 1, 3, 3],
        [1/3, 1, 1/3, 1, 1],
        [1/3, 1, 1/3, 1, 1]
    ]

    # Матрица К5: Подсветка клавиатуры
    matrix_K5 = [
        [1, 3, 1, 1, 3],
        [1/3, 1, 1/3, 1/3, 1],
        [1, 3, 1, 1, 3],
        [1, 3, 1, 1, 3],
        [1/3, 1, 1/3, 1/3, 1]
    ]


    _, w2i = calc_w(criteria_matrix)
    _, w3k1i = calc_w(matrix_K1)
    _, w3k2i = calc_w(matrix_K2)
    _, w3k3i = calc_w(matrix_K3)
    _, w3k4i = calc_w(matrix_K4)
    _, w3k5i = calc_w(matrix_K5)

    w3k_list = [w3k1i, w3k2i, w3k3i, w3k4i, w3k5i]

    priorities = list(alternative_synthesis(w2i, w3k_list, autocode=False))
    
    print(*priorities)

    best = sorted(priorities, key=lambda el: -el[0])[0][1]
    print(f"Лучшая_альтернатива: {best}")

if __name__ == "__main__":
    main()