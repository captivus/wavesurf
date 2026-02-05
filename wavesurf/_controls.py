"""Player control UI HTML/CSS generation.

The ``Controls`` dataclass configures which controls appear and how they look.
``build_controls_html()`` emits the HTML for the control bar, and
``build_controls_js()`` wires it up to a wavesurfer instance.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from wavesurf._theme import Theme


@dataclass(frozen=True)
class Controls:
    """Configuration for player controls beneath the waveform.

    Parameters
    ----------
    show_play_button:
        Whether to render the play/pause button.
    show_time:
        Whether to show current time / duration.
    show_volume:
        Whether to show a volume slider.
    show_playback_rate:
        Whether to show a playback-rate selector.
    play_button_style:
        Visual variant: ``"shield"`` (badge shape), ``"circle"``
        (round button), or ``"minimal"`` (text-only).
    layout:
        Position of controls: ``"bottom"`` or ``"top"`` relative to the
        waveform.
    """

    show_play_button: bool = True
    show_time: bool = True
    show_volume: bool = False
    show_playback_rate: bool = False
    play_button_style: str | None = None  # None = inherit from theme
    layout: str = "bottom"

    def effective_style(self, theme: Theme) -> str:
        """Resolve the button style, preferring explicit setting over theme."""
        if self.play_button_style is not None:
            return self.play_button_style
        return theme.play_button_style


def _shield_button_html(uid: str, theme: Theme) -> str:
    """Shield-shaped play button with gradient fill."""
    return f"""\
<button id="play-{uid}" style="
  width: 36px; height: 40px; border: none; cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  padding: 0; background: transparent; position: relative;
  transition: transform 0.2s ease, filter 0.2s ease;
" onmouseover="this.style.transform='scale(1.1)';{f" this.style.filter='{theme.play_button_hover_glow}';" if theme.play_button_hover_glow else ''}"
   onmouseout="this.style.transform='scale(1)'; this.style.filter='none'"
>
  <svg style="position: absolute; inset: 0; width: 100%; height: 100%;"
       viewBox="0 0 36 40" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M18 0L36 6V22C36 31 27 37.5 18 40C9 37.5 0 31 0 22V6L18 0Z"
          fill="url(#copperGrad-{uid})"/>
    <defs>
      <linearGradient id="copperGrad-{uid}" x1="0" y1="0" x2="36" y2="40">
        <stop offset="0%" stop-color="#d4a96a"/>
        <stop offset="100%" stop-color="#b98b5a"/>
      </linearGradient>
    </defs>
  </svg>
  <span id="icon-{uid}" style="
    position: relative; z-index: 1; color: {theme.play_button_color};
    font-size: 11px; margin-left: 2px; line-height: 1;
  ">&#9654;</span>
</button>"""


def _circle_button_html(uid: str, theme: Theme) -> str:
    """Circular play button."""
    return f"""\
<button id="play-{uid}" style="
  width: 36px; height: 36px; border-radius: 50%; border: none; cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  padding: 0; background: {theme.play_button_bg};
  color: {theme.play_button_color}; font-size: 13px;
  transition: transform 0.15s ease, opacity 0.15s ease;
" onmouseover="this.style.transform='scale(1.08)'; this.style.opacity='0.85'"
   onmouseout="this.style.transform='scale(1)'; this.style.opacity='1'"
>
  <span id="icon-{uid}" style="margin-left: 2px; line-height: 1;">&#9654;</span>
</button>"""


def _minimal_button_html(uid: str, theme: Theme) -> str:
    """Minimal text-only play button."""
    return f"""\
<button id="play-{uid}" style="
  border: none; cursor: pointer; background: transparent;
  color: {theme.play_button_color}; font-size: 18px; padding: 4px 8px;
  transition: opacity 0.15s ease;
" onmouseover="this.style.opacity='0.7'"
   onmouseout="this.style.opacity='1'"
>
  <span id="icon-{uid}">&#9654;</span>
