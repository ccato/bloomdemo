import { test, expect } from '@playwright/test';

test.describe('Username Suggestions', () => {
  test('should show suggestions when username is taken', async ({ page }) => {
    await page.goto('/');
    
    const input = page.locator('input[type="text"]');
    await input.fill('alice');
    
    // Wait for API call to complete
    await page.waitForTimeout(500);
    
    const suggestions = page.locator('.username-suggestions');
    await expect(suggestions).toBeVisible();
    await expect(suggestions).toContainText('Available:');
  });

  test('should show suggestion buttons', async ({ page }) => {
    await page.goto('/');
    
    const input = page.locator('input[type="text"]');
    await input.fill('alice');
    
    // Wait for API call to complete
    await page.waitForTimeout(500);
    
    const buttons = page.locator('.username-suggestions button');
    await expect(buttons).toHaveCount(3);
  });

  test('should update input when clicking suggestion', async ({ page }) => {
    await page.goto('/');
    
    const input = page.locator('input[type="text"]');
    await input.fill('alice');
    
    // Wait for API call to complete
    await page.waitForTimeout(500);
    
    const firstButton = page.locator('.username-suggestions button').first();
    const buttonText = await firstButton.textContent();
    
    await firstButton.click();
    
    if (buttonText) {
      await expect(input).toHaveValue(buttonText);
    }
  });

  test('should not show suggestions for available username', async ({ page }) => {
    await page.goto('/');
    
    const input = page.locator('input[type="text"]');
    await input.fill('veryuniqueusername12345');
    
    // Wait for API call to complete
    await page.waitForTimeout(500);
    
    const suggestions = page.locator('.username-suggestions');
    await expect(suggestions).not.toBeVisible();
  });

  test('should hide suggestions when username becomes available', async ({ page }) => {
    await page.goto('/');
    
    const input = page.locator('input[type="text"]');
    
    // Type taken username
    await input.fill('alice');
    await page.waitForTimeout(500);
    
    const suggestions = page.locator('.username-suggestions');
    await expect(suggestions).toBeVisible();
    
    // Type available username
    await input.fill('veryuniqueusername12345');
    await page.waitForTimeout(500);
    
    await expect(suggestions).not.toBeVisible();
  });
});
