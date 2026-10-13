// Double wipe: the owner's paste, then a second RESYNC attempt on the wiped board. Does the saved prior board survive?
import fs from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";
const { chromium } = createRequire(import.meta.url)(process.env.PW_MODULE || "/opt/node22/lib/node_modules/playwright");
const [html, outPath] = process.argv.slice(2);
const here = path.dirname(new URL(import.meta.url).pathname);
const recap = JSON.parse(fs.readFileSync(path.join(here, "recap.json"), "utf8"));
const pasteLines = JSON.parse(fs.readFileSync(path.join(here, "owner_paste_lines.json"), "utf8"));
const browser = await chromium.launch({ executablePath: process.env.PW_CHROMIUM || "/opt/pw-browsers/chromium", args: ["--no-sandbox"] });
const page = await (await browser.newContext()).newPage();
const errors = []; page.on("pageerror", e => errors.push(String(e && e.message || e)));
await page.goto("file://" + path.resolve(html));
await page.fill("#cfgTeams", "12"); await page.fill("#cfgSize", "13"); await page.fill("#cfgSlot", "10");
await page.click("#modeLive"); await page.click("#startBtn"); await page.waitForSelector("#draft:not(.hidden)");
const resync = async (text) => { if (await page.locator("#resyncBar").evaluate(el => el.classList.contains("hidden"))) await page.click("#resyncBtn"); await page.fill("#resyncPaste", text); await page.click("#resyncGo"); };
const n = async (k) => page.evaluate(k => { const v = JSON.parse(localStorage.getItem(k)); return v ? (v.state ? v.state.picks.length : v.picks.length) : null; }, k);
await resync(recap.slice(0, 141).map(p => p.name).join("; "));
const a = { board: await n("draftdeck.v1") };
await resync(pasteLines.join(" "));
const b = { board: await n("draftdeck.v1"), saved: await n("draftdeck.v1:preresync") };
await resync(pasteLines.join(" "));            // the natural retry: paste the same thing again
const c = { board: await n("draftdeck.v1"), saved: await n("draftdeck.v1:preresync") };
const out = { deck: html, afterClean: a, afterFirstWipe: b, afterRetry: c, pageErrors: errors };
await browser.close();
fs.writeFileSync(outPath, JSON.stringify(out, null, 1)); console.log(JSON.stringify(out));
