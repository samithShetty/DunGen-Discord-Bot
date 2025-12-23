from config import BOT_TOKEN
import discord
from discord.ext import commands

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
async def slash_demo(ctx):
    """A simple slash command demo"""
    await ctx.reply('This is a slash command response!')

bot.run(BOT_TOKEN)
