// Page behaviour: answer slip, calculators, copy buttons. Maths lives in calc.js.
const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];
const still = matchMedia("(prefers-reduced-motion: reduce)").matches;
const inr = (n) => "₹" + Math.round(n).toLocaleString("en-IN");
const usd = (n) => "$" + Math.round(n).toLocaleString("en-US");
const num = (el) => Math.max(parseFloat(el.value) || 0, 0);

// count a figure up to its value
function countUp(el, to, fmt) {
  if (still) { el.textContent = fmt(to); return; }
  const t0 = performance.now(), d = 700;
  const step = (t) => { const k = Math.min((t - t0) / d, 1); el.textContent = fmt(to * (1 - (1 - k) ** 3)); if (k < 1) requestAnimationFrame(step); };
  requestAnimationFrame(step);
}

// home: the answer slip prints a real result for each country
const SLIPS = {
  india: () => { const n = indiaRegime(1500000, true, 150000, true), o = indiaRegime(1500000, true, 150000, false);
    return { ask: "I earn ₹15 lakh with ₹2 lakh in 80C. Which regime?", skill: "india-income-tax",
      rows: [["New regime tax", inr(n.tax)], ["Old regime tax", inr(o.tax)], ["80C capped at", "₹1,50,000", 1]],
      total: "You save", big: o.tax - n.tax, fmt: inr, note: "Pick the new regime." }; },
  canada: () => { const r = tfsaRoom(2018, 2026, 30000, 0);
    return { ask: "I've been in Canada since 2018 and put $30,000 in my TFSA. How much room is left?", skill: "canada-registered-accounts",
      rows: [["Room since 2018", "$57,000"], ["Contributed", "−$30,000"], ["2026 limit", "$7,000", 1]],
      total: "Room left", big: r, fmt: usd, note: "Check against CRA My Account before you deposit." }; },
  us: () => { const t = usTax(95000, "single", 10000, 0);
    return { ask: "Single, $95,000 salary and $10,000 long-term gains. Federal tax?", skill: "us-income-tax",
      rows: [["Standard deduction", "$16,100", 1], ["Tax on salary", usd(t.ordinaryTax)], ["Tax on gains at 15%", usd(t.gainsTax)]],
      total: "Federal tax", big: t.tax, fmt: usd, note: "State tax not included." }; }
};
function printSlip(key) {
  const s = SLIPS[key](), slip = $(".slip");
  slip.innerHTML = `<p class="ask"><small>You ask ${s.skill}</small>${s.ask}</p>` +
    s.rows.map(([a, b, q]) => `<div class="row${q ? " quiet" : ""}"><span>${a}</span><span>${b}</span></div>`).join("") +
    `<div class="row total"><span>${s.total}</span><span></span></div><span class="big"><span class="mark">0</span></span><p class="note">${s.note}</p>`;
  $$(".printer-tabs button").forEach((b) => b.setAttribute("aria-selected", b.dataset.k === key));
  slip.classList.remove("printing"); void slip.offsetWidth; slip.classList.add("printing");
  countUp($(".big .mark", slip), s.big, s.fmt);
}
if ($(".slip")) {
  const keys = Object.keys(SLIPS); let i = 0, timer;
  const go = (k) => { i = keys.indexOf(k); printSlip(k); };
  $$(".printer-tabs button").forEach((b) => b.addEventListener("click", () => { clearInterval(timer); go(b.dataset.k); }));
  go("india");
  if (!still) timer = setInterval(() => go(keys[(i + 1) % keys.length]), 6000);
}

// calculators: each form has data-calc and an output .result
const CALCS = {
  india(f) {
    const gross = num(f.gross), c80 = Math.min(num(f.c80), 150000), other = num(f.other), sal = f.salaried.checked;
    const n = indiaRegime(gross, sal, 0, true), o = indiaRegime(gross, sal, c80 + other, false);
    const best = n.tax <= o.tax ? "new" : "old";
    return { rows: [["New regime", inr(n.tax)], ["Old regime", inr(o.tax)], ["80C counted", inr(c80)]],
      big: Math.abs(o.tax - n.tax), fmt: inr, verdict: n.tax === o.tax ? "Both regimes cost the same." : `The ${best} regime saves you this much.` };
  },
  canada(f) {
    const room = tfsaRoom(num(f.start), 2026, num(f.contributed), num(f.withdrawn));
    return { rows: [["Years counted", `${Math.max(num(f.start), 2009)} to 2026`], ["Contributed", usd(num(f.contributed))], ["Withdrawn before 2026", usd(num(f.withdrawn))]],
      big: Math.max(room, 0), fmt: usd, verdict: room < 0 ? `Over the limit by ${usd(-room)}. CRA charges 1% a month on the excess.` : "TFSA room you can use in 2026." };
  },
  us(f) {
    const t = usTax(num(f.wages), f.status.value, num(f.ltcg), 0);
    return { rows: [["Taxable income", usd(t.taxable)], ["Tax on ordinary income", usd(t.ordinaryTax)], ["Tax on long-term gains", usd(t.gainsTax)]],
      big: t.tax, fmt: usd, verdict: "Estimated 2026 federal tax, before credits and state tax." };
  },
  creator(f) {
    const [lo, hi] = priceRange(num(f.views), num(f.lo), num(f.hi));
    return { rows: [["Median views", Math.round(num(f.views)).toLocaleString("en-US")], ["Your CPM range", `${num(f.lo)} to ${num(f.hi)}`]],
      big: lo, fmt: (n) => Math.round(n).toLocaleString("en-US"), tail: ` to ${hi.toLocaleString("en-US")}`, verdict: "One post, same currency as your CPM. Charge more for usage rights and exclusivity." };
  }
};
$$("form[data-calc]").forEach((f) => {
  const out = $(".result", f.parentElement);
  const run = (animate) => {
    const r = CALCS[f.dataset.calc](f.elements);
    out.innerHTML = r.rows.map(([a, b]) => `<div class="row"><span>${a}</span><span>${b}</span></div>`).join("") +
      `<span class="big"><span class="mark">0</span>${r.tail || ""}</span><p class="verdict">${r.verdict}</p>`;
    const m = $(".mark", out);
    animate ? countUp(m, r.big, r.fmt) : (m.textContent = r.fmt(r.big));
  };
  f.addEventListener("input", () => run(false));
  f.addEventListener("submit", (e) => { e.preventDefault(); run(true); });
  run(true);
});

// copy buttons
$$(".copy").forEach((b) => b.addEventListener("click", async () => {
  try { await navigator.clipboard.writeText(b.previousElementSibling.textContent); b.textContent = "Copied"; setTimeout(() => (b.textContent = "Copy"), 1500); } catch {}
}));

// crypto: feed animation only while visible
const merge = $(".merge");
if (merge && !still) new IntersectionObserver(([e]) => merge.classList.toggle("live", e.isIntersecting)).observe(merge);

// videos: no autoplay for reduced motion
if (still) $$("video[autoplay]").forEach((v) => { v.removeAttribute("autoplay"); v.pause(); v.controls = true; });
