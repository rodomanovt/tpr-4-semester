class Laptop:
    def __init__(self, name: str, price: int, processor: int, battery: int, weight: int, backlight: int):
        self.name = name
        self.price = price
        self.processor = processor
        self.battery = battery
        self.weight = weight
        self.backlight = backlight
    

    def __repr__(self):
        return (f"Laptop({self.name}: price={self.price}, "
                f"processor={self.processor}, battery={self.battery}, "
                f"weight={self.weight}, backlight={self.backlight})")
    

    def get_values(self) -> list:
        """Возвращает список значений критериев."""
        return [self.price, self.processor, self.battery, 
                self.weight, self.backlight]



def electra(alternatives: list[Laptop], autocode=False) -> list[list[str]]:
    """Построение матрицы предпочтений"""
    n = len(alternatives)
    res = [["---" for i in range(n)] for j in range(n)]

    for i in range(n):
        for j in range(i+1, n):
            alt1 = alternatives[i].get_values()
            alt2 = alternatives[j].get_values()
            pij = [] # За
            nij = [] # Против

            if alt1[0] < alt2[0]: # Цена
                pij.append(5) # прибавляем вес критерия
                nij.append(0)
            elif alt1[0] > alt2[0]:
                pij.append(0)
                nij.append(5)
            else:
                pij.append(0)
                nij.append(0)

            if alt1[1] > alt2[1]: # Мощность
                pij.append(5)
                nij.append(0)
            elif alt1[1] < alt2[1]:
                pij.append(0)
                nij.append(5)
            else:
                pij.append(0)
                nij.append(0)

            if alt1[2] > alt2[2]: # Время работы
                pij.append(4)
                nij.append(0)
            elif alt1[2] < alt2[2]:
                pij.append(0)
                nij.append(4)
            else:
                pij.append(0)
                nij.append(0)

            if alt1[3] < alt2[3]: # Вес устройства
                pij.append(3)
                nij.append(0)
            elif alt1[3] > alt2[3]:
                pij.append(0)
                nij.append(3)
            else:
                pij.append(0)
                nij.append(0)

            if alt1[4] > alt2[4]: # Подсветка клавиатуры
                pij.append(2)
                nij.append(0)
            elif alt1[4] < alt2[4]:
                pij.append(0)
                nij.append(2)
            else:
                pij.append(0)
                nij.append(0)


            try:
                dij = round(sum(pij) / sum(nij), 1)
            except ZeroDivisionError:
                dij = float('inf')
            try:
                dji = round(sum(nij) / sum(pij), 1)
            except ZeroDivisionError:
                dji = float('inf')

            if dij > 1:
                res[i][j] = dij
            if dji > 1:
                res[j][i] = dji


            if autocode:
                joined_pji = ' + '.join(map(str, pij))
                joined_nji = ' + '.join(map(str, nij))

                print(f"\nРассмотрим альтернативы {i+1} и {j+1}:")
                print(f"P{i+1}{j+1} = {joined_pji} = {sum(pij)};")
                print(f"N{i+1}{j+1} = {joined_nji} = {sum(nij)};")

                print(f"D{i+1}{j+1} = P{i+1}{j+1}/N{i+1}{j+1} = {sum(pij)}/{sum(nij)} = {dij}", end='')
                if dij < 1:
                    print(" < 1 - отбрасываем")
                elif dij > 1:
                    print(" > 1 - принимаем")

                print(f"P{j+1}{i+1} = {joined_nji} = {sum(nij)};")
                print(f"N{j+1}{i+1} = {joined_pji} = {sum(pij)};")

                print(f"D{j+1}{i+1} = P{i+1}{j+1}/N{i+1}{j+1} = {sum(nij)}/{sum(pij)} = {dji}", end='')
                if dji < 1:
                    print(" < 1 - отбрасываем")
                elif dji > 1:
                    print(" > 1 - принимаем")

    return res


def reduce_matrix(matrix: list[list[str]], threshold: float) -> list[list[str]]:
    """Разрежение матрицы предпочтений с учетом порога"""
    pass


def print_matrix(matrix: list[list[str]]):
    n = len(matrix)
    print("", *[str(i+1) + "  " for i in range(n)])
    for i in range(n):
        for j in range(n):
            print(matrix[i][j], end=" ")
        print(i+1)


def main():
    alternatives = [
        Laptop("A", price=7, processor=10, battery=7, weight=5, backlight=10),
        Laptop("B", price=5, processor=5, battery=5, weight=10, backlight=5),
        Laptop("C", price=15, processor=10, battery=10, weight=5, backlight=10),
        Laptop("D", price=10, processor=5, battery=7, weight=10, backlight=10),
        Laptop("E", price=5, processor=2, battery=5, weight=10, backlight=5),
        Laptop("F", price=7, processor=10, battery=10, weight=5, backlight=10),
        Laptop("G", price=5, processor=5, battery=7, weight=5, backlight=10),
        Laptop("H", price=15, processor=10, battery=7, weight=10, backlight=10),
        Laptop("I", price=7, processor=5, battery=10, weight=5, backlight=5),
    ]

    matrix = electra(alternatives, autocode=True)
    print_matrix(matrix)


if __name__ == "__main__":
    main()