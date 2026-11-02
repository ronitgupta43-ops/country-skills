// Browser copies of the repo's Python calculators (2026 rules). tools/check_site.py compares them with the Python on every CI run.
const INF = Infinity;
// Python round(): exact halves go to the even number
const pyRound = (x) => { const f = Math.floor(x), d = x - f; return d > 0.5 + 1e-9 ? f + 1 : d < 0.5 - 1e-9 ? f : (f % 2 === 0 ? f : f + 1); };
const slab = (x, slabs) => { let t = 0, lo = 0; for (const [hi, r] of slabs) { if (x > lo) t += (Math.min(x, hi) - lo) * r; lo = hi; } return t; };

// india-income-tax/scripts/tax_calc.py
const IN_NEW = [[400000, 0], [800000, .05], [1200000, .10], [1600000, .15], [2000000, .20], [2400000, .25], [INF, .30]];
const IN_OLD = [[250000, 0], [500000, .05], [1000000, .20], [INF, .30]];
function indiaRegime(gross, salaried, deductions, isNew) {
  const taxable = Math.max(gross - (isNew ? 75000 : 50000) * (salaried ? 1 : 0) - (isNew ? 0 : deductions), 0);
  let tax = slab(taxable, isNew ? IN_NEW : IN_OLD);
  const limit = isNew ? 1200000 : 500000;
  if (taxable <= limit) tax = 0; else if (isNew) tax = Math.min(tax, taxable - limit);
  return { taxable, tax: pyRound(tax * 1.04) };
}

// canada-registered-accounts/scripts/tfsa_room.py
const TFSA = { 2009: 5000, 2010: 5000, 2011: 5000, 2012: 5000, 2013: 5500, 2014: 5500, 2015: 10000, 2016: 5500, 2017: 5500, 2018: 5500,
  2019: 6000, 2020: 6000, 2021: 6000, 2022: 6000, 2023: 6500, 2024: 7000, 2025: 7000, 2026: 7000 };
function tfsaRoom(start, year, contributed, withdrawnBefore) {
  let room = 0; for (let y = Math.max(start, 2009); y <= year; y++) room += TFSA[y] || 0;
  return room - contributed + withdrawnBefore;
}

// us-income-tax/scripts/us_tax.py
const US = {
  single: { br: [[12400, .10], [50400, .12], [105700, .22], [201775, .24], [256225, .32], [640600, .35], [INF, .37]], std: 16100, lt: [49450, 545500] },
  mfj: { br: [[24800, .10], [100800, .12], [211400, .22], [403550, .24], [512450, .32], [768700, .35], [INF, .37]], std: 32200, lt: [98900, 613700] }
};
function usTax(wages, status, ltcg, deductions) {
  const s = US[status], taxable = Math.max(wages + ltcg - Math.max(s.std, deductions), 0);
  const ordinary = Math.max(taxable - ltcg, 0), gains = taxable - ordinary, [t0, t15] = s.lt;
  const at0 = Math.max(Math.min(gains, t0 - ordinary), 0), at15 = Math.max(Math.min(gains - at0, t15 - ordinary - at0), 0);
  const tax = slab(ordinary, s.br) + at15 * .15 + (gains - at0 - at15) * .20;
  return { taxable, tax: Math.round(tax * 100) / 100, ordinaryTax: slab(ordinary, s.br), gainsTax: at15 * .15 + (gains - at0 - at15) * .20 };
}

// creator-brand-deals/scripts/rates.py
const priceRange = (views, lo, hi) => [pyRound(views / 1000 * lo), pyRound(views / 1000 * hi)];

if (typeof module !== "undefined") module.exports = { indiaRegime, tfsaRoom, usTax, priceRange };
