"""
diff.py
-------
Extracts diffs from git using subprocess.

Supports two modes:
  - staged:  changes added with `git add` (used during pre-push / manual review)
  - head:    diff of the last commit vs its parent (useful for post-commit review)
"""

import subprocess
from dataclasses import dataclass


@dataclass
class DiffResult:
    raw: str           # full unified diff text
    file_count: int    # number of changed files
    additions: int     # total lines added
    deletions: int     # total lines removed
    files: list[str]   # list of changed file paths


def get_staged_diff() -> DiffResult:
    """Return the diff of all staged changes (git diff --cached)."""
    return _run_diff(["git", "diff", "--cached"])


def get_head_diff() -> DiffResult:
    """Return the diff of the last commit vs its parent (git diff HEAD~1 HEAD)."""
    return _run_diff(["git", "diff", "HEAD~1", "HEAD"])


def get_branch_diff(base: str = "main") -> DiffResult:
    """Return the diff of the current branch vs a base branch."""
    return _run_diff(["git", "diff", f"{base}...HEAD"])


def _run_diff(cmd: list[str]) -> DiffResult:
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"git diff failed:\n{result.stderr.strip()}"
        )

    raw = result.stdout

    if not raw.strip():
        return DiffResult(raw="", file_count=0, additions=0, deletions=0, files=[])

    additions = sum(1 for line in raw.splitlines() if line.startswith("+") and not line.startswith("+++"))
    deletions = sum(1 for line in raw.splitlines() if line.startswith("-") and not line.startswith("---"))
    files = _extract_files(raw)

    return DiffResult(
        raw=raw,
        file_count=len(files),
        additions=additions,
        deletions=deletions,
        files=files,
    )


def _extract_files(diff_text: str) -> list[str]:
    files = []
    for line in diff_text.splitlines():
        if line.startswith("+++ b/"):
            path = line.removeprefix("+++ b/")
            if path not in files:
                files.append(path)
    return files