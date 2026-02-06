"""Tests for wavesurf._events."""

from __future__ import annotations

from wavesurf._events import EVENT_PARAMS, EventHandler


class TestEventParams:
    def test_all_events_defined(self):
        assert len(EVENT_PARAMS) == 24

    def test_ready_params(self):
        assert EVENT_PARAMS["ready"] == ["duration"]

    def test_audioprocess_params(self):
        assert EVENT_PARAMS["audioprocess"] == ["currentTime"]

    def test_click_params(self):
        assert EVENT_PARAMS["click"] == ["relativeX", "relativeY"]

    def test_scroll_params(self):
        assert EVENT_PARAMS["scroll"] == [
            "visibleStartTime", "visibleEndTime", "scrollLeft", "scrollRight",
        ]

    def test_paramless_events(self):
        for event in ("destroy", "finish", "init", "pause", "play", "redraw", "redrawcomplete"):
            assert EVENT_PARAMS[event] == [], f"{event} should have no params"


class TestEventHandler:
    def test_basic_to_js(self):
        handler = EventHandler(event="ready", js="console.log('ready');")
        js = handler.to_js()
        assert 'ws.on("ready"' in js
        assert "console.log('ready');" in js

    def test_once_flag(self):
        handler = EventHandler(event="ready", js="doSomething();", once=True)
        js = handler.to_js()
        assert 'ws.once("ready"' in js

    def test_custom_ws_var(self):
        handler = EventHandler(event="play", js="log();")
        js = handler.to_js(ws_var="player")
        assert 'player.on("play"' in js

    def test_params_included(self):
        handler = EventHandler(event="audioprocess", js="update(currentTime);")
        js = handler.to_js()
        assert "function(currentTime)" in js

    def test_multi_param_event(self):
        handler = EventHandler(event="click", js="handle(relativeX, relativeY);")
        js = handler.to_js()
        assert "function(relativeX, relativeY)" in js


class TestFactoryMethods:
    def test_on_ready(self):
        handler = EventHandler.on_ready(js="init();")
        assert handler.event == "ready"
        assert handler.js == "init();"
        assert handler.once is False

    def test_on_ready_once(self):
        handler = EventHandler.on_ready(js="init();", once=True)
        assert handler.once is True

    def test_on_finish(self):
        handler = EventHandler.on_finish(js="done();")
        assert handler.event == "finish"

    def test_on_error(self):
        handler = EventHandler.on_error(js="handleError(error);")
        assert handler.event == "error"

    def test_all_factory_methods_exist(self):
        """Every event in EVENT_PARAMS should have a factory method."""
        for event_name in EVENT_PARAMS:
            method_name = f"on_{event_name}"
            assert hasattr(EventHandler, method_name), f"Missing factory: {method_name}"
