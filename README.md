# git-sage

> Local AI code review right before you push. No cloud. No subscriptions. No data leaving your machine.

`git-sage` hooks into your git workflow and runs a code review using a locally hosted LLM via [Ollama](https://ollama.com). When you run `git push`, the tool intercepts it, sends your staged diff to the model, and either approves the push or asks you to revise, all on your machine, in seconds.
```
$ git push

  Staged: 3 file(s)  +47 / -12

  ╭─ Summary ───────────────────────────────────────────────────────────╮
  │ Adds a /login endpoint with bcrypt password hashing.                │
  ╰─────────────────────────────────────────────────────────────────────╯

  Issues  (2 found)

  ●  1. The SECRET_KEY is hardcoded as a string literal on line 14.
  ●  2. There is no rate limiting on the /login route.

  Suggestions  (1)

  ◆  1. Load SECRET_KEY from os.getenv('SECRET_KEY') instead.

  ╭─────────────────────────────────────────────────────────────────────╮
  │  ✗  REVISE                                                          │
  │  Address the issues above before pushing.                           │
  ╰─────────────────────────────────────────────────────────────────────╯

  Push aborted by git-sage. Fix the issues above, or run:
    git push --no-verify   to bypass the hook.
```

📖 **[Full documentation →](https://wolz-codelife.github.io/git-sage/)**

---

## Why git-sage?

Most AI code review tools sit at the pull request stage, by then your code has already reached a remote server. A hardcoded secret has already been pushed. A vulnerable dependency is already on a branch other developers may have pulled.

`git-sage` moves the review to your local machine, before any code leaves it. If the model finds a problem, the push is aborted and you fix it right there in your editor.

---

## Requirements

- Python 3.9+
- [Ollama](https://ollama.com) installed and running
- macOS, Linux, or Windows (WSL2)
- ~5 GB disk space for the default model

No GPU required. Runs on any modern laptop.

---

## Quick start

**1. Install Ollama and pull the model**
```bash
brew install ollama      # macOS — see docs for Linux/Windows
ollama serve
ollama pull qwen2.5-coder:7b
```

**2. Install git-sage**
```bash
pip install git-sage
```

**3. Install the hook in your repo**
```bash
cd your-project
git-sage install
```

**4. Push as normal**
```bash
git push   # review runs automatically
```

---

## Commands

| Command                                            | Description                               |
|----------------------------------------------------|-------------------------------------------|
| `git-sage review`                                  | Manually review staged changes            |
| `git-sage review --model llama3.2`                 | Use a different local model               |
| `git-sage review --context "Adds OAuth"`           | Provide context to the model              |
| `git-sage review --diff-mode head`                 | Review the last commit instead            |
| `git-sage review --diff-mode branch --base main`   | Review the whole branch                   |
| `git-sage review --force`                          | Review but don't abort push on REVISE     |
| `git-sage install`                                 | Install the pre-push hook                 |
| `git-sage uninstall`                               | Remove the pre-push hook                  |
| `git-sage status`                                  | Check Ollama availability and hook status |
| `git-sage models`                                  | List locally available Ollama models      |

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

For a full breakdown of the architecture and each module, see the **[Architecture docs](https://wolz-codelife.github.io/git-sage/docs/architecture)**.

---

## Bypassing the hook
```bash
git push --no-verify
```

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
docs/              Docusaurus documentation site
CHANGELOG.md       Version history
```

---

## Running tests
```bash
pip install pytest
pytest tests/ -v
```

Tests are self-contained; no Ollama or git repo needed.

---

## Contributing

Contributions are welcome. See the **[Contributing guide](https://wolz-codelife.github.io/git-sage/docs/contributing)** for how to get started, issue templates, and a PR template.

---

## License

MIT