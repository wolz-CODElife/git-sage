"""
parser.py
---------
Parses the structured text output from the LLM into a ReviewResult dataclass.

The system prompt (prompt.py) tells the model to respond with four labelled
sections: SUMMARY, ISSUES, SUGGESTIONS, VERDICT. This parser extracts each
section by scanning for those headings, making it tolerant of minor formatting
variations in the model output.
"""

import re
from dataclasses import dataclass, field
from enum import Enum


class Verdict(str, Enum):
    APPROVE = "APPROVE"
    REVISE  = "REVISE"
    UNKNOWN = "UNKNOWN"  # fallback if the model didn't follow instructions


@dataclass
class ReviewResult:
    summary:     str
    issues:      list[str]
    suggestions: list[str]
    verdict:     Verdict
    raw:         str        # full original LLM response (useful for debugging)

    @property
    def has_issues(self) -> bool:
        return bool(self.issues)

    @property
    def is_approved(self) -> bool:
        return self.verdict == Verdict.APPROVE


# Section heading patterns (case-insensitive, allow trailing colon or whitespace)
_HEADING = re.compile(
    r"^(SUMMARY|ISSUES|SUGGESTIONS|VERDICT)\s*:?\s*$",
    re.IGNORECASE | re.MULTILINE,
)

# A numbered list item: "1. text" or "1) text"
_LIST_ITEM = re.compile(r"^\s*\d+[.)]\s+(.+)$")


def parse(raw: str) -> ReviewResult:
    """
    Parse the raw LLM response text into a ReviewResult.

    Tolerates extra whitespace, minor heading variations, and models
    that add a colon after the heading name.
    """
    sections = _split_sections(raw)

    summary     = _extract_text(sections.get("summary", ""))
    issues      = _extract_list(sections.get("issues", ""))
    suggestions = _extract_list(sections.get("suggestions", ""))
    verdict     = _extract_verdict(sections.get("verdict", ""))

    return ReviewResult(
        summary=summary,
        issues=issues,
        suggestions=suggestions,
        verdict=verdict,
        raw=raw,
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _split_sections(text: str) -> dict[str, str]:
    """
    Split the response into a dict keyed by lowercase section name.

    Example input:
        SUMMARY
        Adds OAuth login via GitHub.

        ISSUES
        1. Missing CSRF token validation.

        ...
    """
    result: dict[str, str] = {}
    current_key: str | None = None
    current_lines: list[str] = []

    for line in text.splitlines():
        m = _HEADING.match(line.strip())
        if m:
            # Save previous section
            if current_key is not None:
                result[current_key] = "\n".join(current_lines).strip()
            current_key = m.group(1).lower()
            current_lines = []
        else:
            if current_key is not None:
                current_lines.append(line)

    # Save the last section
    if current_key is not None:
        result[current_key] = "\n".join(current_lines).strip()

    return result


def _extract_text(section: str) -> str:
    """Return the section content as a single stripped string."""
    return section.strip()


def _extract_list(section: str) -> list[str]:
    """
    Extract numbered list items from a section.

    Falls back to plain non-empty lines if no numbered items are found
    (handles models that skip numbering).
    """
    items = []
    for line in section.splitlines():
        m = _LIST_ITEM.match(line)
        if m:
            items.append(m.group(1).strip())

    if not items:
        # Fallback: any non-empty line that isn't "None" / "None found."
        items = [
            line.strip()
            for line in section.splitlines()
            if line.strip() and not re.match(r"^none[. ]*(?:found)?\.?$", line.strip(), re.IGNORECASE)
        ]

    return items


def _extract_verdict(section: str) -> Verdict:
    text = section.strip().upper()
    if "APPROVE" in text:
        return Verdict.APPROVE
    if "REVISE" in text:
        return Verdict.REVISE
    return Verdict.UNKNOWN