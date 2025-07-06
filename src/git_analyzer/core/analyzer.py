"""Report generation and analysis functionality."""

import requests


def get_report_from_openai(git_logs: str, api_key: str) -> str:
    """Send logs and prompt to OpenAI for analysis.

    Args:
        git_logs: Git log output to analyze
        api_key: OpenAI API key

    Returns:
        Generated report from OpenAI

    Raises:
        RuntimeError: If OpenAI API call fails
    """
    prompt = (
        "Below is my Git commit log from the last period:\n\n"
        + git_logs
        + (
            "\n\nPlease generate a monthly development report formatted as a "
            "retro, three-dimensional terminal UI. "
        )
        + (
            "Use ASCII box-drawing characters to create borders and boxes, "
            "include relevant emojis for each section, "
        )
        + (
            "and present the output in a visually appealing, old-school style "
            "as if rendered on a classic text-based terminal.\n\n"
        )
        + "Report outline:\n"
        + "  • Which feature took how many days?\n"
        + "  • What is the most refactored feature?\n"
        + "  • What is causing the most problems?\n"
        + "  • What have I spent my time on?\n"
    )

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    data = {
        "model": "gpt-4o",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 2000,
        "temperature": 0.3,
    }

    resp = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=data,
    )
    if resp.status_code != 200:
        raise RuntimeError(f"OpenAI API error: {resp.status_code} {resp.text}")
    return resp.json()["choices"][0]["message"]["content"]
