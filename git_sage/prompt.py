"""
prompt.py
---------
Builds the system + user prompt that is sent to the local LLM.

Keeping prompts in one place makes them easy to tweak, test, and
document.
"""

from git_sage.diff import DiffResult

# ---------------------------------------------------------------------------
# System prompt
# ---------------------------------------------------------------------------
# Instruct the model to act as a senior code reviewer and return structured
# output the parser can reliably split on.
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """\
You are an expert code reviewer. Your job is to review the git diff provided \
by the user and give concise, actionable feedback.

Your response MUST follow this exact structure — do not deviate:

SUMMARY
<one or two sentences describing what this change does overall>

ISSUES
<a numbered list of concrete problems found; each item on its own line>
<if no issues found, write: None found.>

SUGGESTIONS
<a numbered list of optional improvements; each item on its own line>
<if no suggestions, write: None.>

VERDICT
<exactly one word: APPROVE or REVISE>

Rules:
- Be direct. No preamble or closing remarks outside the structure above.
- Focus on correctness, security, and maintainability — not style.
- Flag: hardcoded secrets or tokens, missing error handling, potential \
  null/index errors, SQL injection risks, blocking calls in async code, \
  N+1 query patterns, obvious logic bugs.
- Do NOT flag: formatting, naming conventions, missing comments (unless \
  a function is genuinely unclear), or subjective preferences.
- Keep each issue and suggestion to one sentence.
"""


# ---------------------------------------------------------------------------
# User message builder
# ---------------------------------------------------------------------------

def build_review_prompt(diff: DiffResult, context: str | None = None) -> str:
    """
    Construct the user-turn message from a DiffResult.

    Parameters
    ----------
    diff:
        The DiffResult from diff.py.
    context:
        Optional free-text context the developer can pass (e.g. "This adds
        OAuth support for GitHub"). Helps the model give better feedback.
    """
    parts: list[str] = [f"Changed files ({diff.file_count}): {', '.join(diff.files)}\n"
                        f"Lines: +{diff.additions} / -{diff.deletions}"]

    # Stats header — gives the model a quick orientation

    if context:
        parts.append(f"Developer note: {context}")

    parts.append("Diff:\n```diff\n" + diff.raw.strip() + "\n```")

    return "\n\n".join(parts)


def build_messages(diff: DiffResult, context: str | None = None) -> list[dict]:
    """
    Return the messages array ready to POST to the Ollama /api/chat endpoint.
    """
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user",   "content": build_review_prompt(diff, context)},
    ]