import { test, expect } from '@playwright/test';

test.describe('Username Check', () => {
  test('should show input field with label', async ({ page }) => {
    await page.goto('/');
    
    const input = page.locator('input[type="text"]');
    await expect(input).toBeVisible();
    
    const label = page.locator('label');
    await expect(label).toHaveText('Pick a username');
  });

  test('should not trigger API call for username < 3 characters', async ({ page }) => {
    await page.goto('/');
    
    const input = page.locator('input[type="text"]');
    await input.fill('ab');
    
    // Wait for debounce timeout
    await page.waitForTimeout(500);
    
    // Should not show loading or status icons
    const loader = page.locator('.animate-spin');
    await expect(loader).not.toBeVisible();
    
    const checkIcon = page.locator('text=Check').first();
    await expect(checkIcon).not.toBeVisible();
  });

  test('should show loading state while checking username', async ({ page }) => {
    await page.goto('/');
    
    const input = page.locator('input[type="text"]');
    await input.fill('testuser');
    
    // Should show loading spinner
    const loader = page.locator('.animate-spin');
    await expect(loader).toBeVisible();
  });

  test('should show success icon for available username', async ({ page }) => {
    await page.goto('/');
    
    const input = page.locator('input[type="text"]');
    await input.fill('veryuniqueusername12345');
    
    // Wait for API call to complete
    await page.waitForTimeout(500);
    
    // Should show check icon (green)
    const checkIcon = page.locator('svg[color="#0b8043"]');
    await expect(checkIcon).toBeVisible();
  });

  test('should show error icon for taken username', async ({ page }) => {
    await page.goto('/');
    
    const input = page.locator('input[type="text"]');
    await input.fill('alice');
    
    // Wait for API call to complete
    await page.waitForTimeout(500);
    
    // Should show error icon (red)
    const errorIcon = page.locator('svg[color="#d93025"]');
    await expect(errorIcon).toBeVisible();
  });

  test('should show error message when username is taken', async ({ page }) => {
    await page.goto('/');
    
    const input = page.locator('input[type="text"]');
    await input.fill('alice');
    
    // Wait for API call to complete
    await page.waitForTimeout(500);
    
    const errorMsg = page.locator('.error-msg');
    await expect(errorMsg).toBeVisible();
    await expect(errorMsg).toContainText('That username is taken');
  });

  test('should apply focused class when input is focused', async ({ page }) => {
    await page.goto('/');
    
    const inputGroup = page.locator('.input-group');
    const input = page.locator('input[type="text"]');
    
    await expect(inputGroup).not.toHaveClass(/focused/);
    
    await input.focus();
    await expect(inputGroup).toHaveClass(/focused/);
    
    await input.blur();
    await expect(inputGroup).not.toHaveClass(/focused/);
  });

  test('should shrink label when input has value or is focused', async ({ page }) => {
    await page.goto('/');
    
    const label = page.locator('label');
    const input = page.locator('input[type="text"]');
    
    // Label should shrink when focused
    await input.focus();
    await expect(label).toHaveClass(/shrink/);
    
    // Label should shrink when has value
    await input.fill('test');
    await input.blur();
    await expect(label).toHaveClass(/shrink/);
  });
});
