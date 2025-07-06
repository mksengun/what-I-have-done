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
    parser.add_argument(
        '-s', '--since',
        help='Git log since date (e.g., "1.month", "2.weeks", "yesterday", "this-week")',
        required=True
    )
    parser.add_argument(
        '-f', '--format',
        help='Output format',
        choices=['terminal', 'markdown', 'json'],
        default='terminal'
    )
    parser.add_argument(
        '-t', '--template',
        help='Report template/focus',
        choices=['developer', 'manager', 'technical-debt', 'productivity'],
        default='developer'
    )
    parser.add_argument(
        '--exclude-merges',
        help='Exclude merge commits from analysis',
        action='store_true'
    )
    return parser.parse_args()

# Execute Git command
def get_git_logs(since, exclude_merges=False):
    # Handle time period presets
    time_presets = {
        'yesterday': '1.day',
        'this-week': '1.week',
        'last-sprint': '2.weeks',
        'this-month': '1.month'
    }
    
    # Convert preset to git format if needed
    git_since = time_presets.get(since, since)
    
    # Build git command
    git_cmd = (
        f'git log --since="{git_since}" --walk-reflogs --all '
        '--author="$(git config user.email)" '
        '--pretty="format:%ad|%s|%H" '
        '--date=format:"%Y-%m-%d %H:%M:%S"'
    )
    
    # Add exclude merges option
    if exclude_merges:
        git_cmd += ' --no-merges'
    
    result = subprocess.run(git_cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Git command failed: {result.stderr.strip()}")
    return result.stdout

# Generate AI prompt based on template
def generate_prompt(git_logs, template, output_format):
    base_logs = f"Below is my Git commit log from the last period:\n\n{git_logs}\n\n"
    
    template_prompts = {
        'developer': {
            'focus': "Please generate a development report focusing on technical aspects.",
            'sections': [
                "• Which feature took how many days?",
                "• What is the most refactored feature?",
                "• What is causing the most problems?",
                "• What have I spent my time on?",
                "• Code quality patterns and improvements"
            ]
        },
        'manager': {
            'focus': "Please generate a management-focused report highlighting productivity and deliverables.",
            'sections': [
                "• Key deliverables and milestones achieved",
                "• Time allocation across different projects/features",
                "• Productivity patterns and peak work periods",
                "• Potential blockers or areas needing attention",
                "• Team collaboration and code review activity"
            ]
        },
        'technical-debt': {
            'focus': "Please generate a technical debt analysis report.",
            'sections': [
                "• Most frequently modified files (potential hotspots)",
                "• Refactoring patterns and debt reduction efforts",
                "• Areas requiring maintenance or cleanup",
                "• Technical improvements and code quality enhancements",
                "• Dependencies and architectural changes"
            ]
        },
        'productivity': {
            'focus': "Please generate a productivity analysis report.",
            'sections': [
                "• Daily/weekly activity patterns",
                "• Most productive time periods",
                "• Commit frequency and consistency",
                "• Focus areas and context switching",
                "• Efficiency trends and improvements"
            ]
        }
    }
    
    template_config = template_prompts.get(template, template_prompts['developer'])
    sections = "\n".join(template_config['sections'])
    
    # Format instructions based on output format
    if output_format == 'terminal':
        format_instruction = ("formatted as a retro, three-dimensional terminal UI. "
                            "Use ASCII box-drawing characters to create borders and boxes, include relevant emojis for each section, "
                            "and present the output in a visually appealing, old-school style as if rendered on a classic text-based terminal.")
    elif output_format == 'markdown':
        format_instruction = ("formatted as clean Markdown with headers, bullet points, and appropriate formatting. "
                            "Use emojis for section headers and maintain good readability.")
    elif output_format == 'json':
        format_instruction = ("formatted as valid JSON with structured data. "
                            "Include sections as keys and provide detailed analysis in arrays or objects as appropriate.")
    
    return f"{base_logs}{template_config['focus']} {format_instruction}\n\nReport outline:\n{sections}"

# Send logs and prompt to OpenAI
def get_report_from_openai(git_logs, api_key, template='developer', output_format='terminal'):
    prompt = generate_prompt(git_logs, template, output_format)

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

# Analyze git logs for enhanced insights
def analyze_git_logs(git_logs):
    """Analyze git logs to extract additional insights"""
    if not git_logs.strip():
        return {}
    
    lines = git_logs.strip().split('\n')
    commits = []
    
    for line in lines:
        if '|' in line:
            parts = line.split('|')
            if len(parts) >= 2:
                commits.append({
                    'date': parts[0],
                    'message': parts[1],
                    'hash': parts[2] if len(parts) > 2 else ''
                })
    
    analysis = {
        'total_commits': len(commits),
        'date_range': {
            'start': commits[-1]['date'] if commits else '',
            'end': commits[0]['date'] if commits else ''
        },
        'commit_messages': [c['message'] for c in commits]
    }
    
    return analysis

# Main execution
def main():
    args = parse_args()
    api_key = args.api_key or os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise RuntimeError('OpenAI API key must be provided via --api-key or environment variable OPENAI_API_KEY')

    print('🔍 Fetching Git logs...')
    git_logs = get_git_logs(args.since, args.exclude_merges)
    
    # Analyze logs for additional insights
    analysis = analyze_git_logs(git_logs)
    
    # Add analysis summary to logs if we have data
    if analysis['total_commits'] > 0:
        enhanced_logs = f"{git_logs}\n\n--- Analysis Summary ---\n"
        enhanced_logs += f"Total commits: {analysis['total_commits']}\n"
        enhanced_logs += f"Date range: {analysis['date_range']['start']} to {analysis['date_range']['end']}\n"
    else:
        enhanced_logs = git_logs
        print("⚠️  No commits found for the specified period.")

    print('📡 Sending logs to OpenAI...')
    report = get_report_from_openai(enhanced_logs, api_key, args.template, args.format)

    # Display report with appropriate header
    format_headers = {
        'terminal': '\n📊 Your Development Report:\n',
        'markdown': '\n📝 Development Report (Markdown):\n',
        'json': '\n🔢 Development Report (JSON):\n'
    }
    
    print(format_headers.get(args.format, format_headers['terminal']))
    print(report)

if __name__ == '__main__':
    main()
