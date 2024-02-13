import sys
import uvicorn

from app import app

from utils.config import Settings

HOST = Settings.get_env("APP_HOST")
PORT = Settings.get_env("APP_PORT", int)
DEBUG = Settings.get_env("APP_DEBUG", bool)

def handle(args):
    if len(args) <= 1:
        print("No command provided exiting...")
        return None
    
    cmd = sys.argv[1]

    match (cmd):
        case "start":
            uvicorn.run("manage:app", host=HOST, port=PORT, reload=DEBUG)

        case _:
            print("No command provided exiting...")

handle(sys.argv)
