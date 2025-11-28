from __future__ import annotations

import os
from random import Random

import discord
from discord import app_commands
from discord.ext import commands

from dice_roller.roller import format_discord_header, format_discord_sets, roll_sets


intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready() -> None:
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")


@bot.tree.command(description="Roll heroic-mode D&D stats (4d6, reroll 1s until not 1, drop lowest)")
@app_commands.describe(
    sets="Number of stat sets (1-12)",
)
async def roll(
    interaction: discord.Interaction, sets: int = 6
) -> None:
    # Clamp to avoid spam in shared servers.
    sets = max(1, min(sets, 12))

    rng = Random()
    results = roll_sets(sets, rng)
    header = format_discord_header()
    body = format_discord_sets(results)
    content = f"```\n{header}\n{body}\n```"
    await interaction.response.send_message(content)


def main() -> None:
    token = os.environ.get("DISCORD_TOKEN")
    if not token:
        raise SystemExit("DISCORD_TOKEN not set")
    bot.run(token)


if __name__ == "__main__":
    main()
