// Reproduce the 2026-10-13 live-room RESYNC wipe on the real page, then test recovery and the recap format.
//   env -u TMPDIR node repro_resync.mjs <deck.html> <out.json>
import fs from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";
const { chromium } = createRequire(import.meta.url)(process.env.PW_MODULE || "/opt/node22/lib/node_modules/playwright");
const [html, outPath] = process.argv.slice(2);
const here = path.dirname(new URL(import.meta.url).pathname);
const recap = JSON.parse(fs.readFileSync(path.join(here, "recap.json"), "utf8"));
const pasteLines = JSON.parse(fs.readFileSync(path.join(here, "owner_paste_lines.json"), "utf8"));
const ownerEcho = JSON.parse(fs.readFileSync(path.join(here, "owner_unknown_echo.json"), "utf8"));
const out = { deck: html, steps: [] };
const browser = await chromium.launch({ executablePath: process.env.PW_CHROMIUM || "/opt/pw-browsers/chromium", args: ["--no-sandbox"] });
const ctx = await browser.newContext();
const page = await ctx.newPage();
const errors = [];
page.on("pageerror", e => errors.push(String(e && e.message || e)));
await page.goto("file://" + path.resolve(html));
await page.fill("#cfgTeams", "12"); await page.fill("#cfgSize", "13"); await page.fill("#cfgSlot", "10");
await page.click("#modeLive"); await page.click("#startBtn");
await page.waitForSelector("#draft:not(.hidden)");
const mirror = async () => (await page.locator("#mirror").innerText()).split("\n").map(s => s.trim()).filter(Boolean);
const saved = async () => page.evaluate(() => JSON.parse(localStorage.getItem("draftdeck.v1")));
const pre = async () => page.evaluate(() => JSON.parse(localStorage.getItem("draftdeck.v1:preresync")));
const resync = async (text, how = "click") => {
  if (await page.locator("#resyncBar").evaluate(el => el.classList.contains("hidden"))) await page.click("#resyncBtn");
  await page.fill("#resyncPaste", text);
  const v = await page.inputValue("#resyncPaste");
  if (how === "enter") await page.press("#resyncPaste", "Enter"); else await page.click("#resyncGo");
  return v;
};
// Step A: a clean semicolon list of the room's first 141 picks (the board the owner had before the wipe)
const clean141 = recap.slice(0, 141).map(p => p.name).join("; ");
let lb = (await mirror()).length;
await resync(clean141);
let d = await saved(); let lines = (await mirror()).slice(lb);
const unkA = d.state.picks.map((pk, i) => [i + 1, pk.player]).filter(([, n]) => /^UNKNOWN/.test(n));
const mineA = d.state.picks.map((pk, i) => [i + 1, pk]).filter(([, pk]) => pk.slot === 10).map(([n, pk]) => [n, pk.player]);
out.steps.push({ step: "A clean 141-name list", picks: d.state.picks.length, unknown: unkA, ownerSlotPicks: mineA, firstLines: lines.slice(0, 2) });
const board141 = d.state.picks.map(pk => pk.player);
// Step B: the owner's verbatim history text, newlines pasted as spaces (the owner's echo shows three spaces at each line break)
const ownerPaste = pasteLines.join(" ");
lb = (await mirror()).length;
const filled = await resync(ownerPaste, "enter");
d = await saved(); lines = (await mirror()).slice(lb);
const p = await pre();
const echoMine = lines.filter(l => l.startsWith("⚠ (R1) #"));
const norm = s => s.replace(/\s+/g, " ").trim();
out.steps.push({
  step: "B owner's verbatim paste",
  pasteChars: ownerPaste.length, inputValueChars: filled.length, semicolons: (ownerPaste.match(/;/g) || []).length,
  logLine: lines.find(l => l.startsWith("RESYNC")) || null,
  picksAfter: d.state.picks.length, unknownAfter: d.state.picks.filter(pk => /^UNKNOWN/.test(pk.player)).length,
  preresyncPicks: p && p.picks ? p.picks.length : null,
  preresyncEqualsBoard141: !!(p && p.picks && p.picks.length === 141 && p.picks.every((pk, i) => pk.player === board141[i])),
  echoCount: echoMine.length,
  echoExactVsOwner: echoMine.length === ownerEcho.length && echoMine.every((l, i) => l === ownerEcho[i].trim()),
  echoWhitespaceNormalizedVsOwner: echoMine.length === ownerEcho.length && echoMine.every((l, i) => norm(l) === norm(ownerEcho[i])),
  echoFirstDiff: echoMine.map((l, i) => l === (ownerEcho[i] || "").trim() ? null : { i, mine: l.slice(0, 160), owner: (ownerEcho[i] || "").slice(0, 160) }).filter(Boolean).slice(0, 2),
});
// Step C: reload — does the page resume the wiped board (what the owner saw)?
await page.reload(); await page.waitForSelector("#draft:not(.hidden)", { timeout: 15000 }).catch(() => {});
d = await saved();
out.steps.push({ step: "C reload after the wipe", picks: d.state.picks.length, lastLine: (await mirror()).slice(-1)[0] });
// Step D: console recovery — splice the saved prior board back into the saved deck, reload
const rec = await page.evaluate(() => {
  const d = JSON.parse(localStorage.getItem("draftdeck.v1"));
  d.state = JSON.parse(localStorage.getItem("draftdeck.v1:preresync"));
  localStorage.setItem("draftdeck.v1", JSON.stringify(d));
  return d.state.picks.length;
});
await page.reload(); await page.waitForSelector("#draft:not(.hidden)", { timeout: 15000 }).catch(() => {});
d = await saved();
const stripD = (await page.locator("#strip").innerText()).replace(/\s+/g, " ").trim();
out.steps.push({ step: "D console recovery + reload", splicedPicks: rec, picks: d.state.picks.length,
  equalsBoard141: d.state.picks.length === 141 && d.state.picks.every((pk, i) => pk.player === board141[i]),
  lastLine: (await mirror()).slice(-1)[0], strip: stripD.slice(0, 300) });
