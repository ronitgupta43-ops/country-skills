---
name: canada-capital-gains
description: Adjusted cost base (average cost), realized capital gains/losses per year and superficial loss warnings for a Canadian non-registered account. Use when the user asks "what's my ACB", "how much tax if I sell", "capital gains", "superficial loss", or uploads a trades CSV.
---

# Capital gains (non-registered account)

## Input

A CSV with columns `date,action,symbol,qty,price,fees` (action = buy or sell, date = YYYY-MM-DD, prices in CAD). If the user's broker export looks different (Wealthsimple, Questrade, Coinbase), rename the columns to match first. Convert USD trades to CAD at the Bank of Canada rate for the trade date.

## Run

```
python scripts/acb.py trades.csv
```

It prints ACB per share for each holding, realized gain/loss per year, and flags any loss that may be superficial.

## Rules the script uses

- ACB is average cost: (total cost incl. fees) / shares. Selling doesn't change ACB per share.
- Gain = proceeds - fees - ACB of shares sold.
- 50% of a net capital gain is taxable (inclusion rate).
- Superficial loss: a loss is denied if the same security was bought within 30 days before or after the sale (by the user or a spouse) and is still held 30 days after. The denied loss is added to the ACB of the new shares.

## After running

- For flagged losses, explain the rule and that the loss gets added to the ACB of the repurchased shares, not lost forever.
- Gains in TFSA/RRSP/FHSA are not taxed; this is only for non-registered accounts.
- Say this is an estimate; the user should check against their T5008 slips.
