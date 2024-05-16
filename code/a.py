import os
import json
from rich.console import Console
from rich.traceback import install

install()
console = Console()

currentDir = os.path.dirname(os.path.abspath(__file__))
missingPagesPath = os.path.join(currentDir, "missingPages.txt")
pagesDir = os.path.join(currentDir, "..", "pages")


def loadMissingPages():
    try:
        with open(missingPagesPath, "r") as f:
            res = [line.strip() for line in f.readlines() if line.strip()]
    except:
        res = []
    return res


def loadFileNames():
    try:
        with open(fileNamesPath, "r", encoding="utf-8") as f:
            fileNames = json.load(f)
    except:
        fileNames = []
    return fileNames


def saveFileNames(fileNames):
    with open(fileNamesPath, "w", encoding="utf-8") as f:
        json.dump(fileNames, f, indent=2)


fileNamesPath = os.path.join(currentDir, "fileNames.json")
fileNames = loadFileNames()


def readFileNames():
    fileNames
    for file in os.listdir(pagesDir):
        if file.endswith(".jpg"):
            console.print(f"Reading '{file}'")
            fileNames.append(file)
    fileNames.sort(key=lambda x: int(x.split(".")[0]))
    saveFileNames(fileNames)


def cleanFileNames():
    for file in os.listdir(pagesDir):
        if file.endswith(".jpg"):
            name = file.split(".")[0]
            num = name.split("_")[-1]
            os.rename(
                os.path.join(pagesDir, file), os.path.join(pagesDir, f"{num}.jpg")
            )


def removeExcessZeros():
    for file in os.listdir(pagesDir):
        if file.endswith(".jpg"):
            name = file.split(".")[0]
            newName = name[1:] + ".jpg"
            console.print(f"Renaming '{file}' to '{newName}'")
            os.rename(os.path.join(pagesDir, file), os.path.join(pagesDir, newName))