// Step E: a second bad RESYNC overwrites the saved prior board (one level of backup only)
lb = (await mirror()).length;
await resync("Draft started: x; y");
const p2 = await pre();
d = await saved();
out.steps.push({ step: "E second bad RESYNC", picksAfter: d.state.picks.length, preresyncPicks: p2 && p2.picks ? p2.picks.length : null });
// restore again for step F
await page.evaluate(() => { const d = JSON.parse(localStorage.getItem("draftdeck.v1")); d.state = JSON.parse(localStorage.getItem("draftdeck.v1:preresync")); localStorage.setItem("draftdeck.v1", JSON.stringify(d)); });
await page.reload(); await page.waitForSelector("#draft:not(.hidden)", { timeout: 15000 }).catch(() => {});
// Step F: Yahoo's round-by-round recap pasted as-is (newlines as spaces)
const msg = fs.readFileSync(path.join(here, "owner_message.txt"), "utf8").split("\n");
const ri = msg.indexOf("Round by Round results");
const recapText = msg.slice(ri).join(" ");
d = await saved(); const beforeF = d.state.picks.length;
lb = (await mirror()).length;
await resync(recapText);
d = await saved(); lines = (await mirror()).slice(lb);
out.steps.push({ step: "F Yahoo recap pasted as-is", picksBefore: beforeF, picksAfter: d.state.picks.length,
  logLine: lines.find(l => l.startsWith("RESYNC")) || null, unknownAfter: d.state.picks.filter(pk => /^UNKNOWN/.test(pk.player)).length });
// Step G: the same recap turned into the documented format (First Last; ...) — all 156
await page.evaluate(() => { const d = JSON.parse(localStorage.getItem("draftdeck.v1")); d.state.picks = []; localStorage.setItem("draftdeck.v1", JSON.stringify(d)); });
await page.reload(); await page.waitForSelector("#draft:not(.hidden)", { timeout: 15000 }).catch(() => {});
lb = (await mirror()).length;
await resync(recap.map(p => p.name).join("; "));
d = await saved(); lines = (await mirror()).slice(lb);
out.steps.push({ step: "G recap as a semicolon list", picks: d.state.picks.length,
  unknown: d.state.picks.map((pk, i) => [i + 1, pk.player]).filter(([, n]) => /^UNKNOWN/.test(n)),
  mismatches: d.state.picks.map((pk, i) => [i + 1, recap[i].name, pk.player]).filter(([, a, b]) => a !== b).slice(0, 40),
  ownerSlot: d.state.picks.map((pk, i) => [i + 1, pk]).filter(([, pk]) => pk.slot === 10).map(([n]) => n) });
out.pageErrors = errors;
await browser.close();
fs.writeFileSync(outPath, JSON.stringify(out, null, 1));
console.log(JSON.stringify(out, null, 1).slice(0, 6000));
