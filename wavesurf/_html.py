"""HTML / JavaScript code generation and iframe wrapping.

Takes a fully-configured player description and produces self-contained HTML
that can be rendered inside a Jupyter notebook via ``_repr_html_()``.
"""

from __future__ import annotations

import html as html_module
import json
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from wavesurf._controls import Controls
    from wavesurf._events import EventHandler
    from wavesurf._options import WaveSurferOptions
    from wavesurf._plugins import PluginConfig
    from wavesurf._theme import Theme

# Load wavesurfer.min.js once at import time.
_WAVESURFER_JS = (Path(__file__).parent / "wavesurfer.min.js").read_text()


def _build_title_html(title: str, theme: Theme) -> str:
    """Generate the title block above the waveform."""
    marker = ""
    if theme.title_marker_color and theme.title_marker_shape:
        marker = (
            f'<span style="'
            f"width: 8px; height: 9px; flex-shrink: 0;"
            f" background: {theme.title_marker_color};"
            f" clip-path: {theme.title_marker_shape};"
            f'"></span>'
        )

    # Escape title for safe HTML embedding
    safe_title = html_module.escape(title)

    return (
        f'<div style="'
        f"font-size: {theme.title_font_size}; font-weight: {theme.title_font_weight};"
        f" color: {theme.title_color};"
        f" margin-bottom: 14px; display: flex; align-items: center; gap: 10px;"
        f" font-family: {theme.font_family};"
        f'">'
        f"{marker}{safe_title}</div>"
    )


def _build_container_html(
    uid: str,
    title: str | None,
    theme: Theme,
    controls_html: str,
) -> str:
    """Build the outer container div with theme styling."""
    # Optional decorative top accent line
    accent = ""
    if theme.top_accent:
        accent = (
            f'<div style="'
            f"position: absolute; top: 0; left: 0; right: 0; height: 2px;"
            f" background: {theme.top_accent}; z-index: 1;"
            f'"></div>'
        )

    # Optional background pattern
    pattern = ""
    if theme.background_pattern:
        pattern = (
            f'<div style="'
            f"position: absolute; inset: 0;"
            f" background-image: {theme.background_pattern};"
            f" pointer-events: none; z-index: 0;"
            f'"></div>'
        )

    title_html = ""
    if title:
        title_html = _build_title_html(title=title, theme=theme)

    # Controls go inside the relative z-index wrapper
    controls_section = controls_html

    return (
        f'<div id="player-{uid}" style="'
        f"background: {theme.background}; border-radius: {theme.border_radius};"
        f" padding: {theme.padding}; border: {theme.border};"
        f" font-family: {theme.font_family};"
        f" margin-bottom: {theme.card_margin_bottom};"
        f" position: relative; overflow: hidden;"
        f'">'
        f"{accent}{pattern}"
        f'<div style="position: relative; z-index: 1;">'
        f"{title_html}"
        f'<div id="waveform-{uid}" style="border-radius: 8px; overflow: hidden;"></div>'
        f"{controls_section}"
        f"</div></div>"
    )


def _build_wavesurfer_js(
    uid: str,
    url: str,
    options: WaveSurferOptions,
    events: list[EventHandler] | None,
    plugins: list[PluginConfig] | None,
    controls_js: str,
) -> str:
    """Generate the JavaScript block for a single player."""
    # Build the options object
    js_opts = options.to_js_dict()
    js_opts["container"] = f"#waveform-{uid}"
    js_opts["url"] = url

    # Always set some sensible defaults if not specified
    js_opts.setdefault("hideScrollbar", True)
    js_opts.setdefault("cursorWidth", 2)

    # Handle special serialization for list values (colors)
    opts_json = json.dumps(js_opts)

    lines = [
        "(function() {",
        f"  var ws = WaveSurfer.create({opts_json});",
    ]

    # Plugin registration
    if plugins:
        for plugin in plugins:
            lines.append(f"  ws.registerPlugin({plugin.to_js_create()});")

    # Event handlers
    if events:
        for handler in events:
            lines.append(f"  {handler.to_js(ws_var='ws')}")

    # Controls wiring
    if controls_js:
        for line in controls_js.split("\n"):
            lines.append(f"  {line}")

    lines.append("})();")
    return "\n".join(lines)


def build_player_html(
    uid: str,
    url: str,
    title: str | None,
    options: WaveSurferOptions,
    theme: Theme,
    controls: Controls,
    events: list[EventHandler] | None = None,
    plugins: list[PluginConfig] | None = None,
) -> str:
    """Build the complete HTML + JS for a single player (no iframe wrapper)."""
    from wavesurf._controls import build_controls_html, build_controls_js

    controls_html = build_controls_html(uid=uid, controls=controls, theme=theme)
    controls_js = build_controls_js(uid=uid, controls=controls, ws_var="ws")

    container = _build_container_html(
        uid=uid,
        title=title,
        theme=theme,
        controls_html=controls_html,
    )

    js_block = _build_wavesurfer_js(
        uid=uid,
        url=url,
        options=options,
        events=events,
        plugins=plugins,
        controls_js=controls_js,
    )

    return f"{container}\n<script>\n{js_block}\n</script>"


def wrap_in_iframe(body_html: str, height: int) -> str:
    """Wrap HTML content in a self-contained iframe via srcdoc.

    JupyterLab strips ``<script>`` tags from IPython.display.HTML output.
    An iframe with ``srcdoc`` has its own document context where scripts
    execute normally.
    """
    full_page = (
        "<!DOCTYPE html>"
        "<html><head>"
        "<style>body { margin: 0; background: transparent; }</style>"
        f"<script>{_WAVESURFER_JS}</script>"
        "</head><body>"
        f"{body_html}"
        "</body></html>"
    )
    escaped = html_module.escape(full_page, quote=True)
    return (
        f'<iframe srcdoc="{escaped}" '
        f'style="width: 100%; height: {height}px; border: none; overflow: hidden;" '
        f'allow="autoplay">'
        f"</iframe>"
    )


def estimate_player_height(
    title: str | None,
    theme: Theme,
    controls: Controls,
) -> int:
    """Estimate the pixel height of a single player card for iframe sizing."""
    from wavesurf._controls import controls_height as _controls_height

    # Padding top + bottom (approximation from "20px 24px" → 40px vertical)
    padding_v = 40
    # Title block
    title_h = 28 + 14 if title else 0  # font ~14px + margin 14px
    # Waveform
    waveform_h = theme.height if isinstance(theme.height, int) and theme.height else 80
    # Controls
    ctrl_h = _controls_height(controls=controls)
    # Card margin
    margin = 8

    return padding_v + title_h + waveform_h + ctrl_h + margin
