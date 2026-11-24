#!/usr/bin/env python3
"""06 - Secure password / passphrase generator.

Uses the `secrets` module (cryptographically secure), never `random`.

Usage:
    python3 06_password_generator.py                  # 20-char password
    python3 06_password_generator.py -l 32 --no-symbols
    python3 06_password_generator.py --passphrase 5   # 5-word passphrase
"""
import argparse
import math
import secrets
import string

WORDS = """able acid aged also area army away baby back ball band bank base bath bear beat been
bell belt best bird blow blue boat body bold bone book born both bowl bulk burn bush busy cafe
cake calm came camp card care cart case cash cast cell chat chip city clay club coal coat code
cold come cook cool cope copy core cost crew crop dark data dawn deal dear deep deer desk dial
dirt dish dive door dose down draw drop drum dust duty each earn east easy edge else even ever
face fact fall farm fast fate fear feed feel fern file fill film find fine fire firm fish five
flag flat flow foam fold food foot form fort four free from fuel full fund gain game gate gear
gift girl give glad glow goal gold golf good grab gray grid grow gulf hair half hall hand hard
harm hawk head heat help here hero hide high hill hold home hope horn host hour huge hunt idea
iron isle jade jazz join joke jump june jury keen keep kind king knee lake lamp land lane lark
last late lawn lead leaf lean left lens life lift lime line link lion list live load loan lock
long loop lost loud love luck made mail main make many maps mark mask mate meal mean melt menu
mile milk mind mint miss mode moon more moss most move much must name navy near neck need nest
news next nice nine node none noon note noun oath odds once only open oval over pace pack page
pain pair palm park part past path peak pear pine pink pipe plan play plot plum pole pond pool
port post pull pure push quiz race rain rank rare read real reef rest rice rich ride ring rise
road rock role roof room root rope rose ruby rule rush safe sail salt sand save seal seed seek
self sell send shed ship shop show shut sign silk site size skip slow snow soft soil solo song
soon sort soul spot star stay stem step stop such sure swim tail take tale tall tank task team
tell tent term test text thin tide tied tile time tiny tire toll tone tool town tree trip true
tube tune turn twin type unit upon urge used user vast verb very view vine void vote wade wage
wait wake walk wall warm wash wave wear week well west whale wide wild will wind wine wing wire
wise wish wolf wood wool word work yard yarn year zero zinc zone""".split()


def password(length, symbols=True):
    alphabet = string.ascii_letters + string.digits + (string.punctuation if symbols else "")
    while True:
        pw = "".join(secrets.choice(alphabet) for _ in range(length))
        ok = any(c.islower() for c in pw) and any(c.isupper() for c in pw) and any(c.isdigit() for c in pw)
        if symbols:
            ok = ok and any(c in string.punctuation for c in pw)
        if ok:
            return pw, length * math.log2(len(alphabet))


def passphrase(n):
    words = [secrets.choice(WORDS) for _ in range(n)]
    return "-".join(words), n * math.log2(len(WORDS))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-l", "--length", type=int, default=20)
    ap.add_argument("--no-symbols", action="store_true")
    ap.add_argument("--passphrase", type=int, metavar="WORDS", help="generate N-word passphrase")
    ap.add_argument("-n", "--count", type=int, default=1)
    args = ap.parse_args()

    if not args.passphrase and args.length < 8:
        ap.error("length must be at least 8")
    for _ in range(args.count):
        pw, bits = passphrase(args.passphrase) if args.passphrase else password(args.length, not args.no_symbols)
        print(f"{pw}    (~{bits:.0f} bits entropy)")


if __name__ == "__main__":
    main()
