"""Check wavesurf Python definitions against upstream wavesurfer.js TypeScript source.

Fetches the TypeScript source for a pinned version, parses the type definitions,
and reports any drift between the upstream API and the Python wrapper.

Usage:
    uv run python scripts/sync_upstream.py                       # report drift
    uv run python scripts/sync_upstream.py --version 7.13.0      # check specific version
    uv run python scripts/sync_upstream.py --download-bundles     # download core + plugin .min.js
    uv run python scripts/sync_upstream.py --check-latest         # query npm for latest version
"""

from __future__ import annotations

import argparse
import inspect
import json
import re
import sys
import tomllib
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PACKAGE_DIR = PROJECT_ROOT / "wavesurf"
SYNC_CONFIG_PATH = PROJECT_ROOT / "sync.toml"

# Ensure the package is importable.
sys.path.insert(0, str(PROJECT_ROOT))


# ---------------------------------------------------------------------------
# Data types
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class TSField:
    """A single field parsed from a TypeScript type definition."""

    name: str
    ts_type: str
    optional: bool
    comment: str = ""


@dataclass
class SyncReport:
    """Accumulated drift report."""

    options_added: list[TSField] = field(default_factory=list)
    options_removed: list[str] = field(default_factory=list)
    events_added: dict[str, list[str]] = field(default_factory=dict)
    events_removed: list[str] = field(default_factory=list)
    plugin_options_added: dict[str, list[TSField]] = field(default_factory=dict)
    unwrapped_plugins: list[str] = field(default_factory=list)
    version_current: str = ""
    version_upstream: str = ""

    @property
    def has_drift(self) -> bool:
        return bool(
            self.options_added
            or self.options_removed
            or self.events_added
            or self.events_removed
            or self.plugin_options_added
        )


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

def load_sync_config(*, config_path: Path = SYNC_CONFIG_PATH) -> dict:
    """Load and return the sync.toml configuration."""
    with open(config_path, "rb") as f:
        return tomllib.load(f)


# ---------------------------------------------------------------------------
# Network helpers
# ---------------------------------------------------------------------------

def fetch_upstream_source(
    *,
    repository: str,
    version: str,
    file_path: str,
) -> str:
    """Fetch a TypeScript source file from GitHub at a specific version tag."""
    url = f"https://raw.githubusercontent.com/{repository}/{version}/{file_path}"
    with urllib.request.urlopen(url=url, timeout=30) as response:
        return response.read().decode("utf-8")


def check_latest_npm_version(*, package_name: str = "wavesurfer.js") -> str:
    """Query the npm registry for the latest published version."""
    url = f"https://registry.npmjs.org/{package_name}/latest"
    with urllib.request.urlopen(url=url, timeout=15) as response:
        data = json.loads(response.read().decode("utf-8"))
    return data["version"]


# ---------------------------------------------------------------------------
# TypeScript parsers
# ---------------------------------------------------------------------------

def parse_ts_type_block(*, source: str, type_name: str) -> list[TSField]:
    """Parse a ``export type Foo = { ... }`` block into a list of fields.

    Handles the flat field syntax:
        fieldName?: type
        fieldName: type

    With optional preceding ``/** doc */`` comments.
    """
    # Match the type block from opening { to the closing } on its own line.
    # Using \n} avoids stopping at nested braces (e.g. inside { debounceTime: number }).
    pattern = rf"export\s+type\s+{re.escape(type_name)}\s*=\s*\{{(.*?)\n\}}"
    match = re.search(pattern=pattern, string=source, flags=re.DOTALL)
    if not match:
        return []

    body = match.group(1)
    fields_found: list[TSField] = []

    field_pattern = re.compile(
        r"(?:/\*\*\s*(.*?)\s*\*/\s*)?"  # optional JSDoc comment
        r"(\w+)(\??):\s*(.+?)$",        # name, optional marker, type
        re.MULTILINE,
    )

    for m in field_pattern.finditer(string=body):
        comment = (m.group(1) or "").strip()
        name = m.group(2)
        optional = m.group(3) == "?"
        ts_type = m.group(4).strip().rstrip(",")
        fields_found.append(TSField(
            name=name,
            ts_type=ts_type,
            optional=optional,
            comment=comment,
        ))

    return fields_found


