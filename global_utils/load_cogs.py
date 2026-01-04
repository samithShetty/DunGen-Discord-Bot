import os
from typing import List

from discord.ext import commands


async def load_all_cogs(bot: commands.Bot, reload: bool = False) -> List[str]:
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
