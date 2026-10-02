import { expect, test } from "@playwright/test";

// The video path: offline visit -> Urgent -> sync -> facility inbox ->
// Emergency after reconciliation -> contest -> recomputes.
test.describe("Mizani demo path", () => {
  test("offline decide, sync, reconcile, contest", async ({ page }) => {
    // 1. Community side, offline
    await page.goto("/community");
    await expect(page.getByText("Decisions run on this device's rule pack")).toBeVisible();

    await page.getByLabel("Gestational age in weeks").fill("34");

    // tap the two danger signs
    await page.locator('[data-sign="severe-headache"]').getByLabel("Present").click();
    await page.locator('[data-sign="visual-disturbance"]').getByLabel("Present").click();

    await page.getByLabel("Systolic").fill("152");
    await page.getByLabel("Diastolic").fill("98");

    await page.getByRole("button", { name: "Get Decision" }).click();
    await expect(page.getByLabel("Risk level: Urgent").first()).toBeVisible({ timeout: 30000 });
    await expect(page.getByText("Queued, will sync when connection returns")).toBeVisible();

    // 2. Connectivity returns
    await page.getByLabel("Connectivity").click();
    await expect(page.getByText("Referral synced to Mtwapa Health Centre.")).toBeVisible({ timeout: 15000 });

    // 3. Facility inbox shows the referral (the pending row is Amina's new one)
    await page.goto("/facility");
    const aminaRow = page.getByRole("row", { name: /Amina/ }).filter({ hasText: "Pending" });
    await expect(aminaRow).toBeVisible({ timeout: 10000 });
    await aminaRow.click();
    await expect(page.getByText("Community Witness").first()).toBeVisible();

    // 4. Add facility readings: nifedipine, 138/88, repeat 148/96, protein 2+
    await page.getByRole("button", { name: "Add Facility Reading" }).first().click();
    await page.getByLabel("Systolic").fill("138");
    await page.getByLabel("Diastolic").fill("88");
    await page.locator("select").first().selectOption("2");
    await page.locator("select").nth(1).selectOption("nifedipine-oral");
    await page.getByRole("button", { name: "Save And Reconcile" }).click();

    // 5. Reconciled: Emergency with the diff
    await expect(page.getByLabel("Risk level: Emergency").first()).toBeVisible({ timeout: 30000 });
    await page.getByRole("tab", { name: "Changes" }).click();
    await expect(page.getByText("Level Changed").first()).toBeVisible();
    await expect(page.getByText("From Memory").first()).toBeVisible();

    // 6. Contest the headache: still Emergency (visual remains)
    await page.getByRole("tab", { name: "Reasoning" }).click();
    const severeRow = page.locator("[data-slot='item']", { hasText: "Severe symptom" });
    await severeRow.getByRole("button", { name: "Contest" }).click();
    await page.getByPlaceholder(/Reason, for example/).fill("Headache resolved after paracetamol");
    await page.getByRole("button", { name: "Withdraw Premise" }).click();
    await expect(page.getByLabel("Risk level: Emergency").first()).toBeVisible({ timeout: 30000 });

    // 7. Contest the visual disturbance too: drops to Urgent (pre-eclampsia)
    await severeRow.getByRole("button", { name: "Contest" }).click();
    await page.getByPlaceholder(/Reason, for example/).fill("Vision normal after rest");
    await page.getByRole("button", { name: "Withdraw Premise" }).click();
    await expect(page.getByLabel("Risk level: Urgent").first()).toBeVisible({ timeout: 30000 });
  });
});
