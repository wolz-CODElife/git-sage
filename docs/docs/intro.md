---
id: intro
title: Getting Started
sidebar_position: 1
slug: /
---

# git-sage

> Local AI code review for your git workflow no cloud, no subscriptions, no data leaving your machine.

`git-sage` is a Python CLI tool that hooks into git and runs an AI-powered code review using a **locally hosted model via [Ollama](https://ollama.com)** every time you push. It intercepts the push, analyzes your staged diff, and either approves it or asks you to revise; all in seconds, entirely on your machine.

## What it does

Most AI code review tools sit at the pull request stage, they analyse your code after it has already been pushed to a remote repository. By that point, a hardcoded secret has already touched a cloud server. A vulnerable dependency has already been committed to a branch that other developers may have pulled. The damage window opens the moment you push, not the moment the PR is reviewed.

`git-sage` moves the review earlier. It runs as a `pre-push` git hook, which means it catches issues on your local machine before any code is uploaded to the cloud. No remote repository involved. No branch created. If the model finds a problem, the push is aborted and you fix it right there in your editor.

```
$ git push

  Staged: 1 file(s)  +6 / -0

  ╭─ Summary ──────────────────────────────────────────────────╮
  │ Adds a login endpoint with bcrypt password hashing.        │
  ╰────────────────────────────────────────────────────────────╯

  Issues  (2 found)

  ●  1. SECRET_KEY is hardcoded as a string literal on line 14.
  ●  2. No rate limiting on the /login route.

  Suggestions  (1)

  ◆  1. Load SECRET_KEY from os.getenv('SECRET_KEY') instead.

  ╭────────────────────────────────────────────────────────────╮
  │  ✗  REVISE                                                 │
  │  Address the issues above before pushing.                  │
  ╰────────────────────────────────────────────────────────────╯

  Push aborted by git-sage. Fix the issues above, or run:
    git push --no-verify   to bypass the hook.
```

## Why local AI?

Since most code review tools send your code to a remote server. `git-sage` keeps everything on your machine, ensuring the following:

- **Privacy:** your code never leaves your laptop
- **No API costs:** runs on your own hardware
- **Works offline:** no internet connection required
- **Speed:** no network latency, runs in 10–30 seconds depending on your machine

## The model: `qwen2.5-coder:7b`

`git-sage` uses [`qwen2.5-coder:7b`](https://ollama.com/library/qwen2.5-coder) by default, a code-specialized model that:

- Understands unified diffs natively
- Outperforms general-purpose 7B models on code tasks
- Runs in ~4.5 GB RAM at Q4 quantization
- Works on any modern laptop without a GPU

You can swap it for any Ollama-compatible model with the `--model` flag.

## Quick start

```bash
# 1. Install Ollama and pull the model
brew install ollama
ollama serve
ollama pull qwen2.5-coder:7b

# 2. Install git-sage
pip install git-sage

# 3. Install the hook in your repo
cd your-project
git-sage install

# 4. Push normally; git-sage runs automatically
git push
```

That's it. Continue to [Installation](./installation.md) for a detailed setup guide.