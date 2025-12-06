import discord
from discord import app_commands
from discord.ext import commands

from data.storage import get_or_create_user, save_user
from data.balance import (
    BUILDINGS,
    building_cost,
    get_effective_incomes,
    compute_upgrade_effects,
)
from utils.constants import EMBED_COLOR_MAIN


def _total_cost_for_qty(user, key: str, owned: int, qty: int) -> int:
    from data.balance import building_cost as single_cost

    base_total = 0
    for i in range(qty):
        base_total += single_cost(key, owned + i)

    effects = compute_upgrade_effects(user)
    discount = effects["cost_discount"]
    final = int(base_total * (1.0 - discount))
    return max(final, 0)


def _format_income_line(info) -> str:
    money = float(info["base_income_money"])
    gems = float(info["base_income_gems"])
    dark = float(info["base_income_dark"])
    parts = []
    if money > 0:
        parts.append(f"+{money}/s 💰")
    if gems > 0:
        parts.append(f"+{gems}/s 💎")
    if dark > 0:
        parts.append(f"+{dark}/s 🌑")
    if not parts:
        return "No income (???)"
    return ", ".join(parts)


def make_shop_detail_embed(user: dict, building_key: str) -> discord.Embed:
    info = BUILDINGS[building_key]
    owned = user["buildings"].get(building_key, 0)

    cost1 = _total_cost_for_qty(user, building_key, owned, 1)
    cost10 = _total_cost_for_qty(user, building_key, owned, 10)

    incomes = get_effective_incomes(user)

    embed = discord.Embed(
        title="🛒 GS Incremental Shop",
        color=EMBED_COLOR_MAIN,
    )

    embed.add_field(
        name="Selected Building",
        value=f"{info['emoji']} {info['label']}",
        inline=False,
    )
    embed.add_field(name="Owned", value=str(owned), inline=True)
    embed.add_field(
        name="Income (per building)",
        value=_format_income_line(info),
        inline=False,
    )

    embed.add_field(
        name="💰 Your Resources",
        value=f"{user['resources']:.0f}",
        inline=True,
    )
    embed.add_field(
        name="💎 Your Gems",
        value=f"{user.get('gems', 0.0):.0f}",
        inline=True,
    )
    embed.add_field(
        name="🌑 Your Dark Matter",
        value=f"{user.get('dark_matter', 0.0):.3f}",
        inline=True,
    )

    embed.add_field(name="Cost (Buy 1)", value=str(cost1), inline=True)
    embed.add_field(name="Cost (Buy 10)", value=str(cost10), inline=True)

    embed.add_field(
        name="Total Income/sec",
        value=(
            f"💰 {incomes['money']:.2f}/s | "
            f"💎 {incomes['gems']:.2f}/s | "
            f"🌑 {incomes['dark']:.4f}/s"
        ),
        inline=False,
    )
    embed.set_footer(
        text="Select a building from the menu, then use Buy 1 or Buy 10. (Only first 25 buildings shown due to Discord limits.)"
    )
    return embed


class ShopView(discord.ui.View):
    def __init__(self, user_id: int) -> None:
        super().__init__(timeout=300)
        self.user_id = user_id

        # Default selected building = first key
        self.current_key = next(iter(BUILDINGS.keys()))

        # Discord limit: max 25 options per select
        buildings_items = list(BUILDINGS.items())[:25]

        options = []
        for key, info in buildings_items:
            options.append(
                discord.SelectOption(
                    label=str(info["label"]),
                    value=key,
                    emoji=str(info["emoji"]),
                    description=f"Cost {info['base_cost']} | {_format_income_line(info)}",
                )
            )

        self.select = discord.ui.Select(
            placeholder="Select a building",
            options=options,
            min_values=1,
            max_values=1,
        )
        self.select.callback = self.select_callback
        self.add_item(self.select)

    async def select_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message(
                "❌ This shop GUI belongs to someone else.",
                ephemeral=True,
            )
            return

        self.current_key = self.select.values[0]
        user = get_or_create_user(interaction.user.id)
        embed = make_shop_detail_embed(user, self.current_key)
        await interaction.response.edit_message(embed=embed, view=self)

    async def _handle_buy(self, interaction: discord.Interaction, qty: int):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message(
                "❌ This shop GUI belongs to someone else.",
                ephemeral=True,
            )
            return

        user = get_or_create_user(interaction.user.id)
        key = self.current_key
        info = BUILDINGS[key]
        owned = user["buildings"].get(key, 0)
        total_cost = _total_cost_for_qty(user, key, owned, qty)

        if user["resources"] < total_cost:
            await interaction.response.send_message(
                f"❌ Not enough resources to buy {qty}x {info['label']}.\n"
                f"Need: {total_cost}, You have: {user['resources']:.0f}",
                ephemeral=True,
            )
            return

        user["resources"] -= total_cost
        user["buildings"][key] = owned + qty

        incomes = get_effective_incomes(user)
        user["income_per_sec"] = incomes["money"]
        user["gems_per_sec"] = incomes["gems"]
        user["dark_per_sec"] = incomes["dark"]

        from data.balance import update_multiplier
        update_multiplier(user)

        save_user(interaction.user.id, user)

        embed = make_shop_detail_embed(user, key)
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


class Shop(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="shop",
        description="Open a shop GUI to buy buildings.",
    )
    async def shop(self, interaction: discord.Interaction):
        user = get_or_create_user(interaction.user.id)
        default_key = next(iter(BUILDINGS.keys()))
        embed = make_shop_detail_embed(user, default_key)
        view = ShopView(interaction.user.id)
        await interaction.response.send_message(
            embed=embed,
            view=view,
            ephemeral=True,
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(Shop(bot))