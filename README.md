# git-sage

> Local AI code review right before you push. No cloud. No subscriptions. No data leaving your machine.

`git-sage` hooks into your git workflow and runs a code review using a locally hosted LLM via [Ollama](https://ollama.com). When you run `git push`, the tool intercepts it, sends your staged diff to the model, and either approves the push or asks you to revise.

```
$ git push

  Staged: 3 file(s)  +47 / -12

  ╭─ Summary ───────────────────────────────────────────────────────────╮
  │ Adds a /login endpoint with bcrypt password hashing.               │
  ╰─────────────────────────────────────────────────────────────────────╯

  Issues  (2 found)

  ●  1. The SECRET_KEY is hardcoded as a string literal on line 14.
  ●  2. There is no rate limiting on the /login route.

  Suggestions  (1)

  ◆  1. Load SECRET_KEY from os.getenv('SECRET_KEY') instead.

  ╭─────────────────────────────────────────────────────────────────────╮
  │  ✗  REVISE                                                          │
  │  Address the issues above before pushing.                          │
  ╰─────────────────────────────────────────────────────────────────────╯

  Push aborted by git-sage. Fix the issues above, or run:
    git push --no-verify   to bypass the hook.
```

---

## Requirements

- Python 3.9+
- [Ollama](https://ollama.com) installed and running (`ollama serve`)
- The `qwen2.5-coder:7b` model pulled locally (see Setup below)

No GPU required. The recommended model runs comfortably on 8 GB RAM.

---

## Setup

**1. Install Ollama**

Download from [ollama.com](https://ollama.com) and start the server:

```bash
ollama serve
```

**2. Pull the model**

```bash
ollama pull qwen2.5-coder:7b
```

> **Why `qwen2.5-coder:7b`?**
> It's a code-specialized model that understands unified diffs natively,
> outperforms general-purpose 7B models on code tasks, and runs in ~4.5 GB
> of RAM at Q4 quantization. It's the best code-focused model available
> at the 7B size tier as of early 2025.

**3. Install git-sage**

```bash
pip install git-sage
```

Or from source:

```bash
git clone https://github.com/yourname/git-sage
cd git-sage
pip install -e .
```

**4. Install the pre-push hook in your repo**

```bash
cd your-project
git-sage install
```

That's it. The next `git push` will trigger a review.

---

## Commands

| Command | Description |
|---|---|
| `git-sage review` | Manually review staged changes |
| `git-sage review --model llama3.2` | Use a different local model |
| `git-sage review --context "Adds OAuth"` | Provide context to the model |
| `git-sage review --diff-mode head` | Review the last commit instead |
| `git-sage review --diff-mode branch --base main` | Review the whole branch |
| `git-sage review --force` | Review but don't abort push on REVISE |
| `git-sage install` | Install the pre-push hook |
| `git-sage uninstall` | Remove the pre-push hook |
| `git-sage status` | Check Ollama availability and hook status |
| `git-sage models` | List locally available models |

---

## How it works

```
git push
  → .git/hooks/pre-push fires
    → git-sage review --hook
      → git diff --cached        (extract the staged diff)
      → build prompt             (diff + system instructions)
      → POST localhost:11434     (Ollama local API)
      → parse response           (SUMMARY / ISSUES / SUGGESTIONS / VERDICT)
      → render to terminal       (rich coloured output)
      → exit 0 (APPROVE) or exit 1 (REVISE, aborts push)
```

See [docs/architecture.md](docs/architecture.md) for a full walkthrough.

---

## Bypassing the hook

If you need to push without a review (e.g. a hotfix):

```bash
git push --no-verify
```

---

## Extending git-sage

**Add a custom rule to the system prompt**

Edit `git_sage/prompt.py` and add your rule to the `SYSTEM_PROMPT` string.
For example, to flag any print statement:

```
- Flag any print() or console.log() calls left in production code paths.
```

**Use a different model**

```bash
ollama pull codellama:13b
git-sage review --model codellama:13b
```

**Output JSON for CI pipelines**

Currently the output is human-readable only. A `--json` flag is a natural
extension — see [docs/extending.md](docs/extending.md).

---

## Running tests

```bash
pip install pytest
pytest tests/ -v
```

Tests are self-contained and don't require Ollama or a git repo.

---

## Project structure

```
git_sage/
  cli.py       CLI entrypoint (click)
  diff.py      Git diff extraction
  prompt.py    Prompt builder
  ollama.py    Ollama HTTP client
  parser.py    Response parser
  output.py    Terminal renderer (rich)
  hook.py      Git hook installer
tests/
  test_parser.py
  test_diff.py
  test_prompt.py
```

---

## License

MIT