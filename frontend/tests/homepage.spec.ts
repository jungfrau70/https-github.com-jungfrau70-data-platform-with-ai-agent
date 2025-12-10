import { test, expect } from '@playwright/test';

test('homepage loads application content', async ({ page }) => {
    const response = await page.goto('/');

    // Verify we got a successful response
    expect(response?.status()).toBe(200);

    // Wait for the page to be fully loaded
    await page.waitForLoadState('networkidle');

    // Check for actual application content, not the Nuxt welcome page
    const pageContent = await page.textContent('body');

    // If we see the welcome page text, the app isn't loading correctly
    const hasWelcomePage = pageContent?.includes('Remove this welcome page');
    expect(hasWelcomePage).toBeFalsy();

    // Check for actual app content
    const hasAppContent = pageContent?.includes('Data Insight to') ||
        pageContent?.includes('Video Content') ||
        await page.locator('text=Get Started').count() > 0;
    expect(hasAppContent).toBeTruthy();
});
