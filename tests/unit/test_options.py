"""Tests for wavesurf._options."""

from __future__ import annotations

import json

from wavesurf._options import WaveSurferOptions, _SNAKE_TO_CAMEL


class TestSnakeToCamelMapping:
    def test_all_dataclass_fields_have_mapping(self):
        """Every option field must have an explicit camel mapping."""
        from dataclasses import fields
        for f in fields(WaveSurferOptions):
            assert f.name in _SNAKE_TO_CAMEL, f"Missing mapping for {f.name}"

    def test_known_edge_cases(self):
        assert _SNAKE_TO_CAMEL["csp_nonce"] == "cspNonce"
        assert _SNAKE_TO_CAMEL["drag_to_seek"] == "dragToSeek"
        assert _SNAKE_TO_CAMEL["min_px_per_sec"] == "minPxPerSec"
        assert _SNAKE_TO_CAMEL["hide_scrollbar"] == "hideScrollbar"
        assert _SNAKE_TO_CAMEL["blob_mime_type"] == "blobMimeType"

    def test_simple_names_unchanged(self):
        assert _SNAKE_TO_CAMEL["autoplay"] == "autoplay"
        assert _SNAKE_TO_CAMEL["height"] == "height"
        assert _SNAKE_TO_CAMEL["url"] == "url"
        assert _SNAKE_TO_CAMEL["width"] == "width"


class TestToJsDict:
    def test_none_values_omitted(self):
        opts = WaveSurferOptions()
        assert opts.to_js_dict() == {}

    def test_set_values_included(self):
        opts = WaveSurferOptions(bar_width=3, height=80, normalize=True)
        d = opts.to_js_dict()
        assert d == {"barWidth": 3, "height": 80, "normalize": True}

    def test_list_colors(self):
        opts = WaveSurferOptions(wave_color=["#aaa", "#bbb"])
        d = opts.to_js_dict()
        assert d["waveColor"] == ["#aaa", "#bbb"]

    def test_drag_to_seek_dict(self):
        opts = WaveSurferOptions(drag_to_seek={"debounceTime": 200})
        d = opts.to_js_dict()
        assert d["dragToSeek"] == {"debounceTime": 200}


class TestToJson:
    def test_valid_json(self):
        opts = WaveSurferOptions(bar_width=3, height=80)
        parsed = json.loads(opts.to_json())
        assert parsed["barWidth"] == 3
        assert parsed["height"] == 80

    def test_render_function_not_quoted(self):
        opts = WaveSurferOptions(
            render_function="function(peaks, ctx) { ctx.fillRect(0,0,100,100); }"
        )
        js = opts.to_json()
        # The render function should appear raw, not as a quoted string
        assert '"renderFunction": function(peaks, ctx)' in js

    def test_empty_options(self):
        opts = WaveSurferOptions()
        assert opts.to_json() == "{}"


class TestFromKwargs:
    def test_known_keys_accepted(self):
        opts = WaveSurferOptions.from_kwargs(bar_width=3, height=80)
        assert opts.bar_width == 3
        assert opts.height == 80

    def test_unknown_keys_ignored(self):
        opts = WaveSurferOptions.from_kwargs(bar_width=3, unknown_key="ignored")
        assert opts.bar_width == 3

    def test_empty_kwargs(self):
        opts = WaveSurferOptions.from_kwargs()
        assert opts.bar_width is None


class TestMerge:
    def test_override_existing(self):
        base = WaveSurferOptions(bar_width=3, height=80)
        merged = base.merge(overrides={"height": 120})
        assert merged.height == 120
        assert merged.bar_width == 3

    def test_add_new_field(self):
        base = WaveSurferOptions(bar_width=3)
        merged = base.merge(overrides={"normalize": True})
        assert merged.normalize is True
        assert merged.bar_width == 3

    def test_unknown_keys_ignored_in_merge(self):
        base = WaveSurferOptions(bar_width=3)
        merged = base.merge(overrides={"unknown": "value"})
        assert merged.bar_width == 3
