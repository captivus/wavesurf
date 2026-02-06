"""WaveSurfer options dataclass with snake_case → camelCase conversion."""

from __future__ import annotations

import json
from dataclasses import dataclass, fields
from typing import Any


# Explicit mapping for snake_case Python names → camelCase JS property names.
# Not algorithmic, to handle edge cases like csp_nonce → cspNonce correctly.
_SNAKE_TO_CAMEL: dict[str, str] = {
    "audio_rate": "audioRate",
    "auto_center": "autoCenter",
    "auto_scroll": "autoScroll",
    "autoplay": "autoplay",
    "backend": "backend",
    "bar_align": "barAlign",
    "bar_gap": "barGap",
    "bar_height": "barHeight",
    "bar_min_height": "barMinHeight",
    "bar_radius": "barRadius",
    "bar_width": "barWidth",
    "blob_mime_type": "blobMimeType",
    "container": "container",
    "csp_nonce": "cspNonce",
    "cursor_color": "cursorColor",
    "cursor_width": "cursorWidth",
    "drag_to_seek": "dragToSeek",
    "duration": "duration",
    "fetch_params": "fetchParams",
    "fill_parent": "fillParent",
    "height": "height",
    "hide_scrollbar": "hideScrollbar",
    "interact": "interact",
    "media_controls": "mediaControls",
    "max_peak": "maxPeak",
    "min_px_per_sec": "minPxPerSec",
    "normalize": "normalize",
    "progress_color": "progressColor",
    "render_function": "renderFunction",
    "sample_rate": "sampleRate",
    "split_channels": "splitChannels",
    "url": "url",
    "wave_color": "waveColor",
    "width": "width",
}


@dataclass
class WaveSurferOptions:
    """All wavesurfer.js constructor options, expressed in snake_case.

    Only non-None values are emitted when converting to JS.  The ``container``
    field is intentionally omitted here — it is always set by the HTML
    generator to the per-player DOM selector.
    """

    audio_rate: float | None = None
    auto_center: bool | None = None
    auto_scroll: bool | None = None
    autoplay: bool | None = None
    backend: str | None = None
    bar_align: str | None = None
    bar_gap: int | None = None
    bar_height: float | None = None
    bar_min_height: int | None = None
    bar_radius: int | None = None
    bar_width: int | None = None
    blob_mime_type: str | None = None
    csp_nonce: str | None = None
    cursor_color: str | None = None
    cursor_width: int | None = None
    drag_to_seek: bool | dict | None = None
    duration: float | None = None
    fetch_params: dict | None = None
    fill_parent: bool | None = None
    height: int | str | None = None
    hide_scrollbar: bool | None = None
    interact: bool | None = None
    media_controls: bool | None = None
    max_peak: float | None = None
    min_px_per_sec: int | None = None
    normalize: bool | None = None
    progress_color: str | list[str] | None = None
    render_function: str | None = None  # raw JS function body
    sample_rate: int | None = None
    split_channels: list[dict] | None = None
    url: str | None = None
    wave_color: str | list[str] | None = None
    width: int | str | None = None

    def to_js_dict(self) -> dict[str, Any]:
        """Return a camelCase dict with only non-None values."""
        result: dict[str, Any] = {}
        for f in fields(self):
            value = getattr(self, f.name)
            if value is None:
                continue
            camel_key = _SNAKE_TO_CAMEL.get(f.name, f.name)
            result[camel_key] = value
        return result

    def to_json(self) -> str:
        """Serialize to a JS-embeddable JSON string.

        Special handling: ``render_function`` is emitted as raw JS (not a
        quoted string) so it can be used as a callback in WaveSurfer.create().
        """
        js_dict = self.to_js_dict()
        render_fn = js_dict.pop("renderFunction", None)

        json_str = json.dumps(js_dict)

        if render_fn is not None:
            # Insert the raw JS function before the closing brace.
            json_str = json_str[:-1] + f', "renderFunction": {render_fn}' + "}"

        return json_str

    @classmethod
    def from_kwargs(cls, **kwargs: Any) -> WaveSurferOptions:
        """Create from arbitrary keyword arguments, ignoring unknown keys."""
        known = {f.name for f in fields(cls)}
        filtered = {k: v for k, v in kwargs.items() if k in known}
        return cls(**filtered)

    def merge(self, overrides: dict[str, Any]) -> WaveSurferOptions:
        """Return a new instance with *overrides* applied on top."""
        current = {f.name: getattr(self, f.name) for f in fields(self)}
        known = {f.name for f in fields(self.__class__)}
        for k, v in overrides.items():
            if k in known:
                current[k] = v
        return WaveSurferOptions(**current)