def parse_ts_events(*, source: str, type_name: str = "WaveSurferEvents") -> dict[str, list[str]]:
    """Parse labeled-tuple event definitions from TypeScript source.

    Handles::

        eventName: [label: type, label2: type2]
        eventName: []
    """
    # Match the type block from opening { to the closing } on its own line.
    # Using \n} avoids stopping at nested braces (e.g. inside { debounceTime: number }).
    pattern = rf"export\s+type\s+{re.escape(type_name)}\s*=\s*\{{(.*?)\n\}}"
    match = re.search(pattern=pattern, string=source, flags=re.DOTALL)
    if not match:
        return {}

    body = match.group(1)
    events: dict[str, list[str]] = {}

    event_pattern = re.compile(r"(\w+)\s*:\s*\[(.*?)\]", re.MULTILINE)

    for m in event_pattern.finditer(string=body):
        event_name = m.group(1)
        params_str = m.group(2).strip()

        if not params_str:
            events[event_name] = []
        else:
            params: list[str] = []
            for param in params_str.split(","):
                param = param.strip()
                if ":" in param:
                    label = param.split(":")[0].strip()
                    params.append(label)
            events[event_name] = params

    return events


# ---------------------------------------------------------------------------
# Name conversion
# ---------------------------------------------------------------------------

def camel_to_snake(name: str) -> str:
    """Convert a camelCase name to snake_case.

    Used for *suggestions* only — the canonical mapping lives in
    ``_options._SNAKE_TO_CAMEL``.
    """
    # Insert underscore before each uppercase letter.
    result = re.sub(pattern=r"([A-Z])", repl=r"_\1", string=name)
    return result.lower().lstrip("_")


# ---------------------------------------------------------------------------
# Comparison logic
# ---------------------------------------------------------------------------

def compare_options(
    *,
    upstream_fields: list[TSField],
    excluded: list[str],
) -> tuple[list[TSField], list[str]]:
    """Compare upstream options against the current Python wrapper.

    Returns (added_upstream, removed_from_upstream).
    """
    from wavesurf._options import _SNAKE_TO_CAMEL

    current_camel_names = set(_SNAKE_TO_CAMEL.values())
    excluded_set = set(excluded)

    added: list[TSField] = []
    for f in upstream_fields:
        if f.name in excluded_set:
            continue
        if f.name not in current_camel_names:
            added.append(f)

    upstream_names = {f.name for f in upstream_fields} | excluded_set
    removed: list[str] = []
    for camel_name in current_camel_names:
        if camel_name not in upstream_names:
            removed.append(camel_name)

    return added, removed


def compare_events(
    *,
    upstream_events: dict[str, list[str]],
    excluded: list[str],
) -> tuple[dict[str, list[str]], list[str]]:
    """Compare upstream events against the current Python wrapper.

    Returns (added_upstream, removed_from_upstream).
    """
    from wavesurf._events import EVENT_PARAMS

    excluded_set = set(excluded)

    added: dict[str, list[str]] = {}
    for name, params in upstream_events.items():
        if name in excluded_set:
            continue
        if name not in EVENT_PARAMS:
            added[name] = params

    removed: list[str] = []
    for name in EVENT_PARAMS:
        if name not in upstream_events and name not in excluded_set:
            removed.append(name)

    return added, removed


def get_plugin_factory_params(*, plugin_name: str) -> set[str]:
    """Extract parameter names from a Plugins factory method."""
    from wavesurf._plugins import Plugins

    method = getattr(Plugins, plugin_name, None)
    if method is None:
        return set()

    sig = inspect.signature(obj=method)
    return {
        name
        for name, _param in sig.parameters.items()
        if name not in ("self", "cls")
    }


def compare_plugin_options(
    *,
    upstream_fields: list[TSField],
    excluded_options: list[str],
    wrapper_params: set[str],
) -> list[TSField]:
    """Compare upstream plugin options against the wrapper's factory params.

    Returns fields present upstream but missing from the wrapper.
    """
    excluded_set = set(excluded_options)
    added: list[TSField] = []
    for f in upstream_fields:
        if f.name in excluded_set:
            continue
        snake_name = camel_to_snake(name=f.name)
        if snake_name not in wrapper_params and f.name not in wrapper_params:
            added.append(f)
    return added


