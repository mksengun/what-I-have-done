"""Pytest configuration and fixtures."""

import pytest
from typer.testing import CliRunner


@pytest.fixture
def runner():
    """Create a CLI runner for testing."""
    return CliRunner()


@pytest.fixture
def mock_git_logs():
    """Mock Git log output."""
    return "2024-01-01 12:00:00|Initial commit\n2024-01-02 15:30:00|Add feature X"


@pytest.fixture
def mock_openai_response():
    """Mock OpenAI API response."""
    return {"choices": [{"message": {"content": "Test Report"}}]}
