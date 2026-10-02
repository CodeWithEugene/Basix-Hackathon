import { test } from "@playwright/test";

test("light mode check", async ({ page }) => {
  await page.emulateMedia({ colorScheme: "light" });
  await page.goto("https://mizani.codewitheugene.top/");
  await page.waitForTimeout(2500);
  const bg = await page.evaluate(() => getComputedStyle(document.body).backgroundColor);
  console.log("body background:", bg);
  await page.screenshot({ path: "/tmp/mizani-video/light-home.png" });
  await page.goto("https://mizani.codewitheugene.top/community");
  await page.waitForTimeout(1500);
  await page.screenshot({ path: "/tmp/mizani-video/light-community.png" });
  await page.goto("https://mizani.codewitheugene.top/facility");
  await page.waitForTimeout(2000);
  await page.screenshot({ path: "/tmp/mizani-video/light-facility.png" });
});
