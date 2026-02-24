class Laptop:
    def __init__(self, name: str, price: int, ram: int, weight: int, storage: int, battery: int):
        self.name = name 
        self.price = price     # -
        self.ram = ram         # +
        self.weight = weight   # -
        self.storage = storage # +
        self.battery = battery # +

    def __repr__(self):
        return f"{self.name}"



def pareto_optimal(alternatives: list[Laptop], output_table = False) -> set[str]:
    n = len(alternatives)
    table = [["x" for i in range(n)] for j in range(n)]
    res = set()
    
    for i in range(0, n): # сравниваем каждый с каждым
        for j in range(0, n):
            if i != j:
                alt1 = alternatives[i]
                alt2 = alternatives[j]

                # пытаемся понять, лучше ли alt1, чем alt2
                # если crit положительный, то alt1 лучше по этому критерию
                crit1 = alt2.price - alt1.price # отрицательное стремление
                crit2 = alt1.ram - alt2.ram # положительное стемление
                crit3 = alt2.weight - alt1.weight
                crit4 = alt1.storage - alt2.storage
                crit5 = alt1.battery - alt2.battery
                crits = [crit1, crit2, crit3, crit4, crit5]

                if 1 <= sum([c < 0 for c in crits]) <= 4:
                    # если расхождение в знаках критериев, то alt1 и alt2 несравнимы
                    if table[i][j] == 'x': # чтобы буква случано не заменилась на н
                        table[i][j] = "н"
                    continue

                if crit1 + crit2 + crit3 + crit4 + crit5 > 0:
                    # говорим, что alt1 лучше, чем alt2
                    if i > j: # ставим букву в нижний треугольник матрицы
                        table[i][j] = alt1.name
                    else:
                        table[j][i] = alt1.name
                    res.add(alt1.name)
    
    if output_table:
        # вывод таблицы
        for i in range(n): # заполняем верхний треугольник крестиками
            for j in range(i+1, n):
                table[i][j] = 'x'

        print(*[a.name for a in alternatives])
        for i in range(n):
            for j in range(n):
                print(table[i][j], end=" ")
            print(alternatives[i].name)

    print("Парето-оптимальное множество:")
    return res
            

def convert_bounds(bounds: list[float | None]) -> list[float]:
    """Переводим границы в формат для сравнения"""
    new_bounds = bounds.copy()

    for i in range(len(bounds)):
        if i == 0 and bounds[i] == "": new_bounds[i] = float("inf")
        if i == 1 and bounds[i] == "": new_bounds[i] = 0
        if i == 2 and bounds[i] == "": new_bounds[i] = float("inf")
        if i == 3 and bounds[i] == "": new_bounds[i] = 0
        if i == 4 and bounds[i] == "": new_bounds[i] = 0

    new_bounds = [float(el) if el != float("inf") else el for el in new_bounds]

    return new_bounds


def bounds(alternatives: list[Laptop], bounds: list[float | None]) -> set[str]:
    bounds = convert_bounds(bounds)
    filtered_alternatives: list[Laptop] = []

    for alt in alternatives:
        if alt.price <= bounds[0] and alt.ram >= bounds[1] and alt.weight <= bounds[2]\
        and alt.storage >= bounds[3] and alt.battery >= bounds[4]:
            filtered_alternatives.append(alt)

    print(f"Рассматирваем альтернативы {filtered_alternatives}")

    return pareto_optimal(filtered_alternatives)



def suboptimization(alternatives: list[Laptop], bounds: list[float | None]) -> str:
    # ищем главный критерий
    main_crit = 0
    for i in range(len(bounds)):
        if bounds[i] == None:
            main_crit = i
    print(f"Главный критерий: {main_crit}")

    # фильтруем по границам
    bounds = convert_bounds(bounds)
    filtered_alternatives: list[Laptop] = []

    for alt in alternatives:
        if alt.price <= bounds[0] and alt.ram >= bounds[1] and alt.weight <= bounds[2]\
        and alt.storage >= bounds[3] and alt.battery >= bounds[4]:
            filtered_alternatives.append(alt)

    print(f"Рассматирваем альтернативы {filtered_alternatives}")

    def key(alt: Laptop) -> float:
        if main_crit == 0:
            return -alt.price
        if main_crit == 1:
            return alt.ram
        if main_crit == 2:
            return -alt.weight
        if main_crit == 3:
            return alt.storage
        if main_crit == 4:
            return alt.battery

    # выбираем максимум по главному критерию из отфильтрованных альтернатив
    res = max(filtered_alternatives, key=key)
    print("Оптимальный вариант:")
    return res.name


