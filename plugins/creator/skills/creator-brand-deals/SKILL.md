---
name: creator-brand-deals
description: Help creators land and run brand deals - media kit, rate card from their own numbers, pitch emails to brands, contract red flags (usage rights, exclusivity, payment terms), and sponsorship disclosure rules for India (ASCI), Canada and the US (FTC). Use when the user asks "how much should I charge", "make my media kit", "pitch this brand", "is this contract ok", or "how do I disclose a sponsored post".
---

# Brand deals

## Media kit (1 page)
Name/handle, niche in one line, audience (top countries/cities, age, gender split from platform insights), followers per platform, median views, engagement rate, 2 to 3 best posts with numbers, past brands, contact. Use real numbers only.

## Pricing: run the script on their recent posts
```
python scripts/rates.py posts.csv --followers 25000 --cpm-low 15 --cpm-high 30
```
- Price from median views (not followers): views/1000 × CPM.
- CPM comes from their past deals, the brand's stated budget, or an agency rate card the user provides. Don't make up market rates; if they have none, give a range and tell them to test it.
- Add-ons (state them separately): usage rights for ads (priced per month of use), exclusivity (no competitor posts for X days), raw footage, extra stories/links, rush delivery.
- Bundle discounts for 3+ deliverables. Gifted-only deals are fine for growth, but the product still counts as income for tax.

## Pitch email
Under 120 words: who they are + one audience stat, why this brand fits (a real detail about the brand), one concrete content idea, a link to the media kit, a simple ask ("Open to a call next week?"). Follow up once after 5 to 7 days.

## Contract red flags (explain each one found)
- Perpetual or worldwide usage rights, or rights to use their face in ads without extra pay.
- Long exclusivity for a small fee.
- Payment terms over 30 to 45 days, or "on brand approval" with no deadline.
- Unlimited revisions; no cap on reshoots.
- Brand can edit their content or captions without approval.
- Kill fee missing (what they're paid if the brand cancels).
- Morality or claw-back clauses that are vague.
Suggest exact replacement wording. Not legal advice; for big contracts suggest a lawyer.

## Disclosure (always required for paid, gifted or affiliate posts)
- India: ASCI influencer guidelines: a clear label like #ad, #collab, #sponsored or "Paid partnership", visible upfront (not buried in hashtags); in video, say it and show it. Health/finance creators have extra qualification rules.
- US: FTC Endorsement Guides: "#ad" or "Sponsored" at the start, plus the platform's paid-partnership tool; say it in the video too.
- Canada: Ad Standards Influencer Marketing Disclosure Guidelines and the Competition Act: same idea, clear and upfront, including for gifted products and affiliate links.

For tax on brand income and gifted products, use the country skill: india-creator-tax, canada-creator-tax or us-creator-tax.