# ---------------------------------------------------------------------------
# Report formatting
# ---------------------------------------------------------------------------

def format_report(*, report: SyncReport) -> str:
    """Format the sync report for terminal output with copy-paste suggestions."""
    lines: list[str] = []
    lines.append(f"Upstream version: {report.version_upstream}")
    lines.append(f"Tracked version:  {report.version_current}")
    lines.append("")

    if not report.has_drift and not report.unwrapped_plugins:
        lines.append("No drift detected. Python wrapper is in sync.")
        return "\n".join(lines)

    if not report.has_drift:
        lines.append("No API drift detected.")
        lines.append("")

    # --- Options ---
    if report.options_added:
        lines.append("=== OPTIONS: Added upstream ===")
        for f in report.options_added:
            snake = camel_to_snake(name=f.name)
            lines.append(f"  + {f.name} ({f.ts_type})")
            lines.append(f"    Suggested Python name: {snake}")
            lines.append(f'    Add to _SNAKE_TO_CAMEL: "{snake}": "{f.name}",')
            lines.append(f"    Add to WaveSurferOptions: {snake}: ... | None = None")
            if f.comment:
                lines.append(f"    Upstream doc: {f.comment}")
        lines.append("")

    if report.options_removed:
        lines.append("=== OPTIONS: Removed upstream ===")
        for name in report.options_removed:
            lines.append(f"  - {name}")
        lines.append("")

    # --- Events ---
    if report.events_added:
        lines.append("=== EVENTS: Added upstream ===")
        for name, params in report.events_added.items():
            param_str = str(params) if params else "[]"
            lines.append(f"  + {name}: {param_str}")
            lines.append(f'    Add to EVENT_PARAMS: "{name}": {param_str},')
            lines.append(f"    Add factory method: on_{name}")
        lines.append("")

    if report.events_removed:
        lines.append("=== EVENTS: Removed upstream ===")
        for name in report.events_removed:
            lines.append(f"  - {name}")
        lines.append("")

    # --- Plugin options ---
    if report.plugin_options_added:
        lines.append("=== PLUGIN OPTIONS: Added upstream ===")
        for plugin, fields_list in report.plugin_options_added.items():
            lines.append(f"  [{plugin}]")
            for f in fields_list:
                snake = camel_to_snake(name=f.name)
                lines.append(f"    + {f.name} ({f.ts_type}) -> {snake}")
        lines.append("")

    # --- Unwrapped plugins ---
    if report.unwrapped_plugins:
        lines.append("=== UNWRAPPED PLUGINS (available upstream) ===")
        lines.append(f"  {', '.join(report.unwrapped_plugins)}")
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Bundle downloads
# ---------------------------------------------------------------------------

_UNPKG_BASE = "https://unpkg.com/wavesurfer.js@{version}/dist"


def download_core_bundle(*, version: str, output_path: Path) -> None:
    """Download wavesurfer.min.js from the unpkg CDN."""
    url = f"{_UNPKG_BASE.format(version=version)}/wavesurfer.min.js"
    print(f"Downloading wavesurfer.min.js v{version} ...")
    with urllib.request.urlopen(url=url, timeout=30) as response:
        content = response.read().decode("utf-8")
    output_path.write_text(data=content, encoding="utf-8")
    print(f"  Written to {output_path} ({len(content):,} bytes)")


