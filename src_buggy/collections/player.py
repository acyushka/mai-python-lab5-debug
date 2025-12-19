from collections.abc import Iterator
from random import choice
from typing import Any

from src_buggy.models.player import Player


class PlayerCollection:
    """Списковая коллекция игроков через композицию"""

    def __init__(self):
        self.players: list[Player] = []

    def __len__(self) -> int:
        return len(self.players)

    def __iter__(self) -> Iterator:
        return iter(self.players)

    def __repr__(self) -> str:
        return f"PlayerCollection({self.__len__()} игроков)"

    def __getitem__(self, i: int | slice) -> Any:
        if isinstance(i, slice):
            collection_slice = PlayerCollection()
            collection_slice.players = self.players[i]
            return collection_slice

        return self.players[i]


    def append(self, player: Player) -> None:
        if not isinstance(player, Player):
            raise TypeError("Поддерживается только объект Player")

        self.players.append(player)

    def remove(self, player: Player) -> None:
        if player in self.players:
            self.players.remove(player)
        else:
            raise Exception("Игрока не существует")

    def get_random_player(self) -> Player | str:
        if not self.players:
            return "В коллекции нет игроков"
        return choice(self.players)

    def get_random_alive_player(self) -> Player | str:
        alive_players = [player for player in self.players if player.is_alive()]
        if not alive_players:
            return "В коллекции нет живых игроков"

        return choice(alive_players)
