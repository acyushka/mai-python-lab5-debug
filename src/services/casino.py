import random
from random import randint, choice

from src.collections.balance import CasinoBalance
from src.collections.goose import GooseCollection
from src.collections.gooses_income import GoosesIncomeCollection
from src.collections.player import PlayerCollection
from src.models.chips import Chip
from src.models.gooses import Goose, WarGoose, HonkGoose
from src.models.player import Player

NAMES = [
        "Алекс", "Боб", "Виктория", "Джон", "Майк", "Сара", "Елена", "Дмитрий",
        "Ольга", "Макс", "Ник", "Кейт", "Лео", "Анна", "Сергей", "Ирина", "Даша",
        "Игорь", "Эвелина", "Артем", "Леди Гага", "Дарт Вейдер", "Сабина", "Герасим",
    ]

class Casino:
    def __init__(self):
        self.players = PlayerCollection()
        self.gooses = GooseCollection()
        self.balances = CasinoBalance()
        self.gooses_income = GoosesIncomeCollection()
        self.names = NAMES

        self.steps_count = 0

    def register_player(self, name: str = "---1", balance: int = -1) -> str | None:
        if self.names:
            if name == "---1":
                name = self.names.pop()
            if balance == -1:
                balance = randint(30, 777)

            player = Player(name, balance)
            self.players.append(player)
            self.balances[name] = balance

            return f"Игрок {name} сел за стол (HP: 100, Баланс: ${self.balances[name]})"

    def register_goose(self, goose_type: str = "0", name: str = "---1", honk_volume: int = -1) -> str | None:
        if self.names:
            if goose_type == "0":
                goose_type = choice(("war", "honk"))
            if name == "---1":
                name = self.names.pop()
            if honk_volume == -1:
                honk_volume = randint(1, 20)

            match goose_type:
                case "war":
                    goose = WarGoose(name, honk_volume)
                    msg = f"Боевой гусь {name} встал неподалеку от стола с игроками"
                case "honk":
                    goose = HonkGoose(name, honk_volume)
                    msg = f"Гусь-крикун {name} встал неподалеку от стола с игроками"
                case _:
                    raise ValueError("Неизвестный тип гуся")

            self.gooses.append(goose)
            self.gooses_income[name] = 0

            return msg

    def player_dep(self) -> str | None:
        player = self.players.get_random_alive_player()
        if not isinstance(player, Player):
            pass
        else:
            self.steps_count += 1

            dep: Chip = Chip(random.randint(5, player.balance))
            self.balances[player.name] -= dep.value

            if random.random() > 0.9:  # ставка залетела
                win = Chip(dep.value * randint(1, 5))

                payout: Chip = dep + win

                self.balances[player.name] += payout.value
                return f"Игрок {player.name} поставил ${dep.value} и выиграл! Общая выплата: {payout.value}."

            else:  # ставка не залетела
                if self.balances[player.name] <= 0:
                    del self.balances[player.name]
                    self.players.remove(player)
                    return f"Игрок {player.name} поставил все свои фишки и проиграл. Вдруг за ним пришли два гуся с дубинами и увели его.."

                return f"Игрок {player.name} поставил ${dep.value} и ставка не залетела.."

    def goose_action(self) -> str | None:
        if self.gooses:
            self.steps_count += 1

            goose = self.gooses.get_random_goose()
            return goose.action(self)
        else:
            pass

    def goose_group(self) -> str | None:
        if len(self.gooses) > 1 and self.players:
            self.steps_count += 1

            group: GooseCollection = self.gooses + self.gooses
            group_damage = min(90, len(group)*10)

            msg = f"Неожиданно из-за угла вылетела орава гусей! HP всех игроков уменьшилось на {group_damage}! "

            amount = 0
            killed_players = 0

            for victim in self.players:
                previous_hp = victim.hp
                victim.hp -= group_damage
                print(f"  HP игрока {victim.name}: {previous_hp} -> {victim.hp}")

                if not victim.is_alive():
                    killed_players += 1
                    amount += self.balances[victim.name]

                    del self.balances[victim.name]
                    self.players.remove(victim)

            if amount > 0:
                random_goose = choice(self.gooses)
                self.gooses_income[random_goose.name] += amount

                msg += f" Не выжило: {killed_players} игрок(-ов). Гусь {random_goose.name} забрал с трупов {amount}.."

            return msg

    def panic_action(self) -> str | None:
        player = self.players.get_random_alive_player()
        goose = self.gooses.get_random_goose()
        if not isinstance(player, Player) or not isinstance(goose, Goose):
            pass
        else:
            self.steps_count += 1

            msg = f"Игрок {player.name} запаниковал при виде агрессивно настроенного гуся {goose.name} и убежал в страхе из казино.."
            amount = self.balances[player.name]
            if amount > 0:
                self.gooses_income[goose.name] += amount
                del self.balances[player.name]
                self.players.remove(player)
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
            self.register_player,
            self.register_goose,
            self.goose_action,
            self.goose_action,
            self.goose_action,
            self.goose_group,
            self.player_dep,
            self.player_dep,
            self.player_dep,
            self.player_dep,
            self.player_dep,
            self.player_dep,
            self.healing_action,
            self.panic_action,
        ]

        random_action = choice(actions)
        print("[ИЗМЕНЕНИЯ ПОСЛЕ СОБЫТИЯ]")
        result = random_action()
        print("[ИЗМЕНЕНИЯ ПОСЛЕ СОБЫТИЯ]")
        print()
        print(f"[СОБЫТИЕ] {result} [СОБЫТИЕ]")


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
        print(f"══════════════════════════════ [ШАГ {casino.steps_count + 1}] ════════════════════════════════════")
        casino.step()
        print(f"══════════════════════════════ [ШАГ {casino.steps_count}] ════════════════════════════════════")

    print()