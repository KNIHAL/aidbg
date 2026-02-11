# aidbg/init.py

import json
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt

console = Console()


def run_init(local: bool = False):
    try:
        console.clear()

        console.print(
            Panel(
                "[bold cyan]aidbg[/bold cyan]\n"
                "[dim]Local-first AI debugging tool[/dim]\n\n"
                "Let's set up your AI debugger.\n"
                "This takes less than a minute.",
                border_style="cyan",
                padding=(1, 4),
            )
        )

        console.print("\n[bold]Select how you want aidbg to think:[/bold]\n")

        console.print("  [cyan]1)[/cyan] Groq     [dim]Fast, low-latency (recommended)[/dim]")
        console.print("  [cyan]2)[/cyan] OpenAI   [dim]Strong reasoning[/dim]")
        console.print("  [cyan]3)[/cyan] Ollama   [dim]Local / offline[/dim]")

        choice = IntPrompt.ask(
            "\nYour choice",
            choices=["1", "2", "3"],
            show_choices=False,
        )

        provider = {1: "groq", 2: "openai", 3: "ollama"}[choice]
        config = {"provider": provider}

        console.print()

        if provider in ("groq", "openai"):
            config["model"] = Prompt.ask("Model name")
            config["api_key"] = Prompt.ask("API key", password=True)
        else:
            config["model"] = Prompt.ask("Local model name")

        config_dir = Path.cwd() / ".aidbg" if local else Path.home() / ".aidbg"
        config_dir.mkdir(parents=True, exist_ok=True)

        config_path = config_dir / "config.json"
        config_path.write_text(json.dumps(config, indent=2))

        scope = "Project" if local else "Global"

        console.print()
        console.print(
            Panel(
                f"[green]✓ Setup complete[/green]\n\n"
                f"[bold]{scope} configuration saved[/bold]\n"
                f"[dim]{config_path}[/dim]",
                border_style="green",
                padding=(1, 4),
            )
        )

    except KeyboardInterrupt:
        console.print("\n[dim]Setup cancelled.[/dim]")
