"""Shared fixtures for wavesurf tests."""

from __future__ import annotations

import tempfile
from pathlib import Path

import numpy as np
import pytest
import soundfile as sf


@pytest.fixture()
def sine_wave() -> tuple[np.ndarray, int]:
    """440 Hz sine wave, 0.5 seconds, 24 kHz."""
    sr = 24000
    t = np.linspace(start=0, stop=0.5, num=sr // 2, dtype=np.float32)
    audio = np.sin(2 * np.pi * 440 * t)
    return audio, sr


@pytest.fixture()
def silence() -> tuple[np.ndarray, int]:
    """Half second of silence at 16 kHz."""
    sr = 16000
    audio = np.zeros(sr // 2, dtype=np.float32)
    return audio, sr


@pytest.fixture()
def single_sample() -> tuple[np.ndarray, int]:
    """A single audio sample."""
    return np.array([0.5], dtype=np.float32), 8000


@pytest.fixture()
def stereo_audio() -> tuple[np.ndarray, int]:
    """Short stereo audio (2 channels)."""
    sr = 24000
    t = np.linspace(start=0, stop=0.1, num=2400, dtype=np.float32)
    left = np.sin(2 * np.pi * 440 * t)
    right = np.sin(2 * np.pi * 880 * t)
    audio = np.column_stack((left, right))
    return audio, sr


@pytest.fixture()
def wav_file(sine_wave: tuple[np.ndarray, int]) -> Path:
    """Write a temporary WAV file and return its path."""
    audio, sr = sine_wave
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        sf.write(file=f.name, data=audio, samplerate=sr, format="WAV", subtype="PCM_16")
        return Path(f.name)
