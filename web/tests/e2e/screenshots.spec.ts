import { test } from "@playwright/test";

// Screenshot pass over the seeded demo flow (for docs/images).
test.use({ viewport: { width: 1440, height: 900 } });

test("screens", async ({ page }) => {
  const shot = (name: string) =>
    page.screenshot({ path: `../docs/images/${name}.png`, fullPage: false });

  await page.goto("/");
  await shot("welcome-light");

  await page.goto("/community");
  await page.getByLabel("Gestational age in weeks").fill("34");
  await page.locator('[data-sign="severe-headache"]').getByLabel("Present").click();
  await page.locator('[data-sign="visual-disturbance"]').getByLabel("Present").click();
  await page.getByLabel("Systolic").fill("152");
  await page.getByLabel("Diastolic").fill("98");
  await page.getByRole("button", { name: "Get Decision" }).click();
  await page.getByLabel("Risk level: Urgent").first().waitFor({ timeout: 30000 });
  await shot("community-offline-urgent");

  await page.getByLabel("Connectivity").click();
  await page.getByText("Referral synced to Mtwapa Health Centre.").waitFor({ timeout: 15000 });

  await page.goto("/facility");
  const row = page.getByRole("row", { name: /Amina/ }).filter({ hasText: "Pending" });
  await row.waitFor({ timeout: 10000 });
  await shot("facility-inbox");
  await row.click();

  await page.getByText("Community Witness").first().waitFor();
  await page.getByRole("button", { name: "Add Facility Reading" }).first().click();
  await page.getByLabel("Systolic").fill("138");
  await page.getByLabel("Diastolic").fill("88");
  await page.locator("select").first().selectOption("2");
  await page.locator("select").nth(1).selectOption("nifedipine-oral");
  await page.getByRole("button", { name: "Save And Reconcile" }).click();
  await page.getByLabel("Risk level: Emergency").first().waitFor({ timeout: 30000 });
  await shot("reconciliation-emergency");

  await page.getByRole("tab", { name: "Changes" }).click();
  await page.getByText("Level Changed").first().waitFor();
  await shot("changes-diff");

  await page.getByRole("tab", { name: "Proof" }).click();
  await shot("proof");

  // dark mode
  await page.emulateMedia({ colorScheme: "dark" });
  await page.getByRole("tab", { name: "Reasoning" }).click();
  await shot("reconciliation-dark");

  const severeRow = page.locator("[data-slot='item']", { hasText: "Severe symptom" });
  await severeRow.getByRole("button", { name: "Contest" }).click();
  await page.getByPlaceholder(/Reason, for example/).fill("Headache resolved after paracetamol");
  await shot("contest-dialog");
  await page.getByRole("button", { name: "Withdraw Premise" }).click();
  await page.getByLabel("Risk level: Emergency").first().waitFor({ timeout: 30000 });
});
