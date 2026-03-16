---
id: implementation
title: Implementation Walkthrough
sidebar_position: 5
---

# Implementation Walkthrough

This page walks through each module in detail: what it does, how it works, and why it's written the way it is. If you want to understand the codebase before contributing or extending it, this is the right place to start. Each module has a single responsibility and stays under 100 lines.

---

## `diff.py` - Git diff extraction

The entry point for every review. It runs `git diff --cached` as a subprocess and parses the output into a structured `DiffResult`.

```python
def get_staged_diff() -> DiffResult:
    return _run_diff(["git", "diff", "--cached"])
```

The `_run_diff` helper handles the subprocess call and extracts three things from the raw text:

1. **Additions** - lines starting with `+` (excluding `+++` file headers)
2. **Deletions** - lines starting with `-` (excluding `---` file headers)
3. **Files** - parsed from `+++ b/` lines in the diff header

Three diff modes are supported: `staged` (default), `head` (last commit), and `branch` (current branch vs a base).

---

## `prompt.py` - Prompt builder

Two functions matter here:

**`build_review_prompt(diff, context)`** constructs the user message. It includes:
- A stats header: `Changed files (2): app/auth.py, app/models.py — +47 / -12`
- An optional developer note (via `--context`)
- A deletion guard: if the diff is pure deletions, the model is told not to flag them
- The raw diff wrapped in a fenced code block

**`SYSTEM_PROMPT`** is where the model's behaviour is defined. Key instructions:

```python
SYSTEM_PROMPT = """\
You are an expert code reviewer ...

Your response MUST follow this exact structure:

SUMMARY
ISSUES
SUGGESTIONS
VERDICT
...

Rules:
- NEVER flag issues in deleted lines (lines starting with `-`).
- Flag: hardcoded secrets, missing error handling, SQL injection risks ...
- Do NOT flag: formatting, naming conventions, missing comments ...
"""
```

The structured output format is the most important part of the prompt. It's what makes the parser reliable.

---

## `ollama.py` - Local AI client

A minimal `httpx` wrapper around Ollama's `/api/chat` endpoint.

```python
def chat(messages, model, host, stream=False) -> str | Iterator[str]:
    payload = {
        "model": model,
        "messages": messages,
        "stream": stream,
        "options": {"temperature": 0.2, "top_p": 0.9},
    }
    # POST to http://localhost:11434/api/chat
```

Two utility functions support the CLI:

- **`is_available(host)`** - pings `/api/tags` with a 3-second timeout to check if Ollama is running
- **`list_models(host)`** - returns model names from `/api/tags` for `git-sage models`

Temperature is set to `0.2` - low enough for consistent, structured output, high enough to avoid repetitive phrasing across reviews.

---

## `parser.py` - Response parser

The parser splits the model's response on the four section headings using a regex:

```python
_HEADING = re.compile(
    r"^(SUMMARY|ISSUES|SUGGESTIONS|VERDICT)\s*:?\s*$",
    re.IGNORECASE | re.MULTILINE,
)
```

The `re.IGNORECASE` flag handles models that return lowercase headings. The optional `:?` handles models that append a colon.

List items are extracted with:

```python
_LIST_ITEM = re.compile(r"^\s*\d+[.)]\s+(.+)$")
```

If no numbered items are found (some models skip numbering), the fallback extracts any non-empty line that isn't a "None" placeholder.

The `Verdict` enum has three values:

```python
class Verdict(str, Enum):
    APPROVE = "APPROVE"
    REVISE  = "REVISE"
    UNKNOWN = "UNKNOWN"   # model didn't follow instructions
```

`UNKNOWN` is treated as a non-blocking result; the review is shown but the push is not aborted.

---

## `output.py` - Terminal renderer

Uses the `Rich` library for coloured panels and formatted output. The key functions:

**`print_review(result)`** - renders all four sections in sequence.

**`thinking_spinner(label)`** - returns a `Rich` `Live` context manager that shows a spinner while Ollama is running:

```python
with output.thinking_spinner(f"Reviewing with {model}…"):
    raw_response = ollama.chat(messages, model=model, host=host)
```

The spinner is `transient=True` so it disappears once the review is ready, leaving a clean output.

---

## `hook.py` - Git hook manager

The hook script written to `.git/hooks/pre-push`:

```sh
#!/usr/bin/env sh
# git-sage managed hook
git-sage review --hook
```

The `# git-sage managed hook` comment is a marker used to detect whether the file was created by git-sage. This prevents the tool from overwriting a hook that was written by something else.

Install and uninstall are idempotent, running `git-sage install` twice is safe.

---

## `cli.py` - Entry point

Built with [Click](https://click.palletsprojects.com). The `review` command wires the full pipeline:

```python
@main.command()
def review(model, host, context, hook, diff_mode, base, force):
    # 1. Check Ollama is available
    # 2. Extract the diff
    # 3. Build the prompt
    # 4. Call Ollama with a spinner
    # 5. Parse the response
    # 6. Render to terminal
    # 7. Exit 1 if hook mode + REVISE + not force
```

The `--hook` flag is hidden from `--help`, it's an internal flag used only by the pre-push script.