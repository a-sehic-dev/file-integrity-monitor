"""Save and load a JSON baseline. Compare against a fresh snapshot."""

import json
import os
from datetime import datetime, timezone


def save_baseline(path, root, records):
    payload = {
        "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "root": os.path.abspath(root),
        "file_count": len(records),
        "files": records,
    }
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")


def load_baseline(path):
    with open(path, "r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if "files" not in payload or not isinstance(payload["files"], dict):
        raise ValueError("baseline is missing a files object")
    return payload


def diff_snapshots(old_files, new_files):
    old_keys = set(old_files)
    new_keys = set(new_files)
    added = sorted(new_keys - old_keys)
    removed = sorted(old_keys - new_keys)
    changed = sorted(
        rel
        for rel in (old_keys & new_keys)
        if old_files[rel].get("sha256") != new_files[rel].get("sha256")
    )
    return {"added": added, "removed": removed, "changed": changed}


def is_clean(diff):
    return not (diff["added"] or diff["removed"] or diff["changed"])
