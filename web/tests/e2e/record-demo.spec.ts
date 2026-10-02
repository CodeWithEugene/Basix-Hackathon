import { expect, test, type Locator, type Page } from "@playwright/test";

// Records the full demo at 1080p in light mode with a visible cursor.
// One continuous take; beat timestamps are printed for the edit.

const BASE = "https://mizani.codewitheugene.top";

const CURSOR_CSS = `
#mizani-cursor {
  position: fixed; z-index: 2147483647; pointer-events: none;
  width: 30px; height: 30px; margin: -3px 0 0 -3px;
  filter: drop-shadow(0 2px 6px rgba(0,0,0,0.45));
  transition: none;
}
#mizani-cursor svg { display: block; }
`;

const CURSOR_SVG = `<svg width="30" height="30" viewBox="0 0 30 30" xmlns="http://www.w3.org/2000/svg">
  <path d="M7 3 L24 15 L15.5 16.5 L12 24 Z" fill="#0b0e14" stroke="#ffffff" stroke-width="1.6" stroke-linejoin="round"/>
</svg>`;

async function injectCursor(page: Page) {
  await page.addStyleTag({ content: CURSOR_CSS }).catch(() => {});
  await page.evaluate((svg) => {
    if (document.getElementById("mizani-cursor")) return;
    const el = document.createElement("div");
    el.id = "mizani-cursor";
    el.innerHTML = svg;
    document.body.appendChild(el);
  }, CURSOR_SVG);
}

async function placeCursor(page: Page, x: number, y: number) {
  await page.evaluate(
    ([x, y]) => {
      const el = document.getElementById("mizani-cursor");
      if (el) {
        (el as HTMLElement).style.left = `${x}px`;
        (el as HTMLElement).style.top = `${y}px`;
      }
    },
    [x, y],
  );
}

async function moveTo(page: Page, x: number, y: number, steps = 18) {
  const from = await page.evaluate(() => {
    const el = document.getElementById("mizani-cursor") as HTMLElement | null;
    return el
      ? [parseFloat(el.style.left || "960"), parseFloat(el.style.top || "540")]
      : [960, 540];
  });
  for (let i = 1; i <= steps; i++) {
    const t = i / steps;
    const ease = 1 - Math.pow(1 - t, 3);
    const cx = from[0] + (x - from[0]) * ease;
    const cy = from[1] + (y - from[1]) * ease;
    await page.mouse.move(cx, cy);
    await placeCursor(page, cx, cy);
    await page.waitForTimeout(22);
  }
}

async function center(loc: Locator): Promise<[number, number]> {
  const box = await loc.boundingBox();
  if (!box) throw new Error("element not visible");
  return [box.x + box.width / 2, box.y + box.height / 2];
}

async function clickAt(page: Page, loc: Locator, label: string) {
  const [x, y] = await center(loc);
  await moveTo(page, x, y);
  await page.waitForTimeout(260);
  await loc.click({ timeout: 15000 });
  console.log(`[beat] click ${label}`);
  await page.waitForTimeout(320);
}

async function typeSlow(page: Page, loc: Locator, text: string, label: string, delay = 55) {
  const [x, y] = await center(loc);
  await moveTo(page, x, y);
  await page.mouse.down();
  await page.waitForTimeout(80);
  await page.mouse.up();
  await loc.fill("");
  for (const ch of text) {
    await page.keyboard.type(ch);
    await page.waitForTimeout(delay);
  }
  console.log(`[beat] typed ${label}`);
  await page.waitForTimeout(300);
}

async function scrollTo(page: Page, loc: Locator) {
  await loc.scrollIntoViewIfNeeded();
  await page.waitForTimeout(450);
}

test.describe.configure({ mode: "serial" });

