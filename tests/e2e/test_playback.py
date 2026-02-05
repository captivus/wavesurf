"""E2E tests for playback controls inside iframes."""

from playwright.sync_api import Page, expect


class TestPlaybackControls:
    def test_has_play_button(self, page: Page, base_url: str) -> None:
        page.goto(f"{base_url}/tests/e2e/fixtures/basic_dark.html")
        iframe = page.frame_locator("iframe")
        expect(iframe.locator('[id^="play-"]')).to_be_attached()

    def test_shows_initial_time_zero(self, page: Page, base_url: str) -> None:
        page.goto(f"{base_url}/tests/e2e/fixtures/basic_dark.html")
        iframe = page.frame_locator("iframe")
        expect(iframe.locator('[id^="time-"]')).to_contain_text("0:00")

    def test_play_icon_starts_with_play_symbol(
        self, page: Page, base_url: str
    ) -> None:
        page.goto(f"{base_url}/tests/e2e/fixtures/basic_dark.html")
        iframe = page.frame_locator("iframe")
        expect(iframe.locator('[id^="icon-"]')).to_contain_text("\u25b6")
