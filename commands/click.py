import discord
from discord import app_commands
from discord.ext import commands

from data.storage import get_or_create_user, save_user
from data.balance import get_click_gain
from utils.formatter import make_click_embed


class ClickView(discord.ui.View):
    def __init__(self, user_id: int) -> None:
        super().__init__(timeout=None)
        self.user_id = user_id

    @discord.ui.button(
        label="Click",
        style=discord.ButtonStyle.primary,
        emoji="🖱️",
    )
    async def click_button(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message(
                "❌ This clicker belongs to someone else.",
                ephemeral=True,
            )
            return

        user = get_or_create_user(interaction.user.id)
        gain = get_click_gain(user)
        user["resources"] += gain
        user["lifetime_resources"] = user.get("lifetime_resources", 0.0) + gain
        user["total_clicks"] = user.get("total_clicks", 0) + 1

        save_user(interaction.user.id, user)

        embed = make_click_embed(user)
        await interaction.response.edit_message(embed=embed, view=self)


class Click(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="click",
        description="Open a clicker GUI you can repeatedly press.",
    )
    async def click(self, interaction: discord.Interaction):
        user = get_or_create_user(interaction.user.id)
        embed = make_click_embed(user)
        view = ClickView(interaction.user.id)
        await interaction.response.send_message(
            embed=embed,
            view=view,
            ephemeral=True,
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(Click(bot))