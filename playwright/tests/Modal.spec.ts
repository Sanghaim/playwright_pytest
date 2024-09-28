import { test, expect, Locator } from "@playwright/test";

const url = "https://vuejs.org/examples/#modal";

async function hoverAndClickAsync(locator: Locator): Promise<void> {
  await locator.hover();
  await locator.click();
}

test("Show modal, check content, close modal", async ({ page }) => {
  await page.goto(url);
  const frame = page.frameLocator("iFrame");
  const showModalButton = frame.getByRole("button", { name: "Show Modal" });
  await expect(showModalButton).toBeVisible();
  await hoverAndClickAsync(showModalButton);

  const modalContainer = frame.locator(".modal-container");
  await expect(modalContainer).toBeVisible();
  await expect(
    frame.getByRole("heading", { name: "Custom Header" })
  ).toBeVisible();
  const modalBody = frame.locator(".modal-body");
  await expect(modalBody).toBeVisible();
  await expect(modalBody).toHaveText("default body");
  const modalFooter = frame.locator(".modal-footer");
  await expect(modalFooter).toBeVisible();
  await expect(modalFooter).toHaveText(" default footer OK");
  const modalButton = frame.locator(".modal-default-button");
  await expect(modalButton).toBeVisible();
  await hoverAndClickAsync(modalButton);

  await expect(modalContainer).not.toBeVisible();
});
