"""Shared building blocks for every language definition.

A locale is described by a rectangular grid of letters plus a mapping from a
word token to the list of grid segments that spell it.  The helper functions in
this module build both pieces from a simple, ordered list of words so that each
language file stays declarative and readable.
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
    tokens: Iterable[tuple[str, str]], width: int, height: int
) -> list[tuple[int, int, str, str]]:
    """Place words in reading order, filling each row with the next words that fit.

    Keeping the original order means phrases tend to be illuminated from top to
    bottom, while the "scan all remaining words" step keeps the grid compact.
    """
    remaining = list(tokens)
    for _, word in remaining:
        if len(word) > width:
            raise LocaleError(f"word {word!r} wider than grid ({width})")

    placements: list[tuple[int, int, str, str]] = []
    row = 0
    while remaining:
        if row >= height:
            raise LocaleError(f"grid {width}x{height} too small to hold all words")
        col = 0
        leftover: list[tuple[str, str]] = []
        for token, word in remaining:
            if col + len(word) <= width:
                placements.append((row, col, word, token))
                col += len(word)
            else:
                leftover.append((token, word))
        remaining = leftover
        row += 1
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
    hours: Mapping[int, Sequence[str]],
    minute_map: Mapping[int, tuple[Sequence[str], int]],
    oclock: Sequence[str] = (),
) -> Callable[[int, int], list[str]]:
    """Build the token list for a given time.

    ``minute_map`` maps a five minute bucket (5..55) to the tokens to light and
    an hour offset (0 for "past", +1 for "to" constructions).
    """

    def build(hour: int, minute: int) -> list[str]:
        normalized = hour % 12 or 12
        bucket = (minute // 5) * 5
        tokens = list(intro)
        if bucket == 0:
            tokens += list(hours[normalized])
            tokens += list(oclock)
        else:
            minute_tokens, offset = minute_map[bucket]
            target = (normalized + offset - 1) % 12 + 1
            tokens += list(hours[target])
            tokens += list(minute_tokens)
        return tokens

    return build


def build_locale(
    *,
    code: str,
    name: str,
    intro: Sequence[str],
    hours: Sequence[Sequence[str]],
    minute_map: Mapping[int, tuple[Sequence[str], int]],
    filler: str,
    oclock: Sequence[str] = (),
    extra_tokens: Sequence[str] = (),
    width: int = 11,
    height: int = 11,
    optional: bool = False,
    rtl: bool = False,
) -> Locale:
    ordered: list[tuple[str, str]] = []
    seen: set[str] = set()

    def add(tokens: Iterable[str]) -> None:
        for token in tokens:
            if token not in seen:
                seen.add(token)
                ordered.append((token, token))

    add(intro)
    for hour_tokens in hours:
        add(hour_tokens)
    for bucket in sorted(minute_map):
        add(minute_map[bucket][0])
    add(oclock)
    add(extra_tokens)

    placements = pack_placements(ordered, width, height)
    grid, words = make_grid(placements, width, height, filler)
    hour_dict = {index + 1: tuple(tokens) for index, tokens in enumerate(hours)}
    build = make_standard_build(intro, hour_dict, minute_map, oclock)
    locale = Locale(
        code=code,
        name=name,
        grid=grid,
        words=words,
        build=build,
        optional=optional,
        rtl=rtl,
    )
    locale.validate()
    return locale


def minute_dots(minute: int) -> int:
    """Number of corner dots lit for the given minute (0..4)."""
    return minute % 5
