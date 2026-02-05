"""Generate standalone HTML example pages for the wavesurf library.

Each page is fully self-contained: wavesurfer.js (and any plugin JS) is
embedded inline, and audio is encoded as base64 WAV data-URLs.

Run with: uv run python examples/generate_examples.py
"""

from __future__ import annotations

import sys
import urllib.request
import uuid
from pathlib import Path
from string import Template

_PROJECT_ROOT = str(Path(__file__).resolve().parent.parent)
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

import numpy as np

from wavesurf import Controls, Plugins, Theme, WaveSurfer
from wavesurf._audio import resolve_audio
from wavesurf._html import _WAVESURFER_JS, build_player_html
from wavesurf._theme import DARK, LIGHT

EXAMPLES_DIR = Path(__file__).parent
SR = 24000

# ---------------------------------------------------------------------------
# Audio generation helpers
# ---------------------------------------------------------------------------


def _sine(freq: float = 440.0, duration: float = 2.0) -> np.ndarray:
    t = np.linspace(start=0, stop=duration, num=int(SR * duration), dtype=np.float32)
    return np.sin(2 * np.pi * freq * t)


def _chord(freqs: list[float], duration: float = 2.0) -> np.ndarray:
    t = np.linspace(start=0, stop=duration, num=int(SR * duration), dtype=np.float32)
    signal = sum(np.sin(2 * np.pi * f * t) for f in freqs)
    return (signal / len(freqs)).astype(np.float32)


def _sweep(f_start: float = 200.0, f_end: float = 2000.0, duration: float = 3.0) -> np.ndarray:
    t = np.linspace(start=0, stop=duration, num=int(SR * duration), dtype=np.float32)
    freq = np.linspace(start=f_start, stop=f_end, num=len(t))
    phase = 2 * np.pi * np.cumsum(freq) / SR
    return np.sin(phase).astype(np.float32)


# ---------------------------------------------------------------------------
# Plugin JS downloading
# ---------------------------------------------------------------------------

_PLUGIN_CACHE: dict[str, str] = {}

_PLUGIN_CDN_URLS = {
    "timeline": "https://unpkg.com/wavesurfer.js@7/dist/plugins/timeline.min.js",
    "minimap": "https://unpkg.com/wavesurfer.js@7/dist/plugins/minimap.min.js",
    "regions": "https://unpkg.com/wavesurfer.js@7/dist/plugins/regions.min.js",
    "spectrogram": "https://unpkg.com/wavesurfer.js@7/dist/plugins/spectrogram.min.js",
}


def _get_plugin_js(name: str) -> str:
    """Download plugin JS from CDN (cached in memory for the run)."""
    if name in _PLUGIN_CACHE:
        return _PLUGIN_CACHE[name]
    url = _PLUGIN_CDN_URLS[name]
    print(f"  Downloading {name} plugin from {url} ...")
    with urllib.request.urlopen(url=url, timeout=30) as resp:
        js = resp.read().decode("utf-8")
    _PLUGIN_CACHE[name] = js
    return js


# ---------------------------------------------------------------------------
# HTML generation helpers
# ---------------------------------------------------------------------------


def _player_inner_html(player: WaveSurfer) -> str:
    """Extract player HTML + JS from a WaveSurfer without iframe wrapping."""
    url, _sr = resolve_audio(audio=player.audio, sr=player.sr)
    uid = uuid.uuid4().hex[:12]
    options = player._build_options()
    return build_player_html(
        uid=uid,
        url=url,
        title=player.title,
        options=options,
        theme=player.theme,
        controls=player.controls,
        events=player.events or None,
        plugins=player.plugins or None,
    )


