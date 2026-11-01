# Adding a country

Each country is two plugins: `<country>-finance` and `<country>-jobs`. Start with whichever you know best; one skill is a fine first PR.

## 1. Folders

```
plugins/<country>-finance/
  .claude-plugin/plugin.json
  skills/<country>-<topic>/SKILL.md
  skills/<country>-<topic>/scripts/<script>.py   (optional)
```

Prefix every skill name with the country (`uk-income-tax`, not `income-tax`) so skills from different countries don't clash.

## 2. plugin.json

```json
{
  "name": "uk-finance",
  "description": "One line on what it covers",
  "version": "0.1.0",
  "author": { "name": "Your Name" }
}
```

Then add the plugin to `.claude-plugin/marketplace.json` and the table in `README.md`.

## 3. SKILL.md

```markdown
---
name: uk-income-tax
description: What it does and when to use it, with the phrases people actually type ("how much tax", "ISA allowance"). Name the country so it doesn't trigger for other countries.
---

# Title

What to ask the user for, the rules with this year's numbers, how to run any script, and what's not covered.
End with a one-line "not advice, check with <official source>".
```

## 4. Rules for good skills

- Numbers must come from the official source (tax authority, budget). Put the tax year next to every limit.
- Anything that's arithmetic (tax slabs, contribution room, cost base) goes in a script, not in the model's head. Python stdlib only, with an `assert` self-check in `__main__`.
- Never let a skill invent experience on a resume or guess a user's personal tax numbers.
- Keep each SKILL.md short; it loads into the AI's context.

## 5. Check before the PR

```
claude plugin validate .
python plugins/<country>-finance/skills/<skill>/scripts/<script>.py --help
```

Then add a line running your script to `.github/workflows/check.yml` so CI tests it on every PR.

Good first countries: UK, Australia, UAE, Germany, Philippines, Nigeria. Open an issue to claim one.
