"""Tests for wavesurf._html."""

from __future__ import annotations

from wavesurf._controls import Controls
from wavesurf._events import EventHandler
from wavesurf._html import (
    build_player_html,
    estimate_player_height,
    wrap_in_iframe,
)
from wavesurf._options import WaveSurferOptions
from wavesurf._theme import DARK, Theme


class TestBuildPlayerHtml:
    def test_contains_waveform_div(self):
        html = build_player_html(
            uid="test123",
            url="https://example.com/audio.wav",
            title=None,
            options=WaveSurferOptions(),
            theme=DARK,
            controls=Controls(),
        )
        assert 'id="waveform-test123"' in html

    def test_contains_wavesurfer_create(self):
        html = build_player_html(
            uid="test123",
            url="https://example.com/audio.wav",
            title=None,
            options=WaveSurferOptions(),
            theme=DARK,
            controls=Controls(),
        )
        assert "WaveSurfer.create(" in html

    def test_title_rendered(self):
        html = build_player_html(
            uid="t1",
            url="data:audio/wav;base64,x",
            title="My Title",
            options=WaveSurferOptions(),
            theme=DARK,
            controls=Controls(),
        )
        assert "My Title" in html

    def test_no_title_block_when_none(self):
        html = build_player_html(
            uid="t1",
            url="data:audio/wav;base64,x",
            title=None,
            options=WaveSurferOptions(),
            theme=DARK,
            controls=Controls(),
        )
        # No title text or title div marker
        assert "margin-bottom: 14px" not in html

    def test_shield_button_theme(self):
        shield_theme = Theme(
            wave_color=["#aaa", "#bbb"],
            progress_color=["#ccc", "#ddd"],
            background="#1a293d",
            play_button_style="shield",
            play_button_color="#0A141F",
            play_button_bg="linear-gradient(135deg, #d4a96a, #b98b5a)",
            top_accent="linear-gradient(90deg, transparent, #aaa, transparent)",
            background_pattern="url('data:image/svg+xml,...')",
        )
        html = build_player_html(
            uid="r1",
            url="data:audio/wav;base64,x",
            title="Brand Test",
            options=WaveSurferOptions(),
            theme=shield_theme,
            controls=Controls(),
        )
        # Shield button SVG gradient
        assert "copperGrad-r1" in html
        # Background pattern
        assert "background-image" in html
        # Top accent
        assert "linear-gradient(90deg, transparent, #aaa, transparent)" in html

    def test_events_wired(self):
        events = [EventHandler(event="ready", js="console.log('hi');")]
        html = build_player_html(
            uid="e1",
            url="data:audio/wav;base64,x",
            title=None,
            options=WaveSurferOptions(),
            theme=DARK,
            controls=Controls(),
            events=events,
        )
        assert 'ws.on("ready"' in html

    def test_options_applied(self):
        opts = WaveSurferOptions(bar_width=5, normalize=True)
        html = build_player_html(
            uid="o1",
            url="data:audio/wav;base64,x",
            title=None,
            options=opts,
            theme=DARK,
            controls=Controls(),
        )
        assert '"barWidth": 5' in html
        assert '"normalize": true' in html


class TestWrapInIframe:
    def test_iframe_structure(self):
        iframe = wrap_in_iframe(body_html="<p>test</p>", height=200)
        assert iframe.startswith("<iframe")
        assert 'srcdoc="' in iframe
        assert 'height: 200px' in iframe
        assert 'allow="autoplay"' in iframe

    def test_contains_wavesurfer_script(self):
        iframe = wrap_in_iframe(body_html="<p>test</p>", height=200)
        # The wavesurfer.js source should be embedded (escaped)
        assert "&lt;script&gt;" in iframe


class TestEstimatePlayerHeight:
    def test_with_title_and_controls(self):
        h = estimate_player_height(
            title="Test",
            theme=DARK,
            controls=Controls(),
        )
        # Should be > waveform height alone
        assert h > 80

    def test_without_title(self):
        h_with = estimate_player_height(title="Test", theme=DARK, controls=Controls())
        h_without = estimate_player_height(title=None, theme=DARK, controls=Controls())
        assert h_with > h_without

    def test_no_controls(self):
        h = estimate_player_height(
            title=None,
            theme=DARK,
            controls=Controls(
                show_play_button=False,
                show_time=False,
            ),
        )
        # Just padding + waveform + margin
        assert h < 150
