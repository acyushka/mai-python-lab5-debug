import typer
from src.services.casino import run_simulation

app = typer.Typer()

@app.command()
def run(
    steps: int = typer.Option(20, "--steps", "-s", help="Количество шагов симуляции"),
    seed: int = typer.Option(None, "--seed", help="Сид псевдослучайности")
):
    run_simulation(steps, seed)

@app.command()
def demo():
    run_simulation(steps=5, seed=141)

if __name__ == "__main__":
    app()
