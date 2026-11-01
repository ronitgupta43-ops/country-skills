"""Equity / equity MF capital gains for India (FIFO). Usage: python cg.py trades.csv
CSV columns: date,action,symbol,qty,price,charges  (action = buy/sell, date = YYYY-MM-DD)
"""
import csv
import sys
from collections import defaultdict, deque
from datetime import date


def run(rows):
    lots = defaultdict(deque)  # symbol -> [qty, cost per unit, buy date]
    stcg, ltcg = defaultdict(float), defaultdict(float)
    for r in sorted(rows, key=lambda r: r["date"]):
        s, q, px = r["symbol"].upper(), float(r["qty"]), float(r["price"])
        fee, d = float(r.get("charges") or 0), date.fromisoformat(r["date"])
        if r["action"].lower() == "buy":
            lots[s].append([q, px + fee / q, d])
            continue
        fy = d.year if d.month >= 4 else d.year - 1  # tax year starts 1 April
        net_px = px - fee / q
        while q > 1e-9:
            if not lots[s]:
                raise ValueError(f"{r['date']}: selling more {s} than held")
            lot = lots[s][0]
            used = min(q, lot[0])
            gain = used * (net_px - lot[1])
            b = lot[2]  # long term if held more than 12 months
            (ltcg if (d.year, d.month, d.day) > (b.year + 1, b.month, b.day) else stcg)[fy] += gain
            lot[0] -= used
            q -= used
            if lot[0] <= 1e-9:
                lots[s].popleft()
    return stcg, ltcg


def tax(stcg, ltcg):
    # ponytail: losses set off simply (STCL against STCG then LTCG); no carry-forward
    if stcg < 0:
        ltcg, stcg = ltcg + stcg, 0
    return round((max(stcg, 0) * .20 + max(ltcg - 125000, 0) * .125) * 1.04)


if __name__ == "__main__":
    t = [{"date": "2025-01-10", "action": "buy", "symbol": "INFY", "qty": "100", "price": "1500"},
         {"date": "2026-06-01", "action": "buy", "symbol": "INFY", "qty": "50", "price": "1600"},
         {"date": "2026-07-01", "action": "sell", "symbol": "INFY", "qty": "120", "price": "1700"}]
    s, l = run(t)
    assert l[2026] == 20000 and s[2026] == 2000  # FIFO: 100 old lots long term, 20 new lots short term
    assert tax(2000, 20000) == round(400 * 1.04)

    with open(sys.argv[1], newline="") as f:
        stcg, ltcg = run(list(csv.DictReader(f)))
    for fy in sorted(set(stcg) | set(ltcg)):
        print(f"Tax year {fy}-{str(fy + 1)[2:]}: STCG Rs {stcg[fy]:,.0f}, LTCG Rs {ltcg[fy]:,.0f}, "
              f"est. tax incl. cess Rs {tax(stcg[fy], ltcg[fy]):,.0f}")
