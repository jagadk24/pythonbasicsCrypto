#!/usr/bin/env python3
"""05 - File organizer.

Sorts files in a folder into subfolders by type (Images, Documents, ...).
Dry-run by default; pass --apply to actually move files. Never overwrites.

Usage:
    python3 05_file_organizer.py ~/Downloads            # preview
    python3 05_file_organizer.py ~/Downloads --apply    # move files
"""
import argparse
import shutil
from pathlib import Path

CATEGORIES = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"},
    "Documents": {".pdf", ".doc", ".docx", ".txt", ".md", ".odt", ".rtf", ".pptx", ".xlsx", ".csv"},
    "Archives": {".zip", ".tar", ".gz", ".7z", ".rar"},
    "Code": {".py", ".js", ".html", ".css", ".java", ".c", ".cpp", ".sh", ".json"},
    "Media": {".mp3", ".wav", ".mp4", ".mkv", ".mov"},
}


def category_for(path):
    ext = path.suffix.lower()
    for name, exts in CATEGORIES.items():
        if ext in exts:
            return name
    return "Other"


def unique_target(target):
    if not target.exists():
        return target
    i = 1
    while True:
        cand = target.with_name(f"{target.stem}_{i}{target.suffix}")
        if not cand.exists():
            return cand
        i += 1


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder", type=Path)
    ap.add_argument("--apply", action="store_true", help="actually move files")
    args = ap.parse_args()

    if not args.folder.is_dir():
        raise SystemExit(f"Not a folder: {args.folder}")

    moved = 0
    for item in sorted(args.folder.iterdir()):
        if not item.is_file() or item.name.startswith("."):
            continue
        dest_dir = args.folder / category_for(item)
        dest = unique_target(dest_dir / item.name)
        print(f"{'MOVE' if args.apply else 'would move'}: {item.name} -> {dest_dir.name}/{dest.name}")
        if args.apply:
            dest_dir.mkdir(exist_ok=True)
            shutil.move(str(item), str(dest))
        moved += 1
    print(f"\n{moved} file(s) {'moved' if args.apply else 'would be moved (use --apply)'}.")


if __name__ == "__main__":
    main()
