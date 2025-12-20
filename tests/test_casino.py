import random
from src_buggy.services.casino import Casino


class TestCasino:
    def test_register_player_random(self):
        casino = Casino()
        old_names_count = len(casino.names)

        result = casino.register_player()

        assert result is not None
        assert "Игрок" in result
        assert len(casino.players) == 1
        assert len(casino.names) == old_names_count - 1

    def test_register_player_custom(self):
        casino = Casino()
        result = casino.register_player("lala", 1488)

        assert "lala" in result
        assert casino.balances["lala"] == 1488
        assert len(casino.players) == 1

    def test_register_goose_war(self):
        casino = Casino()
        result = casino.register_goose("war", "lala", 5)

        assert "Боевой гусь lala" in result
        assert len(casino.gooses) == 1
        assert casino.gooses_income["lala"] == 0

    def test_register_goose_honk(self):
        casino = Casino()
        result = casino.register_goose("honk", "lala", 10)

        assert "Гусь-крикун lala" in result
        assert len(casino.gooses) == 1
        assert casino.gooses_income["lala"] == 0

    def test_dep_win(self, monkeypatch):
        casino = Casino()
        casino.register_player("lala", 100)

        monkeypatch.setattr(random, 'random', lambda: 0.99)

        result = casino.player_dep()

        assert result is not None
        assert "выиграл" in result

    def testdep_loss(self, monkeypatch):
        casino = Casino()
        casino.register_player("lala", 100)

        monkeypatch.setattr(random, 'random', lambda: 0.89999)

        result = casino.player_dep()

        assert result is not None
        assert "не залетела" in result

    def test_dep_killed(self, monkeypatch):
        casino = Casino()
        casino.register_player("lala", 10)

        monkeypatch.setattr(random, 'random', lambda: 0.5)
        monkeypatch.setattr(random, 'randint', lambda a, b: 10)

        result = casino.player_dep()

        assert result is not None
        assert "проиграл" in result
        assert "Игрок" not in casino.balances
        assert len(casino.players) == 0

    def test_goose_action_1(self):
        casino = Casino()
        casino.register_player("lala", 10)
        casino.register_goose("war", "osa", 10)

        result = casino.goose_action()

        assert result is not None

    def test_goose_action_no_gooses(self):
        casino = Casino()
        result = casino.goose_action()
        assert result is None

    def test_goose_group(self):
        casino = Casino()
        casino.register_player("wfe", 100)
        casino.register_player("efw", 100)
        casino.register_goose("war", "da", 10)
        casino.register_goose("honk", "daads", 5)

        result = casino.goose_group()

        assert result is not None
        assert "орава гусей" in result

    def test_panic(self):
        casino = Casino()
        casino.register_player("ladls", 100)
        casino.register_goose("war", "dlsa", 10)

        result = casino.panic_action()

        assert result is not None
        assert "запаниковал" in result

    def test_healing(self):
        casino = Casino()
        casino.register_player("rew", 100)

        casino.players[0].hp -= 50

        result = casino.healing_action()

        assert result is not None
        assert "энергетик" in result
        assert casino.players[0].hp > 50