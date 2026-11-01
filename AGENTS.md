# AGENTS.md

This repo is a collection of Agent Skills for personal finance and job searching, one set per country. Each skill is a folder with a `SKILL.md` under `plugins/*/skills/`, named `<country>-<topic>`.

When a user's request matches a skill's `description` and their country, read that `SKILL.md` and follow it:

- Canada: `canada-registered-accounts`, `canada-capital-gains` (plugins/canada-finance); `canada-resume`, `canada-cover-letter`, `canada-interview-prep` (plugins/canada-jobs)
- India: `india-income-tax`, `india-capital-gains`, `india-gst`, `india-nri-return` (plugins/india-finance); `india-resume`, `india-interview-prep` (plugins/india-jobs)
- United States: `us-income-tax`, `us-retirement-accounts` (plugins/us-finance); `us-resume`, `us-interview-prep` (plugins/us-jobs)

Scripts are Python 3.9+ with no dependencies. Run them from the skill folder, e.g. `python scripts/tax_calc.py --income 1500000 --salaried`.
