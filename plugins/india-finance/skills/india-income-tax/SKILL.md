---
name: india-income-tax
description: Calculate Indian income tax and compare the new and old regimes for Tax Year 2026-27. Use when the user asks "how much tax will I pay", "new vs old regime", "is 12 lakh tax free", "in-hand salary", "80C", or shares a CTC or salary in rupees.
---

# Indian income tax (Tax Year 2026-27)

From 1 April 2026 the Income-tax Act, 2025 replaced the 1961 Act. "Financial year / assessment year" became one "tax year". Rates did not change. Old section numbers still appear everywhere, so mention both when useful (87A → 156, 111A → 196, 112A → 198).

## Run the script, don't do slab math by hand

```
python scripts/tax_calc.py --income 1500000 --salaried --deductions 200000
```

It prints tax under both regimes (with 4% cess, 87A rebate and marginal relief) and which is lower.

## Rules it uses

New regime (default): nil to 4L, 5% to 8L, 10% to 12L, 15% to 16L, 20% to 20L, 25% to 24L, 30% above. Standard deduction Rs 75,000. No tax up to Rs 12L taxable (Rs 12.75L gross for salaried).

Old regime (must opt out of new): nil to 2.5L, 5% to 5L, 20% to 10L, 30% above. Standard deduction Rs 50,000. Rebate up to Rs 5L taxable. Allows 80C (Rs 1.5L), 80D, HRA, home loan interest (Rs 2L), NPS 80CCD(1B) (Rs 50,000).

## Before running, ask for
- Gross annual income (not CTC: remove employer PF and gratuity).
- Salaried or not.
- Old-regime deductions, if they want a comparison.

## Not handled (say so)
- Surcharge above Rs 50L income.
- Capital gains: taxed separately at special rates, and the 87A rebate does not apply to them. Use the india-capital-gains skill.

End with: rough estimate, confirm with Form 16 / a CA.
