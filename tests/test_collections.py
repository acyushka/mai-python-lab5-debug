import pytest
from src_buggy.collections.player import PlayerCollection
from src_buggy.models.player import Player
from src_buggy.collections.goose import GooseCollection
from src_buggy.models.gooses import Goose, WarGoose


class TestPlayerCollection:
    def test_append(self):
        collection = PlayerCollection()
        player = Player("houh", 1111)
        collection.append(player)
        assert len(collection) == 1
        assert collection[0] == player

    def test_append_invalid_type(self):
        collection = PlayerCollection()
        with pytest.raises(TypeError):
            collection.append("ifks")

    def test_remove(self):
        collection = PlayerCollection()
        player = Player("fsea;", 100)
        collection.append(player)
        collection.remove(player)
        assert len(collection) == 0

    def test_remove_invalid(self):
        collection = PlayerCollection()
        player = Player("Иван", 100)
        with pytest.raises(Exception):
            collection.remove(player)

    def test_get_random_alive(self):
        collection = PlayerCollection()
        player1 = Player("ghdf", 10032)
        player2 = Player("htrs", 100321)
        player2.hp = 0

        collection.append(player1)
        collection.append(player2)

        result = collection.get_random_alive_player()
        assert result == player1

    def test_iter(self):
        collection = PlayerCollection()
        player1 = Player("ghdf", 10032)
        player2 = Player("htrs", 100321)
        collection.append(player1)
        collection.append(player2)

        players = list(collection)
        assert len(players) == 2
        assert player1 in players
        assert player2 in players


class TestGooseCollection:
    def test_append(self):
        collection = GooseCollection()
        goose = Goose("hfg", 5)
        collection.append(goose)
        assert len(collection) == 1
        assert collection[0] == goose

    def test_remove(self):
        collection = GooseCollection()
        goose = Goose("jkl", 5)
        collection.append(goose)
        collection.remove(goose)
        assert len(collection) == 0

    def test_get_random(self):
        collection = GooseCollection()
        goose1 = Goose("hrfts", 3)
        goose2 = WarGoose("das", 10)
        collection.append(goose1)
        collection.append(goose2)

        result = collection.get_random_goose()
        assert result in [goose1, goose2]

    def test_add(self):
        collection1 = GooseCollection()
        collection2 = GooseCollection()

        goose1 = Goose("hrfts", 3)
        goose2 = WarGoose("das", 10)
        collection1.append(goose1)
        collection2.append(goose2)

        group = collection1 + collection2
        assert len(group) == 2
        assert goose1 in group.gooses
        assert goose2 in group.gooses