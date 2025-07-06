"""Tests for CLI functionality."""

from unittest.mock import patch

from typer.testing import CliRunner

from src.git_analyzer.cli import app


def test_cli_help():
    """Test CLI help output."""
    runner = CliRunner()
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "A command-line tool that fetches your Git commit history" in result.output
    assert "OpenAI API key" in result.output
    assert "since" in result.output


def test_cli_missing_required_params():
    """Test CLI with missing required parameters."""
    runner = CliRunner()
    result = runner.invoke(app, [])
    assert result.exit_code != 0
    assert "Missing option" in result.output


@patch("src.git_analyzer.commands.monthly_report.get_git_logs")
@patch("src.git_analyzer.commands.monthly_report.get_report_from_openai")
@patch("os.getenv")
def test_cli_with_env_api_key(mock_getenv, mock_get_report, mock_get_logs):
    """Test CLI with API key from environment."""
    mock_getenv.return_value = "test-api-key"
    mock_get_logs.return_value = "mock git logs"
    mock_get_report.return_value = "mock report"

    runner = CliRunner()
    result = runner.invoke(app, ["--since", "1.month"])

    assert result.exit_code == 0
    assert "🔍 Fetching Git logs..." in result.output
    assert "📡 Sending logs to OpenAI..." in result.output
    assert "📊 Your Monthly Development Report:" in result.output
    mock_get_logs.assert_called_once_with("1.month")
    mock_get_report.assert_called_once_with("mock git logs", "test-api-key")


@patch("src.git_analyzer.commands.monthly_report.get_git_logs")
@patch("src.git_analyzer.commands.monthly_report.get_report_from_openai")
@patch("os.getenv")
def test_cli_with_arg_api_key(mock_getenv, mock_get_report, mock_get_logs):
    """Test CLI with API key from command line argument."""
    mock_getenv.return_value = None
    mock_get_logs.return_value = "mock git logs"
    mock_get_report.return_value = "mock report"

    runner = CliRunner()
    result = runner.invoke(app, ["--since", "1.month", "--api-key", "arg-api-key"])

    assert result.exit_code == 0
    assert "🔍 Fetching Git logs..." in result.output
    assert "📡 Sending logs to OpenAI..." in result.output
    assert "📊 Your Monthly Development Report:" in result.output
    mock_get_logs.assert_called_once_with("1.month")
    mock_get_report.assert_called_once_with("mock git logs", "arg-api-key")


@patch("os.getenv")
def test_cli_no_api_key(mock_getenv):
    """Test CLI without API key."""
    mock_getenv.return_value = None

    runner = CliRunner()
    result = runner.invoke(app, ["--since", "1.month"])

    assert result.exit_code == 1
    assert "OpenAI API key must be provided" in result.output
