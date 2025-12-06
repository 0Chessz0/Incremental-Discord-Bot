import discord
from discord import app_commands
from discord.ext import commands

from data.storage import get_or_create_user, save_user
from data.balance import GEM_UPGRADES, get_gem_upgrade_cost, update_multiplier
from utils.constants import EMBED_COLOR_MAIN


def make_gem_upgrade_embed(user: dict, key: str) -> discord.Embed:
    info = GEM_UPGRADES[key]
    lvl = user["gem_upgrades"].get(key, 0)
    max_lvl = int(info["max_level"])
    cost = get_gem_upgrade_cost(key, lvl)

    embed = discord.Embed(
        title="💎 Gem Upgrades",
        color=EMBED_COLOR_MAIN,
    )
    embed.add_field(
        name=f"{info['label']} (Level {lvl}/{max_lvl})",
        value=str(info["description"]),
        inline=False,
    )
    embed.add_field(
        name="Next Level Cost",
        value=f"{cost} 💎",
        inline=True,
    )
    embed.add_field(
        name="Your Gems",
        value=f"{user.get('gems', 0.0):.0f}",
        inline=True,
    )

    total_lvls = sum(user.get("gem_upgrades", {}).values())
    embed.set_footer(
        text=f"Total gem upgrade levels: {total_lvls} | Use /stats to see effects."
    )
    return embed


class GemUpgradesView(discord.ui.View):
    def __init__(self, user_id: int) -> None:
        super().__init__(timeout=300)
        self.user_id = user_id
        self.current_key = next(iter(GEM_UPGRADES.keys()))

        options = [
            discord.SelectOption(
                label=str(info["label"]),
                value=key,
                description=str(info["description"])[:90],
            )
            for key, info in GEM_UPGRADES.items()
        ]

        self.select = discord.ui.Select(
            placeholder="Select a gem upgrade",
            options=options,
            min_values=1,
            max_values=1,
        )
        self.select.callback = self.select_callback
        self.add_item(self.select)

    async def select_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message(
                "❌ This gem upgrade GUI belongs to someone else.",
                ephemeral=True,
            )
            return

        self.current_key = self.select.values[0]
        user = get_or_create_user(interaction.user.id)
        embed = make_gem_upgrade_embed(user, self.current_key)
        await interaction.response.edit_message(embed=embed, view=self)

    async def _handle_buy(self, interaction: discord.Interaction, qty: int = 1):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message(
                "❌ This gem upgrade GUI belongs to someone else.",
                ephemeral=True,
            )
            return

        user = get_or_create_user(interaction.user.id)
        key = self.current_key
        info = GEM_UPGRADES[key]
        lvl = user["gem_upgrades"].get(key, 0)
        max_lvl = int(info["max_level"])

        qty_bought = 0
        for _ in range(qty):
            if lvl >= max_lvl:
                break
            cost = get_gem_upgrade_cost(key, lvl)
            if user["gems"] < cost:
                break
            user["gems"] -= cost
            lvl += 1
            qty_bought += 1

        user["gem_upgrades"][key] = lvl
        update_multiplier(user)
        save_user(interaction.user.id, user)

        if qty_bought == 0:
            await interaction.response.send_message(
                "❌ You can't buy that upgrade (not enough gems or already maxed).",
                ephemeral=True,
            )
            return

        embed = make_gem_upgrade_embed(user, key)
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Buy 1", style=discord.ButtonStyle.success, emoji="➕")
    async def buy_one(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ):
        await self._handle_buy(interaction, qty=1)

    @discord.ui.button(label="Buy 10", style=discord.ButtonStyle.primary, emoji="🔟")
    async def buy_ten(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ):
        await self._handle_buy(interaction, qty=10)


class Upgrades(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="upgrades",
        description="Spend gems on powerful upgrades.",
    )
    async def upgrades(self, interaction: discord.Interaction):
        user = get_or_create_user(interaction.user.id)
        default_key = next(iter(GEM_UPGRADES.keys()))
        embed = make_gem_upgrade_embed(user, default_key)
        view = GemUpgradesView(interaction.user.id)
        await interaction.response.send_message(
            embed=embed,
            view=view,
            ephemeral=True,
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(Upgrades(bot))