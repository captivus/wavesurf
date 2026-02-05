"""Shared fixtures for wavesurf Playwright e2e tests."""

from __future__ import annotations

import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Generator

import pytest

SERVER_PORT = 8765
BASE_URL = f"http://localhost:{SERVER_PORT}"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


@pytest.fixture(scope="session")
def _generate_fixtures() -> None:
    """Regenerate HTML fixture and example files before the test session."""
    subprocess.run(
        ["uv", "run", "python", str(PROJECT_ROOT / "tests" / "e2e" / "fixtures" / "generate_fixtures.py")],
        cwd=str(PROJECT_ROOT),
        check=True,
    )
    subprocess.run(
        ["uv", "run", "python", str(PROJECT_ROOT / "examples" / "generate_examples.py")],
        cwd=str(PROJECT_ROOT),
        check=True,
    )


@pytest.fixture(scope="session")
def _http_server(_generate_fixtures: None) -> Generator[str, None, None]:
    """Start a local HTTP server for the test session, serving from project root."""
    proc = subprocess.Popen(
        [
            "uv", "run", "python", "-m", "http.server",
            str(SERVER_PORT),
            "--directory", str(PROJECT_ROOT),
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    # Wait until the server is ready.
    for _ in range(50):
        try:
            urllib.request.urlopen(url=BASE_URL, timeout=1)
            break
        except (urllib.error.URLError, ConnectionError):
            time.sleep(0.1)
    else:
        proc.kill()
        raise RuntimeError(f"HTTP server failed to start on port {SERVER_PORT}")

    yield BASE_URL

    proc.terminate()
    proc.wait(timeout=5)


@pytest.fixture(scope="session")
def base_url(_http_server: str) -> str:
    """Provide the base URL for all tests.

    pytest-playwright recognises this fixture name and uses it automatically.
    """
    return _http_server


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict) -> dict:
    """Set viewport to 800x600 matching the previous Cypress configuration."""
    return {
        **browser_context_args,
        "viewport": {"width": 800, "height": 600},
    }
