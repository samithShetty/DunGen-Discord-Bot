import importlib

import discord
from discord.ext import commands
from discord.ext.commands import Cog, Context

from cogs.hero.utils import create_hero_menu_for_user
from models import Hero
from mongo import get_heroes_for_user


class HeroCog(Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._last_member = None

    @commands.hybrid_command(aliases=["heroes", "lh"])
    async def list_heroes(self, ctx: Context, *, user: discord.Member = None, index=1):
        user = user or ctx.author
        hero_menu = create_hero_menu_for_user(user, index)

        message = await ctx.reply(embed=hero_menu)
        await message.add_reaction("◀️")
        await message.add_reaction("▶️")
        print(f"Listed Heroes for User: {user.display_name=}")
        return message

    @commands.Cog.listener()
    async def on_reaction_add(
        self, reaction: discord.Reaction, user: discord.Member
    ) -> None:
        """
        Hero Menu Handler. Fetches new heroes and updates the embed when users react with arrows
        """
        reaction_options = {"◀️": -1, "▶️": 1}
        message = reaction.message
        # TODO: Fix/Update this check when the bot has other embeds/menus
        if (
            message.author.id != self.bot.application_id
            or len(message.embeds) == 0
            or user.id == self.bot.application_id
            or reaction.emoji not in reaction_options.keys()
        ):
            print("hit guard")
            return

        old_hero_menu = message.embeds[0]
        # e.g. Embed Author Field --> "@[User]'s Party - [index]/[total_heroes]"
        old_hero_index = int(old_hero_menu.author.name.split(" - ")[1].split("/")[0])
        # e.g. Embed Footer --> "Player ID: [user_id]"
        player_id = int(old_hero_menu.footer.text.split(": ")[1])
        player = user.guild.get_member(player_id)
        new_hero_menu = create_hero_menu_for_user(
            user=player,
            hero_index=old_hero_index + reaction_options[reaction.emoji],
        )
        await reaction.remove(player)
        await message.edit(embed=new_hero_menu)

    async def cog_unload(self):
        return await super().cog_unload()


async def setup(bot: commands.Bot):
    await bot.add_cog(HeroCog(bot))
    print("Added HeroCog")