def download_plugin_bundles(
    *,
    version: str,
    plugin_names: list[str],
    output_dir: Path,
) -> None:
    """Download plugin .min.js files from the unpkg CDN."""
    output_dir.mkdir(parents=True, exist_ok=True)
    for name in plugin_names:
        url = f"{_UNPKG_BASE.format(version=version)}/plugins/{name}.min.js"
        output_path = output_dir / f"{name}.min.js"
        print(f"Downloading {name}.min.js v{version} ...")
        try:
            with urllib.request.urlopen(url=url, timeout=30) as response:
                content = response.read().decode("utf-8")
            output_path.write_text(data=content, encoding="utf-8")
            print(f"  Written to {output_path} ({len(content):,} bytes)")
        except urllib.error.HTTPError as exc:
            print(f"  Warning: could not download {name}.min.js: {exc}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def build_report(*, config: dict, version: str) -> SyncReport:
    """Fetch upstream source, parse types, and build a drift report."""
    repository = config["upstream"]["repository"]

    # --- Fetch and parse core types ---
    print(f"Fetching upstream wavesurfer.js v{version} ...")
    ws_source = fetch_upstream_source(
        repository=repository,
        version=version,
        file_path="src/wavesurfer.ts",
    )

    upstream_options = parse_ts_type_block(
        source=ws_source,
        type_name="WaveSurferOptions",
    )
    upstream_events = parse_ts_events(
        source=ws_source,
        type_name="WaveSurferEvents",
    )

    # --- Compare options ---
    options_added, options_removed = compare_options(
        upstream_fields=upstream_options,
        excluded=config["options"]["excluded"],
    )

    # --- Compare events ---
    events_added, events_removed = compare_events(
        upstream_events=upstream_events,
        excluded=config["events"]["excluded"],
    )

    # --- Compare plugin options for wrapped plugins ---
    plugin_options_added: dict[str, list[TSField]] = {}
    for plugin_name in config["plugins"]["wrapped"]:
        ts_type_name = f"{plugin_name.capitalize()}PluginOptions"
        ts_file = f"src/plugins/{plugin_name}.ts"

        try:
            plugin_source = fetch_upstream_source(
                repository=repository,
                version=version,
                file_path=ts_file,
            )
        except Exception as exc:
            print(f"  Warning: could not fetch {ts_file}: {exc}")
            continue

        plugin_fields = parse_ts_type_block(
            source=plugin_source,
            type_name=ts_type_name,
        )

        wrapper_params = get_plugin_factory_params(plugin_name=plugin_name)
        excluded_opts = config["plugins"].get("excluded_options", {}).get(plugin_name, [])

        added = compare_plugin_options(
            upstream_fields=plugin_fields,
            excluded_options=excluded_opts,
            wrapper_params=wrapper_params,
        )
        if added:
            plugin_options_added[plugin_name] = added

    # --- Unwrapped plugins ---
    wrapped_set = set(config["plugins"]["wrapped"])
    unwrapped = [
        name for name in config["plugins"]["all_upstream"]
        if name not in wrapped_set
    ]

    return SyncReport(
        options_added=options_added,
        options_removed=options_removed,
        events_added=events_added,
        events_removed=events_removed,
        plugin_options_added=plugin_options_added,
        unwrapped_plugins=unwrapped,
        version_current=config["upstream"]["version"],
        version_upstream=version,
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Check wavesurf against upstream wavesurfer.js",
    )
    parser.add_argument(
        "--version",
        default=None,
        help="Override the upstream version to check (default: from sync.toml)",
    )
    parser.add_argument(
        "--download-bundles",
        action="store_true",
        help="Download wavesurfer.min.js and plugin bundles for the tracked version",
    )
    parser.add_argument(
        "--check-latest",
        action="store_true",
        help="Query the npm registry for the latest upstream version",
    )
    args = parser.parse_args()

    config = load_sync_config()
    upstream_version = args.version or config["upstream"]["version"]

    # --- Check latest ---
    if args.check_latest:
        latest = check_latest_npm_version()
        pinned = config["upstream"]["version"]
        print(f"Latest npm version: {latest}")
        print(f"Pinned version:     {pinned}")
        if latest != pinned:
            print(f"  -> New version available! Update sync.toml to track {latest}")
        else:
            print("  -> Already tracking the latest version.")
        print()

    # --- Build and print drift report ---
    report = build_report(config=config, version=upstream_version)
    print()
    print(format_report(report=report))

    # --- Download bundles ---
    if args.download_bundles:
        download_core_bundle(
            version=upstream_version,
            output_path=PACKAGE_DIR / "wavesurfer.min.js",
        )
        download_plugin_bundles(
            version=upstream_version,
            plugin_names=config["plugins"]["wrapped"],
            output_dir=PACKAGE_DIR / "plugins",
        )

    # Exit non-zero if drift detected (useful for CI).
    if report.has_drift:
        sys.exit(1)


if __name__ == "__main__":
    main()
