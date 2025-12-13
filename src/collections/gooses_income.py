from collections import UserDict


class GoosesIncomeCollection(UserDict):
    """Словарная коллекция доходов гусей, наследуется от UserDict, производится логирование при изменении значения элемента"""

    def __setitem__(self, key: str, new_value: int) -> None:
        if not isinstance(key, str):
            raise TypeError("Имя гуся должно быть строкой!")
        if not isinstance(new_value, int):
            raise TypeError("Доход должен быть числом!")

        previous_value = self.data.get(key, 0)

        super().__setitem__(key, new_value)

        balance_changes = new_value - previous_value
        if balance_changes != 0:
            print(f"  Гусь {key} заработал: {previous_value} -> {new_value}")
