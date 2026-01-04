import discord

from models import Hero
from mongo import get_heroes_for_user


def create_hero_embed(hero: Hero) -> discord.Embed:
    """Contructs the basic Embed for displaying a Hero's Stats"""
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


def create_hero_menu_for_user(
    user: discord.Member | discord.User, hero_index: int
) -> discord.Embed:
    """
    Creates a Hero Embed with extra context and information on the owning player.
    For use in scrollable Hero Menus in list_hero
    """
    owned_heroes = get_heroes_for_user(user.id)
    print("t2")
    if len(owned_heroes) == 0:
        return discord.Embed(description="User has no Heroes in their party...")

    true_index = (hero_index - 1) % len(owned_heroes)
    hero_embed = create_hero_embed(owned_heroes[true_index])
    hero_embed.set_author(
        name=f"{user.display_name}'s Party - {true_index+1}/{len(owned_heroes)}",
        icon_url=user.display_avatar.url,
    )
    hero_embed.set_footer(text=f"Player ID: {user.id}")
    return hero_embed


def get_hero_index_from_embed(embed: discord.Embed) -> int:
    """
    Parses the current selected index of a list_hero menu from the author field
    Embed Author Name: '@[User.name]'s Party - [index]/[total_heroes]'
    """
    if embed.author.name is None:
        raise ValueError("Embed has no Author Name. Unable to parse hero index.")
    return int(embed.author.name.split(" - ")[1].split("/")[0])


def get_player_id_from_embed(embed: discord.Embed) -> int:
    """
    Parses the player ID from the footer of a list_hero menu
    Embed Footer Format: 'Player ID: [user_id]'
    """
    if embed.footer.text is None:
        raise ValueError("Embed has no Footer Text. Unable to parse player ID.")
    return int(embed.footer.text.split(": ")[1])
