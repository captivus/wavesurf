"""Core WaveSurfer class and convenience functions."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Any

from wavesurf._audio import resolve_audio
from wavesurf._controls import Controls
from wavesurf._events import EventHandler
from wavesurf._html import build_player_html, estimate_player_height, wrap_in_iframe
from wavesurf._options import WaveSurferOptions
from wavesurf._plugins import PluginConfig
from wavesurf._theme import Theme, themes


@dataclass
class WaveSurfer:
    """A wavesurfer.js audio player for Jupyter notebooks.

    Parameters
    ----------
    audio:
        Audio source — numpy array, torch tensor, file path, or URL string.
    sr:
        Sample rate.  Required when *audio* is a numpy array or torch tensor.
    title:
        Optional label displayed above the waveform.
    theme:
        Visual theme.  Defaults to ``DARK``.
    controls:
        Player control configuration.  Defaults to play button + time display.
    events:
        List of ``EventHandler`` instances to attach.
    plugins:
        List of ``PluginConfig`` instances to register.
    on_ready:
        Shorthand — raw JS to run when the player is ready.
    **options:
        Any wavesurfer.js option in snake_case (e.g. ``bar_width=3``).
        These override theme defaults.
    """

    audio: Any
    sr: int | None = None
    title: str | None = None
    theme: Theme = field(default_factory=lambda: themes.resolve(None))
    controls: Controls = field(default_factory=Controls)
    events: list[EventHandler] = field(default_factory=list)
    plugins: list[PluginConfig] = field(default_factory=list)
    _extra_options: dict[str, Any] = field(default_factory=dict, repr=False)

    def __init__(
        self,
        audio: Any,
        sr: int | None = None,
        *,
        title: str | None = None,
        theme: Theme | str | None = None,
        controls: Controls | None = None,
        events: list[EventHandler] | None = None,
        plugins: list[PluginConfig] | None = None,
        on_ready: str | None = None,
        **options: Any,
    ) -> None:
        self.audio = audio
        self.sr = sr
        self.title = title
        self.theme = themes.resolve(theme=theme)
        self.controls = controls if controls is not None else Controls()
        self.events = list(events) if events else []
        self.plugins = list(plugins) if plugins else []
        self._extra_options = options

        if on_ready:
            self.events.append(
                EventHandler(event="ready", js=on_ready, once=True)
            )

    def _build_options(self) -> WaveSurferOptions:
        """Merge theme defaults + explicit overrides into a WaveSurferOptions."""
        # Start with theme waveform settings
        merged = dict(self.theme.waveform_overrides())
        # User kwargs override theme
        merged.update(self._extra_options)
        return WaveSurferOptions.from_kwargs(**merged)

    def to_html(self) -> str:
        """Render to a complete iframe-wrapped HTML string."""
        url, _sr = resolve_audio(audio=self.audio, sr=self.sr)
        uid = uuid.uuid4().hex[:12]
        options = self._build_options()

        player = build_player_html(
            uid=uid,
            url=url,
            title=self.title,
            options=options,
            theme=self.theme,
            controls=self.controls,
            events=self.events or None,
            plugins=self.plugins or None,
        )
        height = estimate_player_height(
            title=self.title,
            theme=self.theme,
            controls=self.controls,
            options=options,
            plugins=self.plugins or None,
        )
        plugin_names = (
            [p.name.lower() for p in self.plugins] if self.plugins else None
        )
        return wrap_in_iframe(
            body_html=player,
            height=height,
            plugin_names=plugin_names,
        )

    def _repr_html_(self) -> str:
        """IPython rich display — auto-renders in Jupyter."""
        return self.to_html()

    # -- Immutable builder methods ------------------------------------------

    def with_options(self, **kwargs: Any) -> WaveSurfer:
        """Return a copy with additional wavesurfer options."""
        new_opts = {**self._extra_options, **kwargs}
        return WaveSurfer(
            audio=self.audio, sr=self.sr, title=self.title,
            theme=self.theme, controls=self.controls,
            events=self.events, plugins=self.plugins,
            **new_opts,
        )

    def with_theme(self, theme: Theme | str) -> WaveSurfer:
        """Return a copy with a different theme (name or ``Theme`` object)."""
        return WaveSurfer(
            audio=self.audio, sr=self.sr, title=self.title,
            theme=theme, controls=self.controls,
            events=self.events, plugins=self.plugins,
            **self._extra_options,
        )

    def with_events(self, *handlers: EventHandler) -> WaveSurfer:
        """Return a copy with additional event handlers."""
        return WaveSurfer(
            audio=self.audio, sr=self.sr, title=self.title,
            theme=self.theme, controls=self.controls,
            events=[*self.events, *handlers], plugins=self.plugins,
            **self._extra_options,
        )

    def with_plugins(self, *configs: PluginConfig) -> WaveSurfer:
        """Return a copy with additional plugins."""
        return WaveSurfer(
            audio=self.audio, sr=self.sr, title=self.title,
            theme=self.theme, controls=self.controls,
            events=self.events, plugins=[*self.plugins, *configs],
            **self._extra_options,
        )


# ---------------------------------------------------------------------------
# Convenience functions
# ---------------------------------------------------------------------------


def display_audio(
    audio: Any,
    sr: int | None = None,
    *,
    title: str | None = None,
    theme: Theme | str | None = None,
    controls: Controls | None = None,
    **options: Any,
) -> WaveSurfer:
    """Create and display a single audio player.

    Returns a ``WaveSurfer`` instance that auto-displays in Jupyter via
    ``_repr_html_()``.
    """
    return WaveSurfer(
        audio=audio, sr=sr, title=title,
        theme=theme, controls=controls,
        **options,
    )


def compare_audio(
    audio_dict: dict[str, Any],
    sr: int | None = None,
    *,
    columns: int = 1,
    theme: Theme | str | None = None,
    controls: Controls | None = None,
    **options: Any,
) -> _CompareResult:
    """Display multiple audio players for side-by-side comparison.

    Parameters
    ----------
    audio_dict:
        Mapping of ``{label: audio}`` or ``{label: (array, sr)}``.
    sr:
        Default sample rate for plain arrays.
    columns:
        Number of grid columns (default 1 = stacked).
    theme:
        Theme applied to all players.
    controls:
        Controls config applied to all players.
    **options:
        Extra wavesurfer options applied to all players.
    """
    players: list[WaveSurfer] = []
    for label, value in audio_dict.items():
        if isinstance(value, tuple):
            audio_data, audio_sr = value
        else:
            audio_data = value
            audio_sr = sr
        player = WaveSurfer(
            audio=audio_data, sr=audio_sr, title=label,
            theme=theme, controls=controls,
            **options,
        )
        players.append(player)

    from wavesurf._layouts import compare
    return compare(players=players, columns=columns)


class _CompareResult:
    """Display wrapper for a multi-player comparison grid."""

    def __init__(self, html: str) -> None:
        self._html = html

    def _repr_html_(self) -> str:
        return self._html
