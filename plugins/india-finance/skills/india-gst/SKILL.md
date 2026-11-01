---
name: india-gst
description: Indian GST for small businesses and freelancers - GST 2.0 rates, whether to register, CGST/SGST vs IGST on an invoice, GSTIN validation and return due dates. Use when the user asks "do I need GST registration", "how much GST to charge", "check this GSTIN", "GSTR-1/3B due date", or "composition scheme".
---

# GST (India)

## Rates: GST 2.0, from 22 September 2025
The 12% and 28% slabs were removed. Main slabs are 5% (essentials, processed food, many textiles) and 18% (most goods and services, including IT, consulting, design, SaaS), plus 40% for luxury and sin goods. Special rates: 3% gold/silver, 0.25% rough diamonds. Many essentials, healthcare, education and individual health/life insurance are 0% or exempt.
Always confirm the exact rate for the HSN (goods) or SAC (services) code; don't guess a product's slab.

## Calculations: use the script
```
python scripts/gst.py calc 50000 18 --from 07 --to 07           # Delhi to Delhi: CGST + SGST
python scripts/gst.py calc 50000 18 --from 07 --to 29           # Delhi to Karnataka: IGST
python scripts/gst.py calc 59000 18 --from 07 --to 07 --inclusive
python scripts/gst.py check 27AAPFU0939F1ZV
```
- Same state = CGST + SGST (half each). Different state, export or SEZ = IGST.
- Exports of services are zero-rated (file a LUT to invoice without IGST).
- GSTIN check only proves the format and check character are right. Tell the user to confirm it's active on the GST portal (Search Taxpayer).

## Registration
- Mandatory above aggregate turnover of Rs 40 lakh (goods) or Rs 20 lakh (services); Rs 20 lakh / Rs 10 lakh in special category states.
- Mandatory from day one for inter-state supply of goods, selling through e-commerce operators, and reverse-charge liability.
- Freelancers serving foreign clients only: exports count toward turnover; registration plus LUT is common once over the threshold.
- Voluntary registration helps when B2B clients want input tax credit.

## Composition scheme
Turnover up to Rs 1.5 crore (goods; lower for services). Flat low rate (1% traders/manufacturers, 5% restaurants, 6% services), no input tax credit, can't charge GST on the bill, no inter-state sales. Files CMP-08 quarterly and GSTR-4 yearly.

## Returns
- GSTR-1 (sales): 11th of next month; quarterly filers (QRMP, turnover up to Rs 5 crore) by the 13th after the quarter.
- GSTR-3B (summary + payment): 20th of next month (22nd/24th for QRMP depending on state).
- GSTR-9 annual: 31 December.
- Late fee and 18% p.a. interest on unpaid tax. Many 3B fields are now auto-filled from GSTR-1 and locked; fix errors through GSTR-1/1A.

## A valid tax invoice has
Supplier name, address and GSTIN; invoice number (new series each tax year) and date; buyer GSTIN for B2B; HSN/SAC; taxable value; rate and CGST/SGST or IGST amounts; place of supply; signature.

End with: rates and dates change by notification; confirm on gst.gov.in or with a CA.
