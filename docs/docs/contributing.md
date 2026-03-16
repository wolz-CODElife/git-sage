---
id: contributing
title: Contributing
sidebar_position: 6
---

# Contributing

`git-sage` is open source and welcome contributions. The codebase is small and well-structured; most contributions touch a single module. Whether you're fixing a bug, adding a feature, or improving the docs, this guide has everything you need to get started.

## Getting started

**1. Fork and clone the repo**

```bash
git clone https://github.com/your-username/git-sage
cd git-sage
```

**2. Set up the development environment**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
pip install pytest
```

**3. Run the tests**

```bash
pytest tests/ -v
```

All 17 tests should pass before you start making changes.

---

## Project structure

```
git_sage/
├── cli.py          CLI commands (Click)
├── diff.py         Git diff extraction
├── prompt.py       Prompt builder — edit this to change review behaviour
├── ollama.py       Ollama HTTP client
├── parser.py       LLM response parser
├── output.py       Terminal renderer (Rich)
└── hook.py         Git hook installer
tests/
├── test_diff.py
├── test_parser.py
└── test_prompt.py
docs/               Docusaurus documentation site
```

---

## Good first issues

These are self-contained improvements that don't require deep knowledge of the codebase:

### Add `--json` output flag

Add a `--json` flag to `git-sage review` that outputs the `ReviewResult` as JSON instead of the rich terminal output. Useful for CI pipelines.

```bash
git-sage review --json
# {"summary": "...", "issues": [...], "verdict": "REVISE"}
```

The `ReviewResult` dataclass in `parser.py` already has all the fields — it just needs a serialiser and a flag in `cli.py`.

### Add `--severity` filter

Add a `--severity` option to filter the issues shown:

```bash
git-sage review --severity high   # only show critical issues
```

This requires updating `SYSTEM_PROMPT` in `prompt.py` to ask the model to label each issue with a severity (`high`, `medium`, `low`), and updating `parser.py` to extract and store that label.

### Support multiple models as fallback

If the requested model isn't available locally, fall back to the next available model instead of exiting with an error.

### Add a `--watch` mode

A `--watch` flag that re-runs the review every time a staged file changes, using `watchfiles` or `polling`.

---

## Changing the review behaviour

The fastest way to extend `git-sage` is to edit the system prompt in `git_sage/prompt.py`. 

**Example: flag `print()` statements**

```python
# In SYSTEM_PROMPT, add to the Flag list:
- print() or console.log() calls left in non-test code paths.
```

**Example: focus only on security issues**

```python
# Replace the Flag list with:
- Focus exclusively on security issues: secrets, injection risks, \
  authentication flaws, insecure dependencies, and data exposure.
```

**Example: add support for a custom rule file**

Load rules from a `.git-sage.toml` file in the repo root and inject them into the prompt at review time.

---

## Adding a new command

Commands are defined in `git_sage/cli.py` using Click decorators:

```python
@main.command()
@click.option("--flag", default="value", help="Description.")
def my_command(flag):
    """One-line description shown in --help."""
    # implementation
```

After adding a command, add a test in `tests/` and update the docs in `docs/docs/usage.md`.

---

## Submitting a pull request

1. Create a branch: `git checkout -b feat/my-feature`
2. Make your changes
3. Run `pytest tests/ -v` — all tests must pass
4. Add or update tests for your change
5. Open a pull request against `master` with a clear description of what you changed and why

---

## Reporting bugs

Open an issue at [github.com/wolz-CODElife/git-sage/issues](https://github.com/wolz-CODElife/git-sage/issues) with:

- Your OS and Python version
- The command you ran
- The full error output
- What you expected to happen