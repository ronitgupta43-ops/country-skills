---
name: canada-registered-accounts
description: Work out TFSA, RRSP and FHSA contribution room and which account to fund first. Use when the user asks "how much TFSA room do I have", "RRSP limit", "FHSA", "TFSA vs RRSP", or is a newcomer to Canada asking where to save.
---

# Registered accounts (TFSA / RRSP / FHSA)

## Limits (update every January)

| | 2026 |
|---|---|
| TFSA yearly limit | $7,000 |
| TFSA total since 2009 (eligible every year) | $109,000 |
| RRSP dollar limit | $33,810 (2027: $35,390) |
| RRSP rule | 18% of last year's earned income, up to the dollar limit |
| FHSA | $8,000/year, $40,000 lifetime |

## TFSA room

Run the script instead of adding by hand:

```
python scripts/tfsa_room.py --start 2022 --contributed 5000 --withdrawn-before-this-year 1000
```

`--start` is the later of: the year the user turned 18, the year they became a Canadian resident, or 2009. Room only builds while they are 18+ and resident.

## RRSP room

Don't estimate it. Tell the user it's on their Notice of Assessment or CRA My Account. Newcomers have no RRSP room until they have filed a return with earned income.
Over-contributing more than $2,000 costs 1% per month on the excess.

## FHSA

- Must be a first-time home buyer, resident, 18+.
- Room starts only when the account is opened; unused room carries forward at most $8,000 (so max $16,000 in one year).
- Contributions are deductible like an RRSP; qualifying withdrawals are tax-free.
- Can be combined with the RRSP Home Buyers' Plan for the same home.

## Which first (general order, not advice)

1. Employer RRSP match, if any.
2. FHSA if they may buy a first home.
3. TFSA if income is low or they may need the money / leave Canada.
4. RRSP if income is in a higher bracket now than expected at withdrawal.

If they plan to leave Canada: TFSA contributions made while non-resident are taxed 1%/month; RRSP withdrawals as a non-resident have 25% withholding.

Always end with: check exact room in CRA My Account; this is information, not financial advice.
