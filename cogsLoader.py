import os
import discord
from discord.ext import commands, tasks
from discord import app_commands
import sys
import asyncio
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, FileSystemEventHandler

observer = Observer()
saved_bot = None

async def get_file_names(directory_path):
    file_names = []
    for entry in os.listdir(directory_path):
        full_path = os.path.join(directory_path, entry)
        if os.path.isfile(full_path):
            file_names.append(entry)
    return file_names

async def loadAll( bot ):
    global saved_bot
    saved_bot = bot

    files_in_directory = await get_file_names("cogs")
    for file_name in files_in_directory:
        codeReader = open(f"cogs/{file_name}", "r")
        code = codeReader.read()
        codeReader.close()

        if( len(code) < 5 ):
            continue
    
        exec( code, globals(), globals() )

        await bot.add_cog( globals()[ file_name.capitalize().split(".")[0] ](bot) )
        print(f"Loaded {file_name}")



async def reloadCog( path ):
    if( "cogs/" in path ):
        codeReader = open(path, "r")
        code = codeReader.read()
        codeReader.close()

        file_name = path.split("/")[-1]

        if( len(code) < 5 ):
            return

        await saved_bot.remove_cog( file_name.capitalize().split(".")[0] )
        del globals()[ file_name.capitalize().split(".")[0] ]
    
        exec( code, globals(), globals() )
        
        await saved_bot.add_cog( globals()[ file_name.capitalize().split(".")[0] ](saved_bot) )
        print(f"Reloaded {file_name}")


class ChangeHandler(FileSystemEventHandler):
    def __init__(self, loop):
        self.loop = loop

    def on_modified(self, event):
        if not event.is_directory:
            self.loop.create_task(reloadCog(event.src_path))

    def on_created(self, event):
        return

async def hotReloader():
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    loop = asyncio.get_running_loop()

    event_handler = ChangeHandler(loop)

    observer.schedule(event_handler, path, recursive=True)
    observer.start()
