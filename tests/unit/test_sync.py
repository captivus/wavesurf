"""Unit tests for the sync_upstream.py TypeScript parsers and helpers.

All tests use inline TypeScript source strings — no network access required.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

# Make the scripts directory importable.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "scripts"))

from sync_upstream import (
    TSField,
    SyncReport,
    camel_to_snake,
    compare_events,
    compare_options,
    compare_plugin_options,
    format_report,
    parse_ts_events,
    parse_ts_type_block,
)


# ---------------------------------------------------------------------------
# TypeScript type-block parser
# ---------------------------------------------------------------------------


class TestParseTsTypeBlock:
    """Tests for parse_ts_type_block()."""

    SIMPLE_SOURCE = """\
export type FooOptions = {
  height?: number
  width?: number | string
  autoplay?: boolean
}
"""

    def test_parses_simple_fields(self):
        fields = parse_ts_type_block(source=self.SIMPLE_SOURCE, type_name="FooOptions")
        names = [f.name for f in fields]
        assert names == ["height", "width", "autoplay"]

    def test_handles_optional_marker(self):
        fields = parse_ts_type_block(source=self.SIMPLE_SOURCE, type_name="FooOptions")
        assert all(f.optional for f in fields)

    def test_extracts_type_strings(self):
        fields = parse_ts_type_block(source=self.SIMPLE_SOURCE, type_name="FooOptions")
        type_map = {f.name: f.ts_type for f in fields}
        assert type_map["height"] == "number"
        assert type_map["width"] == "number | string"
        assert type_map["autoplay"] == "boolean"

    def test_handles_required_fields(self):
        source = "export type Bar = {\n  name: string\n}"
        fields = parse_ts_type_block(source=source, type_name="Bar")
        assert len(fields) == 1
        assert fields[0].name == "name"
        assert not fields[0].optional

    def test_handles_union_types(self):
        source = "export type Baz = {\n  color?: string | string[] | CanvasGradient\n}"
        fields = parse_ts_type_block(source=source, type_name="Baz")
        assert fields[0].ts_type == "string | string[] | CanvasGradient"

    def test_handles_complex_types(self):
        source = "export type Qux = {\n  channels?: Array<Partial<FooOptions> & { overlay?: boolean }>\n}"
        fields = parse_ts_type_block(source=source, type_name="Qux")
        assert len(fields) == 1
        assert fields[0].name == "channels"

    def test_handles_dict_type(self):
        source = "export type Opts = {\n  dragToSeek?: boolean | { debounceTime: number }\n}"
        fields = parse_ts_type_block(source=source, type_name="Opts")
        assert fields[0].name == "dragToSeek"

    def test_handles_jsdoc_comments(self):
        source = """\
export type Opts = {
  /** The height of the waveform in pixels */
  height?: number
}
"""
        fields = parse_ts_type_block(source=source, type_name="Opts")
        assert fields[0].comment == "The height of the waveform in pixels"

    def test_returns_empty_for_missing_type(self):
        fields = parse_ts_type_block(source="no type here", type_name="Missing")
        assert fields == []

    def test_handles_trailing_commas(self):
        source = "export type Opts = {\n  height?: number,\n  width?: number,\n}"
        fields = parse_ts_type_block(source=source, type_name="Opts")
        assert len(fields) == 2
        assert fields[0].ts_type == "number"
        assert fields[1].ts_type == "number"

    def test_nested_braces_do_not_truncate(self):
        """Fields after a nested brace type should still be parsed."""
        source = """\
export type Opts = {
  dragToSeek?: boolean | { debounceTime: number }
  hideScrollbar?: boolean
  audioRate?: number
}
"""
        fields = parse_ts_type_block(source=source, type_name="Opts")
        names = [f.name for f in fields]
        assert "dragToSeek" in names
        assert "hideScrollbar" in names
        assert "audioRate" in names
        assert len(fields) == 3


# ---------------------------------------------------------------------------
# TypeScript events parser
# ---------------------------------------------------------------------------


class TestParseTsEvents:
    """Tests for parse_ts_events()."""

    EVENTS_SOURCE = """\
