// Undo / Insert-at-# integrity check on the REAL deck page (owner request 2026-10-14):
// "test, validate integrity, that when using the 'undo pick' and 'insert at #' features
// are used, the arithmetic computation and correct team association is accurate".
//
// Differential method: a PATH page reaches a final pick list through Undo and
// Insert-at-# (the owner's corrections); an ORACLE page is fed the same final list
// cleanly in one feed. Everything the page derives from the picks must agree:
// the picks and their seats (and every seat must equal the snake formula), each
// team's roster, the nine z-total categories per team, the owner's category ranks,
// the next-pick clock, the available pool, the Top-5 card, and the visible text of
// every tab (the history box excepted — it is a log, checked separately against the
// state). Per-team totals are dumped for an independent Python recomputation
// (totals_oracle.py). Read-only on the page file.
//   node undo_insert_check.mjs <deck.html> <out.json> [seedFrom=1] [seedTo=10] [hand=1]
import fs from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";
const { chromium } = createRequire(import.meta.url)(process.env.PW_MODULE || "/opt/node22/lib/node_modules/playwright");
const [html, outPath, seedFrom = "1", seedTo = "10", handArg = "1"] = process.argv.slice(2);
const SEED_FROM = parseInt(seedFrom, 10), SEED_TO = parseInt(seedTo, 10), HAND = handArg !== "0";
const TEAMS = 12, SIZE = 13, SLOT = 10, MAXP = TEAMS * SIZE;
const snake = (n, t) => { const r = Math.floor(n / t), i = n % t; return r % 2 === 0 ? i + 1 : t - i; };

const A = []; const dumps = []; const errors = []; const notes = {};
function ok(id, cond, detail) { A.push({ id, ok: !!cond, detail: cond ? null : (detail === undefined ? null : detail) }); return !!cond; }
const browser = await chromium.launch({ executablePath: process.env.PW_CHROMIUM || "/opt/pw-browsers/chromium", args: ["--no-sandbox"] });

async function newPage() {
  const ctx = await browser.newContext();
  const page = await ctx.newPage();
  page.setDefaultTimeout(180000);
  page.on("pageerror", e => errors.push(String(e && e.message || e)));
  page.on("console", m => { if (m.type() === "error") errors.push(m.text()); });
  await page.goto("file://" + path.resolve(html));
  await page.fill("#cfgTeams", String(TEAMS)); await page.fill("#cfgSize", String(SIZE)); await page.fill("#cfgSlot", String(SLOT));
  await page.click("#modeLive"); await page.click("#startBtn"); await page.waitForSelector("#draft:not(.hidden)", { timeout: 180000 });
  return { ctx, page };
}
const feed = async (page, text) => { await page.fill("#feed", text); await page.click("#logBtn"); };
const undo = page => page.click("#undoBtn");
async function insert(page, P, name) {
  if (await page.locator("#insertBar").evaluate(el => el.classList.contains("hidden"))) await page.click("#insertToggle");
  await page.fill("#insNum", String(P)); await page.fill("#insName", name); await page.click("#insBtn");
}
const picksOf = page => page.evaluate(() => JSON.parse(localStorage.getItem("draftdeck.v1")).state.picks);
const mirrorLines = async page => (await page.locator("#mirror").innerText()).split("\n").map(s => s.trim()).filter(Boolean);

