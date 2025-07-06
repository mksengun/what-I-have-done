"""Tests for analyzer functionality."""

from unittest.mock import MagicMock, patch

import pytest

from src.git_analyzer.core.analyzer import get_report_from_openai


@patch("requests.post")
def test_get_report_from_openai_success(mock_requests_post):
    """Test successful OpenAI API call."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "choices": [{"message": {"content": "Test Report"}}]
    }
    mock_requests_post.return_value = mock_response

    result = get_report_from_openai("git logs", "test-api-key")

    assert result == "Test Report"
    mock_requests_post.assert_called_once()

    # Check API call parameters
    call_args = mock_requests_post.call_args
    assert call_args[1]["json"]["model"] == "gpt-4o"
    assert call_args[1]["json"]["max_tokens"] == 2000
    assert call_args[1]["json"]["temperature"] == 0.3
    assert "git logs" in call_args[1]["json"]["messages"][0]["content"]


@patch("requests.post")
def test_get_report_from_openai_failure(mock_requests_post):
    """Test OpenAI API call failure."""
    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_response.text = "Bad Request"
    mock_requests_post.return_value = mock_response

    with pytest.raises(RuntimeError, match="OpenAI API error: 400 Bad Request"):
        get_report_from_openai("git logs", "test-api-key")

    mock_requests_post.assert_called_once()


@patch("requests.post")
def test_get_report_from_openai_auth_error(mock_requests_post):
    """Test OpenAI API authentication error."""
    mock_response = MagicMock()
    mock_response.status_code = 401
    mock_response.text = "Unauthorized"
    mock_requests_post.return_value = mock_response

    with pytest.raises(RuntimeError, match="OpenAI API error: 401 Unauthorized"):
        get_report_from_openai("git logs", "invalid-api-key")

    mock_requests_post.assert_called_once()


@patch("requests.post")
def test_get_report_from_openai_prompt_construction(mock_requests_post):
    """Test that the prompt is constructed correctly."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "choices": [{"message": {"content": "Test Report"}}]
    }
    mock_requests_post.return_value = mock_response

    git_logs = "2024-01-01 12:00:00|Initial commit"
    get_report_from_openai(git_logs, "test-api-key")

    # Check that the prompt contains the expected elements
    call_args = mock_requests_post.call_args
    prompt = call_args[1]["json"]["messages"][0]["content"]

    assert "Below is my Git commit log" in prompt
    assert git_logs in prompt
    assert "Which feature took how many days?" in prompt
    assert "What is the most refactored feature?" in prompt
    assert "What is causing the most problems?" in prompt
    assert "What have I spent my time on?" in prompt


@patch("requests.post")
def test_get_report_from_openai_headers(mock_requests_post):
    """Test that the correct headers are sent."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "choices": [{"message": {"content": "Test Report"}}]
    }
    mock_requests_post.return_value = mock_response

    get_report_from_openai("git logs", "test-api-key")

    # Check headers
    call_args = mock_requests_post.call_args
    headers = call_args[1]["headers"]

    assert headers["Content-Type"] == "application/json"
    assert headers["Authorization"] == "Bearer test-api-key"
