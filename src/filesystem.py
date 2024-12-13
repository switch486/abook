import os
from constants import SYSTEM_PROPERTIES, CONSTANTS, FD, FO
from os import listdir, popen
from os.path import isdir, isfile, join, expanduser
from calculator import calculateTimes

# TODO load property files for last cast device, volume settings


def loadSystemProperties(currentDialogContext):
    return loadPropertyFile(currentDialogContext.systemPropertiesPath)


def loadPropertyFile(path):
    print('read properties from: ' + path)
    properties = {}
    if os.path.isfile(path):
        with open(path, FO.READ) as file:
            for line in file:
                if line.startswith(FO.COMMENT) or not line.strip():
                    continue
                key, value = line.strip().split(FO.EQUALS, 1)
                properties[key] = value
    return properties


def updateSystemProperty(currentDialogContext, key, new_value):
    properties = loadSystemProperties(currentDialogContext)
    properties[key] = new_value
    with open(currentDialogContext.systemPropertiesPath, FO.WRITE) as file:
        for key, value in properties.items():
            file.write(f'{key}{FO.EQUALS}{value}{FO.NEWLINE}')


def updatePropertyFile(path, key1, new_value1, key2, new_value2):
    properties = {}
    if os.path.isfile(path):
        properties = loadPropertyFile(path)

    properties[key1] = new_value1
    properties[key2] = new_value2
    with open(path, FO.WRITE_CREATE) as file:
        for key, value in properties.items():
            file.write(f'{key}{FO.EQUALS}{value}{FO.NEWLINE}')


def isMp3File(filepath):
    return filepath.endswith(CONSTANTS.MP3_FILETYPE)


def isAbookProgress(filepath):
    return filepath.endswith(CONSTANTS.PROGRESS_FILE)


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
        playpointMp3Name = progressDetails[CONSTANTS.PROGRESS_MP3_KEY]
        playpointMp3Seconds = int(progressDetails[CONSTANTS.PROGRESS_SECOND_KEY])

    # set startup if no progress
    currentMp3Idx = 0
    if playpointMp3Name == '' and len(mp3Files) > 0:
        playpointMp3Name = mp3Files[0]
    elif len(mp3Files) > 0 :
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

    return {FD.ROOT_PATH: rootPath,
            FD.FOLDER: folder,
            FD.MP3_FILES: mp3Files,
            FD.MP3_LENGTHS: mp3Lengths,
            FD.CURRENT_MP3: playpointMp3Name,
            FD.CURRENT_MP3_IDX: currentMp3Idx,
            FD.TOTAL_TIME: totalTime,
            FD.ELAPSED_TIME: elapsedTime,
            FD.PREVIOS_MP3_PROGRESS: previousMp3Progress,
            FD.CURRENT_MP3_PROGRESS: currentMp3Progress,
            FD.PERCENTAGE: percentage}


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
    currentBook = currentDialogContext.currentlySelectedAudiobook()
    print('progress save')
    progressFilePath = currentDialogContext.getCurrentAudiobookProgressFilePath()

    updatePropertyFile(progressFilePath,
                       CONSTANTS.PROGRESS_MP3_KEY,
                       currentBook[FD.CURRENT_MP3],
                       CONSTANTS.PROGRESS_SECOND_KEY,
                       currentBook[FD.CURRENT_MP3_PROGRESS])
