import os
import discord
from discord.ext import commands, tasks
from discord import app_commands
from discord.app_commands import Choice
import sys
import asyncio
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, FileSystemEventHandler
import eloquentLoader
import bot
from dotenv import load_dotenv
load_dotenv()

observer = Observer()
saved_bot = None

async def get_file_names(directory_path):
    file_names = []
    for entry in os.listdir(directory_path):
        full_path = os.path.join(directory_path, entry)
        if os.path.isfile(full_path):
            file_names.append(entry)
    return file_names

async def loadAll():
    await eloquentLoader.loadAll()
    await eloquentLoader.hotReloader()

    files_in_directory = await get_file_names("cogs")
    for file_name in files_in_directory:
        if( "__pycache__" in file_name ):
            continue

        codeReader = open(f"cogs/{file_name}", "r")
        code = codeReader.read()
        codeReader.close()

        if( len(code) < 5 ):
            continue
    
        exec( code, globals(), globals() )

        await bot.controller.add_cog( globals()[ file_name.capitalize().split(".")[0] ](bot.controller) )
        print(f"Loaded {file_name}")


async def reloadCog(path):
    if "cogs/" not in path or "__pycache__" in path:
        return

    codeReader = open(path, "r")
    code = codeReader.read()
    codeReader.close()

    file_name = path.split("/")[-1]
    cog_name = file_name.capitalize().split(".")[0]

    #cog_names = list(bot.controller.cogs.keys())
    #print("Loaded Cogs:", cog_names)

    print(f"Reloading {cog_name}...")

    await bot.controller.remove_cog(cog_name)
    await bot.controller.remove_cog(cog_name.lower())

    guild = discord.Object(id=os.environ.get('discord_guild'))

    bot.controller.tree.clear_commands(guild=guild)

    globals().pop(cog_name, None)
    globals().pop(cog_name.lower(), None)

    exec(code, globals(), globals())
    await bot.controller.add_cog(globals()[cog_name](bot.controller))

    bot.controller.tree.copy_global_to(guild=guild)
    await bot.controller.tree.sync(guild=guild)

    print(f"Reloaded {cog_name}")



class ChangeHandler(FileSystemEventHandler):
    def __init__(self, loop):
        self.loop = loop

    def on_modified(self, event):
        if not event.is_directory:
            self.loop.create_task(reloadCog(event.src_path))

    def on_created(self, event):
        if not event.is_directory:
            self.loop.create_task(reloadCog(event.src_path))


async def hotReloader():
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    loop = asyncio.get_running_loop()

    event_handler = ChangeHandler(loop)

    observer.schedule(event_handler, path, recursive=True)
    observer.start()
