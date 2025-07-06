"""Main CLI entry point for git-analyzer."""

from typing import Optional

import typer

from .commands.monthly_report import generate_monthly_report

# Create a simple app that directly handles the main command
app = typer.Typer(
    name="git-analyzer",
    help=(
        "A command-line tool that fetches your Git commit history and generates "
        "an AI-powered monthly development report"
    ),
    add_completion=False,
)


@app.callback(invoke_without_command=True)
def main(
    since: str = typer.Option(
        ..., "-s", "--since", help="Git log since date (e.g., '1.month', '2.weeks')"
    ),
    api_key: Optional[str] = typer.Option(
        None,
        "-k",
        "--api-key",
        help="OpenAI API key (overrides environment variable OPENAI_API_KEY)",
    ),
) -> None:
    """Generate a retro-style monthly Git development report via OpenAI."""
    generate_monthly_report(since=since, api_key=api_key)


if __name__ == "__main__":
    app()
