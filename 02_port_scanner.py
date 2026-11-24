#!/usr/bin/env python3
"""02 - Simple TCP connect port scanner.

ONLY scan machines you own or have explicit written permission to test.
Defaults to localhost. Uses a thread pool and the standard library.

Usage:
    python3 02_port_scanner.py                       # scan 127.0.0.1, ports 1-1024
    python3 02_port_scanner.py 127.0.0.1 -p 20-100
    python3 02_port_scanner.py scanme.nmap.org -p 22,80,443   # Nmap permits this host
"""
import argparse
import socket
from concurrent.futures import ThreadPoolExecutor

COMMON = {21: "ftp", 22: "ssh", 23: "telnet", 25: "smtp", 53: "dns", 80: "http",
          110: "pop3", 143: "imap", 443: "https", 3306: "mysql", 5432: "postgres",
          8000: "http-alt", 8080: "http-alt"}


def parse_ports(spec):
    ports = set()
    for part in spec.split(","):
        if "-" in part:
            a, b = part.split("-", 1)
            ports.update(range(int(a), int(b) + 1))
        else:
            ports.add(int(part))
    bad = [p for p in ports if not 1 <= p <= 65535]
    if bad:
        raise ValueError(f"invalid ports: {sorted(bad)[:5]}")
    return sorted(ports)


def check(host, port, timeout):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout)
        return port if s.connect_ex((host, port)) == 0 else None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("host", nargs="?", default="127.0.0.1")
    ap.add_argument("-p", "--ports", default="1-1024")
    ap.add_argument("-t", "--timeout", type=float, default=0.5)
    ap.add_argument("-w", "--workers", type=int, default=100)
    args = ap.parse_args()

    try:
        ip = socket.gethostbyname(args.host)
        ports = parse_ports(args.ports)
    except (socket.gaierror, ValueError) as e:
        raise SystemExit(f"Error: {e}")

    print(f"Scanning {args.host} ({ip}), {len(ports)} ports...")
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        results = ex.map(lambda p: check(ip, p, args.timeout), ports)
        open_ports = [p for p in results if p]

    if open_ports:
        for p in open_ports:
            print(f"  {p:<6} open   {COMMON.get(p, '')}")
    else:
        print("  No open ports found.")


if __name__ == "__main__":
    main()
