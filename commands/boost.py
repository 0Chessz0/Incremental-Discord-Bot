import discord
from discord import app_commands
from discord.ext import commands

from data.storage import get_or_create_user, save_user
from data.balance import boost_cost, update_multiplier


class Boost(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="boost",
        description="Spend resources to permanently increase your cash multiplier.",
    )
    async def boost(self, interaction: discord.Interaction):
        user = get_or_create_user(interaction.user.id)

        level = user.get("boost_level", 0)
        cost = boost_cost(level)

        if user["resources"] < cost:
            await interaction.response.send_message(
                f"❌ You need **{cost}** resources to buy the next boost.\n"
                f"You currently have **{user['resources']:.0f}**.",
                ephemeral=True,
            )
            return

        user["resources"] -= cost
        user["boost_level"] = level + 1
        m = update_multiplier(user)
        save_user(interaction.user.id, user)

        await interaction.response.send_message(
            f"⚡ Boost purchased! (Level {user['boost_level']})\n"
            f"Your cash multiplier is now **x{m:.2f}**.\n"
            f"It cost **{cost}** resources.",
            ephemeral=True,
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(Boost(bot))