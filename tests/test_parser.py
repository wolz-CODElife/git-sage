"""
tests/test_parser.py
--------------------
Unit tests for git_sage.parser.

These tests are intentionally self-contained — they don't need Ollama
or git. They document exactly what the parser expects and how it handles
edge cases, making them useful reading for tutorial followers.
"""

import pytest
from git_sage.parser import parse, Verdict


# ---------------------------------------------------------------------------
# Happy path
# ---------------------------------------------------------------------------

WELL_FORMED_RESPONSE = """\
SUMMARY
Adds a new /login endpoint with password hashing via bcrypt.

ISSUES
1. The SECRET_KEY is hardcoded as a string literal on line 14.
2. There is no rate limiting on the /login route.

SUGGESTIONS
1. Move SECRET_KEY to an environment variable and load via os.getenv.
2. Consider adding flask-limiter for rate limiting.

VERDICT
REVISE
"""

def test_parse_well_formed():
    result = parse(WELL_FORMED_RESPONSE)
    assert "login" in result.summary.lower()
    assert len(result.issues) == 2
    assert "SECRET_KEY" in result.issues[0]
    assert len(result.suggestions) == 2
    assert result.verdict == Verdict.REVISE
    assert result.has_issues
    assert not result.is_approved


APPROVE_RESPONSE = """\
SUMMARY
Refactors the user serializer to use dataclasses.

ISSUES
None found.

SUGGESTIONS
None.

VERDICT
APPROVE
"""

def test_parse_approve():
    result = parse(APPROVE_RESPONSE)
    assert result.verdict == Verdict.APPROVE
    assert result.is_approved
    assert not result.has_issues
    assert result.issues == []


# ---------------------------------------------------------------------------
# Tolerances — the model doesn't always follow instructions perfectly
# ---------------------------------------------------------------------------

def test_parse_heading_with_colon():
    """Some models append a colon to headings."""
    raw = """\
SUMMARY:
Minor typo fix in README.

ISSUES:
None found.

SUGGESTIONS:
None.

VERDICT:
APPROVE
"""
    result = parse(raw)
    assert result.verdict == Verdict.APPROVE
    assert "README" in result.summary


def test_parse_lowercase_headings():
    raw = """\
summary
Fixes null pointer in payment handler.

issues
1. No null check before accessing user.address.

suggestions
None.

verdict
REVISE
"""
    result = parse(raw)
    assert result.verdict == Verdict.REVISE
    assert len(result.issues) == 1


def test_parse_unknown_verdict():
    """If the model returns garbage in the verdict section, use UNKNOWN."""
    raw = """\
SUMMARY
Something happened.

ISSUES
None found.

SUGGESTIONS
None.

VERDICT
I'm not sure about this one.
"""
    result = parse(raw)
    assert result.verdict == Verdict.UNKNOWN


def test_parse_empty_response():
    result = parse("")
    assert result.summary == ""
    assert result.issues == []
    assert result.suggestions == []
    assert result.verdict == Verdict.UNKNOWN


# ---------------------------------------------------------------------------
# raw field preserved
# ---------------------------------------------------------------------------

def test_raw_field_preserved():
    raw = WELL_FORMED_RESPONSE
    result = parse(raw)
    assert result.raw == raw