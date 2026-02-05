"""Theme system for wavesurfer players.

A ``Theme`` controls both the wavesurfer.js appearance (colors, bars, height)
and the container chrome (background, border, padding, title style, button
style, decorative patterns).

Two built-in themes are provided:

- ``DARK``  — minimal dark theme (default)
- ``LIGHT`` — clean light theme

Custom themes can be registered via the module-level ``themes`` registry::

    import wavesurf as ws

    ws.themes.register("my-brand", Theme(wave_color="#ff0000", ...))
    ws.themes.enable("my-brand")
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from typing import Any


@dataclass(frozen=True)
class Theme:
    """Visual theme for a wavesurfer player."""

    # -- Waveform appearance (passed through to WaveSurferOptions) ----------
    wave_color: str | list[str] | None = None
    progress_color: str | list[str] | None = None
    cursor_color: str | None = None
    bar_width: int | None = None
    bar_gap: int | None = None
    bar_radius: int | None = None
    height: int | None = None

    # -- Container chrome ---------------------------------------------------
    background: str = "#1a1a2e"
    border: str = "1px solid rgba(255, 255, 255, 0.08)"
    border_radius: str = "12px"
    padding: str = "20px 24px"
    font_family: str = "-apple-system, BlinkMacSystemFont, system-ui, sans-serif"

    # -- Title styling ------------------------------------------------------
    title_color: str = "rgba(255, 255, 255, 0.85)"
    title_font_size: str = "0.8rem"
    title_font_weight: str = "600"
    title_marker_color: str | None = None  # hex bullet/marker before title
    title_marker_shape: str | None = None  # CSS clip-path for marker

    # -- Play button styling ------------------------------------------------
    play_button_style: str = "circle"  # "shield" | "circle" | "minimal"
    play_button_color: str = "#ffffff"
    play_button_bg: str = "rgba(255, 255, 255, 0.12)"
    play_button_hover_glow: str | None = None

    # -- Time display -------------------------------------------------------
    time_color: str = "rgba(255, 255, 255, 0.4)"

    # -- Decorative ---------------------------------------------------------
    top_accent: str | None = None  # gradient line across top edge
    background_pattern: str | None = None  # repeating SVG/CSS pattern

    # -- Margin between stacked cards ---------------------------------------
    card_margin_bottom: str = "8px"

    def waveform_overrides(self) -> dict[str, Any]:
        """Return non-None waveform fields as a dict for merging into options."""
        waveform_fields = {
            "wave_color", "progress_color", "cursor_color",
            "bar_width", "bar_gap", "bar_radius", "height",
        }
        return {
            f.name: getattr(self, f.name)
            for f in fields(self)
            if f.name in waveform_fields and getattr(self, f.name) is not None
        }

    def replace(self, **kwargs: Any) -> Theme:
        """Return a new Theme with selected fields overridden."""
        current = {f.name: getattr(self, f.name) for f in fields(self)}
        current.update(kwargs)
        return Theme(**current)


# ---------------------------------------------------------------------------
# Theme registry
# ---------------------------------------------------------------------------


class ThemeRegistry:
    """Named theme registry with a switchable global default.

    Usage::

        from wavesurf import themes

        themes.register("corporate", my_theme)
        themes.enable("corporate")
    """

    def __init__(self) -> None:
        self._themes: dict[str, Theme] = {}
        self._default: str = "dark"

    def register(self, name: str, theme: Theme) -> None:
        """Register a theme by name."""
        if not isinstance(theme, Theme):
            msg = f"Expected a Theme instance, got {type(theme).__name__}"
            raise TypeError(msg)
        self._themes[name] = theme

    def get(self, name: str) -> Theme:
        """Look up a registered theme by name."""
        try:
            return self._themes[name]
        except KeyError:
            available = ", ".join(sorted(self._themes))
            raise KeyError(
                f"Unknown theme {name!r}. Available: {available}"
            ) from None

    def __getitem__(self, name: str) -> Theme:
        return self.get(name=name)

    def __setitem__(self, name: str, theme: Theme) -> None:
        self.register(name=name, theme=theme)

    def __contains__(self, name: str) -> bool:
        return name in self._themes

    def names(self) -> list[str]:
        """Return sorted list of registered theme names."""
        return sorted(self._themes)

    @property
    def default(self) -> str:
        """Name of the current default theme."""
        return self._default

    @default.setter
    def default(self, name: str) -> None:
        if name not in self._themes:
            msg = f"Cannot set default to unregistered theme {name!r}"
            raise KeyError(msg)
        self._default = name

    def enable(self, name: str) -> None:
        """Set the global default theme by name."""
        self.default = name

    def resolve(self, theme: Theme | str | None) -> Theme:
        """Resolve a theme argument to a concrete ``Theme`` instance.

        - ``None`` → current default theme
        - ``str``  → looked up from the registry
        - ``Theme`` → returned as-is
        """
        if theme is None:
            return self._themes[self._default]
        if isinstance(theme, str):
            return self.get(name=theme)
        return theme


# ---------------------------------------------------------------------------
# Built-in themes
# ---------------------------------------------------------------------------

DARK = Theme(
    wave_color="#8888aa",
    progress_color="#6c63ff",
    cursor_color="#6c63ff",
    bar_width=2,
    bar_gap=1,
    bar_radius=2,
    height=80,
    background="#1a1a2e",
    border="1px solid rgba(255, 255, 255, 0.08)",
    title_color="rgba(255, 255, 255, 0.85)",
    play_button_style="circle",
    play_button_color="#ffffff",
    play_button_bg="rgba(108, 99, 255, 0.25)",
    time_color="rgba(255, 255, 255, 0.4)",
)

LIGHT = Theme(
    wave_color="#555577",
    progress_color="#4a56e2",
    cursor_color="#4a56e2",
    bar_width=2,
    bar_gap=1,
    bar_radius=2,
    height=80,
    background="#f8f8fc",
    border="1px solid rgba(0, 0, 0, 0.08)",
    title_color="rgba(0, 0, 0, 0.8)",
    title_font_weight="600",
    play_button_style="circle",
    play_button_color="#333333",
    play_button_bg="rgba(74, 86, 226, 0.12)",
    time_color="rgba(0, 0, 0, 0.45)",
)


# ---------------------------------------------------------------------------
# Module-level registry — pre-populated with built-in themes
# ---------------------------------------------------------------------------

themes = ThemeRegistry()
themes.register(name="dark", theme=DARK)
themes.register(name="light", theme=LIGHT)
