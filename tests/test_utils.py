"""Tests for utility functions."""

from unittest.mock import patch

import pytest

from src.git_analyzer.utils.helpers import get_api_key, validate_time_period


@patch("os.getenv")
def test_get_api_key_from_argument(mock_getenv):
    """Test getting API key from command line argument."""
    mock_getenv.return_value = "env_key"
    
    result = get_api_key("arg_key")
    
    assert result == "arg_key"
    mock_getenv.assert_not_called()


@patch("os.getenv")
def test_get_api_key_from_environment(mock_getenv):
    """Test getting API key from environment variable."""
    mock_getenv.return_value = "env_key"
    
    result = get_api_key(None)
    
    assert result == "env_key"
    mock_getenv.assert_called_once_with("OPENAI_API_KEY")


@patch("os.getenv")
def test_get_api_key_none(mock_getenv):
    """Test getting API key when none available."""
    mock_getenv.return_value = None
    
    result = get_api_key(None)
    
    assert result is None
    mock_getenv.assert_called_once_with("OPENAI_API_KEY")


def test_validate_time_period_valid():
    """Test validation of valid time periods."""
    valid_periods = [
        "1.month",
        "2.weeks", 
        "7.days",
        "1.year",
        "30 days",
        "12 months",
        "1 week"
    ]
    
    for period in valid_periods:
        assert validate_time_period(period), f"Period '{period}' should be valid"


def test_validate_time_period_invalid():
    """Test validation of invalid time periods."""
    invalid_periods = [
        "month",           # Missing number
        "1",              # Missing unit
        "1.invalid",      # Invalid unit
        "abc.days",       # Invalid number
        "1.2.3.days",     # Too many parts
        "",               # Empty string
        "1 2 days",       # Too many parts
    ]
    
    for period in invalid_periods:
        assert not validate_time_period(period), f"Period '{period}' should be invalid"


def test_validate_time_period_case_insensitive():
    """Test that validation is case insensitive."""
    assert validate_time_period("1.MONTH")
    assert validate_time_period("2.Weeks")
    assert validate_time_period("7.DAYS")