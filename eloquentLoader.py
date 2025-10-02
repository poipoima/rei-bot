import os
import sys
import asyncio
import time
import logging
import bot
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, FileSystemEventHandler
from orator import DatabaseManager, Model
from dotenv import load_dotenv
load_dotenv()

observer = Observer()

config = {
    'mysql': {
        'driver': os.environ.get('db_driver'),
        'host': os.environ.get('db_host'),
        'database': os.environ.get('db_database'),
        'user': os.environ.get('db_user'),
        'password': os.environ.get('db_password'),
        'prefix': ''
    }
}

db = DatabaseManager(config)
Model.set_connection_resolver(db)


async def get_file_names(directory_path):
    file_names = []
    for entry in os.listdir(directory_path):
        full_path = os.path.join(directory_path, entry)
        if os.path.isfile(full_path):
            file_names.append(entry)
    return file_names

def get_file_names_sync(directory_path):
    file_names = []
    for entry in os.listdir(directory_path):
        full_path = os.path.join(directory_path, entry)
        if os.path.isfile(full_path):
            file_names.append(entry)
    return file_names
    

async def loadAll():
    files_in_directory = await get_file_names("models")
    for file_name in files_in_directory:
        if( "__pycache__" in file_name ):
            continue

        codeReader = open(f"models/{file_name}", "r")
        code = codeReader.read()
        codeReader.close()

        if( len(code) < 5 ):
            continue
    
        exec( code, globals(), globals() )

        print(f"+Model {file_name}")


def getModelsList():
    files_in_directory = get_file_names_sync("models")
    models = []
    for file_name in files_in_directory:
        if( "__pycache__" in file_name ):
            continue
        
        models.append( file_name.split(".")[0] )

    return models

async def reloadModel( path ):
    if( "models/" in path ):
        if( "__pycache__" in path ):
            return

        codeReader = open(path, "r")
        code = codeReader.read()
        codeReader.close()

        file_name = path.split("/")[-1]

        if( len(code) < 5 ):
            return

        del globals()[ file_name.capitalize().split(".")[0] ]
    
        exec( code, globals(), globals() )
        
        print(f"Model reloaded {file_name}")


class ChangeHandler(FileSystemEventHandler):
    def __init__(self, loop):
        self.loop = loop

    def on_modified(self, event):
        if not event.is_directory:
            self.loop.create_task(reloadModel(event.src_path))

    def on_created(self, event):
        return

async def hotReloader():
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    loop = asyncio.get_running_loop()

    event_handler = ChangeHandler(loop)

    observer.schedule(event_handler, path, recursive=True)
    observer.start()
