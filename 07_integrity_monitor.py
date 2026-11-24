#!/usr/bin/env python3
"""07 - File integrity monitor (a mini Tripwire).

Create a baseline of SHA-256 hashes for a directory, then check later
to detect modified, added, or deleted files.

Usage:
    python3 07_integrity_monitor.py init  ~/project  -b baseline.json
    python3 07_integrity_monitor.py check ~/project  -b baseline.json
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path


def hash_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while block := f.read(1 << 20):
            h.update(block)
    return h.hexdigest()


def snapshot(root, skip):
    snap = {}
    for p in sorted(root.rglob("*")):
        if p.is_file() and not p.is_symlink() and p.resolve() != skip:
            try:
                snap[str(p.relative_to(root))] = hash_file(p)
            except OSError as e:
                print(f"warning: cannot read {p}: {e}", file=sys.stderr)
    return snap


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("mode", choices=["init", "check"])
    ap.add_argument("directory", type=Path)
    ap.add_argument("-b", "--baseline", type=Path, default=Path("baseline.json"))
    args = ap.parse_args()

    if not args.directory.is_dir():
        sys.exit(f"Not a directory: {args.directory}")
    current = snapshot(args.directory, args.baseline.resolve())

    if args.mode == "init":
        args.baseline.write_text(json.dumps(current, indent=2))
        print(f"Baseline saved: {len(current)} files -> {args.baseline}")
        return

    try:
        base = json.loads(args.baseline.read_text())
    except (OSError, json.JSONDecodeError) as e:
        sys.exit(f"Cannot load baseline: {e}")

    modified = [f for f in current if f in base and current[f] != base[f]]
    added = [f for f in current if f not in base]
    deleted = [f for f in base if f not in current]

    for label, items in (("MODIFIED", modified), ("ADDED", added), ("DELETED", deleted)):
        for f in items:
            print(f"{label}: {f}")
    if not (modified or added or deleted):
        print("OK: no changes detected.")
    sys.exit(1 if (modified or added or deleted) else 0)


if __name__ == "__main__":
    main()
