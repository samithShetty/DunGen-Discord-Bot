import asyncio

import discord
from discord.ext import commands

from config import DISCORD_TOKEN
from global_utils.load_cogs import load_all_cogs
from global_utils.types import Context

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.messages = True

bot = commands.Bot(command_prefix=">", intents=intents)


@bot.event
async def on_ready():
    """Run on Bot startup"""
    print(f"Logged on as {bot.user}!")


@bot.hybrid_command()
async def ping(ctx: Context):
    """Ping bot to check responsiveness"""
    print("Ping command invoked")
    await ctx.reply("Pong!")


async def main():
    """Main entry point for starting the bot"""
    await load_all_cogs(bot)
    await bot.start(DISCORD_TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
