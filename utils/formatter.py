import discord

from .constants import EMBED_COLOR_MAIN
from data.balance import BUILDINGS


def format_buildings_short(user) -> str:
    buildings = user.get("buildings", {})
    total = sum(buildings.values())
    if total == 0:
        return "0"

    parts = []
    for key, count in buildings.items():
        if count <= 0:
            continue
        info = BUILDINGS.get(key)
        if not info:
            continue
        parts.append(f"{info['emoji']} {info['label']} x{count}")
    shown = parts[:6]
    if len(parts) > 6:
        shown.append(f"...+{len(parts) - 6} more")
    return "\n".join(shown)


def make_start_embed() -> discord.Embed:
    embed = discord.Embed(
        title="🕹 Game Started!",
        description="Your session has been initialized!",
        color=EMBED_COLOR_MAIN,
    )
    embed.add_field(name="💰 Starting Resources", value="0", inline=True)
    embed.add_field(name="⚡ Starting Income", value="0/s", inline=True)
    embed.add_field(name="📈 Multiplier", value="x1.00", inline=True)
    embed.set_footer(
        text="Use /stats to check your progress, /shop to buy buildings, /upgrades for gem upgrades, /darklab for dark upgrades!"
    )
    return embed


def make_stats_embed(member: discord.abc.User, user: dict) -> discord.Embed:
    embed = discord.Embed(
        title=f"📊 Statistics of {member.name}",
        color=EMBED_COLOR_MAIN,
    )
    if member.display_avatar:
        embed.set_thumbnail(url=member.display_avatar.url)

    embed.add_field(
        name="💰 Resources",
        value=f"{user['resources']:.0f} ( +{user.get('income_per_sec', 0.0):.2f}/s )",
        inline=False,
    )
    embed.add_field(
        name="💎 Gems",
        value=f"{user.get('gems', 0.0):.0f} ( +{user.get('gems_per_sec', 0.0):.2f}/s )",
        inline=False,
    )
    embed.add_field(
        name="🌑 Dark Matter",
        value=f"{user.get('dark_matter', 0.0):.3f} ( +{user.get('dark_per_sec', 0.0):.4f}/s )",
        inline=False,
    )

    embed.add_field(
        name="📈 Cash Multiplier",
        value=f"x{user.get('multiplier', 1.0):.2f}",
        inline=True,
    )
    embed.add_field(
        name="🖱 Total Clicks",
        value=str(user.get("total_clicks", 0)),
        inline=True,
    )
    embed.add_field(
        name="🔁 Reincarnations",
        value=str(user.get("reincarnations", 0)),
        inline=True,
    )

    r_points = user.get("reincarnation_points", 0)
    gem_upgrades = user.get("gem_upgrades", {})
    dark_upgrades = user.get("dark_upgrades", {})
    gem_levels = sum(gem_upgrades.values())
    dark_levels = sum(dark_upgrades.values())

    embed.add_field(
        name="✨ Reincarnation Points",
        value=str(r_points),
        inline=True,
    )
    embed.add_field(
        name="💎 Gem Upgrades (total levels)",
        value=str(gem_levels),
        inline=True,
    )
    embed.add_field(
        name="🌑 Dark Upgrades (total levels)",
        value=str(dark_levels),
        inline=True,
    )

    embed.add_field(
        name="🏛 Buildings",
        value=format_buildings_short(user),
        inline=False,
    )

    embed.set_footer(text=f"Level: {user.get('level', 1)}")
    return embed


def make_click_embed(user: dict) -> discord.Embed:
    embed = discord.Embed(
        title="🖱 Clicker",
        description="Press the button below to earn resources.",
        color=EMBED_COLOR_MAIN,
    )
    embed.add_field(
        name="💰 Your Resources",
        value=f"{user['resources']:.0f}",
        inline=False,
    )
    return embed