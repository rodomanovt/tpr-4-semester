def calc_comparison_matrix(matrix: list[list[float]], autocode=False) -> tuple[list, list]:
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
        print("Проведена номализация полученных чисел. Для этого определен нормирующий коэффициент ∑Vi.")
        print(f"∑Vi = V1 + V2 + V3 + V4 + V5 = ")
        # TODO


def main():
    criteria_matrix = [
        [1, 3, 3, 5, 9],
        [1/3, 1, 2, 3, 7],
        [1/3, 1/2, 1, 2, 5],
        [1/5, 1/3, 1/2, 1, 3],
        [1/9, 1/7, 1/5, 1/3, 1]
    ]

    calc_comparison_matrix(criteria_matrix, autocode=True)


if __name__ == "__main__":
    main()