_PAGE_TEMPLATE = Template("""\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${title} — wavesurf examples</title>
  <script>${wavesurfer_js}</script>
${extra_scripts}
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      background: ${page_bg};
      color: ${text_color};
      font-family: -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
      padding: 40px 24px;
      min-height: 100vh;
    }
    .container { max-width: 800px; margin: 0 auto; }
    .page-nav { margin-bottom: 24px; }
    .page-nav a {
      color: #6c63ff; text-decoration: none; font-size: 0.85rem;
    }
    .page-nav a:hover { text-decoration: underline; }
    .page-title { font-size: 1.5rem; font-weight: 700; margin-bottom: 8px; }
    .page-description {
      font-size: 0.9rem; color: ${desc_color};
      margin-bottom: 32px; line-height: 1.5;
    }
    .code-block {
      background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08);
      border-radius: 8px; padding: 16px 20px; margin-bottom: 32px;
      font-family: 'SF Mono', Monaco, 'Cascadia Code', monospace;
      font-size: 0.8rem; line-height: 1.6; color: rgba(255,255,255,0.75);
      overflow-x: auto; white-space: pre;
    }
    .players { display: flex; flex-direction: column; gap: 16px; }
    .players.grid {
      display: grid;
      grid-template-columns: repeat(${grid_columns}, 1fr);
      gap: 16px;
    }
  </style>
</head>
<body>
  <div class="container">
    <nav class="page-nav">
      <a href="index.html">&larr; All Examples</a>
    </nav>
    <h1 class="page-title">${title}</h1>
    <p class="page-description">${description}</p>
${code_block}
    <div class="players${grid_class}">
${player_html}
    </div>
  </div>
</body>
</html>
""")


def _build_standalone_page(
    *,
    title: str,
    description: str,
    players: list[WaveSurfer],
    code: str = "",
    grid_columns: int = 1,
    page_bg: str = "#0d1117",
    text_color: str = "rgba(255, 255, 255, 0.85)",
    desc_color: str = "rgba(255, 255, 255, 0.55)",
    plugin_names: list[str] | None = None,
) -> str:
    """Build a complete standalone HTML page from WaveSurfer instances."""
    fragments = [_player_inner_html(player=p) for p in players]
    player_html = "\n".join(f"      {f}" for f in fragments)

    # Plugin scripts (downloaded and embedded inline)
    extra_scripts_parts: list[str] = []
    if plugin_names:
        for name in plugin_names:
            js = _get_plugin_js(name=name)
            extra_scripts_parts.append(f"  <script>{js}</script>")
            # Alias: WaveSurfer.Timeline -> Timeline (matches PluginConfig.to_js_create output)
            cap_name = name.capitalize()
            extra_scripts_parts.append(f"  <script>var {cap_name} = WaveSurfer.{cap_name};</script>")
    extra_scripts = "\n".join(extra_scripts_parts)

    grid_class = " grid" if grid_columns > 1 else ""

    code_block = ""
    if code:
        escaped_code = code.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        code_block = f'    <div class="code-block">{escaped_code}</div>'

    return _PAGE_TEMPLATE.substitute(
        title=title,
        description=description,
        wavesurfer_js=_WAVESURFER_JS,
        extra_scripts=extra_scripts,
        page_bg=page_bg,
        text_color=text_color,
        desc_color=desc_color,
        grid_columns=grid_columns,
        grid_class=grid_class,
        code_block=code_block,
        player_html=player_html,
    )


# ---------------------------------------------------------------------------
# Example page generators
# ---------------------------------------------------------------------------


def generate_basic() -> None:
    player = WaveSurfer(
        audio=_sine(freq=440.0),
        sr=SR,
        title="440 Hz Sine Wave",
    )
    html = _build_standalone_page(
        title="Basic Player",
        description=(
            "The simplest wavesurf player. A single sine wave rendered "
            "with the default DARK theme and standard controls."
        ),
        code=(
            'from wavesurf import display_audio\n'
            'import numpy as np\n'
            '\n'
            't = np.linspace(start=0, stop=1, num=24000, dtype=np.float32)\n'
            'audio = np.sin(2 * np.pi * 440 * t)\n'
            '\n'
            'display_audio(audio=audio, sr=24000, title="440 Hz Sine Wave")'
        ),
        players=[player],
    )
    (EXAMPLES_DIR / "basic.html").write_text(html)


