import os
import json
from rich.console import Console
from rich.traceback import install

install()
console = Console()

currentDir = os.path.dirname(os.path.abspath(__file__))
missingPagesPath = os.path.join(currentDir, "missingPages.txt")


def loadMissingPages():
    try:
        with open(missingPagesPath, "r") as f:
            res = [line.strip() for line in f.readlines() if line.strip()]
    except:
        res = []
    return res
