def calc_w(matrix: list[list[float]], autocode=False, level=3, crit="") -> tuple[list, list]:
    """По любой матрице сравнений находим Vi и Wi"""
    n = len(matrix)
    V = []
    
    for i in range(n):
        if autocode: print(f"Строка №{i+1}\nV{i+1} = (", end='')
        
        row_product = 1
        for el in matrix[i]:
            row_product *= el
            if autocode: print(f"{round(el, 3)} x ", end='')
        
        # ❌ НЕ округляем V - сохраняем полную точность
        V.append(row_product ** (1/n))
        if autocode: print(f") ^ 1/{n} = {round(V[-1], 3)}")
    
    svi = sum(V)
    # ✅ Округляем только финальные веса W
    W = [round(V[i]/svi, 3) for i in range(len(V))]
    
    if autocode:
        print(f"\n∑V{crit}i = {round(svi, 3)}")
        print(f"W{level}{crit}i = {W}")
    
    return V, W


def alternative_synthesis(w2i: list[float], w3k_list: list[list[float]], autocode=False) -> list[float]:
    """
    w2i: веса критериев (5 элементов)
    w3k_list: список из 5 векторов приоритетов альтернатив по каждому критерию
    """
    n_alternatives = len(w3k_list[0])  # Количество альтернатив
    n_criteria = len(w2i)              # Количество критериев
    
    if autocode: 
        print(f"\nВеса критериев: W2i = {w2i}")
        for num, w in enumerate(w3k_list, 1):
            print(f"W3k{num}i = {w}")
    
    result = []
    
    # ✅ Цикл по альтернативам, а не по критериям
    for i in range(n_alternatives):
        w = sum(w2i[j] * w3k_list[j][i] for j in range(n_criteria))
        result.append(round(w, 4))
    
    if autocode:
        print(f"\nГлобальные приоритеты альтернатив: {result}")
        print(f"Сумма приоритетов: {sum(result):.4f}")
    
    return result


def main():
    # Матрица парного сравнения критериев
    criteria_matrix = [
        [1, 3, 3, 5, 9],
        [1/3, 1, 2, 3, 7],
        [1/3, 1/2, 1, 2, 5],
        [1/5, 1/3, 1/2, 1, 3],
        [1/9, 1/7, 1/5, 1/3, 1]
    ]

    # Матрицы альтернатив по критериям
    matrices = [
        [  # K1: Цена
            [1, 1/2, 4, 3, 1/2],
            [2, 1, 5, 3, 1],
            [1/4, 1/5, 1, 1/3, 1/5],
            [1/3, 1/3, 3, 1, 1/3],
            [2, 1, 5, 3, 1]
        ],
        [  # K2: Процессор
            [1, 3, 1, 3, 9],
            [1/3, 1, 1/3, 1, 5],
            [1, 3, 1, 3, 9],
            [1/3, 1, 1/3, 1, 5],
            [1/9, 1/5, 1/9, 1/5, 1]
        ],
        [  # K3: Батарея
            [1, 2, 1/3, 1, 2],
            [1/2, 1, 1/5, 1/2, 1],
            [3, 5, 1, 3, 5],
            [1, 2, 1/3, 1, 2],
            [1/2, 1, 1/5, 1/2, 1]
        ],
        [  # K4: Вес
            [1, 3, 1, 3, 3],
            [1/3, 1, 1/3, 1, 1],
            [1, 3, 1, 3, 3],
            [1/3, 1, 1/3, 1, 1],
            [1/3, 1, 1/3, 1, 1]
        ],
        [  # K5: Подсветка
            [1, 3, 1, 1, 3],
            [1/3, 1, 1/3, 1/3, 1],
            [1, 3, 1, 1, 3],
            [1, 3, 1, 1, 3],
            [1/3, 1, 1/3, 1/3, 1]
        ]
    ]

    # Расчёт весов критериев
    _, w2i = calc_w(criteria_matrix, autocode=True, level=2, crit='Крит')
    
    # Расчёт весов альтернатив по каждому критерию
    w3k_list = []
    for i, matrix in enumerate(matrices, 1):
        _, w = calc_w(matrix, autocode=False, level=3, crit=f'K{i}')
        w3k_list.append(w)
    
    # Синтез глобальных приоритетов
    priorities = alternative_synthesis(w2i, w3k_list, autocode=True)
    
    # Вывод результатов
    alternatives = ['A', 'B', 'C', 'D', 'E']
    print("\n" + "="*50)
    print("ИТОГОВЫЕ ПРИОРИТЕТЫ АЛЬТЕРНАТИВ:")
    print("="*50)
    for i, p in enumerate(priorities):
        print(f"{alternatives[i]}: {p}")
    print(f"\nСумма приоритетов: {sum(priorities):.4f}")
    print(f"Лучшая альтернатива: {alternatives[priorities.index(max(priorities))]}")


if __name__ == "__main__":
    main()