def lexicographic(alternatives: list[Laptop], crits: list[int]) -> str:

    def key(alt: Laptop) -> list[float]:
        """Ищем последовательность критериев для лексикографической сортировки"""
        sequence = []

        for crit in crits:
            if crit == 0:
                sequence.append(-alt.price)
            if crit == 1:
                sequence.append(alt.ram)
            if crit == 2:
                sequence.append(-alt.weight)
            if crit == 3:
                sequence.append(alt.storage)
            if crit == 4:
                sequence.append(alt.battery)

        return sequence

    # максимум по каждому из критериев в указанном порядке
    res = sorted(alternatives, key=key, reverse=True)
    print("Отсортируем по приоритету критериев:")
    print(*[r.name for r in res])
    print("Оптимальный вариант:")
    return res[0]


def main():
    alternatives = [
        Laptop("a", 45, 8, 2.1, 256, 7),
        Laptop('b', 55, 16, 1.9, 512, 5),
        Laptop('c', 50, 8, 2.3, 256, 7),
        Laptop('d', 75, 32, 1.7, 1024, 10),
        Laptop('e', 52, 16, 2.0, 512, 7),
        Laptop('f', 62, 16, 1.8, 512, 9),
        Laptop('g', 48, 12, 1.9, 512, 8),
        Laptop('h', 70, 32, 2.2, 1024, 7),
        Laptop('i', 58, 16, 2.1, 256, 10)
    ]

     # alternatives = [
    #     Laptop("1", 6.3, 33, 1.4, 5, 4),
    #     Laptop("2", 7.5, 40, 4.5, 5, 4),
    #     Laptop("3", 6.2, 35, 6.6, 4, 3),
    #     Laptop("4", 7.3, 34, 1.2, 5, 3),
    #     Laptop("5", 6.3, 38, 6, 0.5, 5),
    #     Laptop("6", 6.8, 42, 7.3, 4, 5),
    #     Laptop("7", 6.2, 33, 2.3, 4, 3),
    #     Laptop("8", 6.5, 38, 1.0, 3, 3),
    #     Laptop("9", 7.3, 46, 5.0, 5, 4),
    # ]

    print("Выберите метод оптимизаци:")
    print("1) Парето-оптимальное множество")
    print("2) Установка верхних и нижних границ")
    print("3) Субоптимизация")
    print("4) Лексикографическая оптимизация")

    choice = int(input())
    match choice:
        case 1:
            print(pareto_optimal(alternatives, True))
        case 2:
            bound1 = input("Верхняя граница цены:")
            bound2 = input("Нижняя граница оперативной памяти:")
            bound3 = input("Верхняя граница веса:")
            bound4 = input("Нижняя граница объема накопителя:")
            bound5 = input("Нижняя граница времени работы от батареи:")
            print(bounds(alternatives, [bound1, bound2, bound3, bound4, bound5]))
        case 3:
            bound1 = input("Верхняя граница цены:")
            bound2 = input("Нижняя граница оперативной памяти:")
            bound3 = input("Верхняя граница веса:")
            bound4 = input("Нижняя граница объема накопителя:")
            bound5 = input("Нижняя граница времени работы от батареи:")
            print(suboptimization(alternatives, [bound1, bound2, bound3, bound4, bound5]))
        case 4:
            print("Введите приоритет критериев:")
            crits = list(map(int, input().split()))
            print(lexicographic(alternatives, crits))
        case _:
            print("Неверный выбор")


if __name__ == "__main__":
    main()
