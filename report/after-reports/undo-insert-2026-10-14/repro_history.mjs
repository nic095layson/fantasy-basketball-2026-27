// Reproduction for finding F2 (history box after Undo then Insert-at-#): feed 12 picks
// (the owner's #10 included), Undo 3, log 3 different players, then insert a missed pick at
// #2. Records the history box and the state so the report quotes the page, not a reading of
// the code. The state is compared with a clean feed of the same final list.
//   node repro_history.mjs <deck.html> <out.json>
import fs from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";
const { chromium } = createRequire(import.meta.url)(process.env.PW_MODULE || "/opt/node22/lib/node_modules/playwright");
const [html, outPath] = process.argv.slice(2);
const browser = await chromium.launch({ executablePath: process.env.PW_CHROMIUM || "/opt/pw-browsers/chromium", args: ["--no-sandbox"] });
async function newPage() {
  const page = await (await browser.newContext()).newPage();
  await page.goto("file://" + path.resolve(html));
  await page.fill("#cfgTeams", "12"); await page.fill("#cfgSize", "13"); await page.fill("#cfgSlot", "10");
  await page.click("#modeLive"); await page.click("#startBtn"); await page.waitForSelector("#draft:not(.hidden)", { timeout: 180000 });
  return page;
}
const feed = async (page, t) => { await page.fill("#feed", t); await page.click("#logBtn"); };
const page = await newPage();
const ORDER = await page.evaluate(() => PLAYERS.filter(p => p.av > 0).slice().sort((a, b) => ((a.mkt ?? 999) - (b.mkt ?? 999)) || (a.n < b.n ? -1 : 1)).map(p => p.n));
const L = ORDER.slice(0, 12), X = ORDER.slice(20, 23), Y = ORDER[30];
for (const n of L) await feed(page, n);
for (let i = 0; i < 3; i++) await page.click("#undoBtn");
for (const n of X) await feed(page, n);
const beforeInsert = (await page.locator("#mirror").innerText()).split("\n").map(s => s.trim()).filter(Boolean);
await page.click("#insertToggle"); await page.fill("#insNum", "2"); await page.fill("#insName", Y); await page.click("#insBtn");
const after = (await page.locator("#mirror").innerText()).split("\n").map(s => s.trim()).filter(Boolean);
const st = await page.evaluate(() => JSON.parse(localStorage.getItem("draftdeck.v1")).state.picks);
const want = [L[0], Y, ...L.slice(1, 9), ...X];
const clean = await newPage();
await feed(clean, want.join("; "));
const st2 = await clean.evaluate(() => JSON.parse(localStorage.getItem("draftdeck.v1")).state.picks);
const out = { L, X, Y, beforeInsert, after, state: st.map(p => [p.player, p.slot]), stateEqualsCleanFeed: JSON.stringify(st) === JSON.stringify(st2) };
fs.writeFileSync(outPath, JSON.stringify(out, null, 1));
console.log(JSON.stringify({ stateEqualsCleanFeed: out.stateEqualsCleanFeed, lines: after.length }));
await browser.close();
