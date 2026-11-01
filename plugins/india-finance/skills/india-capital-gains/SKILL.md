---
name: india-capital-gains
description: STCG and LTCG on Indian listed shares and equity mutual funds using FIFO, with the Rs 1.25 lakh exemption. Use when the user asks "how much tax if I sell", "LTCG", "STCG", "tax harvesting", or uploads a Zerodha/Groww/Upstox tradebook or capital gains statement.
---

# Capital gains on Indian equity

## Input
A CSV with `date,action,symbol,qty,price,charges`. Broker tradebooks (Zerodha Console, Groww, Upstox) have similar columns: rename them to match. For mutual funds use the CAS from CAMS/KFintech; each purchase is a lot.

## Run
```
python scripts/cg.py trades.csv
```
Prints STCG, LTCG and estimated tax per tax year (April to March).

## Rules (unchanged for 2026-27)
- FIFO: the oldest shares are sold first (that's how demat works).
- Held more than 12 months = long term.
- STCG on listed equity / equity MF (STT paid): 20%.
- LTCG: 12.5% on gains above Rs 1.25 lakh per year, no indexation.
- 4% cess on top. The 87A rebate does not apply to these gains.
- Short-term loss can be set off against STCG or LTCG; long-term loss only against LTCG. Unused losses carry forward 8 years if the return is filed on time.
- Share buybacks are taxed as capital gains from 2026-27 (not dividends).

## Not covered
Debt funds bought after 1 April 2023 (taxed at slab rate), property, gold, F&O and intraday (business income). Say so if asked.

## Useful tip
Tax harvesting: selling and rebuying long-term holdings before 31 March to book up to Rs 1.25 lakh LTCG tax-free each year. India has no superficial-loss rule like Canada or the US, but mention that rebuying costs brokerage and STT.
