# country-skills 🌍

[![check](https://github.com/ronitgupta43-ops/country-skills/actions/workflows/check.yml/badge.svg)](https://github.com/ronitgupta43-ops/country-skills/actions/workflows/check.yml)

AI skills for money and jobs, country by country. Most finance and career skills assume you live in the US. These follow each country's real tax rules and hiring norms.

Works with Claude, Codex, Gemini CLI, Cursor, GitHub Copilot and other tools that read the open [Agent Skills](https://agentskills.io) format.

| Country | Finance | Jobs |
|---|---|---|
| 🇨🇦 Canada | TFSA/RRSP/FHSA room, ACB and capital gains, superficial loss | Canadian resume, cover letter, interview prep |
| 🇮🇳 India | Income tax new vs old regime, STCG/LTCG, returning NRI guide | Indian resume and Naukri profile, interview prep and CTC negotiation |
| Your country? | [Add it](CONTRIBUTING.md) | |

## Install

Claude Code (install only the countries you need):
```
/plugin marketplace add ronitgupta43-ops/country-skills
/plugin install canada-finance@country-skills
/plugin install canada-jobs@country-skills
/plugin install india-finance@country-skills
/plugin install india-jobs@country-skills
```

Codex, Gemini CLI, Cursor, Copilot and 30+ other agents:
```
npx skills add ronitgupta43-ops/country-skills
npx skills add ronitgupta43-ops/country-skills --skill india-income-tax   # just one skill
```

claude.ai: zip a skill folder (e.g. `plugins/india-jobs/skills/india-resume`) and upload it in Settings → Capabilities → Skills.

ChatGPT, Gemini app or any chat AI: paste the text of a `SKILL.md` into the chat (or a custom GPT / Gem), then ask your question.

## Skills

**canada-finance:** `canada-registered-accounts`, `canada-capital-gains`
**canada-jobs:** `canada-resume`, `canada-cover-letter`, `canada-interview-prep`
**india-finance:** `india-income-tax`, `india-capital-gains`, `india-nri-return`
**india-jobs:** `india-resume`, `india-interview-prep`

## Try the scripts

```
python plugins/canada-finance/skills/canada-registered-accounts/scripts/tfsa_room.py --start 2022
python plugins/canada-finance/skills/canada-capital-gains/scripts/acb.py examples/canada-trades.csv
python plugins/india-finance/skills/india-income-tax/scripts/tax_calc.py --income 1500000 --salaried
python plugins/india-finance/skills/india-capital-gains/scripts/cg.py examples/india-tradebook.csv
```

Python 3.9+, no dependencies.

## Contributing

Know your country's tax rules or job market? Add it. See [CONTRIBUTING.md](CONTRIBUTING.md). Each country is maintained by people who live there, and limits are updated after each budget.

Not financial, tax or legal advice.

MIT License
