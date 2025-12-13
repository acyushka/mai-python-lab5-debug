from dataclasses import dataclass


@dataclass
class Player:
    """Простая сущность игрока, HP всегда 100 в начале"""
    name: str
    balance: int
    hp: int = 100

    def __repr__(self) -> str:
        if self.is_alive:
            return f"Игрок {self.name} с балансом {self.balance} и здоровьем {self.hp}"
        return f"Игрок {self.name} - безжалостно забит гусями"

    def is_alive(self) -> bool:
        return self.hp > 0
