"""
cli.py
------
Click-based CLI entrypoint for git-sage.

Commands
--------
  git-sage review          Run a review of staged changes (interactive)
  git-sage review --hook   Run a review triggered by the pre-push hook
  git-sage install         Install the pre-push hook in the current repo
  git-sage uninstall       Remove the pre-push hook
  git-sage status          Show tool version, hook status, and Ollama availability
  git-sage models          List locally available Ollama models
"""

import sys
import click

from git_sage import __version__
from git_sage import diff as diff_mod
from git_sage import hook as hook_mod
from git_sage import ollama as ollama_mod
from git_sage import output
from git_sage.prompt import build_messages
from git_sage.parser import parse, Verdict


# ---------------------------------------------------------------------------
# Root group
# ---------------------------------------------------------------------------

@click.group()
@click.version_option(__version__, prog_name="git-sage")
def main() -> None:
    """git-sage — local AI code review for your git workflow."""


# ---------------------------------------------------------------------------
# review
# ---------------------------------------------------------------------------

@main.command()
@click.option(
    "--model", "-m",
    default=ollama_mod.DEFAULT_MODEL,
    show_default=True,
    help="Ollama model to use for review.",
)
@click.option(
    "--host",
    default=ollama_mod.DEFAULT_HOST,
    show_default=True,
    help="Ollama server URL.",
)
@click.option(
    "--context", "-c",
    default=None,
    help='Optional note about this change, e.g. "Adds OAuth login".',
)
@click.option(
    "--hook",
    is_flag=True,
    hidden=True,
    help="Internal flag: invoked from the pre-push hook.",
)
@click.option(
    "--diff-mode",
    type=click.Choice(["staged", "head", "branch"]),
    default="staged",
    show_default=True,
    help="Which diff to review.",
)
@click.option(
    "--base",
    default="main",
    show_default=True,
    help="Base branch for --diff-mode=branch.",
)
@click.option(
    "--force", "-f",
    is_flag=True,
    help="Do not abort the push even if the verdict is REVISE (hook mode only).",
)
def review(model, host, context, hook, diff_mode, base, force) -> None:
    """Review staged (or recent) changes with a local AI model."""

    # 1. Check Ollama is running
    if not ollama_mod.is_available(host):
        output.print_error(
            f"Ollama is not running at {host}.\n"
            "  Start it with:  ollama serve\n"
            f"  Then pull a model:  ollama pull {ollama_mod.DEFAULT_MODEL}"
        )
        sys.exit(1)

    # 2. Extract the diff
    try:
        if diff_mode == "staged":
            diff = diff_mod.get_staged_diff()
        elif diff_mode == "head":
            diff = diff_mod.get_head_diff()
        else:
            diff = diff_mod.get_branch_diff(base)
    except RuntimeError as exc:
        output.print_error(str(exc))
        sys.exit(1)

    if not diff.raw.strip():
        output.print_warning("No changes found to review.")
        sys.exit(0)

    output.print_diff_stats(diff)

    # 3. Build prompt and call Ollama
    messages = build_messages(diff, context)

    try:
        with output.thinking_spinner(f"Reviewing with {model}…"):
            raw_response = ollama_mod.chat(messages, model=model, host=host)
    except ollama_mod.OllamaError as exc:
        output.print_error(f"Ollama error: {exc}")
        sys.exit(1)

    # 4. Parse and render
    result = parse(raw_response)
    output.print_review(result)

    # 5. Hook mode: non-zero exit aborts the push
    if hook and result.verdict == Verdict.REVISE and not force:
        click.echo(
            "  Push aborted by git-sage. Fix the issues above, or run:\n"
            "    git push --no-verify   to bypass the hook.\n"
        )
        sys.exit(1)


# ---------------------------------------------------------------------------
# install
# ---------------------------------------------------------------------------

@main.command()
def install() -> None:
    """Install the git-sage pre-push hook in the current repository."""
    try:
        hook_path = hook_mod.install()
        output.print_success(f"Hook installed at {hook_path}")
        click.echo("  git-sage will now review your changes before every push.\n")
    except RuntimeError as exc:
        output.print_error(str(exc))
        sys.exit(1)


# ---------------------------------------------------------------------------
# uninstall
# ---------------------------------------------------------------------------

@main.command()
def uninstall() -> None:
    """Remove the git-sage pre-push hook from the current repository."""
    try:
        removed = hook_mod.uninstall()
        if removed:
            output.print_success("Hook removed.")
        else:
            output.print_warning("No git-sage hook found in this repository.")
    except RuntimeError as exc:
        output.print_error(str(exc))
        sys.exit(1)


# ---------------------------------------------------------------------------
# status
# ---------------------------------------------------------------------------

@main.command()
@click.option("--host", default=ollama_mod.DEFAULT_HOST, show_default=True)
def status(host) -> None:
    """Show the current status of git-sage, the hook, and Ollama."""
    click.echo(f"\n  git-sage  v{__version__}\n")

    # Ollama
    if ollama_mod.is_available(host):
        click.echo(f"  [✓]  Ollama running at {host}")
        models = ollama_mod.list_models(host)
        if models:
            click.echo(f"       Models: {', '.join(models)}")
    else:
        click.echo(f"  [✗]  Ollama not reachable at {host}")
        click.echo( "       Start with:  ollama serve")

    # Hook
    if hook_mod.is_installed():
        click.echo("  [✓]  pre-push hook installed")
    else:
        click.echo("  [ ]  pre-push hook not installed")
        click.echo("       Run:  git-sage install")

    click.echo()


# ---------------------------------------------------------------------------
# models
# ---------------------------------------------------------------------------

@main.command()
@click.option("--host", default=ollama_mod.DEFAULT_HOST, show_default=True)
def models(host) -> None:
    """List locally available Ollama models."""
    if not ollama_mod.is_available(host):
        output.print_error(f"Ollama is not running at {host}.")
        sys.exit(1)

    model_list = ollama_mod.list_models(host)
    if not model_list:
        click.echo("\n  No models found. Pull one with:\n")
        click.echo(f"    ollama pull {ollama_mod.DEFAULT_MODEL}\n")
    else:
        click.echo(f"\n  Available models ({len(model_list)}):\n")
        for m in model_list:
            marker = "  ●" if m.startswith("qwen2.5-coder") else "  ○"
            click.echo(f"{marker}  {m}")
        click.echo()