def generate_bars() -> None:
    players = [
        WaveSurfer(
            audio=_sine(freq=220.0),
            sr=SR,
            title="Thin Bars",
            bar_width=2,
            bar_gap=1,
            bar_radius=2,
        ),
        WaveSurfer(
            audio=_chord(freqs=[330.0, 440.0]),
            sr=SR,
            title="Wide Rounded Bars",
            bar_width=5,
            bar_gap=3,
            bar_radius=5,
            height=120,
        ),
        WaveSurfer(
            audio=_sweep(),
            sr=SR,
            title="Narrow Spaced Bars",
            bar_width=1,
            bar_gap=2,
            bar_height=1.5,
            height=100,
        ),
    ]
    html = _build_standalone_page(
        title="Bar-Style Waveforms",
        description=(
            "Customize waveform bars using bar_width, bar_gap, "
            "bar_radius, and bar_height options."
        ),
        code=(
            'WaveSurfer(\n'
            '    audio=audio, sr=24000,\n'
            '    title="Wide Rounded Bars",\n'
            '    bar_width=5, bar_gap=3, bar_radius=5, height=120,\n'
            ')'
        ),
        players=players,
    )
    (EXAMPLES_DIR / "bars.html").write_text(html)


def generate_gradients() -> None:
    players = [
        WaveSurfer(
            audio=_chord(freqs=[440.0, 660.0]),
            sr=SR,
            title="Warm Gradient",
            wave_color=["#ff6b6b", "#ffa726"],
            progress_color=["#e91e63", "#ff5722"],
        ),
        WaveSurfer(
            audio=_chord(freqs=[330.0, 550.0]),
            sr=SR,
            title="Cool Gradient",
            wave_color=["#42a5f5", "#7e57c2"],
            progress_color=["#26c6da", "#00bcd4"],
        ),
        WaveSurfer(
            audio=_sweep(),
            sr=SR,
            title="Multi-Stop Gradient",
            wave_color=["#4caf50", "#ffeb3b", "#ff9800"],
            progress_color=["#2196f3", "#9c27b0", "#e91e63"],
        ),
    ]
    html = _build_standalone_page(
        title="Gradient Colors",
        description=(
            "Pass a list of colors to wave_color or progress_color "
            "for smooth gradient effects across the waveform."
        ),
        code=(
            'WaveSurfer(\n'
            '    audio=audio, sr=24000,\n'
            '    title="Warm Gradient",\n'
            '    wave_color=["#ff6b6b", "#ffa726"],\n'
            '    progress_color=["#e91e63", "#ff5722"],\n'
            ')'
        ),
        players=players,
    )
    (EXAMPLES_DIR / "gradients.html").write_text(html)


def generate_timeline() -> None:
    player = WaveSurfer(
        audio=_chord(freqs=[220.0, 330.0, 440.0], duration=5.0),
        sr=SR,
        title="With Timeline",
        plugins=[Plugins.timeline(height=20)],
    )
    html = _build_standalone_page(
        title="Timeline Plugin",
        description=(
            "The timeline plugin displays time markers below the waveform. "
            "Configure height, time intervals, and label styling."
        ),
        code=(
            'from wavesurf import Plugins\n'
            '\n'
            'WaveSurfer(\n'
            '    audio=audio, sr=24000,\n'
            '    title="With Timeline",\n'
            '    plugins=[Plugins.timeline(height=20)],\n'
            ')'
        ),
        players=[player],
        plugin_names=["timeline"],
    )
    (EXAMPLES_DIR / "timeline.html").write_text(html)


def generate_minimap() -> None:
    player = WaveSurfer(
        audio=_sweep(duration=5.0),
        sr=SR,
        title="With Minimap",
        plugins=[
            Plugins.minimap(
                height=30,
                wave_color="#666688",
                progress_color="#6c63ff",
            ),
        ],
    )
    html = _build_standalone_page(
        title="Minimap Plugin",
        description=(
            "The minimap plugin renders a smaller overview of the full waveform. "
            "Useful for long audio files to provide navigation context."
        ),
        code=(
            'from wavesurf import Plugins\n'
            '\n'
            'WaveSurfer(\n'
            '    audio=audio, sr=24000,\n'
            '    title="With Minimap",\n'
            '    plugins=[\n'
            '        Plugins.minimap(\n'
            '            height=30,\n'
            '            wave_color="#666688",\n'
            '            progress_color="#6c63ff",\n'
            '        ),\n'
            '    ],\n'
            ')'
        ),
        players=[player],
        plugin_names=["minimap"],
    )
    (EXAMPLES_DIR / "minimap.html").write_text(html)


