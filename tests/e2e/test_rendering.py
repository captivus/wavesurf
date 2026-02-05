"""E2E tests for waveform rendering inside iframes."""

from playwright.sync_api import Page, expect


class TestWaveformRendering:
    def test_renders_canvas_inside_iframe_dark_theme(
        self, page: Page, base_url: str
    ) -> None:
        page.goto(f"{base_url}/tests/e2e/fixtures/basic_dark.html")
        iframe = page.frame_locator("iframe")
        expect(iframe.locator('[id^="waveform-"]')).to_be_attached()

    def test_renders_canvas_inside_iframe_light_theme(
        self, page: Page, base_url: str
    ) -> None:
        page.goto(f"{base_url}/tests/e2e/fixtures/basic_light.html")
        iframe = page.frame_locator("iframe")
        expect(iframe.locator('[id^="waveform-"]')).to_be_attached()

    def test_contains_correct_element_ids(
        self, page: Page, base_url: str
    ) -> None:
        page.goto(f"{base_url}/tests/e2e/fixtures/basic_dark.html")
        iframe = page.frame_locator("iframe")

        player = iframe.locator('[id^="player-"]')
        expect(player).to_be_attached()

        player_id = player.get_attribute("id")
        uid = player_id.replace("player-", "")

        expect(iframe.locator(f"#waveform-{uid}")).to_be_attached()
        expect(iframe.locator(f"#play-{uid}")).to_be_attached()
        expect(iframe.locator(f"#time-{uid}")).to_be_attached()
        expect(iframe.locator(f"#icon-{uid}")).to_be_attached()
