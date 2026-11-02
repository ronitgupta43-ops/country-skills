"""Check the website's JavaScript calculators (docs/calc.js) give the same answers as the Python ones."""
import json, random, subprocess, sys
sys.path[:0] = ["plugins/india-finance/skills/india-income-tax/scripts", "plugins/canada-finance/skills/canada-registered-accounts/scripts",
                "plugins/us-finance/skills/us-income-tax/scripts", "plugins/creator/skills/creator-brand-deals/scripts"]
import tax_calc, tfsa_room, us_tax, rates

random.seed(1)
cases = []
for _ in range(300):
    g, s, d = random.randrange(0, 6000000, 5000), random.random() < .7, random.randrange(0, 400000, 5000)
    cases.append(["in", [g, s, d, True], tax_calc.regime_tax(g, s, d, True)[1]])
    cases.append(["in", [g, s, d, False], tax_calc.regime_tax(g, s, d, False)[1]])
    y, c, w = random.randrange(2005, 2027), random.randrange(0, 60000, 500), random.randrange(0, 20000, 500)
    cases.append(["tfsa", [y, 2026, c, w], tfsa_room.tfsa_room(y, 2026, c, w)])
    wa, lt, st = random.randrange(0, 900000, 1000), random.randrange(0, 300000, 1000), random.choice(["single", "mfj"])
    cases.append(["us", [wa, st, lt, 0], us_tax.federal_tax(wa, st, lt, 0)[1]])
    v, lo = random.randrange(100, 900000), random.randrange(5, 60)
    cases.append(["rate", [v, lo, lo * 2], list(rates.price_range(v, lo, lo * 2))])
js = """const c=require('./docs/calc.js');const cases=%s;let bad=0;
for(const [k,a,want] of cases){let got=k==='in'?c.indiaRegime(...a).tax:k==='tfsa'?c.tfsaRoom(...a):k==='us'?c.usTax(...a).tax:c.priceRange(...a);
if(JSON.stringify(got)!==JSON.stringify(want)&&!(typeof want==='number'&&Math.abs(got-want)<0.011)){bad++;if(bad<5)console.log(k,a,'js',got,'py',want);}}
console.log(cases.length+' cases, '+bad+' mismatches');process.exit(bad?1:0);""" % json.dumps(cases)
sys.exit(subprocess.run(["node", "-e", js]).returncode)
