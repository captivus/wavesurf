"""E2E tests for compare grid layout inside iframes."""

from playwright.sync_api import Page, expect


class TestCompareGridLayout:
    def test_renders_multiple_players_in_single_iframe(
        self, page: Page, base_url: str
    ) -> None:
        page.goto(f"{base_url}/tests/e2e/fixtures/compare_grid.html")
        iframe = page.frame_locator("iframe")
        expect(iframe.locator('[id^="player-"]')).to_have_count(3)

    def test_each_player_has_own_waveform(
        self, page: Page, base_url: str
    ) -> None:
        page.goto(f"{base_url}/tests/e2e/fixtures/compare_grid.html")
        iframe = page.frame_locator("iframe")
        waveforms = iframe.locator('[id^="waveform-"]')
        expect(waveforms).to_have_count(3)
        # Verify all IDs are unique.
        ids = [waveforms.nth(i).get_attribute("id") for i in range(3)]
        assert len(set(ids)) == 3

    def test_displays_correct_labels(
        self, page: Page, base_url: str
    ) -> None:
        page.goto(f"{base_url}/tests/e2e/fixtures/compare_grid.html")
        iframe = page.frame_locator("iframe")
        body = iframe.locator("body")
        expect(body).to_contain_text("440 Hz")
        expect(body).to_contain_text("660 Hz")
        expect(body).to_contain_text("880 Hz")

    def test_uses_grid_layout_container(
        self, page: Page, base_url: str
    ) -> None:
        page.goto(f"{base_url}/tests/e2e/fixtures/compare_grid.html")
        iframe = page.frame_locator("iframe")
        expect(iframe.locator('div[style*="display: grid"]')).to_be_attached()