// Everything derived from the picks, read from the page's own engine and DOM.
async function snapshot(page) {
  const eng = await page.evaluate(() => {
    const st = JSON.parse(localStorage.getItem("draftdeck.v1")).state;
    const R = buildRosters(st, PLAYERS);
    const totals = {}, rosters = {};
    for (let s = 1; s <= st.teams; s++) {
      rosters[s] = R[s].map(p => p.n).sort();
      const t = rosterTotals(R[s]); totals[s] = Object.fromEntries(Object.entries(t).map(([k, v]) => [k, Math.round(v * 1e9) / 1e9]));
    }
    const cr = categoryRanks(st, PLAYERS);
    const avail = availablePool(st, PLAYERS).map(p => p.n);
    return { picks: st.picks.map(p => [p.player, p.slot]), rosters, totals, ranks: cr.ranks,
             myNext: typeof myNextPick === "function" ? myNextPick(st) : null, availN: avail.length, availHead: avail.slice(0, 40) };
  });
  const tabs = {};
  for (const t of ["best", "boardtab", "rosters", "matrix", "vs"]) {
    await page.click(`#tab-${t}`);
    tabs[t] = await page.evaluate(() => {
      const al = document.getElementById("adviceline"), alt = al ? al.innerText : "";
      let txt = document.getElementById("draft").innerText.replace(document.getElementById("mirror").innerText, "");
      if (window.__stripAdvice && alt) txt = txt.replace(alt, "<advice line>");
      return txt;
    });
  }
  await page.click("#tab-best");
  const advice = await page.evaluate(() => { const a = document.getElementById("adviceline"); return a ? { text: a.innerText, hidden: a.classList.contains("hidden") } : null; });
  const top5 = await page.locator("#recos li").evaluateAll(lis => lis.map(li => li.innerText.replace(/\s+/g, " ").trim()));
  return { ...eng, tabs, top5, advice };
}
// History: the LATEST line naming each pick number must agree with the state at that
// number (earlier lines for the same number are superseded history: an undone or
// corrected pick). Lines naming a number past the end of the state are counted apart.
function historyCheck(lines, picks) {
  const seen = [];   // pick lines in order; an "↶ undid: NAME (Seat S)" supersedes the latest live line for NAME
  for (const l of lines) {
    const m = l.match(/^✓ \(R(\d+)\) #(\d+): (.+?) → Seat (\d+)( \(YOU\))?/);
    if (m) { seen.push({ l, m, dead: false }); continue; }
    const u = l.match(/^↶ undid: (.+) \(Seat (\d+)\)$/);
    if (u) for (let k = seen.length - 1; k >= 0; k--) if (!seen[k].dead && seen[k].m[3] === u[1]) { seen[k].dead = true; break; }
  }
  const last = new Map();
  for (const x of seen) if (!x.dead) last.set(+x.m[2], x);
  const bad = [];
  for (const [num, { l, m }] of last) {
    const i = num - 1, pk = picks[i];
    if (!pk) continue;                      // undone past the end: history only
    if (/^UNKNOWN/.test(pk.player)) continue; // an open UNKNOWN has its own warning line
    const r = Math.floor(i / TEAMS) + 1;
    if (pk.player !== m[3] || pk.slot !== +m[4] || r !== +m[1] || (!!m[5]) !== (pk.slot === SLOT)) bad.push({ line: l, state: pk });
  }
  return bad;
}
function diffSnap(a, b) {
  const d = [];
  for (const k of ["picks", "rosters", "totals", "ranks", "myNext", "availN", "availHead", "top5"])
    if (JSON.stringify(a[k]) !== JSON.stringify(b[k])) d.push(k);
  for (const t of Object.keys(a.tabs)) if (a.tabs[t] !== b.tabs[t]) {
    const al = a.tabs[t].split("\n"), bl = b.tabs[t].split("\n");
    const lines = [];
    for (let i = 0; i < Math.max(al.length, bl.length); i++) if (al[i] !== bl[i]) lines.push(`@${i}: path ${JSON.stringify(al[i])} | oracle ${JSON.stringify(bl[i])}`);
    d.push(`tab:${t} ${lines.length} line(s) differ: ${lines.slice(0, 6).join(" ;; ")}`);
  }
  return d;
}
async function oracleSnap(names) {
  const { ctx, page } = await newPage();
  if (names.length) await feed(page, names.join("; "));
  if (names.length >= MAXP) await page.evaluate(() => { window.__stripAdvice = true; });
  const s = await snapshot(page); await ctx.close(); return s;
}
// Compare a finished PATH page with a clean ORACLE built from `finalNames`.
async function judge(id, page, finalNames, extra = {}) {
  const P = await picksOf(page);
  if (P.length >= MAXP) await page.evaluate(() => { window.__stripAdvice = true; });   // finding F1: stale advice line after the last pick
  const path_ = await snapshot(page);
  const orc = await oracleSnap(finalNames);
  ok(`${id}.final-list`, JSON.stringify(P.map(p => p.player)) === JSON.stringify(finalNames), { got: P.map(p => p.player).slice(0, 40), want: finalNames.slice(0, 40) });
  const offSnake = P.map((p, i) => p.slot !== snake(i, TEAMS) ? [i + 1, p.player, p.slot, snake(i, TEAMS)] : null).filter(Boolean);
  ok(`${id}.seats-equal-snake`, offSnake.length === (extra.offSnake || 0), offSnake);
  const d = diffSnap(path_, orc);
  ok(`${id}.path-equals-oracle`, d.length === 0, d);
  const hb = historyCheck(await mirrorLines(page), P);
  ok(`${id}.history-matches-state`, hb.length === 0, hb.slice(0, 6));
  if (P.length >= MAXP) notes[`${id}.advice_at_complete`] = { path: path_.advice, oracle: orc.advice };
  else ok(`${id}.advice-line-live`, orc.advice && path_.advice && path_.advice.text === orc.advice.text, { path: path_.advice, oracle: orc.advice });
  dumps.push({ id, picks: path_.picks, totals: path_.totals, ranks: path_.ranks });
  return { path_, orc, historyBad: hb };
}

// The draft order the cast would plausibly take: the page's market order (else value).
const { ctx: c0, page: p0 } = await newPage();
const ORDER = await p0.evaluate(() => PLAYERS.filter(p => p.av > 0).slice().sort((a, b) => ((a.mkt ?? 999) - (b.mkt ?? 999)) || (a.n < b.n ? -1 : 1)).map(p => p.n));
notes.pool = ORDER.length; notes.page = html;
await c0.close();
const L = ORDER.slice(0, 40), X = ORDER.slice(40, 50);

if (HAND) {
/* A: undo five, re-log five different players */
{ const { ctx, page } = await newPage();
  for (const n of L.slice(0, 30)) await feed(page, n);
  for (let i = 0; i < 5; i++) await undo(page);
  const after = await picksOf(page);
  ok("A.undo-pops-five", after.length === 25 && after.every((p, i) => p.player === L[i]));
  const ml = await mirrorLines(page);
  ok("A.undo-lines-name-seat", L.slice(25, 30).every((n, k) => ml.some(l => l === `↶ undid: ${n} (Seat ${snake(29 - (4 - k), TEAMS)})`)), ml.slice(-6));
  for (const n of X.slice(0, 5)) await feed(page, n);
  const r = await judge("A", page, [...L.slice(0, 25), ...X.slice(0, 5)]);
  notes.A_history_bad = r.historyBad.length;
  await ctx.close(); }

/* B: a missed pick at #12 inserted after 29 logged — the shift crosses the owner's #15 */
{ const { ctx, page } = await newPage();
  const want = L.slice(0, 30);
  for (const n of want.filter((_, i) => i !== 11)) await feed(page, n);
  const before = await picksOf(page);
  ok("B.pre-owner-#15", before[14].slot === SLOT && before[14].player === want[15], before[14]);   // logged one early
  await insert(page, 12, want[11]);
  const ml = await mirrorLines(page);
  ok("B.insert-line", ml.some(l => l.startsWith(`✎ inserted ${want[11]} at #12 → Seat 12; #12–#29 → #13–#30 (18 shifted, slots recomputed)`)), ml.filter(l => l.includes("inserted")));
  ok("B.moved-off-owner", ml.some(l => l === `· #16 ${want[15]} is no longer your pick after the shift`), ml.slice(-5));
  ok("B.moved-on-owner", ml.some(l => l.startsWith(`⚠ #15 ${want[14]} is YOUR pick after the shift`)), ml.slice(-5));
  await judge("B", page, want);
  /* H: reload persistence of the inserted state */
  const s1 = await snapshot(page); await page.reload(); await page.waitForSelector("#draft:not(.hidden)");
  const s2 = await snapshot(page);
  ok("H.reload-identical", diffSnap(s1, s2).length === 0, diffSnap(s1, s2));
  /* F: undo after insert (3), then re-log three */
  for (let i = 0; i < 3; i++) await undo(page);
  for (const n of X.slice(5, 8)) await feed(page, n);
  await judge("F", page, [...want.slice(0, 27), ...X.slice(5, 8)]);
  await ctx.close(); }

/* C: insert at #1 */
{ const { ctx, page } = await newPage();
  for (const n of L.slice(1, 30)) await feed(page, n);
  await insert(page, 1, L[0]);
  await judge("C", page, L.slice(0, 30));
  await ctx.close(); }

/* D: insert at the end (#picks+1) and the refusals around it */
{ const { ctx, page } = await newPage();
  for (const n of L.slice(0, 29)) await feed(page, n);
  await page.click("#insertToggle");      // the bar open in both snapshots
  const s0 = await snapshot(page);
  await insert(page, 31, L[29]);          // mid-air gap: refused
  await insert(page, 5, L[3]);            // already drafted: refused
  await insert(page, 0, L[29]);           // out of range: refused
  const s1 = await snapshot(page);
  ok("D.refusals-change-nothing", diffSnap(s0, s1).length === 0, diffSnap(s0, s1));
  const ml = await mirrorLines(page);
  ok("D.refusals-logged", ml.some(l => l.startsWith("⚠ insert #31: only 29 pick(s) logged")) && ml.some(l => l.startsWith(`⚠ insert: ${L[3]} is already off the board`)) && ml.some(l => l.startsWith("⚠ insert #0: out of range")), ml.slice(-4));
  await insert(page, 30, L[29]);          // append
  await judge("D", page, L.slice(0, 30));
  await ctx.close(); }

/* E: an insert ahead of a standing UNKNOWN renames it to its new number */
{ const { ctx, page } = await newPage();
  const want = L.slice(0, 20);
  const seq = [...want.slice(0, 4), ...want.slice(5, 14), "Zzqx Nobody", ...want.slice(14, 19)];   // #5 missed; #14 garbage
  for (const n of seq) await feed(page, n);
  const pre = await picksOf(page);
  ok("E.unknown-logged", pre[13].player === "UNKNOWN #14", pre[13]);
  await insert(page, 5, want[4]);
  const P = await picksOf(page);
  ok("E.unknown-renamed", P[14].player === "UNKNOWN #15" && P[14].slot === snake(14, TEAMS), P[14]);
  const finalNames = P.map(p => p.player);
  const expect = [...want.slice(0, 14), "UNKNOWN #15", ...want.slice(14, 19)];
  ok("E.order", JSON.stringify(finalNames) === JSON.stringify(expect), finalNames);
  // the oracle logs the same garbage at #15
  const { ctx: oc, page: op } = await newPage();
  await feed(op, [...want.slice(0, 14), "Zzqx Nobody", ...want.slice(14, 19)].join("; "));
  const o = await snapshot(op); await oc.close();
  const d = diffSnap(await snapshot(page), o);
  ok("E.path-equals-oracle", d.length === 0, d);
  const hb = historyCheck(await mirrorLines(page), P);
  ok("E.history-matches-state", hb.length === 0, hb.slice(0, 6));
  // then fill the UNKNOWN by number and compare again
  await feed(page, `15- ${X[9]}`);
  const P2 = await picksOf(page);
  ok("E.fix-by-number", P2[14].player === X[9] && P2[14].slot === snake(14, TEAMS), P2[14]);
  await judge("E2", page, P2.map(p => p.player));
  await ctx.close(); }

/* G: an off-snake my: pick blocks Insert (refused, nothing moves); after Undo it works */
{ const { ctx, page } = await newPage();
  for (const n of L.slice(0, 10)) await feed(page, n);
  await feed(page, `my: ${L[10]}`);       // #11 is Seat 11 on the snake; logged to YOUR seat 10
  await feed(page, L[11]);
  const P = await picksOf(page);
  ok("G.my-off-snake-to-owner", P[10].slot === SLOT && P[11].slot === snake(11, TEAMS), [P[10], P[11]]);
  await page.click("#insertToggle");
  const s0 = await snapshot(page);
  await insert(page, 5, X[0]);
  const s1 = await snapshot(page);
  ok("G.insert-refused-unchanged", diffSnap(s0, s1).length === 0, diffSnap(s0, s1));
  ok("G.refusal-logged", (await mirrorLines(page)).some(l => l.startsWith("⚠ insert refused: pick(s) 11 carry a non-snake slot")), (await mirrorLines(page)).slice(-3));
  // the owner's roster carries the off-snake pick: totals follow the seat, not the number
  ok("G.owner-roster-has-it", s0.rosters[SLOT].includes(L[10]) && !s0.rosters[11].includes(L[10]), { o: s0.rosters[SLOT], s11: s0.rosters[11] });
  await undo(page); await undo(page);
  await insert(page, 5, X[0]);
  await feed(page, L[10]); await feed(page, L[11]);
  await judge("G", page, [...L.slice(0, 4), X[0], ...L.slice(4, 12)]);
  await ctx.close(); }

}
/* R: seeded random full drafts (156 picks) with misses, wrong logs and undo runs */
function rng(seed) { let s = seed >>> 0; return () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; }
const ops = { insert: 0, undo: 0, wrongLog: 0 };
for (let seed = SEED_FROM; seed <= SEED_TO; seed++) {
  const R = rng(seed * 7919);
  // target draft: market order with noise (a plausible room)
  const pool = ORDER.slice(0, 260).map((n, i) => ({ n, k: i + (R() - 0.5) * 30 })).sort((a, b) => a.k - b.k).map(o => o.n);
  const F = pool.slice(0, MAXP);
  const spare = pool.slice(MAXP);
  const { ctx, page } = await newPage();
  let missed = null, missedAt = null, logged = 0, wait = 0, local = { insert: 0, undo: 0, wrongLog: 0 };
  let i = 0, checked = false;
  const CP = 40 + Math.floor(R() * 110);                               // mid-draft checkpoint (advice line live)
  while (i < MAXP) {
    if (!checked && missed === null && i >= CP) { await judge(`R${seed}@${i}`, page, F.slice(0, i)); checked = true; }
    if (missed !== null && (wait <= 0 || i === MAXP - 1)) {         // insert the missed pick at its true number
      await insert(page, missedAt + 1, missed); local.insert++; missed = null;
      continue;
    }
    const u = R();
    if (missed === null && i < MAXP - 3 && u < 0.07) {                // miss this pick; insert it 1-5 picks later
      missed = F[i]; missedAt = i; wait = 1 + Math.floor(R() * 5); i++; continue;
    }
    if (u > 0.93) {                                                   // a wrong log, caught and undone
      const avail = spare.filter(n => !F.slice(0, i).includes(n));
      await feed(page, avail[Math.floor(R() * Math.min(10, avail.length))]); await undo(page); local.wrongLog++; local.undo++;
    }
    await feed(page, F[i]); i++; if (missed !== null) wait--;
    if (missed === null && R() < 0.04 && i > 3) {                     // an undo run of 1-3 good picks, re-logged
      const k = 1 + Math.floor(R() * 3);
      for (let j = 0; j < k; j++) await undo(page);
      for (let j = i - k; j < i; j++) await feed(page, F[j]);
      local.undo += k;
    }
  }
  if (missed !== null) { await insert(page, missedAt + 1, missed); local.insert++; }
  for (const k of Object.keys(ops)) ops[k] += local[k];
  notes[`R${seed}`] = local;
  await judge(`R${seed}`, page, F);
  await ctx.close();
}
notes.randomOps = ops;
await browser.close();

const failed = A.filter(a => !a.ok);
const out = { page: html, at: new Date().toISOString(), assertions: A.length, failed: failed.length, pageErrors: errors, pass: !failed.length && !errors.length, notes, failures: failed, all: A.map(a => ({ id: a.id, ok: a.ok })) };
fs.writeFileSync(outPath, JSON.stringify(out, null, 1));
fs.writeFileSync(outPath.replace(/\.json$/, "_totals.json"), JSON.stringify(dumps));
console.log(JSON.stringify({ assertions: A.length, failed: failed.length, pageErrors: errors.length, failures: failed.map(f => f.id), ops }));
process.exitCode = out.pass ? 0 : 1;