def generate_spectrogram() -> None:
    player = WaveSurfer(
        audio=_sweep(f_start=100.0, f_end=4000.0, duration=5.0),
        sr=SR,
        title="With Spectrogram",
        plugins=[Plugins.spectrogram(height=128, labels=True)],
    )
    html = _build_standalone_page(
        title="Spectrogram Plugin",
        description=(
            "The spectrogram plugin displays a frequency spectrum visualization "
            "below the waveform. The sweep audio shows a clear rising frequency."
        ),
        code=(
            'from wavesurf import Plugins\n'
            '\n'
            'WaveSurfer(\n'
            '    audio=audio, sr=24000,\n'
            '    title="With Spectrogram",\n'
            '    plugins=[Plugins.spectrogram(height=128, labels=True)],\n'
            ')'
        ),
        players=[player],
        plugin_names=["spectrogram"],
    )
    (EXAMPLES_DIR / "spectrogram.html").write_text(html)


def generate_regions() -> None:
    from wavesurf._events import EventHandler

    # Register regions via on_ready JS since _build_wavesurfer_js doesn't
    # capture the registerPlugin return value.
    player = WaveSurfer(
        audio=_chord(freqs=[440.0, 550.0, 660.0], duration=5.0),
        sr=SR,
        title="With Regions",
        events=[
            EventHandler.on_ready(
                js=(
                    'var regions = ws.registerPlugin(Regions.create({}));'
                    'regions.addRegion({start: 0.5, end: 1.5, color: "rgba(108, 99, 255, 0.2)", content: "Intro"});'
                    'regions.addRegion({start: 2.0, end: 3.5, color: "rgba(255, 107, 107, 0.2)", content: "Main"});'
                    'regions.addRegion({start: 4.0, end: 4.8, color: "rgba(76, 175, 80, 0.2)", content: "Outro"});'
                ),
                once=True,
            ),
        ],
    )
    html = _build_standalone_page(
        title="Regions Plugin",
        description=(
            "The regions plugin lets you highlight and annotate sections of audio. "
            "Regions can be dragged, resized, and styled independently."
        ),
        code=(
            'from wavesurf import Plugins, EventHandler\n'
            '\n'
            'WaveSurfer(\n'
            '    audio=audio, sr=24000,\n'
            '    title="With Regions",\n'
            '    plugins=[Plugins.regions()],\n'
            '    on_ready="""\n'
            '        var regions = ws.plugins[0];\n'
            '        regions.addRegion({start: 0.5, end: 1.5, ...});\n'
            '    """,\n'
            ')'
        ),
        players=[player],
        plugin_names=["regions"],
    )
    (EXAMPLES_DIR / "regions.html").write_text(html)


def generate_controls() -> None:
    audio = _sine(freq=440.0)
    players = [
        WaveSurfer(
            audio=audio,
            sr=SR,
            title="Circle Button (Default)",
            controls=Controls(
                show_play_button=True,
                show_time=True,
                show_volume=True,
                show_playback_rate=True,
                play_button_style="circle",
            ),
        ),
        WaveSurfer(
            audio=audio,
            sr=SR,
            title="Shield Button",
            controls=Controls(
                show_play_button=True,
                show_time=True,
                show_volume=True,
                show_playback_rate=True,
                play_button_style="shield",
            ),
        ),
        WaveSurfer(
            audio=audio,
            sr=SR,
            title="Minimal Button",
            controls=Controls(
                show_play_button=True,
                show_time=True,
                show_volume=True,
                show_playback_rate=True,
                play_button_style="minimal",
            ),
        ),
    ]
    html = _build_standalone_page(
        title="Player Controls",
        description=(
            "Configure play buttons, time display, volume slider, and "
            "playback rate selector. Three button styles: circle, shield, minimal."
        ),
        code=(
            'from wavesurf import Controls\n'
            '\n'
            'controls = Controls(\n'
            '    show_play_button=True,\n'
            '    show_time=True,\n'
            '    show_volume=True,\n'
            '    show_playback_rate=True,\n'
            '    play_button_style="shield",\n'
            ')\n'
            '\n'
            'WaveSurfer(audio=audio, sr=24000, controls=controls)'
        ),
        players=players,
    )
    (EXAMPLES_DIR / "controls.html").write_text(html)


