import os
import sys
import asyncio
import time
import logging
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


def get_file_names(directory_path):
    file_names = []
    for entry in os.listdir(directory_path):
        full_path = os.path.join(directory_path, entry)
        if os.path.isfile(full_path):
            file_names.append(entry)
    return file_names


def loadAll():
    files_in_directory = get_file_names("migrations")

    migratedReader = open(f"migrated", "r")
    migrations = migratedReader.read()
    migratedReader.close()

    migratedAppender = open(f"migrated", "a")

    for file_name in files_in_directory:
        if( "__pycache__" in file_name ):
            continue
        if( ".sql" not in file_name ):
            continue
        if( f"/{file_name}-" in migrations ):
            continue

        codeReader = open(f"migrations/{file_name}", "r")
        code = codeReader.read()
        codeReader.close()

        if( len(code) < 3 ):
            continue
        try:
            db.statement(code)

            migratedAppender.write(f"/{file_name}-\n")

            print(f"+Migration {file_name}")
        except Exception as e:
            print(f"Failed migration {file_name}")


    migratedAppender.close()

loadAll()