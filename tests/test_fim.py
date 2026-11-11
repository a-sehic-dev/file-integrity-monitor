import os
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from fim.baseline import diff_snapshots, is_clean, load_baseline, save_baseline
from fim.hashing import sha256_file
from fim.scan import snapshot


class HashTests(unittest.TestCase):
    def test_same_bytes_same_hash(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "a.txt")
            with open(path, "wb") as handle:
                handle.write(b"hello")
            self.assertEqual(
                sha256_file(path),
                "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824",
            )


class SnapshotTests(unittest.TestCase):
    def test_init_then_clean_check(self):
        with tempfile.TemporaryDirectory() as tmp:
            watched = os.path.join(tmp, "w")
            os.makedirs(watched)
            with open(os.path.join(watched, "a.txt"), "w", encoding="utf-8") as handle:
                handle.write("one")
            records = snapshot(watched)
            baseline = os.path.join(tmp, "baseline.json")
            save_baseline(baseline, watched, records)
            loaded = load_baseline(baseline)["files"]
            diff = diff_snapshots(loaded, snapshot(watched))
            self.assertTrue(is_clean(diff))

    def test_detects_change_add_remove(self):
        with tempfile.TemporaryDirectory() as tmp:
            watched = os.path.join(tmp, "w")
            os.makedirs(watched)
            keep = os.path.join(watched, "keep.txt")
            gone = os.path.join(watched, "gone.txt")
            with open(keep, "w", encoding="utf-8") as handle:
                handle.write("keep")
            with open(gone, "w", encoding="utf-8") as handle:
                handle.write("gone")
            old = snapshot(watched)
            with open(keep, "w", encoding="utf-8") as handle:
                handle.write("changed")
            os.remove(gone)
            with open(os.path.join(watched, "new.txt"), "w", encoding="utf-8") as handle:
                handle.write("new")
            diff = diff_snapshots(old, snapshot(watched))
            self.assertEqual(diff["changed"], ["keep.txt"])
            self.assertEqual(diff["removed"], ["gone.txt"])
            self.assertEqual(diff["added"], ["new.txt"])
            self.assertFalse(is_clean(diff))


if __name__ == "__main__":
    unittest.main()
