import asyncio
import os

import discord
from discord.ext import commands

from cogs.HeroCog import HeroCog
from config import DISCORD_TOKEN

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.messages = True

bot = commands.Bot(command_prefix=">", intents=intents)


@bot.event
async def on_ready():
    print(f"Logged on as {bot.user}!")


@bot.command()
async def ping(ctx):
    print("Ping command invoked")
    await ctx.reply("Pong!")


@bot.command()
async def clear(self, ctx):
    await self.bot.tree.clear_commands()
    await ctx.reply(f"Cleared all bot commands from App Tree")


@bot.hybrid_command()
async def sync(ctx):
    """Syncs slash commands in app commands tree"""
    synced = await ctx.bot.tree.sync()
    await ctx.reply(f"Synced {len(synced)} commands.")
    print(f"Synced the following commands: {[cmd.name for cmd in synced]}")


@bot.hybrid_command(aliases=["reload"])
async def reload_cogs(ctx):
    """A simple slash command demo"""
    await bot.reload_extension(f"cogs.HeroCog")
    await ctx.reply("HeroCog reloaded!")


async def main():
    # Automatically load all the cogs on startup
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")
            except Exception as e:
                print(f"Error loading cog {filename}:\n{e}")
    await bot.start(DISCORD_TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
