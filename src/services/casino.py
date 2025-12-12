import random
from random import randint, choice

from src.collections.balance import CasinoBalance
from src.collections.goose import GooseCollection
from src.collections.gooses_income import GoosesIncomeCollection
from src.collections.player import PlayerCollection
from src.models.gooses import Goose, WarGoose, HonkGoose
from src.models.player import Player


class Casino:
    def __init__(self):
        self.players = PlayerCollection()
        self.gooses = GooseCollection()
        self.balances = CasinoBalance()
        self.gooses_income = GoosesIncomeCollection()

        self.steps_count = 0

    def register_player(self, name: str, balance: int = 100) -> Player:
        player = Player(name, balance)
        self.players.append(player)
        self.balances[name] = balance

        print(f"Игрок {name} сел за стол (HP: 100, Баланс: {self._display_chips(balance)}")
        return player

    def register_goose(self, goose_type: str, name: str, honk_volume: int) -> Goose:
        match goose_type:
            case "war":
                goose = WarGoose(name, honk_volume)
                print(f"Боевой гусь {name} встал неподалеку от стола с игроками")
            case "honk":
                goose = HonkGoose(name, honk_volume)
                print(f"Гусь-крикун {name} встал неподалеку от стола с игроками")
            case _:
                raise ValueError("Неизвестный тип гуся")

        self.gooses.append(goose)
        self.gooses_income[name] = 0

    def _display_chips(self, balance: int) -> str:
        if balance <= 0:
            return "$0"

        return f"${balance}"

    def player_dep(self) -> str | None:
        player = self.players.get_random_alive_player()
        if not isinstance(player, Player):
            pass
        else:
            self.steps_count += 1

            dep = randint(5, min(100, player.balance))

            if random.random() > 0.9:  # ставка залетела
                win = dep * randint(1, 5)
                self.balances[player.name] += win
                return f"Игрок {player.name} поставил ${dep} и выиграл ${win}!"

            else:  # ставка не залетела
                self.balances[player.name] -= dep
                if self.balances[player.name] <= 0:
                    del self.balances[player.name]
                    self.players.remove(player)
                    return f"Игрок {player.name} поставил все свои фишки и проиграл. Вдруг за ним пришли два гуся с дубинами и увели его.."

                return f"Игрок {player.name} поставил ${dep} и ставка не залетела.."

    def goose_action(self) -> str:
        if self.gooses:
            self.steps_count += 1

            goose = self.gooses.get_random_goose()
            return goose.action(self)
        return "Гусей нет поблизости"

    # def goose_group(self) -> str:
    #     if len(self.gooses) > 1:
    #         self.steps_count += 1
    #
    #         goose1 = self.gooses[0]
    #         goose2 = self.gooses[-1]

    def panic_action(self) -> str | None:
        player = self.players.get_random_alive_player()
        goose = self.gooses.get_random_goose()
        if not isinstance(player, Player) or not isinstance(goose, Goose):
            pass
        else:
            self.steps_count += 1

            msg = f"Игрок {player.name} запаниковал при виде агрессивно настроенного гуся {goose.name} и убежал в страхе из казино.."
            amount = self.balances[player.name]
            if self.balances[player.name] > 0:
                msg += f"Гусь {goose.name} забрал со стола оставленные игроком ${amount}"

            return msg

    def healing_action(self) -> str | None:
        player = self.players.get_random_alive_player()
        if not isinstance(player, Player):
            pass
        else:
            self.steps_count += 1

            heal = randint(10, 30)
            player.hp += heal

            return f"Игрок {player.name} нашел недопитый энергетик под столом и выпил его. HP игрока увеличилось на {heal}"

    def step(self) -> None:
        actions = [
            self.goose_action,
            self.goose_action,
            self.player_dep,
            self.player_dep,
            self.player_dep,
            self.healing_action,
            self.panic_action,
        ]

        random_action = choice(actions)
        result = random_action()
        print(f"[ШАГ {self.steps_count}] {result}")


def run_simulation(steps: int = 20, seed: int | None = None) -> None:
    if seed is not None:
        random.seed(seed)

    casino = Casino()

    casino.register_player("Саня", 100)
    casino.register_player("Вован", 220)
    casino.register_player("zxc_иван", 320)
    casino.register_player("Иоанн", 65)

    casino.register_goose("war", "Васян", 10)
    casino.register_goose("honk", "Клык", 5)

    while casino.steps_count < steps:
        print()
        casino.step()
        print()
