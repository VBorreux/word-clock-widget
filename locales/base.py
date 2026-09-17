"""Shared building blocks for every language definition.

A locale is described by a rectangular grid of letters plus a mapping from a
token to the grid segments that spell it.  Tokens carry a *name* that may
differ from the displayed word (``FIVE_M`` for the minute "FIVE", ``FIVE_H``
for the hour "FIVE"): this lets the same word appear at two different places in
the grid, exactly like the original Qlocktwo.

Words are laid out in reading order, so that the illuminated words of any time
read naturally from top-left to bottom-right.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable, Mapping, Sequence

Segment = tuple[int, int, int]


class LocaleError(ValueError):
    """Raised when a locale definition is inconsistent."""


@dataclass(frozen=True)
class Locale:
    code: str
    name: str
    grid: tuple[str, ...]
    words: Mapping[str, tuple[Segment, ...]]
    labels: Mapping[str, str]
    build: Callable[[int, int], list[str]]
    optional: bool = False
    rtl: bool = False

    @property
    def width(self) -> int:
        return len(self.grid[0])

    @property
    def height(self) -> int:
        return len(self.grid)

    def segments(self, token: str) -> tuple[Segment, ...]:
        return tuple(self.words.get(token, ()))

    def label(self, token: str) -> str:
        return self.labels.get(token, token)

    def validate(self) -> None:
        if not self.grid:
            raise LocaleError(f"{self.code}: empty grid")
        width = len(self.grid[0])
        if width == 0:
            raise LocaleError(f"{self.code}: empty rows")
        for index, row in enumerate(self.grid):
            if len(row) != width:
                raise LocaleError(
                    f"{self.code}: row {index} has length {len(row)}, expected {width}"
                )
        for token, segments in self.words.items():
            if not token:
                raise LocaleError(f"{self.code}: empty token")
            if not segments:
                raise LocaleError(f"{self.code}: token {token!r} has no segment")
            for row, col, length in segments:
                if length <= 0:
                    raise LocaleError(f"{self.code}: token {token!r} has empty segment")
                if row < 0 or row >= self.height:
                    raise LocaleError(
                        f"{self.code}: token {token!r} row {row} out of range"
                    )
                if col < 0 or col + length > width:
                    raise LocaleError(
                        f"{self.code}: token {token!r} columns {col}..{col + length} "
                        f"out of range"
                    )


def pack_placements(
    tokens: Sequence[tuple[str, str]], width: int, height: int
) -> list[tuple[int, int, str, str]]:
    """Place words strictly in reading order, wrapping to the next row.

    Strict order is what guarantees that a phrase illuminates words from
    top-left to bottom-right.
    """
    placements: list[tuple[int, int, str, str]] = []
    row = 0
    col = 0
    for token, word in tokens:
        if len(word) > width:
            raise LocaleError(f"word {word!r} wider than grid ({width})")
        if col + len(word) > width:
            row += 1
            col = 0
        if row >= height:
            raise LocaleError(f"grid {width}x{height} too small to hold all words")
        placements.append((row, col, word, token))
        col += len(word)
    return placements


def make_grid(
    placements: Sequence[tuple[int, int, str, str]],
    width: int,
    height: int,
    filler: str,
) -> tuple[tuple[str, ...], dict[str, tuple[Segment, ...]]]:
    if not filler:
        raise LocaleError("filler alphabet must not be empty")
    cells: list[list[str]] = [[""] * width for _ in range(height)]
    words: dict[str, list[Segment]] = {}
    for row, col, word, token in placements:
        if row < 0 or row >= height or col < 0 or col + len(word) > width:
            raise LocaleError(f"placement of {word!r} out of bounds")
        for offset, char in enumerate(word):
            current = cells[row][col + offset]
            if current not in ("", char):
                raise LocaleError(
                    f"overlap at row {row} col {col + offset}: "
                    f"{current!r} vs {char!r}"
                )
            cells[row][col + offset] = char
        words.setdefault(token, []).append((row, col, len(word)))

    filler_index = 0
    for row in range(height):
        for col in range(width):
            if cells[row][col] == "":
                cells[row][col] = filler[filler_index % len(filler)]
                filler_index += 1

    grid = tuple("".join(row) for row in cells)
    return grid, {token: tuple(segments) for token, segments in words.items()}


def make_standard_build(
    intro: Sequence[str],
    hours: Sequence[Sequence[str]],
    minute_map: Mapping[int, tuple[Sequence[str], int]],
    oclock: Sequence[str] = (),
    minute_first: bool = False,
) -> Callable[[int, int], list[str]]:
    """Build the token names for a given time, in reading order.

    ``hours`` is indexed 0..11 for hours 1..12.  ``minute_map`` maps a five
    minute bucket (5..55) to the tokens to light and an hour offset (0 for
    "past", +1 for "to" constructions).
    """

    def build(hour: int, minute: int) -> list[str]:
        normalized = hour % 12 or 12
        bucket = (minute // 5) * 5
        if bucket == 0:
            return list(intro) + list(hours[normalized - 1]) + list(oclock)
        minute_tokens, offset = minute_map[bucket]
        target = (normalized + offset - 1) % 12 + 1
        if minute_first:
            return list(intro) + list(minute_tokens) + list(hours[target - 1])
        return list(intro) + list(hours[target - 1]) + list(minute_tokens)

    return build


def build_locale(
    *,
    code: str,
    name: str,
    tokens: Mapping[str, str],
    order: Sequence[str],
    build: Callable[[int, int], list[str]],
    filler: str,
    width: int = 11,
    height: int = 11,
    optional: bool = False,
    rtl: bool = False,
) -> Locale:
    missing = [token for token in order if token not in tokens]
    if missing:
        raise LocaleError(f"{code}: tokens missing for {missing}")
    placements = pack_placements(
        [(token, tokens[token]) for token in order], width, height
    )
    grid, words = make_grid(placements, width, height, filler)
    locale = Locale(
        code=code,
        name=name,
        grid=grid,
        words=words,
        labels=dict(tokens),
        build=build,
        optional=optional,
        rtl=rtl,
    )
    locale.validate()
    return locale


def minute_dots(minute: int) -> int:
    """Number of corner dots lit for the given minute (0..4)."""
    return minute % 5
