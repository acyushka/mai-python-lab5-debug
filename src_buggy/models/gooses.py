from random import randint, choice

from src_buggy.models.player import Player
from typing import Any


class Goose:
    """Обычный гусь"""

    def __init__(self, name: str, honk_volume: int):
        self.name = name
        self.honk_volume = honk_volume

    def __repr__(self) -> str:
        return f"{self.__class__.__name__} {self.name} с криком {self.honk_volume}"

    def action(self, casino: Any) -> str:
        return "Простой гусь, ничего не умеет"

class WarGoose(Goose):
    """Боевой гусь с дубиной, может бить случайного игрока, если тот умрет, он заберет все его фишки"""
    def action(self, casino: Any) -> str:
        alive_players = [player for player in casino.players if player.is_alive()]
        if not alive_players:
            return f"Боевой гусь {self.name} захотел помахать дубинкой, но жертву найти не удалось"

        victim: Player = choice(alive_players)
        damage = randint(10,25)

        ### ОШИБКА 5 - обращение к несуществующему атрибуту объекта
        previous_hp = victim.health
        victim.health -= damage
        print(f"  HP игрока {victim.name}: {previous_hp} -> {victim.health}")

        msg = f"Боевой гусь {self.name} внезапно долбанул по голове игрока {victim.name} и нанес урон в {damage} HP!"
        if not victim.is_alive():
            msg += " Игрок не выжил.."
            casino.gooses_income[self.name] += casino.balances[victim.name]
            del casino.balances[victim.name]
            casino.players.remove(victim)
            print("  - Игрок")

        return msg


class HonkGoose(Goose):
    """Гусь крикун, своим криком оглушает всех, и пока все приходят в себя, он крадет у всех немного фишек, а если вдруг фишек не остается игрок от шока теряет сознание"""
    def action(self, casino: Any) -> str:
        if not casino.players:
            return f""

        stunned_players = 0
        killed_players = 0
        for player in casino.players:
            if player.balance >= self.honk_volume:
                casino.balances[player.name] -= self.honk_volume
                casino.gooses_income[self.name] += self.honk_volume

                stunned_players += 1
            else:
                casino.gooses_income[self.name] += self.honk_volume

                killed_players += 1
                del casino.balances[player.name]
                casino.players.remove(player)
                print("  - Игрок")

        msg = f"Гусь {self.name} издал крик громкостью {self.honk_volume}. Пострадало {stunned_players} игроков!"
        if killed_players > 1:
            msg += f" {killed_players} игроков потеряли сознание! Группа гусей увела их куда-то.."
        elif killed_players == 1:
            msg += f" {killed_players} игрок потерял сознание! Группа гусей увела его куда-то.."

        return msg
