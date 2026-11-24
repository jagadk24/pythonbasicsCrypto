#!/usr/bin/env python3
"""09 - HTTP security header checker.

Fetches a URL and reports which common security headers are present.
Check your own sites or ones you are authorized to test.

Usage:
    python3 09_header_checker.py https://example.com
"""
import argparse
import sys
import urllib.error
import urllib.request
from urllib.parse import urlparse

HEADERS = {
    "Strict-Transport-Security": "Forces HTTPS (HSTS)",
    "Content-Security-Policy": "Mitigates XSS / injection",
    "X-Content-Type-Options": "Stops MIME sniffing (want: nosniff)",
    "X-Frame-Options": "Clickjacking protection (or CSP frame-ancestors)",
    "Referrer-Policy": "Controls referrer leakage",
    "Permissions-Policy": "Restricts browser features",
}
LEAKY = ["Server", "X-Powered-By", "X-AspNet-Version"]


def fetch_headers(url, timeout=10):
    req = urllib.request.Request(url, headers={"User-Agent": "header-checker/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, dict(r.headers)
    except urllib.error.HTTPError as e:  # still has useful headers
        return e.code, dict(e.headers)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url")
    args = ap.parse_args()

    url = args.url if "://" in args.url else "https://" + args.url
    if urlparse(url).scheme not in ("http", "https"):
        sys.exit("Only http/https URLs are supported")

    try:
        status, hdrs = fetch_headers(url)
    except (urllib.error.URLError, TimeoutError, ValueError) as e:
        sys.exit(f"Request failed: {e}")

    hdrs = {k.lower(): v for k, v in hdrs.items()}
    print(f"{url} -> HTTP {status}\n\nSecurity headers:")
    present = 0
    for name, why in HEADERS.items():
        val = hdrs.get(name.lower())
        present += bool(val)
        print(f"  [{'PASS' if val else 'MISSING'}] {name}: {why}")
        if val:
            print(f"           {val[:90]}")
    print(f"\nScore: {present}/{len(HEADERS)}")

    leaks = [(h, hdrs[h.lower()]) for h in LEAKY if h.lower() in hdrs]
    if leaks:
        print("\nInformation disclosure:")
        for h, v in leaks:
            print(f"  {h}: {v}")


if __name__ == "__main__":
    main()
