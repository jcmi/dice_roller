from __future__ import annotations

from dataclasses import dataclass
from random import Random
from typing import Iterable, List, Sequence


@dataclass(frozen=True)
class DieResult:
    """Represents a single die roll with an optional reroll."""

    initial: int
    rerolled: int | None

    @property
    def final(self) -> int:
        return self.rerolled if self.rerolled is not None else self.initial

    def formatted(self) -> str:
        if self.rerolled is None:
            return str(self.initial)
        return f"{self.initial}\u2192{self.rerolled}*"  # arrow marks reroll


@dataclass(frozen=True)
class SetResult:
    total: int
    kept: Sequence[int]
    dropped: Sequence[int]
    dice: Sequence[DieResult]


def roll_die(rng: Random) -> DieResult:
    first = rng.randint(1, 6)
    if first in (1, 2):
        second = rng.randint(1, 6)
        return DieResult(initial=first, rerolled=second)
    return DieResult(initial=first, rerolled=None)


def roll_heroic_set(rng: Random) -> SetResult:
    dice = [roll_die(rng) for _ in range(4)]
    finals = [d.final for d in dice]

    ordered = sorted(enumerate(finals), key=lambda pair: (pair[1], pair[0]))
    dropped_idx, dropped_value = ordered[0]
    kept_values = [v for i, v in enumerate(finals) if i != dropped_idx]

    return SetResult(
        total=sum(kept_values),
        kept=kept_values,
        dropped=[dropped_value],
        dice=dice,
    )


def roll_sets(count: int, rng: Random | None = None) -> List[SetResult]:
    rng = rng or Random()
    return [roll_heroic_set(rng) for _ in range(count)]


def format_set(idx: int, result: SetResult) -> List[str]:
    header = f"Set {idx}: {result.total}"
    rolls = ", ".join(d.formatted() for d in result.dice)
    rolls_line = f"Rolls: {rolls}"

    kept_str = ", ".join(str(v) for v in result.kept)
    dropped_str = ", ".join(str(v) for v in result.dropped)
    ledger = f"Kept: [{kept_str}]  Dropped: [{dropped_str}]"
    note = "(* indicates a reroll; lowest final die dropped)"

    return [header, rolls_line, ledger, note]


def format_discord_header(title: str = "I rolled these HEROICALLY!") -> str:
    return f"__{title}__"


def format_discord_sets(results: Iterable[SetResult]) -> str:
    results = list(results)
    totals_line = "Totals: " + "  ".join(str(res.total) for res in results)
    detail_lines = [
        f"{res.total}: " + ", ".join(d.formatted() for d in res.dice) for res in results
    ]
    legend = "(* reroll; lowest final die dropped)"
    return "\n".join([totals_line, ""] + detail_lines + [legend])


def format_grid(sets: Iterable[List[str]], columns: int = 3) -> str:
    cells = list(sets)
    width = max(len(line) for cell in cells for line in cell)
    lines: List[str] = []
    for row_start in range(0, len(cells), columns):
        row_cells = cells[row_start : row_start + columns]
        max_lines = max(len(c) for c in row_cells)
        for i in range(max_lines):
            row_line_parts = []
            for cell in row_cells:
                line = cell[i] if i < len(cell) else ""
                row_line_parts.append(line.ljust(width))
            lines.append("  ".join(row_line_parts).rstrip())
        lines.append("")  # spacer between rows
    if lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines)
