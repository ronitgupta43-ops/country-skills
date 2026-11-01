# canada-claude-skills 🇨🇦

Claude skills for life in Canada: money and jobs. Most finance and career skills on GitHub assume the US. These follow CRA rules and Canadian hiring norms.

## Install (Claude Code)

```
/plugin marketplace add ronitgupta43-ops/canada-claude-skills
/plugin install canada-finance@canada-claude-skills
/plugin install canada-jobs@canada-claude-skills
```

For claude.ai: zip any folder under `plugins/*/skills/` and upload it in Settings → Capabilities → Skills.

## Install (Codex, Gemini CLI, Cursor, GitHub Copilot and 30+ other agents)

The skills use the open [Agent Skills](https://agentskills.io) format, so the same files work in other AI tools:

```
npx skills add ronitgupta43-ops/canada-claude-skills            # pick agents interactively
npx skills add ronitgupta43-ops/canada-claude-skills -a codex   # or: gemini-cli, cursor, github-copilot
```

Manual install: copy a skill folder (e.g. `plugins/canada-jobs/skills/canadian-resume`) into your agent's skills folder — `~/.codex/skills/`, `~/.gemini/skills/`, `.cursor/skills/` or `.github/skills/`.

**ChatGPT, Gemini app or any chat AI without skills:** paste the text of a `SKILL.md` into a custom GPT, Gem or the chat itself, then ask your question.

## What's inside

### canada-finance
| Skill | What it does |
|---|---|
| `registered-accounts` | TFSA room calculator, RRSP and FHSA rules, which account to fund first, notes for newcomers and people leaving Canada |
| `capital-gains` | ACB (average cost) from a trades CSV, realized gains per year, superficial loss warnings |

### canada-jobs
| Skill | What it does |
|---|---|
| `canadian-resume` | Converts a resume to Canadian format and tailors it to a posting (ATS keywords) |
| `cover-letter` | Short, specific cover letters without the filler |
| `interview-prep` | Likely questions, STAR answers from your own experience, mock interviews, bank-role pack |

## Try the scripts

```
python plugins/canada-finance/skills/registered-accounts/scripts/tfsa_room.py --start 2022
python plugins/canada-finance/skills/capital-gains/scripts/acb.py examples/trades.csv
```

Python 3.9+, no dependencies.

## Related

[canada-tax-toolkit](https://github.com/ronitgupta43-ops/canada-tax-toolkit) — Ontario income tax, CPP and EI calculator.

## Contributing

PRs welcome — especially other provinces, Quebec rules, and broker CSV converters. Update the limits in `tfsa_room.py` and `registered-accounts/SKILL.md` each January.

Not financial, tax or legal advice.

MIT License
