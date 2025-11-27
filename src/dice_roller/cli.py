from __future__ import annotations

import argparse
from pathlib import Path
from random import Random

from .roller import format_grid, format_set, roll_sets


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Roll heroic-mode D&D stats (4d6, reroll 1s/2s once, drop lowest)."
    )
    parser.add_argument(
        "-s",
        "--sets",
        type=int,
        default=6,
        help="Number of stat sets to roll (default: 6).",
    )
    parser.add_argument(
        "-c",
        "--columns",
        type=int,
        default=3,
        help="Column count for grid output (default: 3).",
    )
    parser.add_argument(
        "--seed",
        type=int,
        help="Optional RNG seed for reproducible results.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Optional path to write results.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    if args.sets < 1:
        raise SystemExit("Error: --sets must be at least 1.")
    if args.columns < 1:
        raise SystemExit("Error: --columns must be at least 1.")

    rng = Random(args.seed)
    results = roll_sets(args.sets, rng)
    rendered_sets = [format_set(idx + 1, res) for idx, res in enumerate(results)]
    grid = format_grid(rendered_sets, columns=args.columns)

    print(grid)

    if args.output:
        args.output.write_text(grid + "\n", encoding="utf-8")
        print(f"\nSaved results to {args.output}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
