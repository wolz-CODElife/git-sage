"""
output.py
---------
Terminal output renderer using the `rich` library.

Rich gives us coloured panels, icons, and clean formatting with zero
configuration — ideal for a CLI tool that developers will stare at
every time they push code.
"""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
from rich.text import Text
from rich.spinner import Spinner
from rich.live import Live

from git_sage.parser import ReviewResult, Verdict
from git_sage.diff import DiffResult

console = Console()


# ---------------------------------------------------------------------------
# Public render functions
# ---------------------------------------------------------------------------

def print_diff_stats(diff: DiffResult) -> None:
    """Print a one-line summary of what's staged."""
    stats = Text()
    stats.append("  Staged: ", style="dim")
    stats.append(f"{diff.file_count} file(s)", style="bold")
    stats.append("  ", style="dim")
    stats.append(f"+{diff.additions}", style="bold green")
    stats.append(" / ", style="dim")
    stats.append(f"-{diff.deletions}", style="bold red")
    console.print(stats)


def print_review(result: ReviewResult) -> None:
    """Render the full review result to the terminal."""
    _print_summary(result)
    _print_issues(result)
    _print_suggestions(result)
    _print_verdict(result)


def print_error(message: str) -> None:
    console.print(f"\n[bold red]✗[/bold red]  {message}\n")


def print_success(message: str) -> None:
    console.print(f"\n[bold green]✓[/bold green]  {message}\n")


def print_warning(message: str) -> None:
    console.print(f"\n[bold yellow]⚠[/bold yellow]  {message}\n")


def thinking_spinner(label: str = "Reviewing with local AI…") -> Live:
    """
    Returns a Rich Live context manager showing a spinner.

    Usage:
        with thinking_spinner():
            result = ollama.chat(...)
    """
    spinner = Spinner("dots", text=f"[dim]{label}[/dim]")
    return Live(spinner, console=console, refresh_per_second=10, transient=True)


# ---------------------------------------------------------------------------
# Private section renderers
# ---------------------------------------------------------------------------

def _print_summary(result: ReviewResult) -> None:
    if not result.summary:
        return
    panel = Panel(
        f"[dim]{result.summary}[/dim]",
        title="[bold]Summary[/bold]",
        border_style="bright_black",
        padding=(0, 1),
    )
    console.print(panel)


def _print_issues(result: ReviewResult) -> None:
    if not result.issues:
        console.print("\n[bold green]  No issues found.[/bold green]\n")
        return

    console.print(f"\n[bold red]  Issues[/bold red]  ({len(result.issues)} found)\n")
    for i, issue in enumerate(result.issues, 1):
        console.print(f"  [red]●[/red]  [dim]{i}.[/dim] {issue}")
    console.print()


def _print_suggestions(result: ReviewResult) -> None:
    if not result.suggestions:
        return

    console.print(f"[bold yellow]  Suggestions[/bold yellow]  ({len(result.suggestions)})\n")
    for i, sug in enumerate(result.suggestions, 1):
        console.print(f"  [yellow]◆[/yellow]  [dim]{i}.[/dim] {sug}")
    console.print()


def _print_verdict(result: ReviewResult) -> None:
    if result.verdict == Verdict.APPROVE:
        panel = Panel(
            "[bold green]  ✓  APPROVE[/bold green]\n[dim]  Ready to push.[/dim]",
            border_style="green",
            padding=(0, 1),
        )
    elif result.verdict == Verdict.REVISE:
        panel = Panel(
            "[bold red]  ✗  REVISE[/bold red]\n[dim]  Address the issues above before pushing.[/dim]",
            border_style="red",
            padding=(0, 1),
        )
    else:
        panel = Panel(
            "[bold yellow]  ?  UNKNOWN[/bold yellow]\n[dim]  The model didn't return a clear verdict.[/dim]",
            border_style="yellow",
            padding=(0, 1),
        )
    console.print(panel)
    console.print()