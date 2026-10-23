import tempfile
import unittest
from pathlib import Path
from scripts.check_doc_languages import blob_sha, verify, PAIRS


class TranslationSyncTest(unittest.TestCase):
    def test_git_blob_checksum(self):
        self.assertEqual(blob_sha(b"hello\n"), "ce013625030ba8dba906f756967f9e9ca394464a")

    def test_detects_changed_source(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for english, chinese in PAIRS:
                (root / english).parent.mkdir(parents=True, exist_ok=True)
                (root / chinese).parent.mkdir(parents=True, exist_ok=True)
                (root / english).write_text("original\n", encoding="utf-8")
                expected = blob_sha(b"original\n")
                (root / chinese).write_text(f"<!-- Source blob SHA: {expected} -->\n翻译\n", encoding="utf-8")
            self.assertEqual(verify(root), [])
            (root / "AGENTS.md").write_text("modified\n", encoding="utf-8")
            self.assertEqual(len(verify(root)), 1)


if __name__ == "__main__":
    unittest.main()
