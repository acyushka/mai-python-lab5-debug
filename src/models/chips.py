from dataclasses import dataclass


@dataclass
class Chip:
    """Простая сущность фишки"""
    value: int

    def __add__(self, other):
        if isinstance(other, Chip):
            total = self.value + other.value
            return Chip(total)
        else:
            raise TypeError

    def __repr__(self) -> str:
        return f"${self.value}"
