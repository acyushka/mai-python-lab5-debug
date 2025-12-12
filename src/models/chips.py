from dataclasses import dataclass


@dataclass
class Chip:
    value: int
    quantity: int = 1

    COLORS = {
        1: "Белая",
        5: "Красная",
        25: "Зеленая",
        100: "Черная",
        500: "Фиолетовая",
        1000: "Оранжевая",
    }

    def get_color(self):
        return self.COLORS.get(self.value, "Неизвестная")

    def get_cost(self):
        return self.value * self.quantity

    def __add__(self, other):
        if isinstance(other, Chip):
            total = self.get_cost() + other.get_cost()
            return Chip(1, total)
        else:
            raise TypeError

    def __repr__(self) -> str:
        if self.quantity == 1:
            return f"{self.get_color} номиналом ${self.value}"
        return f"{self.quantity}x {self.get_color()} номиналом ${self.get_cost()}"
