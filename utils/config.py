import os

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

# Load the default config path
Settings.load_env()