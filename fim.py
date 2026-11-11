#!/usr/bin/env python3
"""File Integrity Monitor — SHA-256 baseline vs current disk. Own files only."""

import argparse
import os
import sys

from fim.baseline import diff_snapshots, is_clean, load_baseline, save_baseline
from fim.scan import snapshot

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_TARGET = os.path.join(BASE_DIR, "samples", "watched")
DEFAULT_BASELINE = os.path.join(BASE_DIR, "baseline.json")


def print_diff(diff):
    print("=" * 60)
    print("           FILE INTEGRITY REPORT")
    print("=" * 60)
    print(f"Changed : {len(diff['changed'])}")
    print(f"Added   : {len(diff['added'])}")
    print(f"Removed : {len(diff['removed'])}")
    for rel in diff["changed"]:
        print(f"  [CHANGED] {rel}")
    for rel in diff["added"]:
        print(f"  [ADDED]   {rel}")
    for rel in diff["removed"]:
        print(f"  [REMOVED] {rel}")
    if is_clean(diff):
        print("\n[OK] Baseline matches disk.")
    else:
        print("\n[ALERT] Integrity drift detected.")
    print("=" * 60)


def cmd_init(args):
    if not os.path.isdir(args.path):
        print(f"Directory not found: {args.path}", file=sys.stderr)
        return 1
    records = snapshot(args.path)
    save_baseline(args.baseline, args.path, records)
    print(f"[*] Baseline written: {os.path.abspath(args.baseline)}")
    print(f"[*] Files hashed: {len(records)}")
    return 0


def cmd_check(args):
    if not os.path.isdir(args.path):
        print(f"Directory not found: {args.path}", file=sys.stderr)
        return 1
    if not os.path.isfile(args.baseline):
        print(
            f"No baseline at {args.baseline}. Run: python fim.py init",
            file=sys.stderr,
        )
        return 2
    old = load_baseline(args.baseline)["files"]
    new = snapshot(args.path)
    diff = diff_snapshots(old, new)
    print_diff(diff)
    return 0 if is_clean(diff) else 1


def parse_args():
    parser = argparse.ArgumentParser(
        description="Build or verify a SHA-256 baseline of a directory you own."
    )
    parser.add_argument(
        "command",
        choices=("init", "check"),
        help="init = save baseline, check = compare disk to baseline",
    )
    parser.add_argument(
        "--path",
        default=DEFAULT_TARGET,
        help="Directory to watch (default: samples/watched)",
    )
    parser.add_argument(
        "--baseline",
        default=DEFAULT_BASELINE,
        help="Baseline JSON path (default: ./baseline.json)",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    args.path = os.path.abspath(args.path)
    args.baseline = os.path.abspath(args.baseline)
    if args.command == "init":
        return cmd_init(args)
    return cmd_check(args)


if __name__ == "__main__":
    raise SystemExit(main())