export type TestEvents = {
  init: []
  ready: [duration: number]
  click: [relativeX: number, relativeY: number]
  scroll: [startTime: number, endTime: number, scrollLeft: number, scrollRight: number]
  error: [error: Error]
}
"""

    def test_parses_all_events(self):
        events = parse_ts_events(source=self.EVENTS_SOURCE, type_name="TestEvents")
        assert len(events) == 5

    def test_parameterless_event(self):
        events = parse_ts_events(source=self.EVENTS_SOURCE, type_name="TestEvents")
        assert events["init"] == []

    def test_single_param_event(self):
        events = parse_ts_events(source=self.EVENTS_SOURCE, type_name="TestEvents")
        assert events["ready"] == ["duration"]

    def test_multi_param_event(self):
        events = parse_ts_events(source=self.EVENTS_SOURCE, type_name="TestEvents")
        assert events["click"] == ["relativeX", "relativeY"]

    def test_four_param_event(self):
        events = parse_ts_events(source=self.EVENTS_SOURCE, type_name="TestEvents")
        assert events["scroll"] == ["startTime", "endTime", "scrollLeft", "scrollRight"]

    def test_error_event(self):
        events = parse_ts_events(source=self.EVENTS_SOURCE, type_name="TestEvents")
        assert events["error"] == ["error"]

    def test_returns_empty_for_missing_type(self):
        events = parse_ts_events(source="no events here", type_name="Missing")
        assert events == {}


# ---------------------------------------------------------------------------
# camelCase to snake_case conversion
# ---------------------------------------------------------------------------


class TestCamelToSnake:
    """Tests for camel_to_snake()."""

    def test_simple_two_word(self):
        assert camel_to_snake(name="barWidth") == "bar_width"

    def test_three_word(self):
        assert camel_to_snake(name="barMinHeight") == "bar_min_height"

    def test_csp_nonce(self):
        assert camel_to_snake(name="cspNonce") == "csp_nonce"

    def test_min_px_per_sec(self):
        assert camel_to_snake(name="minPxPerSec") == "min_px_per_sec"

    def test_already_lowercase(self):
        assert camel_to_snake(name="autoplay") == "autoplay"

    def test_single_word(self):
        assert camel_to_snake(name="height") == "height"

    def test_drag_to_seek(self):
        assert camel_to_snake(name="dragToSeek") == "drag_to_seek"

    def test_max_peak(self):
        assert camel_to_snake(name="maxPeak") == "max_peak"


# ---------------------------------------------------------------------------
# Comparison logic
# ---------------------------------------------------------------------------


class TestCompareOptions:
    """Tests for compare_options()."""

    def test_detects_added_field(self):
        upstream = [TSField(name="newField", ts_type="number", optional=True)]
        added, removed = compare_options(
            upstream_fields=upstream,
            excluded=[],
        )
        assert len(added) == 1
        assert added[0].name == "newField"

    def test_excludes_excluded_fields(self):
        upstream = [TSField(name="container", ts_type="string", optional=False)]
        added, removed = compare_options(
            upstream_fields=upstream,
            excluded=["container"],
        )
        assert added == []

    def test_detects_removed_field(self):
        # Pass an empty upstream list — everything in the wrapper is "removed".
        _added, removed = compare_options(
            upstream_fields=[],
            excluded=[],
        )
        # Should find at least the known fields.
        assert len(removed) > 0


class TestCompareEvents:
    """Tests for compare_events()."""

    def test_detects_added_event(self):
        upstream = {"newEvent": ["param1"]}
        # Merge with existing events so we don't report removals.
        from wavesurf._events import EVENT_PARAMS

        full_upstream = {**EVENT_PARAMS, **upstream}
        added, removed = compare_events(
            upstream_events=full_upstream,
            excluded=[],
        )
        assert "newEvent" in added
        assert added["newEvent"] == ["param1"]
        assert removed == []

    def test_excludes_excluded_events(self):
        from wavesurf._events import EVENT_PARAMS

        upstream = {**EVENT_PARAMS, "secret": []}
        added, _removed = compare_events(
            upstream_events=upstream,
            excluded=["secret"],
        )
        assert "secret" not in added


class TestComparePluginOptions:
    """Tests for compare_plugin_options()."""

    def test_detects_new_option(self):
        upstream = [TSField(name="newOpt", ts_type="number", optional=True)]
        added = compare_plugin_options(
            upstream_fields=upstream,
            excluded_options=[],
            wrapper_params=set(),
        )
        assert len(added) == 1
        assert added[0].name == "newOpt"

    def test_excludes_excluded_options(self):
        upstream = [TSField(name="container", ts_type="HTMLElement", optional=True)]
        added = compare_plugin_options(
            upstream_fields=upstream,
            excluded_options=["container"],
            wrapper_params=set(),
        )
        assert added == []

    def test_recognizes_wrapped_params(self):
        upstream = [TSField(name="height", ts_type="number", optional=True)]
        added = compare_plugin_options(
            upstream_fields=upstream,
            excluded_options=[],
            wrapper_params={"height"},
        )
        assert added == []


# ---------------------------------------------------------------------------
# Report formatting
# ---------------------------------------------------------------------------


class TestFormatReport:
    """Tests for format_report()."""

    def test_clean_report(self):
        report = SyncReport(version_current="7.12.1", version_upstream="7.12.1")
        output = format_report(report=report)
        assert "No drift detected" in output

    def test_added_options_include_suggestions(self):
        report = SyncReport(
            options_added=[
                TSField(name="barMinHeight", ts_type="number", optional=True),
            ],
            version_current="7.12.1",
            version_upstream="7.12.1",
        )
        output = format_report(report=report)
        assert "bar_min_height" in output
        assert '_SNAKE_TO_CAMEL: "bar_min_height": "barMinHeight"' in output
        assert "WaveSurferOptions: bar_min_height:" in output

    def test_added_events_include_suggestions(self):
        report = SyncReport(
            events_added={"resize": []},
            version_current="7.12.1",
            version_upstream="7.12.1",
        )
        output = format_report(report=report)
        assert 'EVENT_PARAMS: "resize": []' in output
        assert "on_resize" in output

    def test_unwrapped_plugins_listed(self):
        report = SyncReport(
            unwrapped_plugins=["envelope", "hover"],
            version_current="7.12.1",
            version_upstream="7.12.1",
        )
        output = format_report(report=report)
        assert "UNWRAPPED PLUGINS" in output
        assert "envelope" in output
        assert "hover" in output
