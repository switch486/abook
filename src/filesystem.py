import os
from constants import SYSTEM_PROPERTIES
from os import listdir, popen
from os.path import isdir, isfile, join, expanduser


# TODO load MP3 folders, with their metadata if present
# TODO - load folder MP3s to be played
# TODO load property files for last cast device, volume settings, audiobook played
# TODO save property files with updated values
# TODO HTTP server setting

# TODO - read file -- https://blog.finxter.com/python-read-and-write-to-a-properties-file/

def loadSystemProperties(currentDialogContext):
    return loadPropertyFile(currentDialogContext.systemPropertiesPath)


def loadPropertyFile(path):
    print('read properties from: ' + path)
    properties = {}
    with open(path, 'r') as file:
        for line in file:
            if line.startswith('#') or not line.strip():
                continue  # Skip comments and blank lines
            key, value = line.strip().split('=', 1)
            properties[key] = value
    return properties


def updateSystemProperty(currentDialogContext, key, new_value):
    properties = loadSystemProperties(currentDialogContext)
    properties[key] = new_value
    with open(currentDialogContext.systemPropertiesPath, 'w') as file:
        for key, value in properties.items():
            file.write(f'{key}={value}\n')


def isMp3File(filepath):
    # TODO - constant
    return filepath.endswith('.mp3')


def isAbookProgress(filepath):
    # TODO - constant
    return filepath.endswith('abook.progress')


def sublist_up_to(lst, element):
    try:
        index = lst.index(element)
        return lst[:index]
    except ValueError:
        return []


def calculateTime(mp3Files, mp3Lengths):
    time = 0
    print(mp3Files)
    print(mp3Lengths)
    for s in mp3Files:
        time += int(mp3Lengths[s])
    return time


def getFolderDetails(rootPath, folder):
    joinedPath = join(rootPath, folder)
    print('check Folder for file contents: ' + joinedPath)

    files = [f for f in listdir(joinedPath) if isfile(join(joinedPath, f))]

    containsMp3Files = any(map(isMp3File, files))
    print('containsMp3s: ' + str(containsMp3Files))
    mp3Files = [x for x in files if isMp3File(x)]
    mp3Files.sort()

    progressFiles = [x for x in files if isAbookProgress(x)]
    progressFile = progressFiles[0] if len(progressFiles) > 0 else None
    print('progressFile: ' + str(progressFile))

    # progress file handling
    progressDetails = None
    if progressFile != None:
        progressDetails = loadPropertyFile(join(joinedPath, progressFile))

    # mp3 durations
    mp3Lengths = None
    if containsMp3Files:
        resultRows = popen('cd "' + joinedPath +
                           '" && mp3info -p "%f#%S\n" *.mp3').read().splitlines()
        mp3Lengths = {}
        for line in resultRows:
            key, value = line.strip().split('#', 1)
            mp3Lengths[key] = value

    # total and elapsed times
    totalTime = calculateTime(mp3Files, mp3Lengths)
    elapsedTime = 0
    previousMp3Progress = 0
    currentMp3Progress = 0
    if progressDetails != None:
        previousMp3Progress = calculateTime(sublist_up_to(
            mp3Files, progressDetails['currentMp3']), mp3Lengths)
        currentMp3Progress += int(progressDetails['second'])
        elapsedTime = previousMp3Progress + currentMp3Progress

    # determine play mp3 title
    playpointMp3Name = ''
    currentMp3Idx = 0
    if len(mp3Files) > 0:
        playpointMp3Name = mp3Files[0]
        if progressDetails != None:
            playpointMp3Name = progressDetails['currentMp3']
            currentMp3Idx = mp3Files.index(playpointMp3Name)

    # percentage
    e = int(elapsedTime)
    t = int(totalTime)
    percentage = 0
    if t != 0:
        percentage = int((100*e)/t)

    return {'rootPath': rootPath,
            'folder': folder,
            'mp3Files': mp3Files,
            'mp3Lengths': mp3Lengths,
            'currentMp3': playpointMp3Name,
            'currentMp3Idx': currentMp3Idx,
            'progressDetails': progressDetails,
            'totalTime': totalTime,
            'elapsedTime': elapsedTime,
            'previousMp3Progress': previousMp3Progress,
            'currentMp3Progress': currentMp3Progress,
            'percentage': percentage}


def computeFolders(rootPath):
    directories = [f for f in listdir(rootPath)
                   if isdir(join(rootPath, f))]

    return [getFolderDetails(rootPath, directory) for directory in directories]


def loadAudiobooks(currentDialogContext):
    rootPath = currentDialogContext.systemProperties[
        SYSTEM_PROPERTIES.LAST_AUDIOBOOK_ROOT_FOLDER]
    print('read audiobooks from: ' + rootPath)

    currentDialogContext.folderDetails[rootPath] = computeFolders(rootPath)
    # TODO - sorting based on percentage
    # currentDialogContext.folderDetails[rootPath].sort() - sorting!
    currentDialogContext.currentRootPath = rootPath


# testing purposes
# print(computeFolders(expanduser('~/Downloads/-kidsSongs/')))
