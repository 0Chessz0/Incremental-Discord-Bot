import discord
from discord import app_commands
from discord.ext import commands

from data.storage import get_or_create_user, save_user
from data.balance import DARK_UPGRADES, get_dark_upgrade_cost, update_multiplier
from utils.constants import EMBED_COLOR_MAIN


def make_dark_upgrade_embed(user: dict, key: str) -> discord.Embed:
    info = DARK_UPGRADES[key]
    lvl = user["dark_upgrades"].get(key, 0)
    max_lvl = int(info["max_level"])
    cost = get_dark_upgrade_cost(key, lvl)

    embed = discord.Embed(
        title="🌑 Dark Matter Lab",
        color=EMBED_COLOR_MAIN,
    )
    embed.add_field(
        name=f"{info['label']} (Level {lvl}/{max_lvl})",
        value=str(info["description"]),
        inline=False,
    )
    embed.add_field(
        name="Next Level Cost",
        value=f"{cost:.3f} 🌑",
        inline=True,
    )
    embed.add_field(
        name="Your Dark Matter",
        value=f"{user.get('dark_matter', 0.0):.3f}",
        inline=True,
    )

    total_lvls = sum(user.get("dark_upgrades", {}).values())
    embed.set_footer(
        text=f"Total dark upgrade levels: {total_lvls} | Reinc rewards and global power scale with these."
    )
    return embed


class DarkUpgradesView(discord.ui.View):
    def __init__(self, user_id: int) -> None:
        super().__init__(timeout=300)
        self.user_id = user_id
        self.current_key = next(iter(DARK_UPGRADES.keys()))

        options = [
            discord.SelectOption(
                label=str(info["label"]),
                value=key,
                description=str(info["description"])[:90],
            )
            for key, info in DARK_UPGRADES.items()
        ]

        self.select = discord.ui.Select(
            placeholder="Select a dark matter upgrade",
            options=options,
            min_values=1,
            max_values=1,
        )
        self.select.callback = self.select_callback
        self.add_item(self.select)

    async def select_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message(
                "❌ This dark lab GUI belongs to someone else.",
                ephemeral=True,
            )
            return

        self.current_key = self.select.values[0]
        user = get_or_create_user(interaction.user.id)
        embed = make_dark_upgrade_embed(user, self.current_key)
        await interaction.response.edit_message(embed=embed, view=self)

    async def _handle_buy(self, interaction: discord.Interaction, qty: int = 1):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message(
                "❌ This dark lab GUI belongs to someone else.",
                ephemeral=True,
            )
            return

        user = get_or_create_user(interaction.user.id)
        key = self.current_key
        info = DARK_UPGRADES[key]
        lvl = user["dark_upgrades"].get(key, 0)
        max_lvl = int(info["max_level"])

        qty_bought = 0
        for _ in range(qty):
            if lvl >= max_lvl:
                break
            cost = get_dark_upgrade_cost(key, lvl)
            if user["dark_matter"] < cost:
                break
            user["dark_matter"] -= cost
            lvl += 1
            qty_bought += 1

        user["dark_upgrades"][key] = lvl
        update_multiplier(user)
        save_user(interaction.user.id, user)

        if qty_bought == 0:
            await interaction.response.send_message(
                "❌ You can't buy that upgrade (not enough dark matter or already maxed).",
                ephemeral=True,
            )
            return

        embed = make_dark_upgrade_embed(user, key)
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Buy 1", style=discord.ButtonStyle.success, emoji="➕")
    async def buy_one(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ):
        await self._handle_buy(interaction, qty=1)

    @discord.ui.button(label="Buy 5", style=discord.ButtonStyle.primary, emoji="5️⃣")
    async def buy_five(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ):
        await self._handle_buy(interaction, qty=5)


class DarkLab(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="darklab",
        description="Spend dark matter on reality-warping upgrades.",
    )
    async def darklab(self, interaction: discord.Interaction):
        user = get_or_create_user(interaction.user.id)
        default_key = next(iter(DARK_UPGRADES.keys()))
        embed = make_dark_upgrade_embed(user, default_key)
        view = DarkUpgradesView(interaction.user.id)
        await interaction.response.send_message(
            embed=embed,
            view=view,
            ephemeral=True,
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(DarkLab(bot))