"""E2E tests for standalone example pages."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

# (page_name, primary_selector, expected_count, extra_selectors)
EXAMPLE_PAGES = [
    ("basic", '[id^="player-"]', 1, ['[id^="waveform-"]', '[id^="play-"]', '[id^="time-"]']),
    ("bars", '[id^="player-"]', 3, ['[id^="waveform-"]']),
    ("gradients", '[id^="player-"]', 3, []),
    ("timeline", '[id^="player-"]', 1, ['[id^="waveform-"]']),
    ("minimap", '[id^="player-"]', 1, ['[id^="waveform-"]']),
    ("spectrogram", '[id^="player-"]', 1, []),
    ("regions", '[id^="player-"]', 1, []),
    ("controls", '[id^="player-"]', 3, ['[id^="play-"]', '[id^="volume-"]', '[id^="rate-"]']),
    ("layout", '[id^="player-"]', 4, ['[id^="waveform-"]']),
    ("custom_theme", '[id^="player-"]', 1, []),
    ("themes", '[id^="player-"]', 2, []),
]

# Regions page needs longer wait for plugin to initialise.
WAIT_OVERRIDES = {"regions": 3000}
DEFAULT_WAIT = 2000


class TestExamplePages:
    @pytest.mark.parametrize(
        "page_name, selector, count, extras",
        EXAMPLE_PAGES,
        ids=[name for name, *_ in EXAMPLE_PAGES],
    )
    def test_dom_structure(
        self,
        page: Page,
        base_url: str,
        page_name: str,
        selector: str,
        count: int,
        extras: list[str],
    ) -> None:
        page.goto(f"{base_url}/examples/{page_name}.html")

        primary = page.locator(selector)
        if count == 1:
            expect(primary.first).to_be_attached()
        else:
            expect(primary).to_have_count(count)

        for extra in extras:
            if count > 1:
                expect(page.locator(extra)).to_have_count(count)
            else:
                expect(page.locator(extra).first).to_be_attached()

    @pytest.mark.parametrize(
        "page_name",
        [name for name, *_ in EXAMPLE_PAGES],
    )
    def test_visual_regression(
        self,
        page: Page,
        base_url: str,
        page_name: str,
        assert_snapshot,
    ) -> None:
        page.goto(f"{base_url}/examples/{page_name}.html")
        wait_ms = WAIT_OVERRIDES.get(page_name, DEFAULT_WAIT)
        page.wait_for_timeout(wait_ms)
        assert_snapshot(page, threshold=0.1)
