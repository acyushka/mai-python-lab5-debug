from collections import UserDict


class CasinoBalance(UserDict):
    """Словарная коллекция балансов игроков в казино, наследуется от UserDict, производится логирование при изменении значения элемента"""

    def __setitem__(self, key: str, new_value: int) -> None:
        if not isinstance(key, str):
            raise TypeError("Имя игрока должно быть строкой!")
        if not isinstance(new_value, int):
            raise TypeError("Баланс должен быть числом!")

        previous_value = self.data.get(key, 0)

        super().__setitem__(key, new_value)

        balance_changes = new_value - previous_value
        if previous_value != 0: # чтобы при регистрации не писало лог
            if balance_changes != 0:
                print(f"  Баланс игрока {key}: {previous_value} -> {new_value}")
            else:
                print(f"  Баланс игрока {key} не изменился")
