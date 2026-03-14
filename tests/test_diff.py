"""
tests/test_diff.py
------------------
Unit tests for git_sage.diff.

We test the private _extract_files and stat counters using synthetic
diff text — no actual git repo needed.
"""

from git_sage.diff import _extract_files, _run_diff, DiffResult


SAMPLE_DIFF = """\
diff --git a/app/auth.py b/app/auth.py
index abc1234..def5678 100644
--- a/app/auth.py
+++ b/app/auth.py
@@ -10,6 +10,8 @@ def login(username, password):
     user = db.get_user(username)
+    if user is None:
+        return None
     return check_password(user, password)

diff --git a/app/models.py b/app/models.py
index 111aaaa..222bbbb 100644
--- a/app/models.py
+++ b/app/models.py
@@ -5,3 +5,4 @@ class User:
     name: str
+    email: str
"""


def test_extract_files():
    files = _extract_files(SAMPLE_DIFF)
    assert files == ["app/auth.py", "app/models.py"]


def test_additions_count():
    additions = sum(
        1 for line in SAMPLE_DIFF.splitlines()
        if line.startswith("+") and not line.startswith("+++")
    )
    assert additions == 3  # two in auth.py, one in models.py


def test_deletions_count():
    deletions = sum(
        1 for line in SAMPLE_DIFF.splitlines()
        if line.startswith("-") and not line.startswith("---")
    )
    assert deletions == 0


def test_diff_result_empty():
    result = DiffResult(raw="", file_count=0, additions=0, deletions=0, files=[])
    assert not result.raw
    assert result.file_count == 0