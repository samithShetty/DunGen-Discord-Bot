import discord
from config import BOT_TOKEN

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print(f'Logged on as {bot.user}!')

@bot.event
async def on_message(message: discord.Message):
    print(f'Message from {message.author}: {message.content}')
    if message.author == bot.user:
        return
    
    if message.content == "arise":
        await message.channel.send("https://media.discordapp.net/attachments/648637142666444840/999212583020146698/TV_wake.gif?ex=694a413c&is=6948efbc&hm=851956e0af8fde60551806115bcd9d23cc256a6f3b3a33030c8f1b5e96f0607a&")

bot.run(BOT_TOKEN)
