# Handoff  (updated 2026-11-02)

## What this repo is
Free, MIT-licensed AI skills for tax, money, jobs, creators and crypto in India, Canada and the US. 27 skills in 9 plugins. Works in Claude Code, the Claude app, Codex, Gemini, Cursor and Copilot. Goal: GitHub stars and an application to Claude for Open Source.

## Layout
- plugins/<plugin>/skills/<skill>/SKILL.md - the skills; scripts/ beside them hold the calculators
- .claude-plugin/marketplace.json, plugins/*/.claude-plugin/plugin.json - Claude Code marketplace
- AGENTS.md - entry point for non-Claude agents
- examples/*.csv - sample inputs the scripts and CI run on
- tools/build.py - embeds each script into its SKILL.md (`<!-- embed: path -->`) and writes the skill tree into README.md and AGENTS.md
- site-src/*.html - website page bodies; tools/build_site.py wraps them into docs/*.html (shared head, nav, footer)
- docs/ - GitHub Pages site (Hallmark Paste-up theme): site.css, tokens.css, base.css, calc.js (browser ports of the calculators), site.js, fonts/, img/, media/
- tools/check_site.py - compares calc.js with the Python scripts on 1,500 random cases
- .github/workflows/check.yml - CI; yearly-update.yml opens a rules-update issue every Jan 5

## Commands
- after editing a skill or script: `python3 tools/build.py`
- after editing site-src: `python3 tools/build_site.py`
- check everything: `python3 tools/build.py --check && python3 tools/build_site.py --check && python3 tools/check_site.py && claude plugin validate .`
- design lint: `node ~/.claude/skills/hallmark/scripts/sloplint.mjs docs/{index,india,canada,us,creators,crypto}.html --genre playful --render`

## Conventions
- Commits authored as `ronitgupta43-ops <ronitgupta43@gmail.com>`, with NO Co-Authored-By line.
- Simplest working code (ponytail). Skill name must equal its folder name.
- The claude.ai upload keeps only SKILL.md, so scripts must stay embedded (build.py does it).
- Never invent numbers on the site; every figure comes from the scripts or official 2026 limits.
- Website: no eyebrows or all-caps labels, every animation has a reduced-motion fallback.

## Done recently
- New skills: canada-first-home (down payment, CMHC, stress test, ON/Toronto LTT) and money/debt-payoff (avalanche vs snowball)
- Six-page website (home, india, canada, us, creators, crypto) with live calculators, video and photos
- Crypto plugin (crypto-portfolio: CA/IN/US tax from exchange CSVs, no API keys)
- Creator plugin (writer, plan, brand deals)
- Promo reels: tax-regime video (docs/media) and a 20s reel with Runway pictures (not in repo)

## Next / open
- Post the new reel and website
- Skill idea from r/IndiaInvestments: RSUs and foreign stocks for Indian residents (vesting tax, Schedule FA, foreign tax credit)
- Rules change each January: follow the yearly-update issue checklist

## Gotchas
- League Gothic has no ₹; the site's font stack falls back to Newsreader for it
- JS rounding must match Python's round-half-even (pyRound in calc.js)
- The cloud workspace can't reach Google Fonts, github.io or Runway downloads; fonts are self-hosted via npm fontsource
- pkill with a pattern that matches your own command kills the shell
