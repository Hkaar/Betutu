import uvicorn

from utils.config import Settings

HOST = Settings.get_env("APP_HOST")
PORT = Settings.get_env("APP_PORT", int)
DEBUG = Settings.get_env("APP_DEBUG", bool)

class Commands:
    def __init__(self, console):
        self.console = console

        self.console.register("start", self.start)
        self.console.register("up", self.up)
        self.console.register("down", self.down)

    def start(self):
        uvicorn.run("manage:app", host=HOST, port=PORT, reload=DEBUG)

    def up(self):
        Settings.set_state("app", "status", True)

    def down(self):
        Settings.set_state("app", "status", False)