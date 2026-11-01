"""Copy each skill's script into its SKILL.md so the skill still works where only SKILL.md is uploaded
(claude.ai, pasting into ChatGPT/Gemini). Usage: python tools/embed.py [--check]"""
import glob
import re
import sys

MARK = re.compile(r"(<!-- embed: (\S+) -->\n```python\n)(.*?)(```)", re.S)
stale = []
for md in glob.glob("plugins/*/skills/*/SKILL.md"):
    text = open(md).read()
    folder = md.rsplit("/", 1)[0]
    new = MARK.sub(lambda m: m[1] + open(f"{folder}/{m[2]}").read() + m[4], text)
    if new != text:
        stale.append(md)
        if "--check" not in sys.argv:
            open(md, "w").write(new)
if stale and "--check" in sys.argv:
    sys.exit("Out of date, run python tools/embed.py: " + ", ".join(stale))
print("updated: " + ", ".join(stale) if stale else "all embeds up to date")
