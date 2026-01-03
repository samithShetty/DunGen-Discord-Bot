import asyncio
import os
from typing import List

import discord
from discord.ext import commands

from config import DISCORD_TOKEN
from utils.types import Context

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


@bot.command()
async def clear(ctx: Context):
    """Clears all slash commands from app commands tree"""
    ctx.bot.tree.clear_commands(guild=ctx.guild)
    await ctx.bot.tree.sync(guild=ctx.guild)
    await ctx.reply("Cleared all bot commands from App Tree")


@bot.hybrid_command()
async def sync(ctx: Context):
    """Syncs slash commands in app commands tree"""
    synced = await ctx.bot.tree.sync(guild=ctx.guild)
    await ctx.reply(f"Synced {len(synced)} commands.")
    print(f"Synced the following commands: {[cmd.name for cmd in synced]}")


@bot.hybrid_command(aliases=["reload"])
async def reload_cogs(ctx: Context):
    """A simple slash command demo"""
    reloaded_cogs = await _load_all_cogs(reload=True)

    if reloaded_cogs:
        await ctx.reply(f"Reloaded Cogs: {', '.join(reloaded_cogs)}")
    else:
        await ctx.reply("Error Occured. No Cogs were reloaded.")


async def _load_all_cogs(reload: bool = False) -> List[str]:
    """Automatically (re)loads all of the cogs in the cog directory"""
    loaded_cogs: List[str] = []
    for module in os.listdir("./cogs"):
        if not module.startswith("__"):
            try:
                if reload:
                    await bot.reload_extension(f"cogs.{module}.cog")
                else:
                    await bot.load_extension(f"cogs.{module}.cog")
                loaded_cogs.append(module)
            except Exception as e:  # pylint: disable=broad-exception-caught
                print(f"Error loading cog from {module} module:\n{e}")
    return loaded_cogs


async def main():  # pylint: disable=missing-function-docstring
    await _load_all_cogs()
    await bot.start(DISCORD_TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