</button>"""


def build_controls_html(uid: str, controls: Controls, theme: Theme) -> str:
    """Generate the HTML for the player control bar."""
    parts: list[str] = []

    if controls.show_play_button:
        style = controls.effective_style(theme=theme)
        if style == "shield":
            parts.append(_shield_button_html(uid=uid, theme=theme))
        elif style == "minimal":
            parts.append(_minimal_button_html(uid=uid, theme=theme))
        else:
            parts.append(_circle_button_html(uid=uid, theme=theme))

    if controls.show_time:
        parts.append(
            f'<span id="time-{uid}" style="'
            f"font-size: 0.72rem; font-weight: 500; color: {theme.time_color};"
            f" font-variant-numeric: tabular-nums; letter-spacing: 0.02em;"
            f'">0:00 / 0:00</span>'
        )

    if controls.show_volume:
        parts.append(
            f'<input id="volume-{uid}" type="range" min="0" max="1" step="0.05"'
            f' value="1" style="width: 80px; accent-color: {theme.cursor_color or "#6c63ff"};">'
        )

    if controls.show_playback_rate:
        parts.append(
            f'<select id="rate-{uid}" style="'
            f"background: transparent; color: {theme.time_color};"
            f" border: 1px solid rgba(255,255,255,0.15); border-radius: 4px;"
            f" padding: 2px 4px; font-size: 0.7rem;"
            f'">'
            f'<option value="0.5">0.5x</option>'
            f'<option value="0.75">0.75x</option>'
            f'<option value="1" selected>1x</option>'
            f'<option value="1.25">1.25x</option>'
            f'<option value="1.5">1.5x</option>'
            f'<option value="2">2x</option>'
            f"</select>"
        )

    if not parts:
        return ""

    return (
        f'<div id="controls-{uid}" style="'
        f'display: flex; align-items: center; gap: 14px; margin-top: 14px;">'
        + "".join(parts)
        + "</div>"
    )


def build_controls_js(uid: str, controls: Controls, ws_var: str = "ws") -> str:
    """Generate JS to wire up controls to a wavesurfer instance."""
    lines: list[str] = []

    # Time formatter
    lines.append(
        "var fmt = function(s) {"
        " var m = Math.floor(s / 60);"
        ' var sec = Math.floor(s % 60);'
        ' return m + ":" + (sec < 10 ? "0" : "") + sec;'
        "};"
    )

    if controls.show_play_button:
        lines.append(f'var btn = document.getElementById("play-{uid}");')
        lines.append(f'var iconEl = document.getElementById("icon-{uid}");')
        lines.append(f"btn.addEventListener(\"click\", function() {{ {ws_var}.playPause(); }});")
        lines.append(f'{ws_var}.on("play", function() {{ iconEl.innerHTML = "&#9646;&#9646;"; }});')
        lines.append(f'{ws_var}.on("pause", function() {{ iconEl.innerHTML = "&#9654;"; }});')

    if controls.show_time:
        lines.append(f'var timeEl = document.getElementById("time-{uid}");')
        lines.append(
            f'{ws_var}.on("audioprocess", function(t) {{'
            f' timeEl.textContent = fmt(t) + " / " + fmt({ws_var}.getDuration());'
            f" }});"
        )
        lines.append(
            f'{ws_var}.on("ready", function() {{'
            f' timeEl.textContent = "0:00 / " + fmt({ws_var}.getDuration());'
            f" }});"
        )

    if controls.show_volume:
        lines.append(f'var volEl = document.getElementById("volume-{uid}");')
        lines.append(
            f'volEl.addEventListener("input", function() {{'
            f" {ws_var}.setVolume(parseFloat(this.value));"
            f" }});"
        )

    if controls.show_playback_rate:
        lines.append(f'var rateEl = document.getElementById("rate-{uid}");')
        lines.append(
            f'rateEl.addEventListener("change", function() {{'
            f" {ws_var}.setPlaybackRate(parseFloat(this.value));"
            f" }});"
        )

    return "\n".join(lines)


def controls_height(controls: Controls) -> int:
    """Estimate pixel height contributed by the controls bar."""
    if not (controls.show_play_button or controls.show_time
            or controls.show_volume or controls.show_playback_rate):
        return 0
    # 14px margin-top + 40px button height
    return 54
