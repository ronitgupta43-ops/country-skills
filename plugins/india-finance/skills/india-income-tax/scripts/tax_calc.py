"""Indian income tax, new vs old regime, Tax Year 2026-27 (FY 2026-27).
Usage: python tax_calc.py --income 1500000 [--salaried] [--deductions 200000]
--deductions = old-regime deductions (80C, 80D, HRA, home loan interest...). Ignored for the new regime.
"""
import argparse

NEW = [(400000, 0), (800000, .05), (1200000, .10), (1600000, .15), (2000000, .20), (2400000, .25), (float("inf"), .30)]
OLD = [(250000, 0), (500000, .05), (1000000, .20), (float("inf"), .30)]


def slab_tax(income, slabs):
    tax, low = 0, 0
    for high, rate in slabs:
        if income > low:
            tax += (min(income, high) - low) * rate
        low = high
    return tax


def regime_tax(gross, salaried, deductions, new):
    taxable = max(gross - (75000 if new else 50000) * salaried - (0 if new else deductions), 0)
    tax = slab_tax(taxable, NEW if new else OLD)
    limit = 1200000 if new else 500000
    if taxable <= limit:  # section 87A rebate (s.156 of the 2025 Act)
        tax = 0
    elif new:  # marginal relief just above 12 lakh
        tax = min(tax, taxable - limit)
    # ponytail: no surcharge (income above 50 lakh) and no special-rate income (capital gains)
    return taxable, round(tax * 1.04)  # 4% health and education cess


if __name__ == "__main__":
    assert regime_tax(1275000, True, 0, True)[1] == 0
    assert regime_tax(1210000, False, 0, True)[1] == round(10000 * 1.04)  # marginal relief
    assert regime_tax(2000000, False, 0, True)[1] == round(200000 * 1.04)
    assert regime_tax(1000000, False, 0, False)[1] == round(112500 * 1.04)
    p = argparse.ArgumentParser()
    p.add_argument("--income", type=float, required=True, help="gross annual income in rupees")
    p.add_argument("--salaried", action="store_true", help="apply standard deduction")
    p.add_argument("--deductions", type=float, default=0, help="old-regime deductions")
    a = p.parse_args()
    if a.income > 5000000:
        print("Note: income above 50 lakh attracts surcharge, not included here.")
    res = {name: regime_tax(a.income, a.salaried, a.deductions, new) for name, new in (("New regime", True), ("Old regime", False))}
    for name, (taxable, tax) in res.items():
        print(f"{name}: taxable Rs {taxable:,.0f}, tax incl. cess Rs {tax:,.0f}")
    best = min(res, key=lambda k: res[k][1])
    print(f"Lower tax: {best} (saves Rs {abs(res['New regime'][1] - res['Old regime'][1]):,.0f})")
