---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---

# wavesurf Jupyter Widgets Developer Guide

This guide demonstrates how to build interactive audio player widgets in Jupyter
notebooks using the **wavesurf** library — a Python wrapper around
[wavesurfer.js](https://wavesurfer.xyz/).

Every code cell below is self-contained and runnable. Audio is synthesized
inline with numpy so there are no external file dependencies.

## Setup

Define reusable audio synthesis helpers and a shared sample rate used
throughout this guide.

```python
import numpy as np

SR = 24000  # Sample rate used throughout the guide


def sine(freq: float = 440.0, duration: float = 2.0, sr: int = SR) -> np.ndarray:
    """Pure sine wave at the given frequency."""
    t = np.linspace(start=0, stop=duration, num=int(sr * duration), dtype=np.float32)
    return np.sin(2 * np.pi * freq * t)


def chord(freqs: list[float], duration: float = 2.0, sr: int = SR) -> np.ndarray:
    """Sum of multiple sine waves, normalized."""
    t = np.linspace(start=0, stop=duration, num=int(sr * duration), dtype=np.float32)
    signal = sum(np.sin(2 * np.pi * f * t) for f in freqs)
    return (signal / len(freqs)).astype(np.float32)


def sweep(f_start: float = 200.0, f_end: float = 2000.0, duration: float = 3.0, sr: int = SR) -> np.ndarray:
    """Frequency sweep from f_start to f_end."""
    t = np.linspace(start=0, stop=duration, num=int(sr * duration), dtype=np.float32)
    freq = np.linspace(start=f_start, stop=f_end, num=len(t))
    phase = 2 * np.pi * np.cumsum(freq) / sr
    return np.sin(phase).astype(np.float32)
```

## Basic Player

The fastest way to get an audio player is `display_audio()`. Pass a numpy
array and sample rate, and it returns a `WaveSurfer` that auto-renders in
Jupyter via `_repr_html_()`. The default theme is `DARK`.

```python
from wavesurf import display_audio

audio = sine(freq=440.0)

display_audio(audio=audio, sr=SR, title="440 Hz Sine Wave")
```

## Bar-Style Waveforms

Wavesurfer.js options can be passed as snake_case keyword arguments.
The key bar-styling parameters are `bar_width`, `bar_gap`, `bar_radius`,
`bar_height`, and `height`. These override theme defaults.

```python
display_audio(
    audio=sine(freq=220.0),
    sr=SR,
    title="Thin Bars",
    bar_width=2,
    bar_gap=1,
    bar_radius=2,
)
```

```python
display_audio(
    audio=chord(freqs=[330.0, 440.0]),
    sr=SR,
    title="Wide Rounded Bars",
    bar_width=5,
    bar_gap=3,
    bar_radius=5,
    height=120,
)
```

```python
display_audio(
    audio=sweep(),
    sr=SR,
    title="Narrow Spaced Bars",
    bar_width=1,
    bar_gap=2,
    bar_height=1.5,
    height=100,
)
```

## Gradient Colors

`wave_color` and `progress_color` accept either a single hex string or a
list of hex strings for gradient effects. Multiple color stops create smooth
gradients across the waveform.

```python
display_audio(
    audio=chord(freqs=[440.0, 660.0]),
    sr=SR,
    title="Warm Gradient",
    wave_color=["#ff6b6b", "#ffa726"],
    progress_color=["#e91e63", "#ff5722"],
)
```

```python
display_audio(
    audio=sweep(),
    sr=SR,
    title="Multi-Stop Gradient",
    wave_color=["#4caf50", "#ffeb3b", "#ff9800"],
    progress_color=["#2196f3", "#9c27b0", "#e91e63"],
)
```

## Built-in Themes

wavesurf ships with two built-in themes: `DARK` (default) and `LIGHT`. The
`theme=` parameter accepts a `Theme` object or a string name. Themes control
both the waveform appearance and the container chrome (background, borders,
buttons, etc.).

```python
from wavesurf import WaveSurfer, DARK, LIGHT

audio = chord(freqs=[440.0, 550.0, 660.0])

WaveSurfer(audio=audio, sr=SR, title="DARK Theme", theme=DARK)
```

```python
WaveSurfer(audio=audio, sr=SR, title="LIGHT Theme", theme=LIGHT)
```

You can also reference themes by string name:

```python
WaveSurfer(audio=audio, sr=SR, title="Theme by Name", theme="light")
```

## Custom Themes

The `Theme` dataclass has 25+ properties organized by category: waveform
colors, container chrome, title styling, play button appearance, and
decorative accents. Use `Theme.replace()` to create modified copies of
existing themes, or build one from scratch.

Create a variant of the built-in dark theme:

```python
from wavesurf import Theme

neon = DARK.replace(
    wave_color="#ff6b9d",
    progress_color="#00d9ff",
    background="#0a0e27",
    play_button_style="minimal",
)

WaveSurfer(audio=audio, sr=SR, title="Neon Variant", theme=neon)
```

Build a fully custom theme from scratch:

```python
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

WaveSurfer(
    audio=chord(freqs=[330.0, 440.0, 550.0]),
    sr=SR,
    title="Custom Branded Player",
    theme=custom,
)
```

Register a custom theme in the global registry so it can be referenced by
name. Use `themes.enable()` to set the project-wide default.

```python
import wavesurf as ws

ws.themes.register(name="branded", theme=custom)
ws.themes.enable(name="branded")

# All subsequent players now use "branded" by default
display_audio(audio=sine(freq=440.0), sr=SR, title="Registry Default")
```

Reset to the default dark theme so later cells are not affected:

```python
ws.themes.enable(name="dark")
```

## Player Controls

The `Controls` dataclass configures which UI controls appear. Four features
can be toggled: `show_play_button`, `show_time`, `show_volume`, and
`show_playback_rate`. Three play button styles are available: `"circle"`,
`"shield"`, and `"minimal"`.

```python
from wavesurf import Controls

WaveSurfer(
    audio=sine(freq=440.0),
    sr=SR,
    title="All Controls (Circle)",
    controls=Controls(
        show_play_button=True,
        show_time=True,
        show_volume=True,
        show_playback_rate=True,
        play_button_style="circle",
    ),
)
```

```python
WaveSurfer(
    audio=sine(freq=440.0),
    sr=SR,
    title="Shield Button Style",
    controls=Controls(
        show_play_button=True,
        show_time=True,
        show_volume=True,
        show_playback_rate=True,
        play_button_style="shield",
    ),
)
```

```python
WaveSurfer(
    audio=sine(freq=440.0),
    sr=SR,
    title="Minimal Button Style",
    controls=Controls(
        show_play_button=True,
        show_time=True,
        show_volume=True,
        show_playback_rate=True,
        play_button_style="minimal",
    ),
)
```

## Plugins

Plugins extend the player with additional visualizations. They are configured
via `Plugins` factory methods and passed as a list to the `plugins=`
parameter.

### Timeline

The Timeline plugin adds time markers below the waveform.

```python
from wavesurf import Plugins

WaveSurfer(
    audio=chord(freqs=[220.0, 330.0, 440.0], duration=5.0),
    sr=SR,
    title="With Timeline",
    plugins=[Plugins.timeline(height=20)],
)
```

### Minimap

The Minimap plugin renders a smaller overview of the full waveform, useful
for long audio to provide navigation context.

```python
WaveSurfer(
    audio=sweep(duration=5.0),
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
```

### Spectrogram

The Spectrogram plugin displays a frequency spectrum visualization below the
waveform. A frequency sweep makes the rising frequency clearly visible.

```python
WaveSurfer(
    audio=sweep(f_start=100.0, f_end=4000.0, duration=5.0),
    sr=SR,
    title="With Spectrogram",
    plugins=[Plugins.spectrogram(height=128, labels=True)],
)
```

### Regions

The Regions plugin highlights and annotates sections of audio. Unlike other
plugins, regions must be added programmatically via JavaScript after the
player is ready. Use `EventHandler.on_ready()` with raw JS to capture the
plugin handle and call `addRegion()`.

```python
from wavesurf import EventHandler

regions_js = (
    'var regions = ws.registerPlugin(Regions.create({}));'
    'regions.addRegion({start: 0.5, end: 1.5, color: "rgba(108, 99, 255, 0.2)", content: "Intro"});'
    'regions.addRegion({start: 2.0, end: 3.5, color: "rgba(255, 107, 107, 0.2)", content: "Main"});'
    'regions.addRegion({start: 4.0, end: 4.8, color: "rgba(76, 175, 80, 0.2)", content: "Outro"});'
)

WaveSurfer(
    audio=chord(freqs=[440.0, 550.0, 660.0], duration=5.0),
    sr=SR,
    title="With Regions",
    events=[
        EventHandler.on_ready(js=regions_js, once=True),
    ],
)
```

## Event Handlers

The `EventHandler` system lets you attach JavaScript callbacks to
wavesurfer.js events. There are 22 events, each with a corresponding factory
method (`EventHandler.on_ready()`, `.on_play()`, `.on_pause()`, etc.). The
`js=` parameter takes raw JavaScript that executes inside the player's iframe
context. Set `once=True` for one-shot handlers.

```python
WaveSurfer(
    audio=sine(freq=440.0),
    sr=SR,
    title="Event Demo",
    events=[
        EventHandler.on_ready(
            js="console.log('Player ready! Duration:', duration);",
            once=True,
        ),
        EventHandler.on_play(js="console.log('Playback started');"),
        EventHandler.on_pause(js="console.log('Playback paused');"),
    ],
)
```

Open the browser console (F12) to see the logged messages when interacting
with the player above.

## Layouts and Comparison

### compare_audio()

`compare_audio()` provides quick side-by-side comparison of multiple audio
signals. Pass a dictionary mapping labels to audio arrays and set `columns=`
for the grid layout.

```python
from wavesurf import compare_audio

compare_audio(
    audio_dict={
        "220 Hz": sine(freq=220.0),
        "440 Hz": sine(freq=440.0),
        "880 Hz": sine(freq=880.0),
    },
    sr=SR,
    columns=1,
)
```

### grid()

For more control, create `WaveSurfer` instances individually and arrange them
with `grid()`. The default for `grid()` is 2 columns, whereas `compare()`
defaults to 1 column.

```python
from wavesurf import grid

players = [
    WaveSurfer(audio=sine(freq=220.0), sr=SR, title="220 Hz"),
    WaveSurfer(audio=sine(freq=440.0), sr=SR, title="440 Hz"),
    WaveSurfer(audio=sine(freq=660.0), sr=SR, title="660 Hz"),
    WaveSurfer(audio=sine(freq=880.0), sr=SR, title="880 Hz"),
]

grid(players=players, columns=2)
```

## Builder Pattern

The immutable builder methods `with_theme()`, `with_options()`,
`with_events()`, and `with_plugins()` return new `WaveSurfer` instances
without modifying the original. This is useful for creating variations of a
base player.

```python
base = WaveSurfer(
    audio=chord(freqs=[440.0, 550.0]),
    sr=SR,
    title="Base Player",
)

enhanced = (
    base
    .with_theme(theme=LIGHT)
    .with_options(bar_width=4, height=100)
    .with_plugins(Plugins.timeline(height=20))
)

enhanced
```

## Putting It All Together

A final example combining a custom theme, full controls, multiple plugins,
and an event handler into a single player.

```python
capstone_theme = Theme(
    wave_color=["#667eea", "#764ba2"],
    progress_color=["#f093fb", "#f5576c"],
    cursor_color="#f5576c",
    bar_width=3,
    bar_gap=2,
    bar_radius=3,
    height=100,
    background="#1a1a2e",
    border="1px solid rgba(102, 126, 234, 0.2)",
    title_color="#e0e0ff",
    title_marker_color="#667eea",
    title_marker_shape="polygon(50% 0%, 100% 50%, 50% 100%, 0% 50%)",
    play_button_style="circle",
    play_button_bg="rgba(102, 126, 234, 0.3)",
    top_accent="linear-gradient(90deg, #667eea, #764ba2, #f093fb)",
)

WaveSurfer(
    audio=sweep(f_start=200.0, f_end=3000.0, duration=5.0),
    sr=SR,
    title="Full-Featured Player",
    theme=capstone_theme,
    controls=Controls(
        show_play_button=True,
        show_time=True,
        show_volume=True,
        show_playback_rate=True,
    ),
    plugins=[
        Plugins.timeline(height=20),
        Plugins.minimap(height=25, wave_color="#667eea", progress_color="#f093fb"),
    ],
    events=[
        EventHandler.on_ready(
            js="console.log('Capstone player ready!');",
            once=True,
        ),
    ],
)
```

## How Iframe Sizing Works

Each wavesurf player renders inside an `<iframe>` with a `srcdoc` attribute.
This is necessary because JupyterLab strips `<script>` tags from HTML output,
so an iframe provides an isolated document context where JavaScript runs
normally.

The iframe height is **estimated automatically** based on the player
configuration: title presence, waveform `height`, visible controls, and
plugin heights (Timeline, Minimap, and Spectrogram each add their configured
`height` in pixels). If you see a scrollbar inside a player widget, it means
the content overflowed the estimated iframe height.

Common causes and solutions:

- **Custom waveform height**: Pass `height=` as a keyword argument (e.g.,
  `height=120`). The library accounts for this automatically.
- **Plugins**: Each plugin's `height` parameter is added to the estimate.
  If you configure a very tall plugin, the iframe grows to fit.
- **Tight layouts**: If content still clips, increase the waveform `height`
  slightly or reduce plugin heights.

The estimation logic lives in `estimate_player_height()` in `_html.py` and
handles the arithmetic so you typically never need to think about it.

## API Quick Reference

| Function / Class | Description |
|---|---|
| `display_audio(audio, sr, *, title, theme, controls, **options)` | Quick single-player display |
| `compare_audio(audio_dict, sr, *, columns, theme, controls, **options)` | Multi-player comparison from dict |
| `WaveSurfer(audio, sr, *, title, theme, controls, events, plugins, **options)` | Full-control player class |
| `grid(players, columns=2)` / `compare(players, columns=1)` | Layout multiple `WaveSurfer` instances |
| `Theme(wave_color, progress_color, background, ...)` | Custom visual theme (25+ properties) |
| `DARK` / `LIGHT` | Built-in theme presets |
| `themes.register(name, theme)` / `themes.enable(name)` | Global theme registry |
| `Controls(show_play_button, show_time, show_volume, show_playback_rate, play_button_style)` | Player UI configuration |
| `Plugins.timeline(height)` | Time markers below waveform |
| `Plugins.minimap(height, wave_color, progress_color)` | Navigation overview |
| `Plugins.spectrogram(height, labels)` | Frequency spectrum visualization |
| `Plugins.regions()` | Audio segment annotation (use with `EventHandler.on_ready`) |
| `EventHandler.on_ready(js, once)` | Attach JS callback to player events |
