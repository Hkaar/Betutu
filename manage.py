import sys

from app import app
from console import Console

def handle(args: list):
    if len(args) <= 1:
        print("No command provided exiting...")
        return 
    
    Console.exec(args[1], *args[2:])

if __name__ == "__main__":
    handle(sys.argv)
