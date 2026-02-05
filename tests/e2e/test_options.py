"""E2E tests for custom options and visual regression."""

from playwright.sync_api import Page, expect


class TestCustomOptions:
    def test_loads_custom_options_page(
        self, page: Page, base_url: str
    ) -> None:
        page.goto(f"{base_url}/tests/e2e/fixtures/custom_options.html")
        expect(page.locator("iframe")).to_be_attached()

    def test_renders_volume_and_rate_controls(
        self, page: Page, base_url: str
    ) -> None:
        page.goto(f"{base_url}/tests/e2e/fixtures/all_controls.html")
        iframe = page.frame_locator("iframe")

        volume = iframe.locator('[id^="volume-"]')
        expect(volume).to_be_attached()
        assert volume.get_attribute("type") == "range"

        rate = iframe.locator('[id^="rate-"]')
        expect(rate).to_be_attached()
        assert rate.evaluate("el => el.tagName.toLowerCase()") == "select"

    def test_visual_regression_dark_theme(
        self, page: Page, base_url: str, assert_snapshot
    ) -> None:
        page.goto(f"{base_url}/tests/e2e/fixtures/basic_dark.html")
        page.wait_for_timeout(1000)
        assert_snapshot(page, threshold=0.1)
