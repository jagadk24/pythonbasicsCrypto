#!/usr/bin/env python3
"""08 - Classical ciphers + brute-force: Caesar and Vigenere.

A bridge to November's crypto topic. These ciphers are NOT secure; they
show why key space and frequency analysis matter.

Usage:
    python3 08_classical_ciphers.py caesar enc "Hello, World" -k 3
    python3 08_classical_ciphers.py caesar dec "Khoor, Zruog" -k 3
    python3 08_classical_ciphers.py caesar crack "Khoor, Zruog"
    python3 08_classical_ciphers.py vigenere enc "Attack at dawn" -k LEMON
    python3 08_classical_ciphers.py vigenere dec "Lxfopv ef rnhr" -k LEMON
"""
import argparse
from collections import Counter

# English letter frequencies (percent), A-Z
FREQ = [8.2, 1.5, 2.8, 4.3, 12.7, 2.2, 2.0, 6.1, 7.0, 0.15, 0.77, 4.0, 2.4,
        6.7, 7.5, 1.9, 0.095, 6.0, 6.3, 9.1, 2.8, 0.98, 2.4, 0.15, 2.0, 0.074]


def shift_char(c, k):
    if c.isalpha():
        base = ord("A") if c.isupper() else ord("a")
        return chr((ord(c) - base + k) % 26 + base)
    return c


def caesar(text, k):
    return "".join(shift_char(c, k) for c in text)


def vigenere(text, key, decrypt=False):
    key = [ord(c.upper()) - 65 for c in key if c.isalpha()]
    if not key:
        raise ValueError("key must contain letters")
    out, i = [], 0
    for c in text:
        if c.isalpha():
            k = -key[i % len(key)] if decrypt else key[i % len(key)]
            out.append(shift_char(c, k))
            i += 1
        else:
            out.append(c)
    return "".join(out)


def score(text):
    """Lower = more English-like (chi-squared against letter frequencies)."""
    letters = [c.lower() for c in text if c.isalpha()]
    if not letters:
        return float("inf")
    counts, n = Counter(letters), len(letters)
    return sum(((counts.get(chr(97 + i), 0) - n * FREQ[i] / 100) ** 2) / (n * FREQ[i] / 100)
               for i in range(26))


def crack_caesar(ct):
    results = sorted(((score(caesar(ct, -k)), k, caesar(ct, -k)) for k in range(26)))
    letters = sum(c.isalpha() for c in ct)
    # Frequency analysis needs enough text; with very little, show every candidate.
    if letters < 40:
        print(f"Only {letters} letters: too short for reliable frequency analysis.")
        print("All 26 candidates (pick the one that reads as English):")
        for k in range(26):
            print(f"  key={k:<2} {caesar(ct, -k)}")
        return
    print("Best guesses (key = shift used to encrypt):")
    for s, k, pt in results[:3]:
        print(f"  key={k:<2} score={s:7.1f}  {pt}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cipher", choices=["caesar", "vigenere"])
    ap.add_argument("action", choices=["enc", "dec", "crack"])
    ap.add_argument("text")
    ap.add_argument("-k", "--key")
    args = ap.parse_args()

    if args.action == "crack":
        if args.cipher != "caesar":
            ap.error("crack is only supported for caesar")
        return crack_caesar(args.text)
    if args.key is None:
        ap.error("-k/--key is required for enc/dec")

    if args.cipher == "caesar":
        k = int(args.key)
        print(caesar(args.text, k if args.action == "enc" else -k))
    else:
        print(vigenere(args.text, args.key, decrypt=(args.action == "dec")))


if __name__ == "__main__":
    main()
