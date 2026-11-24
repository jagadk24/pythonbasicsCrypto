#!/usr/bin/env python3
"""01 - Failed login log parser.

Counts failed SSH login attempts per source IP from an auth log
(e.g. /var/log/auth.log) and flags IPs over a threshold.

Usage:
    python3 01_log_parser.py /var/log/auth.log --threshold 5
    python3 01_log_parser.py --demo
"""
import argparse
import re
import sys
from collections import Counter

FAILED_RE = re.compile(
    r"Failed password for (?:invalid user )?(?P<user>\S+) from (?P<ip>\d{1,3}(?:\.\d{1,3}){3})"
)

DEMO_LOG = """\
Nov 24 08:01:11 host sshd[101]: Failed password for root from 203.0.113.5 port 4022 ssh2
Nov 24 08:01:14 host sshd[101]: Failed password for root from 203.0.113.5 port 4023 ssh2
Nov 24 08:01:17 host sshd[101]: Failed password for invalid user admin from 203.0.113.5 port 4024 ssh2
Nov 24 08:02:00 host sshd[102]: Accepted password for jk from 198.51.100.7 port 5000 ssh2
Nov 24 08:03:10 host sshd[103]: Failed password for invalid user test from 192.0.2.44 port 6001 ssh2
"""


def parse(lines):
    by_ip, by_user = Counter(), Counter()
    for line in lines:
        m = FAILED_RE.search(line)
        if m:
            by_ip[m["ip"]] += 1
            by_user[m["user"]] += 1
    return by_ip, by_user


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("logfile", nargs="?")
    ap.add_argument("--threshold", type=int, default=3, help="flag IPs with >= N failures")
    ap.add_argument("--demo", action="store_true", help="use built-in sample log")
    args = ap.parse_args()

    if args.demo:
        lines = DEMO_LOG.splitlines()
    elif args.logfile:
        try:
            with open(args.logfile, errors="replace") as f:
                lines = f.readlines()
        except OSError as e:
            sys.exit(f"Cannot read log: {e}")
    else:
        ap.error("provide a logfile or --demo")

    by_ip, by_user = parse(lines)
    print("Failed logins by IP:")
    for ip, n in by_ip.most_common():
        flag = "  <-- SUSPICIOUS" if n >= args.threshold else ""
        print(f"  {ip:<16} {n}{flag}")
    print("\nMost targeted usernames:")
    for user, n in by_user.most_common(5):
        print(f"  {user:<16} {n}")


if __name__ == "__main__":
    main()
