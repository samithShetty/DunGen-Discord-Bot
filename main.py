from config import BOT_TOKEN
import discord
from discord.ext import commands
from cogs.HeroCog import HeroCog

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged on as {bot.user}!')

@bot.command()
async def ping(ctx):
    print('Ping command invoked')
    await ctx.reply('Pong!')

@bot.hybrid_command()
async def sync(ctx):
    """Syncs slash commands in app commands tree"""
    synced = await ctx.bot.tree.sync()
    await ctx.reply(f'Synced {len(synced)} commands.')

@bot.hybrid_command()
async def load_cog(ctx):
    """A simple slash command demo"""
    await bot.remove_cog('HeroCog')
    await bot.add_cog(HeroCog(bot))
    print(bot.cogs)
    await ctx.reply('HeroCog loaded!')

bot.run(BOT_TOKEN)
