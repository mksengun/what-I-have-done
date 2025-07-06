"""Monthly report generation command."""

import os
from typing import Optional

import typer
from rich.console import Console

from ..core.analyzer import get_report_from_openai
from ..core.git_parser import get_git_logs

console = Console()


def generate_monthly_report(
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

    # Get API key from argument or environment
    openai_api_key = api_key or os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise typer.Exit(
            "OpenAI API key must be provided via --api-key or environment "
            "variable OPENAI_API_KEY"
        )

    console.print("🔍 Fetching Git logs...")
    git_logs = get_git_logs(since)

    console.print("📡 Sending logs to OpenAI...")
    report = get_report_from_openai(git_logs, openai_api_key)

    console.print("\n📊 Your Monthly Development Report:\n")
    console.print(report)