test("record full demo", async ({ page }) => {
  test.setTimeout(420000);
  await page.emulateMedia({ colorScheme: "light" });
  await injectCursor(page);
  await placeCursor(page, 960, 540);

  // ---- Beat 1: community visit, offline ----
  console.log("[beat] 1 community offline @ 0s");
  await page.goto(BASE + "/community");
  await injectCursor(page);
  await page.waitForTimeout(2600);
  await expect(page.getByText("Decisions run on this device's rule pack")).toBeVisible();
  await page.waitForTimeout(1800);

  const ga = page.getByLabel("Gestational age in weeks");
  await scrollTo(page, ga);
  await typeSlow(page, ga, "34", "ga");

  const note = page.getByPlaceholder(/Andika maelezo/);
  await scrollTo(page, note);
  await typeSlow(
    page,
    note,
    "Mama analalamika kichwa kinauma sana tangu jana, anaona giza kidogo. Miguu imevimba.",
    "note",
    40,
  );
  await page.waitForTimeout(900);

  const headache = page.locator('[data-sign="severe-headache"]');
  await scrollTo(page, headache);
  await clickAt(page, headache.getByLabel("Present"), "headache present");
  await page.waitForTimeout(500);
  const vision = page.locator('[data-sign="visual-disturbance"]');
  await clickAt(page, vision.getByLabel("Present"), "vision present");
  await page.waitForTimeout(600);

  const vitals = page.getByLabel("Systolic");
  await scrollTo(page, vitals);
  await typeSlow(page, page.getByLabel("Systolic"), "152", "sbp");
  await typeSlow(page, page.getByLabel("Diastolic"), "98", "dbp");
  await page.waitForTimeout(600);

  const getDecision = page.getByRole("button", { name: "Get Decision" });
  await scrollTo(page, getDecision);
  console.log("[beat] 2 decision @ ~40s");
  await clickAt(page, getDecision, "get decision");
  await expect(page.getByLabel("Risk level: Urgent").first()).toBeVisible({ timeout: 40000 });
  await page.waitForTimeout(2600);
  const proofCard = page.getByText("Frequency").first();
  await scrollTo(page, proofCard);
  await page.waitForTimeout(2200);

  // ---- Beat 3: connectivity returns ----
  console.log("[beat] 3 sync @ ~55s");
  const conn = page.getByLabel("Connectivity");
  await clickAt(page, conn, "connectivity online");
  await page.waitForTimeout(2600);

  // ---- Beat 4: facility inbox ----
  console.log("[beat] 4 inbox @ ~62s");
  await page.goto(BASE + "/facility");
  await injectCursor(page);
  await page.waitForTimeout(3200);
  const aminaRow = page.getByRole("row", { name: /Amina/ }).first();
  await scrollTo(page, aminaRow);
  await clickAt(page, aminaRow, "open amina");
  await injectCursor(page);
  await expect(page.getByText("Community Witness").first()).toBeVisible({ timeout: 15000 });
  await page.waitForTimeout(2600);
  const facWitness = page.getByText("Facility Witness").first();
  await scrollTo(page, facWitness);
  await page.waitForTimeout(1600);

  // ---- Beat 5: add facility readings -> Emergency ----
  console.log("[beat] 5 facility readings @ ~85s");
  const addReading = page.getByRole("button", { name: "Add Facility Reading" }).first();
  await clickAt(page, addReading, "add facility reading");
  await page.waitForTimeout(1600);
  const sheet = page.getByRole("dialog");
  await typeSlow(page, sheet.getByLabel("Systolic"), "138", "facility sbp");
  await typeSlow(page, sheet.getByLabel("Diastolic"), "88", "facility dbp");
  const protein = sheet.locator("select").first();
  const [px, py] = await center(protein);
  await moveTo(page, px, py);
  await page.waitForTimeout(250);
  await protein.selectOption("2");
  await page.waitForTimeout(500);
  const treatment = sheet.locator("select").nth(1);
  await treatment.selectOption("nifedipine-oral");
  await page.waitForTimeout(700);
  await clickAt(page, page.getByRole("button", { name: "Save And Reconcile" }), "save and reconcile");
  await expect(page.getByLabel("Risk level: Emergency").first()).toBeVisible({ timeout: 40000 });
  await page.waitForTimeout(3000);

  // ---- Beat 6: the diff ----
  console.log("[beat] 6 changes tab @ ~110s");
  const changesTab = page.getByRole("tab", { name: "Changes" });
  await clickAt(page, changesTab, "changes tab");
  await page.waitForTimeout(2400);
  const fromMemory = page.getByText("From Memory").first();
  await scrollTo(page, fromMemory);
  await page.waitForTimeout(2600);

  // ---- Beat 7: proof + reasoning ----
  const reasoningTab = page.getByRole("tab", { name: "Reasoning" });
  await clickAt(page, reasoningTab, "reasoning tab");
  await page.waitForTimeout(2200);
  const defeat = page.getByText("Defeated").first();
  await scrollTo(page, defeat);
  await page.waitForTimeout(2400);

  // ---- Beat 8: contest headache -> still emergency ----
  console.log("[beat] 8 contest @ ~135s");
  const severeRow = page.locator("[data-slot='item']", { hasText: "Severe symptom" });
  await scrollTo(page, severeRow);
  await clickAt(page, severeRow.getByRole("button", { name: "Contest" }), "contest severe symptom");
  await page.waitForTimeout(1000);
  const reason = page.getByPlaceholder(/Reason, for example/);
  await typeSlow(page, reason, "Headache resolved after paracetamol", "contest reason", 45);
  await clickAt(page, page.getByRole("button", { name: "Withdraw Premise" }), "withdraw premise");
  await page.waitForTimeout(3200);
  await expect(page.getByLabel("Risk level: Emergency").first()).toBeVisible({ timeout: 30000 });
  await page.waitForTimeout(2200);

  // ---- Beat 9: contest vision -> urgent ----
  console.log("[beat] 9 contest vision @ ~155s");
  const severeRow2 = page.locator("[data-slot='item']", { hasText: "Severe symptom" });
  await clickAt(page, severeRow2.getByRole("button", { name: "Contest" }), "contest vision");
  await page.waitForTimeout(900);
  const reason2 = page.getByPlaceholder(/Reason, for example/);
  await typeSlow(page, reason2, "Vision normal after rest", "contest reason 2", 45);
  await clickAt(page, page.getByRole("button", { name: "Withdraw Premise" }), "withdraw premise 2");
  await expect(page.getByLabel("Risk level: Urgent").first()).toBeVisible({ timeout: 40000 });
  await page.waitForTimeout(2800);

  // ---- Beat 10: memory ----
  console.log("[beat] 10 memory @ ~175s");
  await page.goto(BASE + "/mothers/M-AMINA");
  await injectCursor(page);
  await page.waitForTimeout(3200);
  const chart = page.getByText("BP Over Pregnancy");
  await scrollTo(page, chart);
  await page.waitForTimeout(2400);
  const encounters = page.getByText("Encounters").first();
  await scrollTo(page, encounters);
  await page.waitForTimeout(2200);

  // ---- Beat 11: audit ----
  console.log("[beat] 11 audit @ ~195s");
  await page.goto(BASE + "/audit");
  await injectCursor(page);
  await page.waitForTimeout(3200);
  const filter = page.getByPlaceholder(/Filter atoms/);
  await typeSlow(page, filter, "contested", "audit filter", 60);
  await page.waitForTimeout(2600);

  // ---- Beat 12: rules ----
  console.log("[beat] 12 rules @ ~210s");
  await page.goto(BASE + "/rules");
  await injectCursor(page);
  await page.waitForTimeout(3000);
  const peRule = page.getByText("r_pe_severe_symp").first();
  await scrollTo(page, peRule);
  await page.waitForTimeout(2800);

  console.log("[beat] done @ ~225s");
});
