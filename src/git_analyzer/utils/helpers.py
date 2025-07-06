"""Utility functions for git-analyzer."""

import os
from typing import Optional


def get_api_key(api_key_arg: Optional[str]) -> Optional[str]:
    """Get API key from argument or environment variable.
    
    Args:
        api_key_arg: API key from command line argument
        
    Returns:
        API key from argument or environment, None if not found
    """
    return api_key_arg or os.getenv("OPENAI_API_KEY")


def validate_time_period(since: str) -> bool:
    """Validate that the time period format is reasonable.
    
    Args:
        since: Time period string like "1.month", "2.weeks"
        
    Returns:
        True if format appears valid, False otherwise
    """
    # Basic validation - could be enhanced in the future
    valid_units = ["day", "days", "week", "weeks", "month", "months", "year", "years"]
    
    # Split on period or space
    parts = since.replace(".", " ").split()
    if len(parts) != 2:
        return False
        
    try:
        # Check if first part is a number
        float(parts[0])
        # Check if second part is a valid unit
        return parts[1].lower() in valid_units
    except ValueError:
        return False