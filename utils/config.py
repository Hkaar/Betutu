import os
import json

from typing import Any

from dotenv import load_dotenv
from functools import cache

class Settings:
    @staticmethod
    @cache
    def get_env(key: str, type = None):
        if type == bool:
            if os.getenv(key).upper() == "TRUE":
                return True
            
            return False
        
        elif type:
            try:
                return type(os.getenv(key))
            
            except TypeError:
                return TypeError(
                    f"Value for environment variable {key} cannot be converted to {type}!"
                )
            
        return os.getenv(key)
    
    @staticmethod
    @cache
    def load_env(path: str = "config.env"):
        load_dotenv(path)

    @staticmethod
    def get_state(root: str, key: str, path: str = "state.json"):
        with open(path, "r") as f:
            try:
                data = json.load(f)
                
            except json.JSONDecodeError as e:
                raise ValueError(f"Error decoding JSON in {path}: {e}")

        if root not in data:
            raise KeyError(f"Root state of {root} does not exist!")
        
        if key not in data[root]:
            raise KeyError(f"State {key} does not exist within root state {root}!")
        
        return data[root][key]
    
    @staticmethod
    @cache
    def set_state(root: str, key: str, value: Any, path: str = "state.json"):
        with open(path, "r") as f:
            try:
                data = json.load(f)
                
            except json.JSONDecodeError as e:
                raise ValueError(f"Error decoding JSON in {path}: {e}")

        if root not in data:
            raise KeyError(f"Root state of {root} does not exist!")
        
        if key not in data[root]:
            raise KeyError(f"State {key} does not exist within root state {root}!")
        
        data[root][key] = value

        with open(path, "w") as f:
            json.dump(data, f, indent=4)

        return True

# Load the default config path
Settings.load_env()