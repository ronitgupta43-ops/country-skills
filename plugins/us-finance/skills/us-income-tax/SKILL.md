---
name: us-income-tax
description: Estimate US federal income tax for 2026 including long-term capital gains, and capital gains rules (holding period, wash sale, loss limit). Use when the user asks "how much federal tax will I owe", "what tax bracket am I in", "tax on selling stock", "wash sale", or gives a US salary.
---

# US federal income tax (tax year 2026)

## Run the script
```
python scripts/us_tax.py --wages 85000 --ltcg 4000
python scripts/us_tax.py --wages 150000 --status mfj --deductions 35000
```
It applies the standard or itemized deduction (whichever is larger), the 2026 brackets, and stacks long-term gains on top at 0/15/20%.

## 2026 numbers (Rev. Proc. 2025-32)
- Brackets: 10, 12, 22, 24, 32, 35, 37%. 37% starts above $640,600 single / $768,700 married filing jointly.
- Standard deduction: $16,100 single, $32,200 MFJ, $24,150 head of household.
- Long-term gains (held more than 1 year): 0% up to $49,450 taxable income single / $98,900 MFJ; 15% up to $545,500 / $613,700; 20% above.
- Short-term gains are taxed as ordinary income.

## Capital gains rules
- Wash sale: a loss is disallowed if you buy the same or a substantially identical security within 30 days before or after the sale (IRAs included); the loss is added to the new shares' basis.
- Net capital losses offset up to $3,000 of ordinary income a year; the rest carries forward.
- Brokers report on Form 1099-B; check cost basis is filled in.

## Not handled (say so)
NIIT (3.8% on investment income above $200k single / $250k MFJ MAGI), state and FICA taxes, credits (child tax credit etc.), AMT, self-employment tax, head of household and married-filing-separately brackets.

End with: estimate only; confirm with tax software or a CPA.
