"""India GST helper.
  python gst.py check 27AAPFU0939F1ZV                       # validate a GSTIN
  python gst.py calc 10000 18 --from 27 --to 29             # tax on a price (exclusive)
  python gst.py calc 11800 18 --from 27 --to 27 --inclusive # split a GST-inclusive price
"""
import argparse
import re

A = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
RATES = {0, 0.25, 3, 5, 18, 40}  # GST 2.0, from 22 Sep 2025


def gstin_ok(g):
    g = g.strip().upper()
    if not re.fullmatch(r"\d{2}[A-Z]{5}\d{4}[A-Z][1-9A-Z]Z[0-9A-Z]", g):
        return False, "wrong format (2-digit state + PAN + entity no. + Z + check char)"
    s = 0
    for i, c in enumerate(g[:14]):
        p = A.index(c) * (2 if i % 2 else 1)
        s += p // 36 + p % 36
    if A[(36 - s % 36) % 36] != g[14]:
        return False, "check character doesn't match (typo or fake GSTIN)"
    return True, f"valid format, state code {g[:2]}, PAN {g[2:12]}"


def calc(amount, rate, same_state, inclusive=False):
    base = amount / (1 + rate / 100) if inclusive else amount
    tax = base * rate / 100
    split = {"CGST": tax / 2, "SGST/UTGST": tax / 2} if same_state else {"IGST": tax}
    return round(base, 2), {k: round(v, 2) for k, v in split.items()}, round(base + tax, 2)


if __name__ == "__main__":
    assert gstin_ok("27AAPFU0939F1ZV")[0] and gstin_ok("29AAGCB7383J1Z4")[0]
    assert not gstin_ok("27AAPFU0939F1ZA")[0]
    assert calc(10000, 18, False) == (10000, {"IGST": 1800}, 11800)
    assert calc(11800, 18, True, inclusive=True) == (10000, {"CGST": 900, "SGST/UTGST": 900}, 11800)

    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check"); c.add_argument("gstin")
    k = sub.add_parser("calc"); k.add_argument("amount", type=float); k.add_argument("rate", type=float)
    k.add_argument("--from", dest="src", required=True, help="supplier state code, e.g. 27"); k.add_argument("--to", required=True, help="place of supply state code")
    k.add_argument("--inclusive", action="store_true")
    a = p.parse_args()
    if a.cmd == "check":
        ok, msg = gstin_ok(a.gstin)
        print(("OK: " if ok else "INVALID: ") + msg)
    else:
        if a.rate not in RATES:
            print(f"Note: {a.rate}% isn't a current GST 2.0 rate ({sorted(RATES)}). Check the HSN/SAC rate.")
        base, split, total = calc(a.amount, a.rate, a.src == a.to, a.inclusive)
        print(f"Taxable value Rs {base:,.2f}")
        for name, v in split.items():
            print(f"{name}: Rs {v:,.2f}")
        print(f"Invoice total Rs {total:,.2f}")
