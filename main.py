import os
import discord
from discord.ext import commands
import cogsLoader
import bot
from dotenv import load_dotenv
load_dotenv()


@bot.controller.event
async def on_ready():
    await cogsLoader.loadAll()
    await cogsLoader.hotReloader()


    guild = discord.Object(id=os.environ.get('discord_guild'))
    bot.controller.tree.copy_global_to(guild=guild)

    await bot.controller.tree.sync(guild=guild)
    #await bot.tree.sync()

    print(f'We have logged in as {bot.controller.user}')

@bot.controller.event
async def on_message(message):
    if message.author == bot.controller.user:
        return

bot.controller.run( os.environ.get('discord_token') )
