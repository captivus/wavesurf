"""Layout helpers for combining multiple wavesurfer players.

``compare()`` and ``grid()`` arrange players in CSS grid layouts, wrapped
in a single iframe.
"""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, Any

from wavesurf._audio import resolve_audio
from wavesurf._html import (
    build_player_html,
    estimate_player_height,
    wrap_in_iframe,
)

if TYPE_CHECKING:
    from wavesurf._core import WaveSurfer, _CompareResult


def compare(
    players: list[WaveSurfer],
    columns: int = 1,
) -> _CompareResult:
    """Lay out multiple players in a grid inside a single iframe.

    Parameters
    ----------
    players:
        List of ``WaveSurfer`` instances to display.
    columns:
        Number of grid columns (default 1 = vertical stack).
    """
    from wavesurf._core import _CompareResult

    cards: list[str] = []
    max_card_height = 0

    for player in players:
        url, _sr = resolve_audio(audio=player.audio, sr=player.sr)
        uid = uuid.uuid4().hex[:12]
        options = player._build_options()

        card = build_player_html(
            uid=uid,
            url=url,
            title=player.title,
            options=options,
            theme=player.theme,
            controls=player.controls,
            events=player.events or None,
            plugins=player.plugins or None,
        )
        cards.append(card)

        h = estimate_player_height(
            title=player.title,
            theme=player.theme,
            controls=player.controls,
        )
        if h > max_card_height:
            max_card_height = h

    # CSS grid layout
    if columns > 1:
        grid_style = (
            f"display: grid; grid-template-columns: repeat({columns}, 1fr);"
            f" gap: 8px;"
        )
        rows = -(-len(cards) // columns)  # ceil division
        total_height = rows * max_card_height + 8
    else:
        grid_style = "display: grid; gap: 8px;"
        total_height = len(cards) * max_card_height

    body = f'<div style="{grid_style}">' + "".join(cards) + "</div>"
    iframe = wrap_in_iframe(body_html=body, height=total_height)
    return _CompareResult(html=iframe)


def grid(
    players: list[WaveSurfer],
    columns: int = 2,
) -> _CompareResult:
    """Alias for ``compare()`` with a default of 2 columns.

    Use this for multi-column dashboard-style layouts.
    """
    return compare(players=players, columns=columns)
