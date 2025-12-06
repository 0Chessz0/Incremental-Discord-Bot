import discord
from discord.ext import commands

from config import get_token

COGS = [
    "commands.stats",
    "commands.click",
    "commands.shop",
    "commands.boost",
    "commands.reincarnate",
    "commands.upgrades",
    "commands.darklab",
]


class GSIncrementalBot(commands.Bot):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self) -> None:
        for ext in COGS:
            await self.load_extension(ext)
        await self.tree.sync()
        print(f"Synced {len(self.tree.get_commands())} slash commands.")


bot = GSIncrementalBot()


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")


def main():
    token = get_token()
    if not token:
        print(
            "wrong"
        )
        return

    bot.run(token)


if __name__ == "__main__":
    main()