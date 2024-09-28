import { test, expect, FrameLocator, Locator } from "@playwright/test";

const url = "https://vuejs.org/examples/#crud";

let frame: FrameLocator;
let filterInput: Locator;
let firstnameInput: Locator;
let surnameInput: Locator;
let select: Locator;
let createButton: Locator;
let updateButton: Locator;
let deleteButton: Locator;

async function hoverAndClickAsync(locator: Locator): Promise<void> {
  await locator.hover();
  await locator.click();
}

test.beforeEach(async ({ page }) => {
  await page.goto(url);
  frame = page.frameLocator("iFrame");
  filterInput = frame.getByPlaceholder("Filter prefix");
  firstnameInput = frame.getByLabel("Name:", { exact: true });
  surnameInput = frame.getByLabel("Surname:");
  select = frame.locator("select");
  createButton = frame.getByRole("button", { name: "Create" });
  updateButton = frame.getByRole("button", { name: "Update" });
  deleteButton = frame.getByRole("button", { name: "Delete" });

  await expect(filterInput).toBeVisible();
  await expect(firstnameInput).toBeVisible();
  await expect(surnameInput).toBeVisible();
  await expect(select).toBeVisible();
  await expect(createButton).toBeVisible();
  await expect(updateButton).toBeVisible();
  await expect(deleteButton).toBeVisible();
});

test("Filter entries", async () => {
  await expect(select).toHaveText("Emil, HansMustermann, MaxTisch, Roman");
  await filterInput.fill("Emil");
  await expect(select).toHaveText("Emil, Hans");
  await filterInput.fill("Mu");
  await expect(select).toHaveText("Mustermann, Max");
  await filterInput.clear();
  await expect(select).toHaveText("Emil, HansMustermann, MaxTisch, Roman");
});

test("Create entry", async () => {
  await firstnameInput.fill("Dude");
  await surnameInput.fill("Dudovic");
  await hoverAndClickAsync(createButton);
  await expect(firstnameInput).toBeEmpty();
  await expect(surnameInput).toBeEmpty();
  await expect(select).toContainText("Dudovic, Dude");
});

test("Select entry", async () => {
  await select.selectOption("Mustermann, Max");
  await expect(firstnameInput).toHaveValue("Max");
  await expect(surnameInput).toHaveValue("Mustermann");
});

test("Create entry while another entry is selected", async () => {
  await select.selectOption("Mustermann, Max");
  await firstnameInput.clear();
  await firstnameInput.fill("Dude");
  await surnameInput.clear();
  await surnameInput.fill("Dudovic");
  await hoverAndClickAsync(createButton);
  await expect(select).toContainText("Dudovic, Dude");
  await expect(select).toContainText("Mustermann, Max");
});

test("Update entry", async () => {
  await select.selectOption("Mustermann, Max");
  await firstnameInput.fill("Hue");
  await hoverAndClickAsync(updateButton);
  await expect(firstnameInput).toHaveValue("Hue");
  await expect(surnameInput).toHaveValue("Mustermann");
  await expect(select).toContainText("Mustermann, Hue");
  await expect(select).not.toContainText("Mustermann, Max");

  await surnameInput.fill("Kaiser");
  await hoverAndClickAsync(updateButton);
  await expect(surnameInput).toHaveValue("Kaiser");
  await expect(select).toContainText("Kaiser, Hue");
  await expect(select).not.toContainText("Mustermann, Hue");

  await firstnameInput.fill("Trent");
  await surnameInput.fill("Reznor");
  await hoverAndClickAsync(updateButton);
  await expect(select).toContainText("Reznor, Trent");
  await expect(select).not.toContainText("Kaiser, Hue");
});

test("Delete entry", async () => {
  await select.selectOption("Mustermann, Max");
  await hoverAndClickAsync(deleteButton);
  await expect(select).not.toHaveText("Mustermann, Max");
  await expect(await firstnameInput).toBeEmpty();
  await expect(await surnameInput).toBeEmpty();
});
