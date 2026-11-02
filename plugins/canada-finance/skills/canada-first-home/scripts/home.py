"""First home in Canada: minimum down payment, CMHC premium, monthly payment, stress test, Ontario/Toronto land transfer tax.
Usage: python home.py --price 700000 --down 50000 --rate 4.5 [--years 25] [--first-time] [--toronto]
                      [--income 120000 --debts 400 --property-tax 4800 --heat 100 --condo-fee 0]
Rules as of 2026; update each January.
"""
import argparse

INSURED_CAP = 1_500_000
CMHC = [(0.15, 0.028), (0.10, 0.031), (0.05, 0.040)]  # down-payment share at least X -> premium on the loan
CMHC_30Y_SURCHARGE = 0.002
ON_LTT = [(55_000, 0.005), (250_000, 0.01), (400_000, 0.015), (2_000_000, 0.02), (float("inf"), 0.025)]
TORONTO_LTT = [(55_000, 0.005), (250_000, 0.01), (400_000, 0.015), (2_000_000, 0.02), (3_000_000, 0.025)]
ON_REBATE, TORONTO_REBATE = 4_000, 4_475
GDS_MAX, TDS_MAX = 0.39, 0.44


def slab(x, slabs):
    tax, lo = 0.0, 0
    for hi, r in slabs:
        if x > lo:
            tax += (min(x, hi) - lo) * r
        lo = hi
    return tax


def min_down(price):
    if price >= INSURED_CAP:
        return price * 0.20
    return min(price, 500_000) * 0.05 + max(price - 500_000, 0) * 0.10


def cmhc_rate(price, down, years):
    share = down / price
    if share >= 0.20:
        return 0.0
    rate = next(r for s, r in CMHC if share >= s - 1e-9)
    return rate + (CMHC_30Y_SURCHARGE if years > 25 else 0)


def payment(principal, annual_rate, years):
    """Canadian fixed-rate mortgages compound semi-annually."""
    m = (1 + annual_rate / 2) ** (1 / 6) - 1
    n = years * 12
    return principal / n if m == 0 else principal * m / (1 - (1 + m) ** -n)


def land_transfer(price, first_time, toronto):
    on = slab(price, ON_LTT)
    on_net = on - (min(on, ON_REBATE) if first_time else 0)
    if not toronto:
        return on, on_net, 0.0, 0.0
    if price > 3_000_000:
        raise ValueError("Toronto has luxury MLTT bands above $3M: check toronto.ca")
    to = slab(price, TORONTO_LTT)
    return on, on_net, to, to - (min(to, TORONTO_REBATE) if first_time else 0)


def plan(price, down, rate, years=25, first_time=False, toronto=False):
    need = min_down(price)
    if down < need - 0.5:
        raise ValueError(f"Down payment too small: minimum is ${need:,.0f}")
    if years > 25 and down / price < 0.20 and not first_time:
        raise ValueError("Insured mortgages over 25 years need a first-time buyer or a new build")
    prem_rate = cmhc_rate(price, down, years)
    premium = (price - down) * prem_rate
    loan = price - down + premium
    on, on_net, to, to_net = land_transfer(price, first_time, toronto)
    q_rate = max(rate + 0.02, 0.0525)
    return {"min_down": need, "premium_rate": prem_rate, "premium": premium, "pst_on_premium": premium * 0.08,
            "loan": loan, "monthly": payment(loan, rate, years), "qualifying_rate": q_rate,
            "qualifying_monthly": payment(loan, q_rate, years), "ontario_ltt": on, "ontario_ltt_net": on_net,
            "toronto_ltt": to, "toronto_ltt_net": to_net}


def ratios(qualifying_monthly, income, debts, property_tax, heat, condo_fee):
    housing = qualifying_monthly + property_tax / 12 + heat + condo_fee * 0.5
    gross = income / 12
    return housing / gross, (housing + debts) / gross


if __name__ == "__main__":
    # hand-checked: $700k, 10% down -> premium 3.10% of $630k = $19,530
    t = plan(700_000, 70_000, 0.045)
    assert round(t["premium"]) == 19_530 and round(t["ontario_ltt"]) == 10_475
    assert min_down(900_000) == 65_000 and min_down(1_500_000) == 300_000
    assert round(plan(700_000, 50_000, 0.045, 30, True, True)["toronto_ltt_net"]) == 6_000

    p = argparse.ArgumentParser()
    p.add_argument("--price", type=float, required=True)
    p.add_argument("--down", type=float, required=True)
    p.add_argument("--rate", type=float, required=True, help="contract rate in %, e.g. 4.5")
    p.add_argument("--years", type=int, default=25)
    p.add_argument("--first-time", action="store_true")
    p.add_argument("--toronto", action="store_true")
    p.add_argument("--income", type=float)
    p.add_argument("--debts", type=float, default=0, help="other monthly debt payments")
    p.add_argument("--property-tax", type=float, default=0, help="yearly")
    p.add_argument("--heat", type=float, default=100, help="monthly")
    p.add_argument("--condo-fee", type=float, default=0, help="monthly")
    a = p.parse_args()
    r = plan(a.price, a.down, a.rate / 100, a.years, a.first_time, a.toronto)
    print(f"Minimum down payment: ${r['min_down']:,.0f} (you have ${a.down:,.0f}, {a.down / a.price:.1%})")
    if r["premium"]:
        print(f"Mortgage insurance: {r['premium_rate']:.2%} = ${r['premium']:,.0f}, added to the loan"
              f" (in Ontario, 8% PST on it is due in cash at closing: ${r['pst_on_premium']:,.0f})")
    print(f"Mortgage: ${r['loan']:,.0f} over {a.years} years at {a.rate:g}% -> ${r['monthly']:,.2f}/month")
    print(f"Stress test at {r['qualifying_rate']:.2%}: ${r['qualifying_monthly']:,.2f}/month")
    lt = f"Ontario land transfer tax: ${r['ontario_ltt']:,.0f}"
    if a.first_time:
        lt += f", ${r['ontario_ltt_net']:,.0f} after the first-time rebate"
    print(lt)
    if a.toronto:
        print(f"Toronto land transfer tax: ${r['toronto_ltt']:,.0f}" + (f", ${r['toronto_ltt_net']:,.0f} after the rebate" if a.first_time else ""))
    cash = a.down + r["ontario_ltt_net"] + r["toronto_ltt_net"] + (r["pst_on_premium"] if r["premium"] else 0)
    print(f"Cash needed at closing (down + LTT + PST), before legal fees and inspection: ${cash:,.0f}")
    if a.income:
        gds, tds = ratios(r["qualifying_monthly"], a.income, a.debts, a.property_tax, a.heat, a.condo_fee)
        ok = gds <= GDS_MAX and tds <= TDS_MAX
        print(f"GDS {gds:.1%} (max 39%), TDS {tds:.1%} (max 44%): {'passes' if ok else 'does NOT pass'} the stress test")
