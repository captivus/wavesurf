"""wavesurf — Python wrapper for wavesurfer.js in Jupyter notebooks.

Quick start::

    from wavesurf import display_audio, compare_audio

    display_audio(audio=my_array, sr=24000, title="Demo")

Custom themes::

    import wavesurf as ws

    ws.themes.register("my-brand", ws.Theme(wave_color="#ff0000"))
    ws.themes.enable("my-brand")
    ws.display_audio(audio=my_array, sr=24000, title="Branded")

Full control::

    from wavesurf import WaveSurfer, DARK, LIGHT

    player = WaveSurfer(
        audio=my_array, sr=24000,
        title="Demo", theme="light",
        bar_width=3, height=80,
    )
    player  # auto-displays via _repr_html_()
"""

from importlib.metadata import version

__version__ = version("wavesurf")

from wavesurf._controls import Controls
from wavesurf._core import WaveSurfer, compare_audio, display_audio
from wavesurf._events import EventHandler
from wavesurf._layouts import compare, grid
from wavesurf._options import WaveSurferOptions
from wavesurf._plugins import PluginConfig, Plugins
from wavesurf._theme import DARK, LIGHT, Theme, ThemeRegistry, themes

__all__ = [
    "__version__",
    # Core
    "WaveSurfer",
    "display_audio",
    "compare_audio",
    # Theme
    "Theme",
    "ThemeRegistry",
    "themes",
    "DARK",
    "LIGHT",
    # Components
    "Controls",
    "EventHandler",
    "PluginConfig",
    "Plugins",
    "WaveSurferOptions",
    # Layouts
    "compare",
    "grid",
]
