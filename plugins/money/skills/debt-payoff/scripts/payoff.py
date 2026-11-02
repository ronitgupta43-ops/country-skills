"""Debt payoff plan: avalanche (highest rate first) vs snowball (smallest balance first).
Usage: python payoff.py debts.csv --budget 1200
debts.csv columns: name,balance,rate,min_payment   (rate = yearly %, e.g. 20.99)
Works in any currency. Interest is charged monthly at rate/12.
"""
import argparse
import csv


def simulate(debts, budget, order):
    debts = [dict(d) for d in debts]
    if budget < sum(d["min_payment"] for d in debts):
        raise ValueError("Budget is below the total minimum payments")
    month, interest, paid_off = 0, 0.0, []
    while any(d["balance"] > 0.005 for d in debts):
        month += 1
        if month > 1200:
            raise ValueError("Not paid off in 100 years: the budget doesn't cover the interest")
        for d in debts:
            if d["balance"] > 0:
                i = d["balance"] * d["rate"] / 100 / 12
                d["balance"] += i
                interest += i
        left = budget
        for d in debts:  # minimums first
            pay = min(d["min_payment"], d["balance"])
            d["balance"] -= pay
            left -= pay
        for d in sorted((d for d in debts if d["balance"] > 0.005), key=order):  # extra goes to the target
            pay = min(left, d["balance"])
            d["balance"] -= pay
            left -= pay
        for d in debts:
            if d["balance"] <= 0.005 and d["name"] not in [n for n, _ in paid_off]:
                paid_off.append((d["name"], month))
    return month, interest, paid_off


AVALANCHE = lambda d: -d["rate"]
SNOWBALL = lambda d: d["balance"]


if __name__ == "__main__":
    # hand-checked: one 12% debt of 1,000 paid 100/month -> 11 months, 58.98 interest
    m, i, _ = simulate([{"name": "a", "balance": 1000, "rate": 12, "min_payment": 100}], 100, AVALANCHE)
    assert m == 11 and abs(i - 58.98) < 0.01

    p = argparse.ArgumentParser()
    p.add_argument("csv")
    p.add_argument("--budget", type=float, required=True, help="total paid toward all debts each month")
    a = p.parse_args()
    with open(a.csv, newline="") as f:
        debts = [{"name": r["name"], "balance": float(r["balance"]), "rate": float(r["rate"]),
                  "min_payment": float(r["min_payment"])} for r in csv.DictReader(f)]
    print(f"Total debt {sum(d['balance'] for d in debts):,.2f}, paying {a.budget:,.2f} a month")
    results = {}
    for label, order in (("Avalanche (highest rate first)", AVALANCHE), ("Snowball (smallest balance first)", SNOWBALL)):
        months, interest, order_done = simulate(debts, a.budget, order)
        results[label] = interest
        print(f"\n{label}: debt-free in {months} months ({months // 12}y {months % 12}m), interest {interest:,.2f}")
        print("  Paid off: " + ", ".join(f"{n} (month {m})" for n, m in order_done))
    (b, bi), (w, wi) = sorted(results.items(), key=lambda kv: kv[1])
    print(f"\n{b.split(' (')[0]} saves {wi - bi:,.2f} in interest.")
