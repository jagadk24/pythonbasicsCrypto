# 10 Python Security Scripts (October '26 roadmap)

All scripts use only the Python 3 standard library (3.8+; 3.10+ recommended). No installs needed.
Run any script with `-h` to see its options.

| # | Script | What it practices |
|---|--------|-------------------|
| 01 | `01_log_parser.py` | Regex, file I/O, `Counter`. Detect brute-force SSH attempts |
| 02 | `02_port_scanner.py` | `socket`, threads. How TCP connect scans work |
| 03 | `03_file_hasher.py` | `hashlib`, chunked reading. Verifying downloads |
| 04 | `04_password_checker.py` | Entropy, patterns, `getpass` |
| 05 | `05_file_organizer.py` | `pathlib`, `shutil`, safe dry-run design |
| 06 | `06_password_generator.py` | `secrets` vs `random`, entropy |
| 07 | `07_integrity_monitor.py` | Hash baselines, change detection (Tripwire idea) |
| 08 | `08_classical_ciphers.py` | Caesar/Vigenere and frequency analysis (ties to November crypto) |
| 09 | `09_header_checker.py` | HTTP, `urllib`, web security headers |
| 10 | `10_duplicate_finder.py` | Size-then-hash optimization |

## Quick start
```bash
python3 01_log_parser.py --demo
python3 04_password_checker.py --demo
python3 08_classical_ciphers.py caesar crack "Khoor, Zruog"
```

## Ethics and safety
- Only run the port scanner (02) and header checker (09) against systems you own or have written permission to test. UGA's network policies apply on campus.
- Scripts 05 and 10 are non-destructive by default (05 is dry-run, 10 only reports).

## Ideas to extend each one (good for your portfolio)
1. Log parser: add GeoIP lookups, output CSV, or watch a log live with `tail -f` logic.
2. Port scanner: add banner grabbing, UDP, or JSON output.
3. Hasher: add recursive directory mode and a `sha256sum`-compatible output file.
4. Password checker: check against a downloaded common-password list.
5. Organizer: add a config file for custom categories and an undo log.
6. Generator: add a clipboard option and a larger wordlist (e.g. EFF diceware).
7. Integrity monitor: sign the baseline with HMAC so tampering with it is detectable.
8. Ciphers: add Vigenere key-length detection (Kasiski/index of coincidence).
9. Header checker: grade headers' values, not just presence; scan a list of URLs.
10. Duplicate finder: add an interactive "keep one" mode with a confirmation step.

Put these in a GitHub repo with this README, and you've checked off both October items on your roadmap.
