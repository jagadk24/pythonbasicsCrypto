#!/usr/bin/env python3
"""03 - File hash calculator / verifier.

Compute SHA-256 (or md5/sha1/sha512) for files, or verify a file
against an expected hash (useful for checking downloads).

Usage:
    python3 03_file_hasher.py file1 file2
    python3 03_file_hasher.py -a sha512 file
    python3 03_file_hasher.py file --verify <expected_hash>
"""
import argparse
import hashlib
import hmac
import sys


def hash_file(path, algo="sha256", chunk=1 << 20):
    h = hashlib.new(algo)
    with open(path, "rb") as f:
        while block := f.read(chunk):
            h.update(block)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+")
    ap.add_argument("-a", "--algo", default="sha256", choices=["md5", "sha1", "sha256", "sha512"])
    ap.add_argument("--verify", metavar="HASH", help="expected hash (single file only)")
    args = ap.parse_args()

    if args.verify and len(args.files) != 1:
        ap.error("--verify works with exactly one file")

    status = 0
    for path in args.files:
        try:
            digest = hash_file(path, args.algo)
        except OSError as e:
            print(f"{path}: ERROR {e}", file=sys.stderr)
            status = 1
            continue
        if args.verify:
            ok = hmac.compare_digest(digest, args.verify.strip().lower())
            print(f"{path}: {'MATCH' if ok else 'MISMATCH'}")
            print(f"  computed: {digest}")
            status = 0 if ok else 2
        else:
            print(f"{digest}  {path}")
    sys.exit(status)


if __name__ == "__main__":
    main()