def generate_layout() -> None:
    players = [
        WaveSurfer(audio=_sine(freq=220.0), sr=SR, title="220 Hz"),
        WaveSurfer(audio=_sine(freq=440.0), sr=SR, title="440 Hz"),
        WaveSurfer(audio=_sine(freq=660.0), sr=SR, title="660 Hz"),
        WaveSurfer(audio=_sine(freq=880.0), sr=SR, title="880 Hz"),
    ]
    html = _build_standalone_page(
        title="Grid Layout",
        description=(
            "Multiple players arranged in a 2-column grid layout, "
            "demonstrating the compare_audio() and grid() functions."
        ),
        code=(
            'from wavesurf import WaveSurfer, grid\n'
            '\n'
            'players = [\n'
            '    WaveSurfer(audio=a1, sr=24000, title="220 Hz"),\n'
            '    WaveSurfer(audio=a2, sr=24000, title="440 Hz"),\n'
            '    WaveSurfer(audio=a3, sr=24000, title="660 Hz"),\n'
            '    WaveSurfer(audio=a4, sr=24000, title="880 Hz"),\n'
            ']\n'
            '\n'
            'grid(players=players, columns=2)'
        ),
        players=players,
        grid_columns=2,
    )
    (EXAMPLES_DIR / "layout.html").write_text(html)


def generate_custom_theme() -> None:
    custom = Theme(
        wave_color=["#e63946", "#d62839"],
        progress_color=["#457b9d", "#1d3557"],
        cursor_color="#457b9d",
        bar_width=3,
        bar_gap=2,
        bar_radius=3,
        height=100,
        background="#1d3557",
        border="1px solid rgba(230, 57, 70, 0.15)",
        border_radius="16px",
        padding="24px 28px",
        title_color="#f1faee",
        title_marker_color="#e63946",
        title_marker_shape="polygon(50% 0%, 0% 100%, 100% 100%)",
        play_button_style="shield",
        play_button_color="#f1faee",
        play_button_bg="linear-gradient(135deg, #e63946, #d62839)",
        time_color="rgba(241, 250, 238, 0.5)",
        top_accent="linear-gradient(90deg, #e63946, #457b9d)",
    )
    player = WaveSurfer(
        audio=_chord(freqs=[330.0, 440.0, 550.0]),
        sr=SR,
        title="Custom Branded Player",
        theme=custom,
    )
    html = _build_standalone_page(
        title="Custom Theme",
        description=(
            "Build a fully customized theme with gradient waveforms, "
            "shield-style play button, title markers, and accent lines."
        ),
        code=(
            'from wavesurf import Theme, WaveSurfer\n'
            '\n'
            'custom = Theme(\n'
            '    wave_color=["#e63946", "#d62839"],\n'
            '    progress_color=["#457b9d", "#1d3557"],\n'
            '    background="#1d3557",\n'
            '    play_button_style="shield",\n'
            '    title_marker_color="#e63946",\n'
            '    top_accent="linear-gradient(90deg, #e63946, #457b9d)",\n'
            ')\n'
            '\n'
            'WaveSurfer(audio=audio, sr=24000, title="Branded", theme=custom)'
        ),
        players=[player],
    )
    (EXAMPLES_DIR / "custom_theme.html").write_text(html)


def generate_themes() -> None:
    audio = _chord(freqs=[440.0, 550.0, 660.0])
    players = [
        WaveSurfer(audio=audio, sr=SR, title="DARK Theme", theme=DARK),
        WaveSurfer(audio=audio, sr=SR, title="LIGHT Theme", theme=LIGHT),
    ]
    html = _build_standalone_page(
        title="Built-in Themes",
        description=(
            "wavesurf ships with two built-in themes: DARK (default) "
            "and LIGHT. Both use the circle play button style."
        ),
        code=(
            'from wavesurf import DARK, LIGHT\n'
            '\n'
            'WaveSurfer(audio=audio, sr=24000, title="DARK Theme", theme=DARK)\n'
            'WaveSurfer(audio=audio, sr=24000, title="LIGHT Theme", theme=LIGHT)'
        ),
        players=players,
        grid_columns=2,
    )
    (EXAMPLES_DIR / "themes.html").write_text(html)


