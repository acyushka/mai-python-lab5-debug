from random import randint, choice

from src.models.player import Player
from typing import Any


class Goose:
    def __init__(self, name: str, honk_volume: int):
        self.name = name
        self.honk_volume = honk_volume
        self.income = 0

    def __repr__(self) -> str:
        return f"{self.__class__.__name__} {self.name} с криком {self.honk_volume}"

    def action(self, casino: Any) -> str:
        return "Простой гусь, ничего не умеет"

class WarGoose(Goose):
    def action(self, casino: Any) -> str:
        alive_players = [player for player in casino.players if player.is_alive()]
        if not alive_players:
            return f"Боевой гусь {self.name} захотел помахать дубинкой, но жертву найти не удалось"

        victim: Player = choice(alive_players)
        damage = randint(10,40)
        victim.hp -= damage

        msg = f"Боевой гусь {self.name} внезапно долбанул по голове игрока {victim.name} и нанес урон в {damage} HP!"
        if not victim.is_alive():
            msg += " Игрок не выжил.."
            self.income += casino.balances[victim.name]
            casino.balances[victim.name] = 0

        return msg


class HonkGoose(Goose):
    def action(self, casino: Any) -> str:
        if not casino.players:
            return f""

        stunned_players = 0
        for player in casino.players:
            if player.balance >= self.honk_volume:
                casino.balances[player.name] -= self.honk_volume
            else:
                casino.balances[player.name] = 0

            self.income += self.honk_volume
            stunned_players += 1

        return f"{self.name} издал крик громкостью {self.honk_volume}. Пострадало {stunned_players} игроков!"

