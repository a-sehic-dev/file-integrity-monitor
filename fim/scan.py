"""Walk a directory and snapshot relative path, size, and SHA-256."""

import os

from .hashing import sha256_file

SKIP_NAMES = {".git", "__pycache__", ".venv", "venv"}


def iter_files(root):
    root = os.path.abspath(root)
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        dirnames[:] = [name for name in dirnames if name not in SKIP_NAMES]
        for name in filenames:
            if name in {"baseline.json"} or name.endswith(".baseline.json"):
                continue
            full = os.path.join(dirpath, name)
            if os.path.islink(full) or not os.path.isfile(full):
                continue
            rel = os.path.relpath(full, root).replace("\\", "/")
            yield rel, full


def snapshot(root):
    records = {}
    for rel, full in iter_files(root):
        records[rel] = {
            "sha256": sha256_file(full),
            "size": os.path.getsize(full),
        }
    return records
