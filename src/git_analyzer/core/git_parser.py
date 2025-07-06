"""Git log parsing functionality."""

import subprocess


def get_git_logs(since: str) -> str:
    """Execute Git command to retrieve commit logs.

    Args:
        since: Git log since date (e.g., "1.month", "2.weeks")

    Returns:
        Git log output as string

    Raises:
        RuntimeError: If git command fails
    """
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
