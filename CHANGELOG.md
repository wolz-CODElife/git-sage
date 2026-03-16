# Changelog

All notable changes to this project will be documented here.
This project follows [Keep a Changelog](https://keepachangelog.com) conventions.

---

## [0.1.0] — 2025-03-16

### Added
- `git-sage review` — review staged changes with a local LLM
- `git-sage install` / `uninstall` — manage the pre-push hook
- `git-sage status` — check Ollama availability and hook status
- `git-sage models` — list locally available Ollama models
- Support for `qwen2.5-coder:7b` via Ollama
- Structured output parsing (SUMMARY / ISSUES / SUGGESTIONS / VERDICT)
- Rich terminal renderer with coloured panels and verdict badges
- `--diff-mode` flag: `staged`, `head`, or `branch`
- `--context` flag for passing developer notes to the model
- `--force` flag to review without aborting the push
- 17 unit tests covering diff extraction, prompt building, and response parsing