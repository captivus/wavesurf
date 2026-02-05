"""Tests for wavesurf._core."""

from __future__ import annotations

import numpy as np

from wavesurf import WaveSurfer, compare_audio, display_audio
from wavesurf._controls import Controls
from wavesurf._events import EventHandler
from wavesurf._theme import DARK, LIGHT, Theme


class TestWaveSurfer:
    def test_repr_html(self, sine_wave):
        audio, sr = sine_wave
        player = WaveSurfer(audio=audio, sr=sr, title="Test")
        html = player._repr_html_()
        assert "<iframe" in html
        assert "WaveSurfer.create(" in html

    def test_to_html_same_as_repr(self, sine_wave):
        audio, sr = sine_wave
        player = WaveSurfer(audio=audio, sr=sr)
        # Both should produce valid HTML (they use different UIDs each time)
        assert "<iframe" in player.to_html()
        assert "<iframe" in player._repr_html_()

    def test_theme_applied(self, sine_wave):
        audio, sr = sine_wave
        player = WaveSurfer(audio=audio, sr=sr, theme=LIGHT)
        html = player.to_html()
        assert "#f8f8fc" in html  # LIGHT background

    def test_theme_by_string(self, sine_wave):
        audio, sr = sine_wave
        player = WaveSurfer(audio=audio, sr=sr, theme="light")
        assert player.theme is LIGHT

    def test_extra_options(self, sine_wave):
        audio, sr = sine_wave
        player = WaveSurfer(audio=audio, sr=sr, bar_width=5)
        html = player.to_html()
        # HTML is iframe-escaped, so JSON quotes become &quot;
        assert "&quot;barWidth&quot;: 5" in html

    def test_on_ready_shorthand(self, sine_wave):
        audio, sr = sine_wave
        player = WaveSurfer(audio=audio, sr=sr, on_ready="console.log('hi');")
        assert len(player.events) == 1
        assert player.events[0].event == "ready"
        assert player.events[0].once is True


class TestBuilderMethods:
    def test_with_options(self, sine_wave):
        audio, sr = sine_wave
        base = WaveSurfer(audio=audio, sr=sr)
        modified = base.with_options(bar_width=10)
        assert modified._extra_options["bar_width"] == 10
        assert "bar_width" not in base._extra_options

    def test_with_theme(self, sine_wave):
        audio, sr = sine_wave
        base = WaveSurfer(audio=audio, sr=sr, theme=DARK)
        modified = base.with_theme(theme=LIGHT)
        assert modified.theme is LIGHT
        assert base.theme is DARK

    def test_with_events(self, sine_wave):
        audio, sr = sine_wave
        base = WaveSurfer(audio=audio, sr=sr)
        handler = EventHandler.on_ready(js="doSomething();")
        modified = base.with_events(handler)
        assert len(modified.events) == 1
        assert len(base.events) == 0

    def test_with_theme_by_string(self, sine_wave):
        audio, sr = sine_wave
        base = WaveSurfer(audio=audio, sr=sr, theme=DARK)
        modified = base.with_theme(theme="light")
        assert modified.theme is LIGHT

    def test_chaining(self, sine_wave):
        audio, sr = sine_wave
        player = (
            WaveSurfer(audio=audio, sr=sr)
            .with_theme(theme=LIGHT)
            .with_options(bar_width=5)
            .with_events(EventHandler.on_ready(js="init();"))
        )
        assert player.theme is LIGHT
        assert player._extra_options["bar_width"] == 5
        assert len(player.events) == 1


class TestDisplayAudio:
    def test_returns_wavesurfer(self, sine_wave):
        audio, sr = sine_wave
        result = display_audio(audio=audio, sr=sr, title="Test")
        assert isinstance(result, WaveSurfer)
        assert "<iframe" in result._repr_html_()

    def test_with_theme(self, sine_wave):
        audio, sr = sine_wave
        result = display_audio(audio=audio, sr=sr, theme=LIGHT)
        assert result.theme is LIGHT

    def test_with_theme_string(self, sine_wave):
        audio, sr = sine_wave
        result = display_audio(audio=audio, sr=sr, theme="light")
        assert result.theme is LIGHT

    def test_url_input(self):
        result = display_audio(audio="https://example.com/audio.wav")
        html = result._repr_html_()
        assert "example.com/audio.wav" in html


class TestCompareAudio:
    def test_multiple_players(self, sine_wave):
        audio, sr = sine_wave
        result = compare_audio(audio_dict={
            "Version A": (audio, sr),
            "Version B": (audio, sr),
        })
        html = result._repr_html_()
        assert "<iframe" in html
        assert "Version A" in html
        assert "Version B" in html

    def test_with_default_sr(self, sine_wave):
        audio, sr = sine_wave
        result = compare_audio(
            audio_dict={"A": audio, "B": audio},
            sr=sr,
        )
        assert "<iframe" in result._repr_html_()
