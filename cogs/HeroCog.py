import importlib

import discord
from discord.ext import commands
from discord.ext.commands import Cog, Context

from models import Hero
from mongo import get_heroes_for_user


class HeroCog(Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._last_member = None

    @commands.hybrid_command(aliases=["heroes", "lh"])
    async def list_heroes(self, ctx: Context, *, user: discord.Member = None, index=1):
        user = user or ctx.author
        hero_menu = _create_hero_menu_for_user(user, index)

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
        new_hero_menu = _create_hero_menu_for_user(
            user=player,
            hero_index=old_hero_index + reaction_options[reaction.emoji],
        )
        await reaction.remove(player)
        await message.edit(embed=new_hero_menu)

    async def cog_unload(self):
        return await super().cog_unload()


def _create_hero_embed(hero: Hero) -> discord.Embed:
    hero_embed = discord.Embed(
        title=hero.name,
        description=f"*Level {hero.level} Hero*",
        color=discord.Color(0x102A45),
    )

    padding = "\u200b " * 5
    hero_embed.add_field(name=f"MAX HP {padding}", value=hero.stats.MAX_HP)
    hero_embed.add_field(name=f"ATTACK {padding}", value=hero.stats.ATK)
    hero_embed.add_field(name=f"DEFENSE {padding}", value=hero.stats.DEF)
    hero_embed.add_field(name=f"SPEED {padding}", value=hero.stats.SPD)
    hero_embed.add_field(name=f"EVASION {padding}", value=hero.stats.EVA)

    return hero_embed


def _create_hero_menu_for_user(user: discord.Member, hero_index: int) -> discord.Embed:
    owned_heroes = get_heroes_for_user(user.id)

    if len(owned_heroes) == 0:
        return discord.Embed(description=f"User has no Heroes in their party...")
    true_index = (hero_index - 1) % len(owned_heroes)
    hero_embed = _create_hero_embed(owned_heroes[true_index])
    hero_embed.set_author(
        name=f"{user.display_name}'s Party - {true_index+1}/{len(owned_heroes)}",
        icon_url=user.avatar.url,
    )
    hero_embed.set_footer(text=f"Player ID: {user.id}")
    return hero_embed


async def setup(bot: commands.Bot):
    await bot.add_cog(HeroCog(bot))
    print("Added HeroCog")
