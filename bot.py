import os
import discord
from discord.ext import commands
import cogsLoader
from dotenv import load_dotenv

intents = discord.Intents.all()
intents.message_content = True

controller = commands.Bot(command_prefix='!', intents=intents)