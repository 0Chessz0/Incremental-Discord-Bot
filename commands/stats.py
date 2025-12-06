import discord
from discord import app_commands
from discord.ext import commands

from data.storage import get_or_create_user
from utils.formatter import make_stats_embed


class Stats(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="stats",
        description="Show your GS Incremental statistics.",
    )
    async def stats(self, interaction: discord.Interaction):
        user = get_or_create_user(interaction.user.id)
        embed = make_stats_embed(interaction.user, user)
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Stats(bot))