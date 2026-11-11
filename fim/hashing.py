"""SHA-256 of a file, read in chunks so large files stay in disk, not RAM."""

import hashlib

CHUNK = 4096


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        while True:
            block = handle.read(CHUNK)
            if not block:
                break
            digest.update(block)
    return digest.hexdigest()
