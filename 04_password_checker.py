#!/usr/bin/env python3
"""04 - Password strength checker.

Scores a password using length, character variety, estimated entropy,
common-password and pattern checks. Password is read with getpass so it
is not echoed or stored in shell history.

Usage:
    python3 04_password_checker.py            # prompts securely
    python3 04_password_checker.py --demo     # runs sample passwords
"""
import argparse
import getpass
import math
import re

COMMON = {"password", "123456", "123456789", "qwerty", "letmein", "admin", "welcome",
          "iloveyou", "monkey", "dragon", "football", "abc123", "password1", "111111"}
SEQUENCES = ["abcdefghijklmnopqrstuvwxyz", "qwertyuiop", "asdfghjkl", "0123456789"]


def pool_size(pw):
    size = 0
    if re.search(r"[a-z]", pw): size += 26
    if re.search(r"[A-Z]", pw): size += 26
    if re.search(r"\d", pw): size += 10
    if re.search(r"[^A-Za-z0-9]", pw): size += 32
    return size


def has_sequence(pw, n=4):
    low = pw.lower()
    for seq in SEQUENCES:
        for i in range(len(seq) - n + 1):
            chunk = seq[i:i + n]
            if chunk in low or chunk[::-1] in low:
                return True
    return False


def evaluate(pw):
    issues = []
    entropy = len(pw) * math.log2(pool_size(pw)) if pw else 0.0
    if len(pw) < 12: issues.append("shorter than 12 characters")
    if pw.lower() in COMMON: issues.append("is a very common password"); entropy = min(entropy, 10)
    if re.search(r"(.)\1{2,}", pw): issues.append("repeats a character 3+ times"); entropy *= 0.8
    if has_sequence(pw): issues.append("contains a keyboard/alphabet/number sequence"); entropy *= 0.8
    if not re.search(r"[A-Z]", pw) or not re.search(r"[a-z]", pw): issues.append("mix upper and lower case")
    if not re.search(r"\d", pw): issues.append("no digits")
    if not re.search(r"[^A-Za-z0-9]", pw): issues.append("no symbols")
    label = ("Very weak" if entropy < 28 else "Weak" if entropy < 36 else
             "Fair" if entropy < 60 else "Strong" if entropy < 80 else "Very strong")
    return label, entropy, issues


def report(pw, show=False):
    label, entropy, issues = evaluate(pw)
    shown = pw if show else "*" * len(pw)
    print(f"Password: {shown}\n  Rating:  {label} (~{entropy:.0f} bits)")
    for i in issues:
        print(f"  - {i}")
    print()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--demo", action="store_true")
    args = ap.parse_args()
    if args.demo:
        for pw in ["password", "Summer2024", "qwerty123!", "t7#Kq!zP9vLm2@xW"]:
            report(pw, show=True)
    else:
        report(getpass.getpass("Enter password to test: "))


if __name__ == "__main__":
    main()
