import { test } from "@playwright/test";

test("capture desktop screenshot", async ({ page }) => {
  await page.goto("/");
  // Wait for the fonts and images to load
  await page.waitForLoadState("networkidle");
  await page.screenshot({ path: "tests/screenshots/desktop-current.png", fullPage: true });
});

test("capture mobile screenshot", async ({ page }) => {
  await page.goto("/");
  await page.waitForLoadState("networkidle");
  await page.screenshot({ path: "tests/screenshots/mobile-current.png", fullPage: true });
});
