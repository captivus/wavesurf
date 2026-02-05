"""Plugin configuration for wavesurfer.js plugins.

Provides a ``PluginConfig`` dataclass and a ``Plugins`` factory class with
static methods for the most common plugins.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class PluginConfig:
    """Configuration for a single wavesurfer.js plugin.

    Parameters
    ----------
    name:
        Plugin constructor name as it appears in wavesurfer.js
        (e.g. ``"Timeline"``, ``"Minimap"``, ``"Regions"``, ``"Spectrogram"``).
    options:
        Options dict passed to the plugin's ``create()`` method.
    js_source:
        Optional URL or inline JS for the plugin bundle.  When ``None`` the
        plugin must already be available in the page scope (e.g. bundled).
    """

    name: str
    options: dict[str, Any] = field(default_factory=dict)
    js_source: str | None = None

    def to_js_create(self) -> str:
        """Generate the JS ``Plugin.create({...})`` expression."""
        import json
        opts = json.dumps(self.options) if self.options else "{}"
        return f"{self.name}.create({opts})"


class Plugins:
    """Factory for common wavesurfer.js plugin configurations."""

    @staticmethod
    def timeline(
        *,
        height: int = 20,
        time_interval: float | None = None,
        primary_label_interval: int | None = None,
        secondary_label_interval: int | None = None,
        style: dict[str, str] | None = None,
    ) -> PluginConfig:
        opts: dict[str, Any] = {"height": height}
        if time_interval is not None:
            opts["timeInterval"] = time_interval
        if primary_label_interval is not None:
            opts["primaryLabelInterval"] = primary_label_interval
        if secondary_label_interval is not None:
            opts["secondaryLabelInterval"] = secondary_label_interval
        if style is not None:
            opts["style"] = style
        return PluginConfig(name="Timeline", options=opts)

    @staticmethod
    def minimap(
        *,
        height: int = 20,
        wave_color: str | list[str] | None = None,
        progress_color: str | list[str] | None = None,
        overlay: bool = True,
    ) -> PluginConfig:
        opts: dict[str, Any] = {"height": height, "overlay": overlay}
        if wave_color is not None:
            opts["waveColor"] = wave_color
        if progress_color is not None:
            opts["progressColor"] = progress_color
        return PluginConfig(name="Minimap", options=opts)

    @staticmethod
    def regions() -> PluginConfig:
        return PluginConfig(name="Regions")

    @staticmethod
    def spectrogram(
        *,
        labels: bool = True,
        height: int = 128,
        color_map: str | None = None,
    ) -> PluginConfig:
        opts: dict[str, Any] = {"labels": labels, "height": height}
        if color_map is not None:
            opts["colorMap"] = color_map
        return PluginConfig(name="Spectrogram", options=opts)
