"""Contract tests for the lightweight PR documentation-impact gate."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from check_pr_docs import check


def test_no_doc_change_requires_explanation_for_implementation():
    body = "## Documentation Impact\n- [x] No maintained documentation change\nReason: Internal refactor; no public interface or behavior changed."
    assert check(body, ["src/example.py"]) == []
    assert check(body.replace("Internal refactor; no public interface or behavior changed.", "n/a"), ["src/example.py"])


def test_doc_updated_requires_doc_path_and_reference():
    body = "## Documentation Impact\n- [x] Maintained documentation updated\nAffected docs: docs/PROJECT.md"
    assert check(body, ["docs/PROJECT.md", "src/example.py"]) == []
    assert check(body, ["src/example.py"])


def test_contract_change_requires_evidence_and_tests():
    body = "## Documentation Impact\n- [x] Contract change requires review\nContract evidence: Ticket 130 redline, approval pending\nTests: tests/test_public_contract.py"
    assert check(body, ["src/example.py"]) == []
    assert check(body.replace("Tests: tests/test_public_contract.py", "Tests: n/a"), ["src/example.py"])


def test_multiple_selections_fail():
    body = "- [x] Maintained documentation updated\n- [x] No maintained documentation change"
    assert check(body, ["docs/PROJECT.md"])
