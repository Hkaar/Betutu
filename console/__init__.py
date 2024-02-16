import pkgutil
import importlib

from typing import Callable
from functools import cache
from inspect import signature

from utils.config import Settings

INCLUDE = Settings.get_env("CONSOLE_INCLUDE", tuple)

class Console:
    _commands = {}

    @classmethod
    @cache
    def exec(cls, name: str, *args):
        if name in cls._commands:
            cmd = cls._commands[name]

            param_amount = signature(cmd).parameters

            if len(param_amount) < len(args):
                raise TypeError(f"Too many arguments provided when executing {name}!")
            
            cmd(*args)
        else:
            raise KeyError(f"Command {name} does not exist!")

    @classmethod
    def register(cls, name: str, handler: Callable):
        cls._commands[name] = handler

    @classmethod
    def autoimport(cls):
        path = __path__

        for (_, module_name, _) in pkgutil.iter_modules(path):
            if not module_name.startswith("__") and (module_name in INCLUDE or INCLUDE[0] == "*"):
                module = importlib.import_module(f".{module_name}", package="console")
                
                if hasattr(module, "Commands"):
                    module.Commands(Console)

# Auto import all the included commands
Console.autoimport()
