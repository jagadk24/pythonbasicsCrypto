#!/usr/bin/env python3
"""10 - Duplicate file finder.

Finds duplicate files by size first, then by SHA-256 content hash.
Report only; it never deletes anything.

Usage:
    python3 10_duplicate_finder.py ~/Pictures
    python3 10_duplicate_finder.py ~/Downloads --min-size 1024
"""
import argparse
import hashlib
from collections import defaultdict
from pathlib import Path


def hash_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while block := f.read(1 << 20):
            h.update(block)
    return h.hexdigest()


def find_duplicates(root, min_size=1):
    by_size = defaultdict(list)
    for p in root.rglob("*"):
        try:
            if p.is_file() and not p.is_symlink():
                size = p.stat().st_size
                if size >= min_size:
                    by_size[size].append(p)
        except OSError:
            continue

    groups = defaultdict(list)
    for size, paths in by_size.items():
        if len(paths) < 2:
            continue  # unique size => cannot be a duplicate
        for p in paths:
            try:
                groups[(size, hash_file(p))].append(p)
            except OSError:
                continue
    return {k: v for k, v in groups.items() if len(v) > 1}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder", type=Path)
    ap.add_argument("--min-size", type=int, default=1, help="ignore files smaller than N bytes")
    args = ap.parse_args()

    if not args.folder.is_dir():
        raise SystemExit(f"Not a folder: {args.folder}")

    dupes = find_duplicates(args.folder, args.min_size)
    wasted = 0
    for i, ((size, digest), paths) in enumerate(sorted(dupes.items()), 1):
        wasted += size * (len(paths) - 1)
        print(f"Group {i}: {size} bytes each, sha256={digest[:12]}...")
        for p in sorted(paths):
            print(f"   {p}")
    if dupes:
        print(f"\n{len(dupes)} duplicate group(s), ~{wasted:,} bytes reclaimable.")
    else:
        print("No duplicates found.")


if __name__ == "__main__":
    main()
