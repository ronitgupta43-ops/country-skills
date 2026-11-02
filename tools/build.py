"""Keep the repo consistent. Run after any change; CI runs it with --check.
1. Copies each skill's script into its SKILL.md (some apps upload only SKILL.md).
2. Writes the skill tree into README.md and AGENTS.md from the skills themselves.
Usage: python tools/build.py [--check]"""
import glob
import json
import re
import sys

EMBED = re.compile(r"(<!-- embed: (\S+) -->\n```python\n)(.*?)(```)", re.S)
TREE = re.compile(r"(<!-- tree:start -->\n)(.*?)(<!-- tree:end -->)", re.S)
COUNTRIES = [("canada", "🇨🇦 Canada"), ("india", "🇮🇳 India"), ("us", "🇺🇸 United States")]


def front(md):
    text = open(md).read()
    name = re.search(r"^name: (.+)$", text, re.M)[1].strip()
    desc = re.search(r"^description: (.+)$", text, re.M)[1].split(". Use when")[0].replace(" - ", ": ").strip()
    if len(desc) > 72:
        desc = desc[:72].rsplit(" ", 1)[0].rstrip(",:;(") + "…"
    return name, desc


def tree():
    plugins = [p["name"] for p in json.load(open(".claude-plugin/marketplace.json"))["plugins"]]
    codes = [c for c, _ in COUNTRIES]
    groups = [(label, [p for p in plugins if p.split("-")[0] == c]) for c, label in COUNTRIES]
    groups.append(("🌍 Any country", [p for p in plugins if p.split("-")[0] not in codes]))
    groups = [g for g in groups if g[1]]
    lines = ["```", "country-skills"]
    for gi, (label, ps) in enumerate(groups):
        g_last = gi == len(groups) - 1
        lines.append(("└── " if g_last else "├── ") + label)
        g_pad = "    " if g_last else "│   "
        for pi, p in enumerate(ps):
            p_last = pi == len(ps) - 1
            lines.append(g_pad + ("└── " if p_last else "├── ") + p)
            p_pad = g_pad + ("    " if p_last else "│   ")
            skills = sorted(front(m) for m in glob.glob(f"plugins/{p}/skills/*/SKILL.md"))
            width = max(len(n) for n, _ in skills)
            for si, (n, d) in enumerate(skills):
                lines.append(p_pad + ("└── " if si == len(skills) - 1 else "├── ") + n.ljust(width) + "  " + d)
    total = len(glob.glob("plugins/*/skills/*/SKILL.md"))
    return "\n".join(lines + ["```", "", f"{total} skills in {len(plugins)} plugins. Install a whole plugin or any single skill."]) + "\n"


def main():
    check = "--check" in sys.argv
    stale = []

    def write(path, old, new):
        if new != old:
            stale.append(path)
            if not check:
                open(path, "w").write(new)

    for md in glob.glob("plugins/*/skills/*/SKILL.md"):
        folder = md.rsplit("/", 1)[0]
        text = open(md).read()
        write(md, text, EMBED.sub(lambda m: m[1] + open(f"{folder}/{m[2]}").read() + m[4], text))
    t = tree()
    for doc in ("README.md", "AGENTS.md"):
        text = open(doc).read()
        write(doc, text, TREE.sub(lambda m: m[1] + t + m[3], text))
    if stale and check:
        sys.exit("Out of date, run python tools/build.py: " + ", ".join(stale))
    print("updated: " + ", ".join(stale) if stale else "everything up to date")


if __name__ == "__main__":
    main()
