"""Integration tests for sync_upstream.py against real upstream TypeScript source.

These tests fetch files from GitHub and require network access.
Marked with ``@pytest.mark.network`` — run explicitly::

    uv run python -m pytest tests/integration/ --verbose -m network
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

# Make the scripts directory importable.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "scripts"))

from sync_upstream import (
    fetch_upstream_source,
    load_sync_config,
    parse_ts_events,
    parse_ts_type_block,
)

pytestmark = pytest.mark.network


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def sync_config() -> dict:
    return load_sync_config()


@pytest.fixture(scope="module")
def upstream_version(sync_config: dict) -> str:
    return sync_config["upstream"]["version"]


@pytest.fixture(scope="module")
def repository(sync_config: dict) -> str:
    return sync_config["upstream"]["repository"]


@pytest.fixture(scope="module")
def ws_source(repository: str, upstream_version: str) -> str:
    """Fetch the upstream wavesurfer.ts source (cached per module)."""
    return fetch_upstream_source(
        repository=repository,
        version=upstream_version,
        file_path="src/wavesurfer.ts",
    )


# ---------------------------------------------------------------------------
# Options parsing against real upstream
# ---------------------------------------------------------------------------

class TestUpstreamOptionsParsing:
    """Validate that our parser works on real upstream WaveSurferOptions."""

    def test_parses_wavesurfer_options(self, ws_source: str):
        fields = parse_ts_type_block(
            source=ws_source,
            type_name="WaveSurferOptions",
        )
        assert len(fields) > 0, "Parser returned no fields from real WaveSurferOptions"

    def test_option_count_at_least_current_wrapper(self, ws_source: str):
        from wavesurf._options import _SNAKE_TO_CAMEL

        fields = parse_ts_type_block(
            source=ws_source,
            type_name="WaveSurferOptions",
        )
        # Upstream should have at least as many options as our wrapper maps.
        # (Some upstream options are intentionally excluded, but upstream
        #  should never have *fewer* total fields than our mapped set.)
        assert len(fields) >= len(_SNAKE_TO_CAMEL) - 5  # margin for excluded fields

    def test_all_wrapped_options_exist_upstream(self, ws_source: str):
        """Every option in our _SNAKE_TO_CAMEL should exist upstream."""
        from wavesurf._options import _SNAKE_TO_CAMEL

        fields = parse_ts_type_block(
            source=ws_source,
            type_name="WaveSurferOptions",
        )
        upstream_names = {f.name for f in fields}

        # These are in our mapping but set internally (not in the TS type).
        internally_set = {"container", "url"}

        for _snake, camel in _SNAKE_TO_CAMEL.items():
            if camel in internally_set:
                continue
            assert camel in upstream_names, (
                f"Wrapped option '{camel}' not found in upstream WaveSurferOptions — "
                f"may have been removed or renamed."
            )

    def test_known_fields_parsed_correctly(self, ws_source: str):
        """Spot-check a few known fields for correct parsing."""
        fields = parse_ts_type_block(
            source=ws_source,
            type_name="WaveSurferOptions",
        )
        field_map = {f.name: f for f in fields}

        assert "height" in field_map
        assert "barWidth" in field_map
        assert "waveColor" in field_map
        assert "autoplay" in field_map


# ---------------------------------------------------------------------------
# Events parsing against real upstream
# ---------------------------------------------------------------------------

class TestUpstreamEventsParsing:
    """Validate that our parser works on real upstream WaveSurferEvents."""

    def test_parses_wavesurfer_events(self, ws_source: str):
        events = parse_ts_events(
            source=ws_source,
            type_name="WaveSurferEvents",
        )
        assert len(events) > 0, "Parser returned no events from real WaveSurferEvents"

    def test_event_count_at_least_current_wrapper(self, ws_source: str):
        from wavesurf._events import EVENT_PARAMS

        events = parse_ts_events(
            source=ws_source,
            type_name="WaveSurferEvents",
        )
        assert len(events) >= len(EVENT_PARAMS), (
            f"Upstream has {len(events)} events, wrapper has {len(EVENT_PARAMS)} — "
            f"upstream should have at least as many."
        )

    def test_all_wrapped_events_exist_upstream(self, ws_source: str):
        """Every event in our EVENT_PARAMS should exist upstream."""
        from wavesurf._events import EVENT_PARAMS

        events = parse_ts_events(
            source=ws_source,
            type_name="WaveSurferEvents",
        )

        for event_name in EVENT_PARAMS:
            assert event_name in events, (
                f"Wrapped event '{event_name}' not found in upstream WaveSurferEvents — "
                f"may have been removed or renamed."
            )

    def test_known_events_parsed_correctly(self, ws_source: str):
        """Spot-check known events and their parameters."""
        events = parse_ts_events(
            source=ws_source,
            type_name="WaveSurferEvents",
        )

        assert events.get("ready") == ["duration"]
        assert events.get("init") == []
        assert events.get("click") == ["relativeX", "relativeY"]
        assert events.get("audioprocess") == ["currentTime"]


# ---------------------------------------------------------------------------
# Plugin source fetchability
# ---------------------------------------------------------------------------

class TestUpstreamPluginSources:
    """Validate that plugin TypeScript sources are fetchable."""

    def test_all_tracked_plugins_fetchable(
        self,
        sync_config: dict,
        repository: str,
        upstream_version: str,
    ):
        """Every plugin in sync.toml all_upstream should be fetchable."""
        for plugin_name in sync_config["plugins"]["all_upstream"]:
            ts_file = f"src/plugins/{plugin_name}.ts"
            try:
                source = fetch_upstream_source(
                    repository=repository,
                    version=upstream_version,
                    file_path=ts_file,
                )
                assert len(source) > 100, (
                    f"Plugin source {ts_file} seems too short ({len(source)} chars)"
                )
            except Exception as exc:
                pytest.fail(
                    f"Could not fetch upstream plugin source {ts_file}: {exc}"
                )

    def test_wrapped_plugins_have_parseable_options(
        self,
        sync_config: dict,
        repository: str,
        upstream_version: str,
    ):
        """Wrapped plugins should have options types our parser can handle."""
        for plugin_name in sync_config["plugins"]["wrapped"]:
            ts_type_name = f"{plugin_name.capitalize()}PluginOptions"
            ts_file = f"src/plugins/{plugin_name}.ts"

            source = fetch_upstream_source(
                repository=repository,
                version=upstream_version,
                file_path=ts_file,
            )

            # Regions has options = undefined, so it may return empty — that's OK.
            if plugin_name == "regions":
                continue

            fields = parse_ts_type_block(
                source=source,
                type_name=ts_type_name,
            )
            assert len(fields) > 0, (
                f"Parser returned no fields for {ts_type_name} in {ts_file}"
            )
