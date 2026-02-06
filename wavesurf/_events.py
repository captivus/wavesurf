"""Event handler definitions for wavesurfer.js events.

Provides an ``EventHandler`` dataclass and class methods for all 24
wavesurfer.js events.
"""

from __future__ import annotations

from dataclasses import dataclass


# Maps each event name to its JS callback parameter names.
EVENT_PARAMS: dict[str, list[str]] = {
    "audioprocess": ["currentTime"],
    "click": ["relativeX", "relativeY"],
    "dblclick": ["relativeX", "relativeY"],
    "decode": ["duration"],
    "destroy": [],
    "drag": ["relativeX"],
    "dragend": ["relativeX"],
    "dragstart": ["relativeX"],
    "error": ["error"],
    "finish": [],
    "init": [],
    "interaction": ["newTime"],
    "load": ["url"],
    "loading": ["percent"],
    "pause": [],
    "play": [],
    "ready": ["duration"],
    "redraw": [],
    "redrawcomplete": [],
    "resize": [],
    "scroll": ["visibleStartTime", "visibleEndTime", "scrollLeft", "scrollRight"],
    "seeking": ["currentTime"],
    "timeupdate": ["currentTime"],
    "zoom": ["minPxPerSec"],
}


@dataclass(frozen=True)
class EventHandler:
    """A single event handler to attach to a wavesurfer instance.

    Parameters
    ----------
    event:
        The wavesurfer.js event name (e.g. ``"ready"``, ``"audioprocess"``).
    js:
        Raw JavaScript function body for the callback.
    once:
        If ``True``, use ``ws.once(...)`` instead of ``ws.on(...)``.
    """

    event: str
    js: str
    once: bool = False

    def to_js(self, ws_var: str = "ws") -> str:
        """Generate the JS event-binding statement."""
        params = EVENT_PARAMS.get(self.event, [])
        param_list = ", ".join(params)
        method = "once" if self.once else "on"
        return f'{ws_var}.{method}("{self.event}", function({param_list}) {{ {self.js} }});'

    # -- Factory class methods for every event ------------------------------

    @classmethod
    def on_audioprocess(cls, js: str, *, once: bool = False) -> EventHandler:
        return cls(event="audioprocess", js=js, once=once)

    @classmethod
    def on_click(cls, js: str, *, once: bool = False) -> EventHandler:
        return cls(event="click", js=js, once=once)

    @classmethod
    def on_dblclick(cls, js: str, *, once: bool = False) -> EventHandler:
        return cls(event="dblclick", js=js, once=once)

    @classmethod
    def on_decode(cls, js: str, *, once: bool = False) -> EventHandler:
        return cls(event="decode", js=js, once=once)

    @classmethod
    def on_destroy(cls, js: str, *, once: bool = False) -> EventHandler:
        return cls(event="destroy", js=js, once=once)

    @classmethod
    def on_drag(cls, js: str, *, once: bool = False) -> EventHandler:
        return cls(event="drag", js=js, once=once)

    @classmethod
    def on_dragend(cls, js: str, *, once: bool = False) -> EventHandler:
        return cls(event="dragend", js=js, once=once)

    @classmethod
    def on_dragstart(cls, js: str, *, once: bool = False) -> EventHandler:
        return cls(event="dragstart", js=js, once=once)

    @classmethod
    def on_error(cls, js: str, *, once: bool = False) -> EventHandler:
        return cls(event="error", js=js, once=once)

    @classmethod
    def on_finish(cls, js: str, *, once: bool = False) -> EventHandler:
        return cls(event="finish", js=js, once=once)

    @classmethod
    def on_init(cls, js: str, *, once: bool = False) -> EventHandler:
        return cls(event="init", js=js, once=once)

    @classmethod
    def on_interaction(cls, js: str, *, once: bool = False) -> EventHandler:
        return cls(event="interaction", js=js, once=once)

    @classmethod
    def on_load(cls, js: str, *, once: bool = False) -> EventHandler:
        return cls(event="load", js=js, once=once)

    @classmethod
    def on_loading(cls, js: str, *, once: bool = False) -> EventHandler:
        return cls(event="loading", js=js, once=once)

    @classmethod
    def on_pause(cls, js: str, *, once: bool = False) -> EventHandler:
        return cls(event="pause", js=js, once=once)

    @classmethod
    def on_play(cls, js: str, *, once: bool = False) -> EventHandler:
        return cls(event="play", js=js, once=once)

    @classmethod
    def on_ready(cls, js: str, *, once: bool = False) -> EventHandler:
        return cls(event="ready", js=js, once=once)

    @classmethod
    def on_redraw(cls, js: str, *, once: bool = False) -> EventHandler:
        return cls(event="redraw", js=js, once=once)

    @classmethod
    def on_redrawcomplete(cls, js: str, *, once: bool = False) -> EventHandler:
        return cls(event="redrawcomplete", js=js, once=once)

    @classmethod
    def on_resize(cls, js: str, *, once: bool = False) -> EventHandler:
        return cls(event="resize", js=js, once=once)

    @classmethod
    def on_scroll(cls, js: str, *, once: bool = False) -> EventHandler:
        return cls(event="scroll", js=js, once=once)

    @classmethod
    def on_seeking(cls, js: str, *, once: bool = False) -> EventHandler:
        return cls(event="seeking", js=js, once=once)

    @classmethod
    def on_timeupdate(cls, js: str, *, once: bool = False) -> EventHandler:
        return cls(event="timeupdate", js=js, once=once)

    @classmethod
    def on_zoom(cls, js: str, *, once: bool = False) -> EventHandler:
        return cls(event="zoom", js=js, once=once)
