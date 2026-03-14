"""
tests/test_prompt.py
--------------------
Tests for git_sage.prompt.
"""

from git_sage.diff import DiffResult
from git_sage.prompt import build_review_prompt, build_messages, SYSTEM_PROMPT


FAKE_DIFF = DiffResult(
    raw="+ added line\n- removed line",
    file_count=1,
    additions=1,
    deletions=1,
    files=["app/main.py"],
)


def test_prompt_contains_filename():
    prompt = build_review_prompt(FAKE_DIFF)
    assert "app/main.py" in prompt


def test_prompt_contains_stats():
    prompt = build_review_prompt(FAKE_DIFF)
    assert "+1" in prompt
    assert "-1" in prompt


def test_prompt_contains_diff():
    prompt = build_review_prompt(FAKE_DIFF)
    assert "added line" in prompt
    assert "removed line" in prompt


def test_prompt_with_context():
    prompt = build_review_prompt(FAKE_DIFF, context="Adds authentication")
    assert "Adds authentication" in prompt


def test_build_messages_structure():
    messages = build_messages(FAKE_DIFF)
    assert len(messages) == 2
    assert messages[0]["role"] == "system"
    assert messages[1]["role"] == "user"
    assert messages[0]["content"] == SYSTEM_PROMPT


def test_system_prompt_has_required_sections():
    for section in ["SUMMARY", "ISSUES", "SUGGESTIONS", "VERDICT"]:
        assert section in SYSTEM_PROMPT