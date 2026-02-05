"""Tests for wavesurf._audio."""

from __future__ import annotations

import base64
import io
from pathlib import Path

import numpy as np
import pytest
import soundfile as sf

from wavesurf._audio import audio_to_data_url, load_audio_file, resolve_audio


class TestAudioToDataUrl:
    def test_returns_data_url_prefix(self, sine_wave):
        audio, sr = sine_wave
        url = audio_to_data_url(audio=audio, sr=sr)
        assert url.startswith("data:audio/wav;base64,")

    def test_roundtrip_decode(self, sine_wave):
        """Encode then decode should yield audio with same shape."""
        audio, sr = sine_wave
        url = audio_to_data_url(audio=audio, sr=sr)
        b64_part = url.split(",", 1)[1]
        raw = base64.b64decode(b64_part)
        decoded, decoded_sr = sf.read(file=io.BytesIO(raw), dtype="float32")
        assert decoded_sr == sr
        assert decoded.shape[0] == audio.shape[0]

    def test_stereo_audio(self, stereo_audio):
        audio, sr = stereo_audio
        url = audio_to_data_url(audio=audio, sr=sr)
        assert url.startswith("data:audio/wav;base64,")


class TestLoadAudioFile:
    def test_loads_wav(self, wav_file):
        data, sr = load_audio_file(path=wav_file)
        assert isinstance(data, np.ndarray)
        assert sr > 0
        assert len(data) > 0

    def test_file_not_found(self):
        with pytest.raises(Exception):
            load_audio_file(path="/nonexistent/file.wav")


class TestResolveAudio:
    def test_numpy_array(self, sine_wave):
        audio, sr = sine_wave
        url, resolved_sr = resolve_audio(audio=audio, sr=sr)
        assert url.startswith("data:audio/wav;base64,")
        assert resolved_sr == sr

    def test_numpy_requires_sr(self, sine_wave):
        audio, _ = sine_wave
        with pytest.raises(ValueError, match="sr.*required"):
            resolve_audio(audio=audio, sr=None)

    def test_file_path_string(self, wav_file):
        url, sr = resolve_audio(audio=str(wav_file))
        assert url.startswith("data:audio/wav;base64,")
        assert sr > 0

    def test_file_path_object(self, wav_file):
        url, sr = resolve_audio(audio=wav_file)
        assert url.startswith("data:audio/wav;base64,")

    def test_url_passthrough_http(self):
        test_url = "https://example.com/audio.wav"
        url, sr = resolve_audio(audio=test_url)
        assert url == test_url
        assert sr is None

    def test_url_passthrough_with_sr(self):
        test_url = "https://example.com/audio.wav"
        url, sr = resolve_audio(audio=test_url, sr=24000)
        assert url == test_url
        assert sr == 24000

    def test_invalid_type_raises(self):
        with pytest.raises(TypeError, match="numpy array"):
            resolve_audio(audio=12345)

    def test_single_sample(self, single_sample):
        audio, sr = single_sample
        url, resolved_sr = resolve_audio(audio=audio, sr=sr)
        assert url.startswith("data:audio/wav;base64,")
