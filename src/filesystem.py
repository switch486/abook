import os
from constants import SYSTEM_PROPERTIES
from os import listdir, popen
from os.path import isdir, isfile, join, expanduser
from calculator import calculateTimes


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
    playpointMp3Name = ''
    playpointMp3Seconds = 0
    progressDetails = None
    if progressFile != None:
        progressDetails = loadPropertyFile(join(joinedPath, progressFile))
        playpointMp3Name = progressDetails['currentMp3']
        playpointMp3Seconds = progressDetails['second']

    # set startup if no progress
    if playpointMp3Name == '':
        playpointMp3Name = mp3Files[0]
        currentMp3Idx = 0
    else:
        currentMp3Idx = mp3Files.index(playpointMp3Name)

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
    totalTime, elapsedTime, previousMp3Progress, currentMp3Progress, percentage = calculateTimes(
        playpointMp3Name, playpointMp3Seconds, mp3Files, mp3Lengths)

    return {'rootPath': rootPath,
            'folder': folder,
            'mp3Files': mp3Files,
            'mp3Lengths': mp3Lengths,
            'currentMp3': playpointMp3Name,
            'currentMp3Idx': currentMp3Idx,
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

def saveProgress(currentDialogContext):
    book = currentDialogContext.currentlySelectedAudiobook()
    print ('progress save')
    
    #TODO - check if progress file is present
    #TODO - save progress

# testing purposes
# print(computeFolders(expanduser('~/Downloads/-kidsSongs/')))
