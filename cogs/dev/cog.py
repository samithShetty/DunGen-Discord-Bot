from discord.ext import commands

from global_utils.load_cogs import load_all_cogs
from global_utils.types import Context


class DevCog(commands.Cog):
    """Cog for development and testing commands"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command()
    async def clear(self, ctx: Context):
        """Clears all slash commands from app commands tree"""
        ctx.bot.tree.clear_commands(guild=None)
        await ctx.bot.tree.sync(guild=None)
        await ctx.reply("Cleared all bot commands from App Tree")

    @commands.hybrid_command()
    async def sync(self, ctx: Context):
        """Syncs slash commands in app commands tree"""
        print(f"Invoked Sync command in guild: {ctx.guild=}")
        print(ctx.bot.tree.get_commands(guild=ctx.guild))
        synced = await ctx.bot.tree.sync(guild=None)
        await ctx.reply(f"Synced {len(synced)} commands.")
        print(f"Synced the following commands: {[cmd.name for cmd in synced]}")

    @commands.hybrid_command(aliases=["reload"])
    async def reload_cogs(self, ctx: Context):
        """A simple slash command demo"""
        reloaded_cogs = await load_all_cogs(self.bot, reload=True)
        if reloaded_cogs:
            await ctx.reply(f"Reloaded Cogs: {', '.join(reloaded_cogs)}")
        else:
            await ctx.reply("Error Occured. No Cogs were reloaded.")


async def setup(bot: commands.Bot):
    """Entry point for loading the module"""
    await bot.add_cog(DevCog(bot))
    print("Loaded DevCog")
