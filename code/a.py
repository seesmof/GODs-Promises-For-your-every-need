import os
import json
import img2pdf
from rich.console import Console
from rich.traceback import install

install()
console = Console()

currentDir = os.path.dirname(os.path.abspath(__file__))
missingPagesPath = os.path.join(currentDir, "blankPages.txt")
pagesDir = os.path.join(currentDir, "..", "pages")
genericName = "GODs_Promises_For_your_every_need"
pdfOutputPath = os.path.join(currentDir, "..", f"{genericName}.pdf")


def loadBlankPages():
    try:
        with open(missingPagesPath, "r") as f:
            res = [int(line.strip()) for line in f.readlines() if line.strip()]
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


def formPdf():
    with open(pdfOutputPath, "wb") as f:
        allImageFiles = [os.path.join(pagesDir, file) for file in fileNames]
        convertedImages = img2pdf.convert(allImageFiles)
        f.write(convertedImages)
    console.print(f"[green bold]Finished forming PDF file[/green bold]")


def checkPages():
    leastPage = int(fileNames[0].split(".")[0])
    mostPage = int(fileNames[-1].split(".")[0])

    blankPages = loadBlankPages()
    console.print(f"Blank pages: {blankPages}")
    missingPages = []

    for i in range(leastPage, mostPage + 1):
        if not os.path.exists(os.path.join(pagesDir, f"{i}.jpg")):
            if i not in blankPages:
                missingPages.append(i)
                console.print(f"[red bold]Page {i} not found[/red bold]")

    if not missingPages:
        console.print("[green bold]All pages found![/green bold]")

    currentDir = os.path.dirname(os.path.abspath(__file__))
    resultsPath = os.path.join(currentDir, "missingPages.json")

    with open(resultsPath, "w", encoding="utf-8") as f:
        json.dump(missingPages, f, indent=2)


def reformatFileNames():
    for file in os.listdir(pagesDir):
        if file.endswith(".jpg"):
            name = file.split(".")[0]
            newName = int(name) + ".jpg"
            os.rename(os.path.join(pagesDir, file), os.path.join(pagesDir, newName))
    readFileNames()


reformatFileNames()
