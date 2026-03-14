"""
hook.py
-------
Installs and removes the git pre-push hook that triggers git-sage automatically.

The hook is a small shell script written to .git/hooks/pre-push. When git push
is run, git executes this script first. If the script exits with a non-zero
code, the push is aborted.

This is intentionally simple — the hook just calls `git-sage review --hook`
which handles all the logic in Python.
"""

import os
import stat
import subprocess
from pathlib import Path


HOOK_MARKER = "# git-sage managed hook"

HOOK_SCRIPT = """\
#!/usr/bin/env sh
{marker}
# This hook was installed by git-sage.
# Run: git-sage uninstall   to remove it.

git-sage review --hook
""".format(marker=HOOK_MARKER)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def install(repo_root: Path | None = None) -> Path:
    """
    Write the pre-push hook to the git repo's hooks directory.

    Parameters
    ----------
    repo_root:
        Path to the git repository root. Auto-detected if not provided.

    Returns
    -------
    Path to the installed hook file.

    Raises
    ------
    RuntimeError if we're not inside a git repository.
    """
    hooks_dir = _get_hooks_dir(repo_root)
    hook_path = hooks_dir / "pre-push"

    if hook_path.exists():
        existing = hook_path.read_text()
        if HOOK_MARKER in existing:
            # Already installed by us — overwrite silently (idempotent)
            pass
        else:
            raise RuntimeError(
                f"A pre-push hook already exists at {hook_path} and was not "
                "created by git-sage. Remove it manually before installing."
            )

    hook_path.write_text(HOOK_SCRIPT)
    # Make the hook executable (equivalent to chmod +x)
    hook_path.chmod(hook_path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    return hook_path


def uninstall(repo_root: Path | None = None) -> bool:
    """
    Remove the git-sage pre-push hook if it exists.

    Returns True if removed, False if no hook was found.
    """
    hooks_dir = _get_hooks_dir(repo_root)
    hook_path = hooks_dir / "pre-push"

    if not hook_path.exists():
        return False

    existing = hook_path.read_text()
    if HOOK_MARKER not in existing:
        raise RuntimeError(
            f"The hook at {hook_path} was not created by git-sage. "
            "Remove it manually."
        )

    hook_path.unlink()
    return True


def is_installed(repo_root: Path | None = None) -> bool:
    """Return True if the git-sage hook is currently installed."""
    try:
        hooks_dir = _get_hooks_dir(repo_root)
        hook_path = hooks_dir / "pre-push"
        return hook_path.exists() and HOOK_MARKER in hook_path.read_text()
    except RuntimeError:
        return False


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _get_hooks_dir(repo_root: Path | None) -> Path:
    if repo_root is None:
        repo_root = _find_repo_root()
    hooks_dir = repo_root / ".git" / "hooks"
    if not hooks_dir.exists():
        raise RuntimeError(f"No .git/hooks directory found at {hooks_dir}")
    return hooks_dir


def _find_repo_root() -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError("Not inside a git repository.")
    return Path(result.stdout.strip())