import { test, expect, FrameLocator, Locator } from "@playwright/test";

const url = "https://vuejs.org/examples/#form-bindings";

let frame: FrameLocator;

async function hoverAndClickAsync(locator: Locator): Promise<void> {
  await locator.hover();
  await locator.click();
}

test.beforeEach(async ({ page }) => {
  await page.goto(url);
  frame = page.frameLocator("iFrame");
  await expect(frame.getByRole("heading", { name: "Text Input" })).toBeVisible();
});

test("Input", async () => {
  const input = frame.locator("input").first();

  await expect(await input.inputValue()).toBe("Edit me");
  await hoverAndClickAsync(input);
  await input.fill("Edited text");
  await expect(await frame.locator("p").first()).toHaveText("Edited text");
});

test("Checkbox", async () => {
  const checkBox = frame.getByLabel("Checked");

  await expect(frame.getByText("Checked: true")).toBeVisible();
  await expect(checkBox).toBeVisible();
  await expect(checkBox).toBeChecked();
  await hoverAndClickAsync(checkBox);
  await expect(checkBox).not.toBeChecked();
  await expect(frame.getByText("Checked: false")).toBeVisible();
});

test("Multi checkbox", async () => {
  const jackBox = frame.getByLabel("Jack");
  const johnBox = frame.getByLabel("John");
  const mikeBox = frame.getByLabel("Mike");
  const namesParagraph = frame.locator("p").nth(1);

  for (const element of [jackBox, johnBox, mikeBox, namesParagraph]) {
    await expect(element).toBeVisible();
  }
  await expect(jackBox).toBeChecked();
  await expect(johnBox).not.toBeChecked();
  await expect(mikeBox).not.toBeChecked();
  await expect(namesParagraph).toHaveText('Checked names: [ "Jack" ]');
  await hoverAndClickAsync(jackBox);
  await expect(jackBox).not.toBeChecked();
  await expect(namesParagraph).toHaveText("Checked names: []");

  await hoverAndClickAsync(johnBox);
  await hoverAndClickAsync(mikeBox);
  await expect(johnBox).toBeChecked();
  await expect(mikeBox).toBeChecked();
  await expect(namesParagraph).toHaveText('Checked names: [ "John", "Mike" ]');
});

test("Radio", async () => {
  const pickedParagraph = frame.locator("p").nth(2);
  const oneRadio = frame.getByLabel("One");
  const twoRadio = frame.getByLabel("Two");

  await expect(pickedParagraph).toBeVisible();
  await expect(oneRadio).toBeVisible();
  await expect(twoRadio).toBeVisible();

  await expect(oneRadio).toBeChecked();
  await expect(twoRadio).not.toBeChecked();
  await expect(pickedParagraph).toHaveText("Picked: One");

  await hoverAndClickAsync(twoRadio);
  await expect(twoRadio).toBeChecked();
  await expect(oneRadio).not.toBeChecked();
  await expect(pickedParagraph).toHaveText("Picked: Two");
});

test("Select", async () => {
  const selectedParagraph = frame.locator("p").nth(3);
  const select = frame.locator("select").first();

  await expect(select).toBeVisible();
  await expect(selectedParagraph).toBeVisible();
  await expect(selectedParagraph).toHaveText("Selected: A");

  await hoverAndClickAsync(select);
  select.selectOption("B");
  await expect(selectedParagraph).toHaveText("Selected: B");
});

test("Multi select", async () => {
  const selectedParagraph = frame.locator("p").nth(4);
  const select = frame.locator("select").last();

  await expect(select).toBeVisible();
  await expect(selectedParagraph).toBeVisible();
  await expect(selectedParagraph).toHaveText('Selected: [ "A" ]');

  await select.hover();
  await select.selectOption(["B", "C"]);
  await expect(selectedParagraph).toHaveText('Selected: [ "B", "C" ]');
});
