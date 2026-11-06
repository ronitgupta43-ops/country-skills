"""RSUs and foreign shares for an Indian resident: perquisite at vest, capital gains on sale (FIFO), Schedule FA holdings.
Usage: python rsu.py events.csv [--slab 30]
events.csv columns: date,type,shares,price,rate
  type  vest  price = FMV per share on the vest date (foreign currency); rate = the rupee rate your employer used
        buy   price = price paid per share; rate = SBI TT buying rate used for the purchase
        sell  price = sale price per share; rate = SBI TT buying rate on the last day of the month before the sale month
Rules as of Tax Year 2026-27; update each year.
"""
import argparse
import csv
from datetime import date

LTCG_RATE = 0.125
CESS = 0.04


def inr(x):
    """Indian digit grouping: 12,34,567."""
    n = f"{abs(round(x)):d}"
    head, tail = n[:-3], n[-3:]
    while len(head) > 2:
        tail = head[-2:] + "," + tail
        head = head[:-2]
    return ("-" if x < 0 else "") + "Rs " + (head + "," + tail if head else tail)


def tax_year(d):
    return f"{d.year}-{(d.year + 1) % 100:02d}" if d.month >= 4 else f"{d.year - 1}-{d.year % 100:02d}"


def long_term(bought, sold):
    """More than 24 months."""
    y, m = bought.year + 2, bought.month
    try:
        cutoff = bought.replace(year=y)
    except ValueError:  # 29 Feb
        cutoff = date(y, m, 28)
    return sold > cutoff


def run(events):
    lots, years, holdings = [], {}, {}
    for e in sorted(events, key=lambda e: e["date"]):
        y = years.setdefault(tax_year(e["date"]), {"perquisite": 0.0, "stcg": 0.0, "ltcg": 0.0})
        if e["type"] in ("vest", "buy"):
            inr = e["shares"] * e["price"] * e["rate"]
            if e["type"] == "vest":
                y["perquisite"] += inr
            lots.append({"date": e["date"], "shares": e["shares"], "cost_each": inr / e["shares"]})
        elif e["type"] == "sell":
            left, proceeds_each = e["shares"], e["price"] * e["rate"]
            while left > 1e-9:
                if not lots:
                    raise ValueError(f"{e['date']}: selling more shares than you hold")
                lot = lots[0]
                n = min(left, lot["shares"])
                gain = n * (proceeds_each - lot["cost_each"])
                y["ltcg" if long_term(lot["date"], e["date"]) else "stcg"] += gain
                lot["shares"] -= n
                left -= n
                if lot["shares"] <= 1e-9:
                    lots.pop(0)
        else:
            raise ValueError(f"unknown type {e['type']}")
        held = sum(l["shares"] for l in lots)
        holdings[e["date"].year] = (held, sum(l["shares"] * l["cost_each"] for l in lots))
    return years, holdings


def net(stcg, ltcg):
    """Short-term loss can reduce long-term gain; long-term loss only carries forward."""
    if stcg < 0 and ltcg > 0:
        used = min(-stcg, ltcg)
        return stcg + used, ltcg - used
    return stcg, ltcg


if __name__ == "__main__":
    # hand-checked: 100 vest at $200 x 85 = 17,00,000; sell 40 at $250 x 86 within 24 months -> STCG 40 x (21,500 - 17,000) = 1,80,000
    ys, _ = run([{"date": date(2025, 6, 15), "type": "vest", "shares": 100, "price": 200, "rate": 85},
                 {"date": date(2026, 9, 1), "type": "sell", "shares": 40, "price": 250, "rate": 86}])
    assert round(ys["2025-26"]["perquisite"]) == 1_700_000 and round(ys["2026-27"]["stcg"]) == 180_000
    assert long_term(date(2024, 1, 10), date(2026, 1, 11)) and not long_term(date(2024, 1, 10), date(2026, 1, 10))
    assert net(-50, 200) == (0, 150)
    assert inr(1404050) == "Rs 14,04,050" and inr(-28500) == "-Rs 28,500"

    p = argparse.ArgumentParser()
    p.add_argument("csv")
    p.add_argument("--slab", type=float, help="your top slab rate in percent, to estimate tax on short-term gains")
    a = p.parse_args()
    with open(a.csv, newline="") as f:
        events = [{"date": date.fromisoformat(r["date"]), "type": r["type"].strip().lower(), "shares": float(r["shares"]),
                   "price": float(r["price"]), "rate": float(r["rate"])} for r in csv.DictReader(f)]
    years, holdings = run(events)
    for ty, y in sorted(years.items()):
        st, lt = net(y["stcg"], y["ltcg"])
        if not (y["perquisite"] or y["stcg"] or y["ltcg"]):
            continue
        print(f"\nTax Year {ty}")
        if y["perquisite"]:
            print(f"  Perquisite at vest (salary, check it matches Form 16): {inr(y['perquisite'])}")
        if y["stcg"] or y["ltcg"]:
            print(f"  Short-term gain (held 24 months or less, slab rate): {inr(st)}")
            print(f"  Long-term gain (held over 24 months, 12.5%, no Rs 1.25 lakh exemption): {inr(lt)}")
            if lt > 0:
                print(f"    Tax at 12.5% + 4% cess: {inr(lt * LTCG_RATE * (1 + CESS))}")
            if st > 0 and a.slab:
                print(f"    Tax at {a.slab:g}% + 4% cess: {inr(st * a.slab / 100 * (1 + CESS))}")
            if lt < 0:
                print("    Long-term loss: set off only against long-term gains; carry forward up to 8 years if you file on time")
    print("\nSchedule FA (calendar year, Table A3): shares held at year end and their cost")
    for yr, (n, cost) in sorted(holdings.items()):
        print(f"  {yr}: {n:g} shares, initial value (cost) {inr(cost)}; add the peak and 31 December values from your broker")
