import random
from random import randint, choice

from src_fixed.collections.balance import CasinoBalance
from src_fixed.collections.goose import GooseCollection
from src_fixed.collections.gooses_income import GoosesIncomeCollection
from src_fixed.collections.player import PlayerCollection
from src_fixed.models.chips import Chip
from src_fixed.models.gooses import Goose, WarGoose, HonkGoose
from src_fixed.models.player import Player

NAMES = [
        "Алекс", "Боб", "Виктория", "Джон", "Майк", "Сара", "Елена", "Дмитрий",
        "Ольга", "Макс", "Ник", "Кейт", "Лео", "Анна", "Сергей", "Ирина", "Даша",
        "Игорь", "Эвелина", "Артем", "Леди Гага", "Дарт Вейдер", "Сабина", "Герасим",
    ] # стек из имен, пока он не пуст, игроки и гуси могут регистрироваться

class Casino:
    """Главная бизнес-логика всего сервиса"""

    def __init__(self):
        """Инициализация всех нужных коллекций, имен, и счетчика шагов симуляции"""
        self.players = PlayerCollection()
        self.gooses = GooseCollection()
        self.balances = CasinoBalance()
        self.gooses_income = GoosesIncomeCollection()
        self.names = NAMES

        self.steps_count = 0

    def register_player(self, name: str = "---1", balance: int = -1) -> str | None:
        """Регистрация игроков"""
        if self.names:
            self.steps_count += 1

            if name == "---1":
                name = self.names.pop()

            ### ИСПРАВЛЕНИЕ 3 - == вместо is
            if balance == -1:
                balance = randint(30, 777)

            player = Player(name, balance)
            self.players.append(player)
            self.balances[name] = balance
            print("  + Игрок")

            return f"Игрок {name} сел за стол (HP: 100, Баланс: ${self.balances[name]})"

    def register_goose(self, goose_type: str = "0", name: str = "---1", honk_volume: int = -1) -> str | None:
        """Регистрация гусей"""
        if self.names:
            self.steps_count += 1

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
            print("  + Гусь")

            return msg

    def player_dep(self) -> str | None:
        """
        Ставка случайного игрока: проверка, что такой есть, формирование случайной суммы фишек, шанс 90%, что ставка не залетит.
        """
        player = self.players.get_random_alive_player()
        if not isinstance(player, Player):
            pass
        else:
            self.steps_count += 1 # в каждом методе счетчик увеличивается только тогда, когда наступает момент точного выполнения события

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
                    print("  - Игрок")

                    return f"Игрок {player.name} поставил все свои фишки и проиграл. Вдруг за ним пришли два гуся с дубинами и увели его.."

                return f"Игрок {player.name} поставил ${dep.value} и ставка не залетела.."

    def goose_action(self) -> str | None:
        """Регистрация игроков"""
        if self.gooses and self.players:
            self.steps_count += 1

            goose = self.gooses.get_random_goose()
            return goose.action(self)
        else:
            pass

    def goose_group(self) -> str | None:
        """Формирование группы гусей для мощного удара по всем, сложение 2-х коллекций для практического использования __add__ у класса коллекции"""
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

                    print("  - Игрок")
                    del self.balances[victim.name]
                    self.players.remove(victim)

            if amount > 0:
                random_goose = self.gooses.get_random_goose()
                self.gooses_income[random_goose.name] += amount

                msg += f" Не выжило: {killed_players} игрок(-ов). Гусь {random_goose.name} забрал с трупов {amount}.."

            return msg

    def panic_action(self) -> str | None:
        """Паника у случайного игрока при виде гуся. Он безвозвратно убегает и оставляет фишки на столе"""
        player = self.players.get_random_alive_player()
        goose = self.gooses.get_random_goose()
        if not isinstance(player, Player) or not isinstance(goose, Goose):
            pass
        else:
            self.steps_count += 1

            msg = f"Игрок {player.name} запаниковал при виде агрессивно настроенного гуся {goose.name} и убежал в страхе из казино.."
            amount = self.balances[player.name]

            ### ИСПРАВЛЕНИЕ 2 - правильное условие
            if amount > 0:
                self.gooses_income[goose.name] += amount

                print("  - Игрок")
                del self.balances[player.name]
                self.players.remove(player)

                msg += f"Гусь {goose.name} забрал со стола оставленные игроком ${amount}"

            return msg

    def healing_action(self) -> str | None:
        """Случайный игрок может найти энергетик под столом и увеличить свое здоровье немного"""
        player = self.players.get_random_alive_player()
        if not isinstance(player, Player):
            pass
        else:
            self.steps_count += 1

            heal = randint(10, 30)
            previous_hp = player.hp
            player.hp += heal
            print(f"  HP игрока {player.name}: {previous_hp} -> {player.hp}")

            return f"Игрок {player.name} нашел недопитый энергетик под столом и выпил его. HP игрока увеличилось на {heal}"

    def step(self) -> None:
        """Метод шага, выбирается случайное событие, некоторые я несколько раз продублировал для баланса, чтобы чаще выполнялись обычные вещи"""
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

        try:
            result = random_action()
            print("[ИЗМЕНЕНИЯ ПОСЛЕ СОБЫТИЯ]")
            print()
            print(f"[СОБЫТИЕ] {result} [СОБЫТИЕ]")

        ### ИСПРАВЛЕНИЕ 4 - перехват слишĸом общего исĸлючения
        except Exception as e:
            print(f"[ОШИБКА] {type(e).__name__}: {e}")


def run_simulation(steps: int = 20, seed: int | None = None) -> None:
    """Симуляция: если не задан сид, то он случайный. В начале симуляции уже зареганы немного сущностей. Потом в цикле выполняются шаги, пока счетчик не остановит."""
    if seed is not None:
        random.seed(seed)

    casino = Casino()

    casino.register_player("Саня", 100)
    casino.register_player("Вован", 220)
    casino.register_player("zxc_иван", 320)
    casino.register_player("Иоанн", 65)

    casino.register_goose("war", "Васян", 10)
    casino.register_goose("honk", "Клык", 5)

    casino.steps_count -= 6 # вернуть счетчик шагов после инициализации к 0

    ### ИСПРАВЛЕНИЕ 1 - правильные границы цикла
    while casino.steps_count < steps:
        print()
        print(f"══════════════════════════════ [ШАГ {casino.steps_count + 1}] ════════════════════════════════════")
        casino.step()
        print(f"══════════════════════════════ [ШАГ {casino.steps_count}] ════════════════════════════════════")

    print()