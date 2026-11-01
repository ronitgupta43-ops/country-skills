# country-skills 🌍

[![check](https://github.com/ronitgupta43-ops/country-skills/actions/workflows/check.yml/badge.svg)](https://github.com/ronitgupta43-ops/country-skills/actions/workflows/check.yml)

AI skills for money, jobs and content creators, country by country. Most finance and career skills assume you live in the US. These follow each country's real tax rules and hiring norms.

Works with Claude, Codex, Gemini CLI, Cursor, GitHub Copilot and other tools that read the open [Agent Skills](https://agentskills.io) format.

| Country | Finance | Jobs |
|---|---|---|
| 🇨🇦 Canada | TFSA/RRSP/FHSA room, ACB and capital gains, superficial loss | Canadian resume, cover letter, interview prep |
| 🇮🇳 India | Income tax new vs old regime, STCG/LTCG, GST and GSTIN check, returning NRI guide | Indian resume and Naukri profile, interview prep and CTC negotiation |
| 🇺🇸 United States | Federal tax and capital gains (2026), 401(k)/IRA/Roth limits | US resume and cover letter, interview prep and offer negotiation |
| Your country? | [Add it](CONTRIBUTING.md) | |

**For creators 🎥** (any country): hooks, captions and scripts in English, Hindi, Punjabi or Hinglish; content calendars with Indian, Canadian and US festivals; repurposing one video into many posts; media kits, rate cards, pitch emails, contract red flags and #ad disclosure rules. Plus creator tax for each country: TDS on gifted products and GST in India, HST and PR packages in Canada, 1099s and self-employment tax in the US.

## Install

Claude Code (install only the countries you need):
```
/plugin marketplace add ronitgupta43-ops/country-skills
/plugin install canada-finance@country-skills
/plugin install canada-jobs@country-skills
/plugin install india-finance@country-skills
/plugin install india-jobs@country-skills
/plugin install us-finance@country-skills
/plugin install us-jobs@country-skills
/plugin install creator@country-skills
```

Codex, Gemini CLI, Cursor, Copilot and 30+ other agents:
```
npx skills add ronitgupta43-ops/country-skills
npx skills add ronitgupta43-ops/country-skills --skill india-income-tax   # just one skill
```

claude.ai: zip a skill folder (e.g. `plugins/india-jobs/skills/india-resume`) and upload it in Settings → Capabilities → Skills.

ChatGPT, Gemini app or any chat AI: paste the text of a `SKILL.md` into the chat (or a custom GPT / Gem), then ask your question.

## Skills

**canada-finance:** `canada-registered-accounts`, `canada-capital-gains`, `canada-creator-tax`
**canada-jobs:** `canada-resume`, `canada-cover-letter`, `canada-interview-prep`
**india-finance:** `india-income-tax`, `india-capital-gains`, `india-gst`, `india-creator-tax`, `india-nri-return`
**india-jobs:** `india-resume`, `india-interview-prep`
**us-finance:** `us-income-tax`, `us-retirement-accounts`, `us-creator-tax`
**us-jobs:** `us-resume`, `us-interview-prep`
**creator:** `creator-content-writer`, `creator-content-plan`, `creator-brand-deals`

## Try the scripts

```
python plugins/canada-finance/skills/canada-registered-accounts/scripts/tfsa_room.py --start 2022
python plugins/canada-finance/skills/canada-capital-gains/scripts/acb.py examples/canada-trades.csv
python plugins/india-finance/skills/india-income-tax/scripts/tax_calc.py --income 1500000 --salaried
python plugins/india-finance/skills/india-capital-gains/scripts/cg.py examples/india-tradebook.csv
python plugins/india-finance/skills/india-gst/scripts/gst.py calc 50000 18 --from 07 --to 29
python plugins/us-finance/skills/us-income-tax/scripts/us_tax.py --wages 85000 --ltcg 4000
python plugins/creator/skills/creator-brand-deals/scripts/rates.py examples/creator-posts.csv --followers 25000 --cpm-low 15 --cpm-high 30
```

Python 3.9+, no dependencies.

## Contributing

Know your country's tax rules or job market? Add it. See [CONTRIBUTING.md](CONTRIBUTING.md). Each country is maintained by people who live there, and limits are updated after each budget.

Not financial, tax or legal advice.

MIT License
