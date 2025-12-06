import discord
from discord import app_commands
from discord.ext import commands

from data.storage import get_or_create_user, save_user
from data.balance import (
    calc_reincarnation_reward,
    reincarnate_user,
    REINCARNATION_MIN_RESOURCES,
)


class Reincarnate(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="reincarnate",
        description="Lose everything to gain a permanent multiplier boost.",
    )
    async def reincarnate(self, interaction: discord.Interaction):
        user = get_or_create_user(interaction.user.id)

        reward = calc_reincarnation_reward(user)
        if reward <= 0:
            lifetime = user.get("lifetime_resources", 0.0)
            await interaction.response.send_message(
                "❌ You are not strong enough to reincarnate yet.\n"
                f"You need at least **{REINCARNATION_MIN_RESOURCES:.0f}** lifetime resources.\n"
                f"Current lifetime resources: **{lifetime:.0f}**.",
                ephemeral=True,
            )
            return

        before_reincs = user.get("reincarnations", 0)
        user = reincarnate_user(user)
        after_reincs = user.get("reincarnations", 0)

        save_user(interaction.user.id, user)

        await interaction.response.send_message(
            f"🔁 Reincarnation complete!\n"
            f"- Previous reincarnations: **{before_reincs}**\n"
            f"- New reincarnations: **{after_reincs}**\n"
            f"- This run reward: **{reward}** reincarnation point(s)\n"
            f"- Total reincarnation points: **{user.get('reincarnation_points', 0)}**\n"
            f"- New cash multiplier: **x{user.get('multiplier', 1.0):.2f}**\n\n"
            "Your buildings, resources and clicks have been reset.",
            ephemeral=True,
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(Reincarnate(bot))