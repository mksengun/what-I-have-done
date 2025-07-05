#!/usr/bin/env python3

import subprocess
import requests
import os
import argparse

# Parse command-line arguments
def parse_args():
    parser = argparse.ArgumentParser(
        description='Generate a retro-style monthly Git development report via OpenAI')
    parser.add_argument(
        '-k', '--api-key',
        help='OpenAI API key (overrides environment variable OPENAI_API_KEY)',
        required=False
    )
    return parser.parse_args()

# Execute Git command
def get_git_logs(since):
    git_cmd = (
        f'git log --since="{since}" --walk-reflogs --all '
        '--author="$(git config user.email)" '
        '--pretty="format:%ad|%s" '
        '--date=format:"%Y-%m-%d %H:%M:%S"'
    )
    result = subprocess.run(git_cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Git command failed: {result.stderr.strip()}")
    return result.stdout

# Send logs and prompt to OpenAI
def get_report_from_openai(git_logs, api_key):
    prompt = (
        "Below is my Git commit log from the last period:\n\n" +
        git_logs +
        "\n\nPlease generate a monthly development report formatted as a retro, three-dimensional terminal UI. "
        "Use ASCII box-drawing characters to create borders and boxes, include relevant emojis for each section, "
        "and present the output in a visually appealing, old-school style as if rendered on a classic text-based terminal.\n\n"
        "Report outline:\n"
        "  • Which feature took how many days?\n"
        "  • What is the most refactored feature?\n"
        "  • What is causing the most problems?\n"
        "  • What have I spent my time on?\n"
    )

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}',
    }
    data = {
        'model': 'gpt-4o',
        'messages': [{'role': 'user', 'content': prompt}],
        'max_tokens': 2000,
        'temperature': 0.3,
    }

    resp = requests.post(
        'https://api.openai.com/v1/chat/completions',
        headers=headers,
        json=data,
    )
    if resp.status_code != 200:
        raise RuntimeError(f"OpenAI API error: {resp.status_code} {resp.text}")
    return resp.json()['choices'][0]['message']['content']

# Main execution
def main():
    args = parse_args()
    api_key = args.api_key or os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise RuntimeError('OpenAI API key must be provided via --api-key or environment variable OPENAI_API_KEY')

    print('🔍 Fetching Git logs...')
    git_logs = get_git_logs(args.since)

    print('📡 Sending logs to OpenAI...')
    report = get_report_from_openai(git_logs, api_key)

    print('\n📊 Your Monthly Development Report:\n')
    print(report)

if __name__ == '__main__':
    main()
