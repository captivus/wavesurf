"""Edge case tests for the wavesurfer package."""

from __future__ import annotations

import numpy as np
import pytest

from wavesurf import WaveSurfer, display_audio
from wavesurf._html import build_player_html
from wavesurf._controls import Controls
from wavesurf._options import WaveSurferOptions
from wavesurf._theme import DARK


class TestXSSInTitles:
    def test_html_escaped(self, sine_wave):
        audio, sr = sine_wave
        malicious = '<script>alert("xss")</script>'
        player = WaveSurfer(audio=audio, sr=sr, title=malicious)
        html = player.to_html()
        # The raw <script> tag should be escaped
        assert "<script>alert" not in html
        assert "&lt;script&gt;" in html or "&#x27;" in html

    def test_quotes_escaped(self):
        html = build_player_html(
            uid="xss1",
            url="data:audio/wav;base64,x",
            title='Test "quotes" & <tags>',
            options=WaveSurferOptions(),
            theme=DARK,
            controls=Controls(),
        )
        assert '&lt;tags&gt;' in html
        assert '&amp;' in html


class TestEmptyAudio:
    def test_zero_length_array(self):
        audio = np.array([], dtype=np.float32)
        # Should not crash — soundfile will handle empty arrays
        player = WaveSurfer(audio=audio, sr=24000)
        html = player.to_html()
        assert "<iframe" in html


class TestSingleSample:
    def test_single_sample_renders(self, single_sample):
        audio, sr = single_sample
        player = WaveSurfer(audio=audio, sr=sr, title="One Sample")
        html = player.to_html()
        assert "<iframe" in html


class TestUidUniqueness:
    def test_different_uids(self, sine_wave):
        audio, sr = sine_wave
        player = WaveSurfer(audio=audio, sr=sr)
        html1 = player.to_html()
        html2 = player.to_html()
        # Extract waveform IDs — they should be different each time
        import re
        ids1 = re.findall(r'waveform-([a-f0-9]+)', html1)
        ids2 = re.findall(r'waveform-([a-f0-9]+)', html2)
        assert ids1 and ids2
        assert ids1[0] != ids2[0]


class TestControlVariants:
    def test_no_controls(self, sine_wave):
        audio, sr = sine_wave
        controls = Controls(show_play_button=False, show_time=False)
        player = WaveSurfer(audio=audio, sr=sr, controls=controls)
        html = player.to_html()
        assert "<iframe" in html
        # Should not contain play button
        assert 'id="play-' not in html

    def test_all_controls(self, sine_wave):
        audio, sr = sine_wave
        controls = Controls(
            show_play_button=True,
            show_time=True,
            show_volume=True,
            show_playback_rate=True,
        )
        player = WaveSurfer(audio=audio, sr=sr, controls=controls)
        html = player.to_html()
        assert "<iframe" in html


class TestURLPassthrough:
    def test_url_not_embedded(self):
        """URL audio should pass through, not be base64 encoded."""
        url = "https://example.com/long/path/to/audio.wav"
        player = WaveSurfer(audio=url)
        html = player.to_html()
        assert url in html
        assert "data:audio/wav;base64" not in html
