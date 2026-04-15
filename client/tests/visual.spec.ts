import { expect, test } from "@playwright/test";

test.describe("Visual Regression", () => {
  test("Desktop Viewport", async ({ page }) => {
    // Reference was 1656px wide
    await page.setViewportSize({ width: 1656, height: 1338 });
    await page.goto("/");
    await page.waitForLoadState("networkidle");
    await page.waitForTimeout(3000);
    await expect(page).toHaveScreenshot("desktop.png", {
      fullPage: true,
      maxDiffPixelRatio: 0.1, // Allowing more leeway due to OS differences
    });
  });

  test("Mobile Viewport", async ({ page }) => {
    // Reference was 700px wide
    await page.setViewportSize({ width: 700, height: 1446 });
    await page.goto("/");
    await page.waitForLoadState("networkidle");
    await page.waitForTimeout(3000);
    await expect(page).toHaveScreenshot("mobile.png", {
      fullPage: true,
      maxDiffPixelRatio: 0.1,
    });
  });
});
