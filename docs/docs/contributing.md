---
id: contributing
title: Contributing
sidebar_position: 6
---

# Contributing

`git-sage` is open source and welcomes contributions. The codebase is small and well-structured; most contributions touch a single module. Whether you're fixing a bug, adding a feature, or improving the docs, this guide has everything you need to get started.

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
├── prompt.py       Prompt builder. Edit this to change review behaviour
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

:::info Good first issues

We tag beginner-friendly issues on GitHub. These are self-contained improvements that don't require deep knowledge of the codebase.

[View good first issues →](https://github.com/wolz-CODElife/git-sage/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22)

:::

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
3. Run `pytest tests/ -v`. All tests must pass
4. Add or update tests for your change
5. Open a pull request against `master` using the template below

When opening your PR, use this description template:
```markdown
## What does this PR do?
<!-- A short summary of the change and why it's needed -->

## How to test it
<!-- Steps to reproduce or verify the change locally -->
\```bash
# example commands
\```

## Checklist
- [ ] Tests pass (`pytest tests/ -v`)
- [ ] New tests added for this change
- [ ] Docs updated if behaviour changed
- [ ] No hardcoded secrets or debug output left in
```

---

## Reporting bugs

Open an issue at [github.com/wolz-CODElife/git-sage/issues](https://github.com/wolz-CODElife/git-sage/issues). We have templates to help you include the right information, just pick the one that fits.

### Bug report

Use this when something isn't working as expected.
```markdown
## Describe the bug
<!-- A clear description of what went wrong -->

## Steps to reproduce
1. 
2. 
3. 

## Expected behaviour
<!-- What you expected to happen -->

## Actual behaviour
<!-- What actually happened, including full error output -->

## Environment
- OS: <!-- e.g. macOS 14.5, Ubuntu 22.04 -->
- Python version: <!-- e.g. 3.11.4 -->
- git-sage version: <!-- run: git-sage --version -->
- Ollama version: <!-- run: ollama --version -->
- Model: <!-- e.g. qwen2.5-coder:7b -->
```

### Feature request

Use this when you have an idea for something new.
```markdown
## What problem does this solve?
<!-- Describe the gap or pain point -->

## Proposed solution
<!-- How you'd like it to work -->

## Alternatives considered
<!-- Any other approaches you thought about -->

## Additional context
<!-- Screenshots, links, examples -->
```