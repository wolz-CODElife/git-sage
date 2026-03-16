---
id: installation
title: Installation
sidebar_position: 2
---

# Installation

This guide walks you through installing Ollama, pulling the right model, and wiring `git-sage` into your git workflow. The whole process takes about 5 minutes, most of which is the model download.

## Requirements

- Python 3.9 or higher
- [Ollama](https://ollama.com) installed and running
- macOS, Linux, or Windows (WSL2)
- ~5 GB disk space for the model

No GPU required. The default model runs on CPU.

---

## Install Ollama

**macOS**

```bash
brew install ollama
```

Or download the desktop app from [ollama.com](https://ollama.com).

**Linux**

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows**

Download the installer from [ollama.com](https://ollama.com). Run it inside **WSL2** for best compatibility.

---

## Start Ollama and pull the model

Start the Ollama server in one terminal:
```bash
ollama serve
```

In a second terminal, pull the model (~4.5 GB):
```bash
ollama pull qwen2.5-coder:7b
```

:::tip Why `qwen2.5-coder:7b`?
It's a code-specialized model trained on source code and diffs. It understands unified diff format natively, flags real issues, and runs comfortably on 8 GB RAM at Q4 quantization — the best code-focused model available at the 7B size tier.
:::

Verify Ollama is running and the model is available:
```bash
ollama list
```

You should see `qwen2.5-coder:7b` in the output.

---

## Using a different model

`qwen2.5-coder:7b` is the recommended default, but `git-sage` works with any model available in Ollama. You might want a different model if:

- Your machine has less than 8 GB RAM. Try `qwen2.5-coder:3b` (~2 GB) for a lighter footprint
- You have more RAM or a GPU. Try `qwen2.5-coder:14b` or `qwen2.5-coder:32b` for sharper reviews
- You prefer a general-purpose model. `llama3.2:3b` or `mistral` work fine for mixed codebases
- You want maximum accuracy and have the hardware. `deepseek-coder-v2:16b` is excellent for complex review tasks

Pull any model the same way:
```bash
ollama pull llama3.2:3b
ollama pull deepseek-coder-v2:16b
```

Then pass it to git-sage with the `--model` flag:
```bash
git-sage review --model llama3.2:3b
```

To browse the full library of available models, visit [ollama.com/search](https://ollama.com/search). Filter by **Code** tag to find models optimised for programming tasks. Any model listed there can be pulled and used with git-sage immediately.

:::tip Persisting your model choice
If you always want to use a specific model, set the `GIT_SAGE_MODEL` environment variable in your shell profile:
```bash
# ~/.zshrc or ~/.bashrc
export GIT_SAGE_MODEL=deepseek-coder-v2:16b
```

Then in your hook script (`.git/hooks/pre-push`), update the call to read it:
```sh
git-sage review --hook --model "${GIT_SAGE_MODEL:-qwen2.5-coder:7b}"
```
:::

---

## Install git-sage

**From PyPI**

```bash
pip install git-sage
```

**From source**

```bash
git clone https://github.com/wolz-CODElife/git-sage
cd git-sage
pip install .
```

:::tip Virtual environments
It's good practice to install inside a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install git-sage
```
:::

---

## Install the pre-push hook

Navigate to any git repository and run:

```bash
git-sage install
```

This writes a small shell script to `.git/hooks/pre-push` that calls `git-sage review --hook` on every push.

Verify everything is set up:

```bash
git-sage status
```

Expected output:

```
  git-sage  v0.1.0
  [✓]  Ollama running at http://localhost:11434
       Models: qwen2.5-coder:7b
  [✓]  pre-push hook installed
```

---

## Uninstalling

To remove the hook from a repo:

```bash
git-sage uninstall
```

To uninstall the tool entirely:

```bash
pip uninstall git-sage
```