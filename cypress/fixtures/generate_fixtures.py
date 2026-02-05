"""Generate HTML fixture files for Cypress e2e tests.

Run with: uv run python cypress/fixtures/generate_fixtures.py
"""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure the project root is importable when running the script directly.
_PROJECT_ROOT = str(Path(__file__).resolve().parent.parent.parent)
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

import numpy as np

from wavesurf import WaveSurfer, compare_audio
from wavesurf._controls import Controls
from wavesurf._events import EventHandler
from wavesurf._theme import DARK, LIGHT

FIXTURES_DIR = Path(__file__).parent


def _wrap_page(title: str, body: str) -> str:
    """Wrap player HTML in a minimal page for testing."""
    return (
        "<!DOCTYPE html>\n"
        "<html>\n"
        "<head>\n"
        f"  <title>{title}</title>\n"
        '  <style>body { margin: 20px; background: #0d1117; }</style>\n'
        "</head>\n"
        f"<body>\n{body}\n</body>\n"
        "</html>\n"
    )


def _sine(freq: float = 440.0, duration: float = 1.0, sr: int = 24000) -> np.ndarray:
    t = np.linspace(start=0, stop=duration, num=int(sr * duration), dtype=np.float32)
    return np.sin(2 * np.pi * freq * t)


def generate_basic_dark() -> None:
    """Single player with DARK theme."""
    audio = _sine()
    player = WaveSurfer(audio=audio, sr=24000, title="Basic Dark", theme=DARK)
    html = _wrap_page(title="Basic Dark", body=player.to_html())
    (FIXTURES_DIR / "basic_dark.html").write_text(html)


def generate_basic_light() -> None:
    """Single player with LIGHT theme."""
    audio = _sine(freq=880.0)
    player = WaveSurfer(audio=audio, sr=24000, title="Basic Light", theme=LIGHT)
    html = _wrap_page(title="Basic Light", body=player.to_html())
    (FIXTURES_DIR / "basic_light.html").write_text(html)


def generate_custom_options() -> None:
    """Player with custom wavesurfer options."""
    audio = _sine()
    player = WaveSurfer(
        audio=audio, sr=24000,
        title="Custom Options",
        theme=DARK,
        bar_width=5, bar_gap=3, bar_radius=5, height=120,
        normalize=True, drag_to_seek=True,
    )
    html = _wrap_page(title="Custom Options", body=player.to_html())
    (FIXTURES_DIR / "custom_options.html").write_text(html)


def generate_compare_grid() -> None:
    """Multi-player comparison grid."""
    audio_a = _sine(freq=440.0)
    audio_b = _sine(freq=660.0)
    audio_c = _sine(freq=880.0)
    result = compare_audio(
        audio_dict={
            "440 Hz": (audio_a, 24000),
            "660 Hz": (audio_b, 24000),
            "880 Hz": (audio_c, 24000),
        },
        theme=DARK,
    )
    html = _wrap_page(title="Compare Grid", body=result._repr_html_())
    (FIXTURES_DIR / "compare_grid.html").write_text(html)


def generate_all_controls() -> None:
    """Player with all controls enabled."""
    audio = _sine()
    controls = Controls(
        show_play_button=True,
        show_time=True,
        show_volume=True,
        show_playback_rate=True,
    )
    player = WaveSurfer(
        audio=audio, sr=24000,
        title="All Controls",
        theme=DARK,
        controls=controls,
    )
    html = _wrap_page(title="All Controls", body=player.to_html())
    (FIXTURES_DIR / "all_controls.html").write_text(html)


if __name__ == "__main__":
    print("Generating Cypress fixtures...")
    generate_basic_dark()
    generate_basic_light()
    generate_custom_options()
    generate_compare_grid()
    generate_all_controls()
    print(f"Done — fixtures written to {FIXTURES_DIR}")
