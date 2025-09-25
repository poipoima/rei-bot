import os
import discord
from discord.ext import commands
import cogsLoader
from dotenv import load_dotenv
load_dotenv()

intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    await cogsLoader.loadAll( bot )
    await cogsLoader.hotReloader()

    guild = discord.Object(id=os.environ.get('guild'))
    #bot.tree.copy_global_to(guild=guild)

    await bot.tree.sync(guild=guild)
    await bot.tree.sync()

    print(f'We have logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

bot.run( os.environ.get('token') )
