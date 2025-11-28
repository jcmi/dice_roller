from random import Random

from dice_roller.roller import DieResult, format_grid, format_set, roll_heroic_set, roll_sets


def test_reroll_happens_on_one_or_two():
    rng = Random(0)
    result = roll_heroic_set(rng)
    assert any(d.initial == 1 for d in result.dice)
    for d in result.dice:
        if d.initial == 1:
            assert d.final != 1
        else:
            assert d.final == d.initial


def test_sets_have_expected_length_and_total_computation():
    rng = Random(42)
    results = roll_sets(2, rng)
    assert len(results) == 2
    for res in results:
        assert len(res.kept) == 3
        assert res.total == sum(res.kept)
        assert len(res.dropped) == 1


def test_formatting_outputs_lines():
    rng = Random(99)
    res = roll_heroic_set(rng)
    lines = format_set(1, res)
    assert lines[0].startswith("Set 1:")
    grid = format_grid([lines], columns=1)
    assert "Set 1:" in grid
