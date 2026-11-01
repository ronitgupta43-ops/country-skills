"""US federal income tax, tax year 2026 (filed in 2027).
Usage: python us_tax.py --wages 85000 [--status mfj] [--ltcg 5000] [--deductions 0] [--magi 160000]
--deductions: itemized total; the larger of this or the standard deduction is used.
--magi: also print the 2026 Roth IRA contribution limit for that income.
"""
import argparse

INF = float("inf")
# Rev. Proc. 2025-32
BRACKETS = {
    "single": [(12400, .10), (50400, .12), (105700, .22), (201775, .24), (256225, .32), (640600, .35), (INF, .37)],
    "mfj": [(24800, .10), (100800, .12), (211400, .22), (403550, .24), (512450, .32), (768700, .35), (INF, .37)],
}
STD = {"single": 16100, "mfj": 32200}
LTCG = {"single": (49450, 545500), "mfj": (98900, 613700)}  # top of 0% and 15% bands
ROTH = {"single": (153000, 168000), "mfj": (242000, 252000)}  # Notice 2025-67
IRA_LIMIT = 7500


def bracket_tax(x, brackets):
    tax, low = 0.0, 0
    for high, rate in brackets:
        if x > low:
            tax += (min(x, high) - low) * rate
        low = high
    return tax


def federal_tax(wages, status="single", ltcg=0.0, deductions=0.0):
    """Ordinary income taxed by bracket; long-term gains stacked on top at 0/15/20%."""
    taxable = max(wages + ltcg - max(STD[status], deductions), 0)
    ordinary = max(taxable - ltcg, 0)
    gains = taxable - ordinary
    t0, t15 = LTCG[status]
    at0 = max(min(gains, t0 - ordinary), 0)
    at15 = max(min(gains - at0, t15 - ordinary - at0), 0)
    at20 = gains - at0 - at15
    # ponytail: no NIIT (3.8% above $200k/$250k MAGI), credits, AMT, state tax or HoH/MFS status
    return taxable, round(bracket_tax(ordinary, BRACKETS[status]) + at15 * .15 + at20 * .20, 2)


def roth_limit(magi, status="single", age50=False):
    full = IRA_LIMIT + (1100 if age50 else 0)
    lo, hi = ROTH[status]
    if magi <= lo:
        return full
    if magi >= hi:
        return 0
    amt = full * (hi - magi) / (hi - lo)
    amt = -(-amt // 10) * 10  # IRS rounds up to the next $10
    return max(amt, 200)  # minimum $200 while inside the phase-out


if __name__ == "__main__":
    assert bracket_tax(70000, BRACKETS["single"]) == 10112  # matches published 2026 example
    assert round(bracket_tax(640600, BRACKETS["single"]), 2) == 192979.25  # Rev. Proc. table
    assert federal_tax(16100)[1] == 0
    assert federal_tax(40000, ltcg=10000)[1] == round(bracket_tax(23900, BRACKETS["single"]) + 0, 2)  # all gains in 0% band
    assert roth_limit(100000) == 7500 and roth_limit(170000) == 0 and roth_limit(160500) == 3750

    p = argparse.ArgumentParser()
    p.add_argument("--wages", type=float, required=True, help="wages + other ordinary income")
    p.add_argument("--status", choices=["single", "mfj"], default="single")
    p.add_argument("--ltcg", type=float, default=0, help="long-term gains + qualified dividends")
    p.add_argument("--deductions", type=float, default=0)
    p.add_argument("--magi", type=float)
    p.add_argument("--age50", action="store_true")
    a = p.parse_args()
    taxable, tax = federal_tax(a.wages, a.status, a.ltcg, a.deductions)
    gross = a.wages + a.ltcg
    print(f"Taxable income ${taxable:,.0f}, federal income tax ${tax:,.2f} (effective {tax / gross:.1%} of ${gross:,.0f})" if gross else "No income")
    if a.magi is not None:
        print(f"2026 Roth IRA contribution allowed: ${roth_limit(a.magi, a.status, a.age50):,.0f}")
