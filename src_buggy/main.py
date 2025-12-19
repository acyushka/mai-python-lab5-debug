from typer import Typer, Option
from src_buggy.services.casino import run_simulation

app = Typer()

@app.command()
def run(
    steps: int = Option(20, "--steps", "-s", help="Количество шагов симуляции"),
    seed: int = Option(None, "--seed", help="Сид псевдослучайности")
) -> None:
    """Главная команда для вывода симуляции с заданными параметрами"""
    run_simulation(steps, seed)

@app.command()
def demo() -> None:
    """Команда, уже готовая, для демонстрации"""
    run_simulation(steps=5, seed=141)

if __name__ == "__main__":
    app()
