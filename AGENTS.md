# AGENTS.md

This repo is a collection of Agent Skills for Canadian personal finance and job searching. Each skill is a folder with a `SKILL.md` under `plugins/*/skills/`.

When a user's request matches a skill's `description`, read that `SKILL.md` and follow it:

- `plugins/canada-finance/skills/registered-accounts` — TFSA/RRSP/FHSA room and rules
- `plugins/canada-finance/skills/capital-gains` — ACB, capital gains, superficial loss
- `plugins/canada-jobs/skills/canadian-resume` — Canadian-format resumes
- `plugins/canada-jobs/skills/cover-letter` — tailored cover letters
- `plugins/canada-jobs/skills/interview-prep` — interview questions, STAR answers, mock interviews

Scripts are Python 3.9+ with no dependencies. Run them from the skill folder, e.g. `python scripts/tfsa_room.py --start 2022`.
