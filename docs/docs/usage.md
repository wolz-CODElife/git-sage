---
id: usage
title: Usage
sidebar_position: 3
---

# Usage

Once installed, `git-sage` works automatically on every `git push`. But it also has a set of commands you can run manually to review without pushing, check your setup, swap models, or manage the hook. This page covers all of them.

## Commands

### `git-sage review`

Manually review your staged changes:

```bash
git add .
git-sage review
```

**Options:**

| Flag | Default | Description |
|---|---|---|
| `--model` / `-m` | `qwen2.5-coder:7b` | Ollama model to use |
| `--host` | `http://localhost:11434` | Ollama server URL |
| `--context` / `-c` | — | Optional note about the change |
| `--diff-mode` | `staged` | `staged`, `head`, or `branch` |
| `--base` | `main` | Base branch for `--diff-mode=branch` |
| `--force` / `-f` | — | Don't abort push on REVISE (hook mode only) |

**Examples:**

```bash
# Review staged changes with a different model
git-sage review --model codellama:13b

# Provide context to help the model give better feedback
git-sage review --context "Adds OAuth login via GitHub"

# Review the last commit instead of staged changes
git-sage review --diff-mode head

# Review everything on the current branch vs main
git-sage review --diff-mode branch --base main
```

---

### `git-sage install`

Install the pre-push hook in the current git repository:

```bash
git-sage install
```

After this, every `git push` triggers a review automatically.

---

### `git-sage uninstall`

Remove the pre-push hook:

```bash
git-sage uninstall
```

---

### `git-sage status`

Check that Ollama is running, the model is available, and the hook is installed:

```bash
git-sage status
```

---

### `git-sage models`

List all locally available Ollama models:

```bash
git-sage models
```

Models compatible with `git-sage` are highlighted.

---

## Bypassing the hook

If you need to push without a review (e.g. a hotfix or WIP commit):

```bash
git push --no-verify
```

:::caution
`--no-verify` skips all git hooks, not just git-sage. Use it intentionally.
:::

---

## Understanding the output

Every review produces four sections:

**Summary** - One or two sentences describing what the change does overall.

**Issues** - Concrete problems the model found. Each issue is one sentence. If none are found, the section is omitted.

**Suggestions** - Optional improvements. These won't cause an abort — they're informational.

**Verdict** - Either `APPROVE` (push proceeds) or `REVISE` (push is aborted).

---

## Verdict behaviour

| Verdict | Hook mode (`git push`) | Manual mode (`git-sage review`) |
|---|---|---|
| `APPROVE` | Push proceeds normally | Exits with code 0 |
| `REVISE` | Push is aborted | Exits with code 1 |

To review without aborting the push on REVISE, use `--force`:

```bash
git-sage review --force
```