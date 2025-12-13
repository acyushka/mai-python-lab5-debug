from collections.abc import Iterator
from random import choice
from typing import Any

from src.models.gooses import Goose


class GooseCollection:
    """Списковая коллекция гусей через композицию"""

    def __init__(self):
        self.gooses: list[Goose] = []

    def __len__(self) -> int:
        return len(self.gooses)

    def __iter__(self) -> Iterator:
        return iter(self.gooses)

    def __repr__(self) -> str:
        return f"GooseCollection({self.__len__()} гусей)"

    def __getitem__(self, i: int | slice) -> Any:
        if isinstance(i, slice):
            collection_slice = GooseCollection
            collection_slice.players = self.gooses[i]
            return collection_slice

        return self.gooses[i]

    def append(self, goose: Goose) -> None:
        if not isinstance(goose, Goose):
            raise TypeError("Поддерживается только объект Goose")

        self.gooses.append(goose)

    def remove(self, goose: Goose) -> None:
        if goose in self.gooses:
            self.gooses.remove(goose)
        else:
            raise Exception("Гуся не существует")

    def get_random_goose(self) -> Goose | str:
        if not self.gooses:
            return "В коллекции нет гусей"
        return choice(self.gooses)

    def __add__(self, other):
        if not isinstance(other, GooseCollection):
            raise TypeError

        new_group = GooseCollection()
        new_group.gooses = self.gooses + other.gooses

        return new_group
