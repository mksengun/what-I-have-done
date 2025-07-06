"""Tests for Git parser functionality."""

from unittest.mock import MagicMock, patch

import pytest

from src.git_analyzer.core.git_parser import get_git_logs


@patch("subprocess.run")
def test_get_git_logs_success(mock_subprocess_run):
    """Test successful Git log retrieval."""
    mock_subprocess_run.return_value = MagicMock(
        stdout="2024-01-01 12:00:00|Initial commit\n2024-01-02 15:30:00|Add feature X",
        stderr="",
        returncode=0,
    )

    result = get_git_logs("1.month")

    assert (
        result
        == "2024-01-01 12:00:00|Initial commit\n2024-01-02 15:30:00|Add feature X"
    )
    mock_subprocess_run.assert_called_once()

    # Check that the correct git command was constructed
    call_args = mock_subprocess_run.call_args[0][0]
    assert 'git log --since="1.month"' in call_args
    assert "--walk-reflogs --all" in call_args
    assert '--pretty="format:%ad|%s"' in call_args


@patch("subprocess.run")
def test_get_git_logs_failure(mock_subprocess_run):
    """Test Git log retrieval failure."""
    mock_subprocess_run.return_value = MagicMock(
        stdout="", stderr="fatal: not a git repository", returncode=1
    )

    with pytest.raises(
        RuntimeError, match="Git command failed: fatal: not a git repository"
    ):
        get_git_logs("1.month")

    mock_subprocess_run.assert_called_once()


@patch("subprocess.run")
def test_get_git_logs_empty_result(mock_subprocess_run):
    """Test Git log retrieval with empty result."""
    mock_subprocess_run.return_value = MagicMock(stdout="", stderr="", returncode=0)

    result = get_git_logs("1.month")

    assert result == ""
    mock_subprocess_run.assert_called_once()


@patch("subprocess.run")
def test_get_git_logs_different_time_periods(mock_subprocess_run):
    """Test Git log retrieval with different time periods."""
    mock_subprocess_run.return_value = MagicMock(
        stdout="mock logs", stderr="", returncode=0
    )

    # Test different time periods
    test_periods = ["1.month", "2.weeks", "1.year", "7.days"]

    for period in test_periods:
        get_git_logs(period)

        # Check that the correct period was used in the command
        call_args = mock_subprocess_run.call_args[0][0]
        assert f'git log --since="{period}"' in call_args
