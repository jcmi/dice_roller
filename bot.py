from __future__ import annotations

import os
from random import Random

import discord
from discord import app_commands
from discord.ext import commands

from dice_roller.roller import format_grid, format_set, roll_sets


intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready() -> None:
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")


@bot.tree.command(description="Roll heroic-mode D&D stats (4d6, reroll 1/2 once, drop lowest)")
@app_commands.describe(
    sets="Number of stat sets (1-12)",
    columns="Number of columns in grid (1-6)",
    seed="Optional RNG seed for reproducible rolls",
)
async def roll(
    interaction: discord.Interaction, sets: int = 6, columns: int = 3, seed: int | None = None
) -> None:
    # Clamp to avoid spam in shared servers.
    sets = max(1, min(sets, 12))
    columns = max(1, min(columns, 6))

    rng = Random(seed) if seed is not None else Random()
    results = roll_sets(sets, rng)
    rendered = [format_set(i + 1, res) for i, res in enumerate(results)]
    grid = format_grid(rendered, columns=columns)

    content = f"```\n{grid}\n```"
    await interaction.response.send_message(content)


def main() -> None:
    token = os.environ.get("DISCORD_TOKEN")
    if not token:
        raise SystemExit("DISCORD_TOKEN not set")
    bot.run(token)


if __name__ == "__main__":
    main()
