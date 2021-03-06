import os
import shutil
import subprocess

from helpers.config import getConfig

def getBytesFromFile(file):
    inFile = open(file, "rb")
    result = inFile.read()
    inFile.close()
    return result


def createBoilerplate(problemName):
    from helpers.programSelector import formatCommand, guessLanguage, formatProgramFile
    cfg = getConfig()
    lang = cfg.get("kat", "language")
    if lang in cfg["Initialize commands"]:
        cmd = cfg["Initialize commands"].getcommand(lang)
        subprocess.run([p for p in cmd], cwd=problemName)
        return
    directory = os.path.dirname(os.path.realpath(__file__)) + "/../boilerplate"
    boilerplates = {
        guessLanguage(formatProgramFile(f)): f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))
    }
    if lang in boilerplates:
        boilerplate = boilerplates[lang]
        fileType = "." + boilerplates[lang].split(".")[-1]
        shutil.copy2(
            directory + "/" + boilerplate,
            problemName + "/" + problemName + fileType,
        )
    else:
        fileType = [file for (file, k) in cfg["File associations"].items() if k.lower() == lang.lower()]
        open(problemName + "/" + problemName + fileType[0], "a").close()


def findProblemLocation(problemName):
    folders = [".archive/", ".solved/", ""]
    for folder in folders:
        if os.path.exists(folder + problemName):
            return folder
    return None


def undoBOM(path):
    import sys, codecs
    BUFSIZE = 4096
    BOMLEN = len(codecs.BOM_UTF8)

    with open(path, "r+b") as fp:
        chunk = fp.read(BUFSIZE)
        if chunk.startswith(codecs.BOM_UTF8):
            i = 0
            chunk = chunk[BOMLEN:]
            while chunk:
                fp.seek(i)
                fp.write(chunk)
                i += len(chunk)
                fp.seek(BOMLEN, os.SEEK_CUR)
                chunk = fp.read(BUFSIZE)
            fp.seek(-BOMLEN, os.SEEK_CUR)
            fp.truncate()