# aidbg/cli.py
import typer
from aidbg.runner import run_program
from aidbg.init import run_init

app = typer.Typer()

@app.command()
def init(local: bool = typer.Option(False, "--local", help="Save config to project")):
    run_init(local=local)

@app.command()
def run(script: str = typer.Argument(...)):
    run_program(script)

if __name__ == "__main__":
    app()
