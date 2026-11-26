import { expect, test } from '@playwright/test';

test('shows a customer order list', async ({ page }) => {
  await page.route('**/api/customers/c-1/orders', (route) =>
    route.fulfill({ json: [{ id: 1, total_cents: 1000, notes: null }] }),
  );
  await page.goto('/?customer=c-1');
  await expect(page.getByRole('row')).toHaveCount(2);
});
