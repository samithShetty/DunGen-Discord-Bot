import importlib

import discord
from discord.ext import commands

from cogs.hero import utils
from cogs.hero.utils import (
    create_hero_menu_for_user,
    get_hero_index_from_embed,
    get_player_id_from_embed,
)


class HeroCog(commands.Cog):
    """Module for displaying and managing Hero data"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._last_member = None

    @commands.hybrid_command(aliases=["heroes", "lh"])
    async def list_heroes(
        self,
        ctx: commands.Context[commands.Bot],
        user: discord.Member | discord.User | None = None,
        index: int = 1,
    ):
        """Creates a scrollable menu of all heroes owned by a user"""
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
        Hero Menu Handler
        When users react with arrows on a hero menu it will grab the next hero and update the embed
        """
        reaction_options = {"◀️": -1, "▶️": 1}
        message = reaction.message
        # TODO: Fix/Update this check when the bot has other embeds/menus
        if (
            message.author.id != self.bot.application_id
            or len(message.embeds) == 0
            or user.id == self.bot.application_id
            or reaction.emoji not in reaction_options
        ):
            return

        old_hero_menu = message.embeds[0]
        # e.g. Embed Author Field --> "@[User]'s Party - [index]/[total_heroes]"
        old_hero_index = get_hero_index_from_embed(old_hero_menu)
        # e.g. Embed Footer --> "Player ID: [user_id]"
        player_id = get_player_id_from_embed(old_hero_menu)
        player = user.guild.get_member(player_id)
        if player is None:
            raise ValueError("Unable to find player in guild with ID {player_id}")

        new_hero_menu = create_hero_menu_for_user(
            user=player,
            hero_index=old_hero_index + reaction_options[str(reaction.emoji)],
        )
        await reaction.remove(player)
        await message.edit(embed=new_hero_menu)

    @commands.Cog.listener()
    async def cog_unload(self):
        importlib.reload(utils)
        return await super().cog_unload()


async def setup(bot: commands.Bot):
    """Entry point for adding the HeroCog to the bot"""
    await bot.add_cog(HeroCog(bot))
    print("Added HeroCog")