def generate_index() -> None:
    examples = [
        ("basic.html", "Basic Player", "Simplest player with default DARK theme"),
        ("bars.html", "Bar-Style Waveforms", "Customize bar width, gap, and radius"),
        ("gradients.html", "Gradient Colors", "Gradient wave and progress colors"),
        ("timeline.html", "Timeline Plugin", "Time markers below the waveform"),
        ("minimap.html", "Minimap Plugin", "Miniature waveform overview"),
        ("spectrogram.html", "Spectrogram Plugin", "Frequency spectrum visualization"),
        ("regions.html", "Regions Plugin", "Highlight and annotate audio segments"),
        ("controls.html", "Player Controls", "Play, time, volume, and rate controls"),
        ("layout.html", "Grid Layout", "Multi-player comparison grids"),
        ("custom_theme.html", "Custom Theme", "Fully customized visual theme"),
        ("themes.html", "Built-in Themes", "DARK and LIGHT themes side by side"),
    ]

    cards = []
    for href, name, desc in examples:
        cards.append(
            f'    <a href="{href}" class="card">'
            f'<div class="card-title">{name}</div>'
            f'<div class="card-desc">{desc}</div>'
            f'</a>'
        )
    cards_html = "\n".join(cards)

    html = f"""\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>wavesurf examples</title>
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      background: #0d1117;
      color: rgba(255, 255, 255, 0.85);
      font-family: -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
      padding: 40px 24px;
      min-height: 100vh;
    }}
    .container {{ max-width: 800px; margin: 0 auto; }}
    h1 {{ font-size: 1.8rem; font-weight: 700; margin-bottom: 8px; }}
    .subtitle {{
      font-size: 0.95rem; color: rgba(255,255,255,0.5);
      margin-bottom: 40px; line-height: 1.5;
    }}
    .subtitle a {{ color: #6c63ff; text-decoration: none; }}
    .subtitle a:hover {{ text-decoration: underline; }}
    .grid {{
      display: grid; grid-template-columns: repeat(2, 1fr);
      gap: 12px;
    }}
    .card {{
      display: block; text-decoration: none; color: inherit;
      background: rgba(255,255,255,0.03);
      border: 1px solid rgba(255,255,255,0.08);
      border-radius: 10px; padding: 20px;
      transition: background 0.15s ease, border-color 0.15s ease;
    }}
    .card:hover {{
      background: rgba(255,255,255,0.06);
      border-color: rgba(108, 99, 255, 0.3);
    }}
    .card-title {{
      font-size: 0.95rem; font-weight: 600; margin-bottom: 6px;
      color: rgba(255,255,255,0.9);
    }}
    .card-desc {{
      font-size: 0.8rem; color: rgba(255,255,255,0.45); line-height: 1.4;
    }}
  </style>
</head>
<body>
  <div class="container">
    <h1>wavesurf examples</h1>
    <p class="subtitle">
      Interactive examples for
      <a href="https://github.com/captivus/wavesurf">wavesurf</a>
      — a Python wrapper around
      <a href="https://wavesurfer.xyz/">wavesurfer.js</a>
      for Jupyter notebooks.
    </p>
    <div class="grid">
{cards_html}
    </div>
  </div>
</body>
</html>
"""
    (EXAMPLES_DIR / "index.html").write_text(html)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Generating example pages...")
    generate_basic()
    print("  basic.html")
    generate_bars()
    print("  bars.html")
    generate_gradients()
    print("  gradients.html")
    generate_timeline()
    print("  timeline.html")
    generate_minimap()
    print("  minimap.html")
    generate_spectrogram()
    print("  spectrogram.html")
    generate_regions()
    print("  regions.html")
    generate_controls()
    print("  controls.html")
    generate_layout()
    print("  layout.html")
    generate_custom_theme()
    print("  custom_theme.html")
    generate_themes()
    print("  themes.html")
    generate_index()
    print("  index.html")
    print(f"Done — {len(list(EXAMPLES_DIR.glob('*.html')))} files written to {EXAMPLES_DIR}")
