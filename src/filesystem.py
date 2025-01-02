import os
from constants import SYSTEM_PROPERTIES, CONSTANTS, FD, FO
from os import listdir, popen
from os.path import isdir, isfile, join
from calculator import calculateTimes
import functools

# TODO V2 load property files for volume settings?


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
    print('progress file: ' + path)
    print(f'{key1}{FO.EQUALS}{new_value1}')
    print(f'{key2}{FO.EQUALS}{new_value2}')
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
        playpointMp3Seconds = int(
            progressDetails[CONSTANTS.PROGRESS_SECOND_KEY])

    # set startup if no progress
    currentMp3Idx = 0
    if playpointMp3Name == '' and len(mp3Files) > 0:
        playpointMp3Name = mp3Files[0]
    elif len(mp3Files) > 0:
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
    print(">> current root path: " + currentDialogContext.currentRootPath)
    if currentDialogContext.currentRootPath == '':
        currentDialogContext.currentRootPath = currentDialogContext.systemProperties.get(
            SYSTEM_PROPERTIES.LAST_AUDIOBOOK_ROOT_FOLDER, "")
        print('start with last audiobook folder :' +
              currentDialogContext.currentRootPath)
    if not isdir(currentDialogContext.currentRootPath):
        currentDialogContext.currentRootPath = currentDialogContext.systemProperties.get(
            SYSTEM_PROPERTIES.DEFAULT_AUDIOBOOK_ROOT_FOLDER, "")
        print('last audiobook folder is missing, reset to default :' +
              currentDialogContext.currentRootPath)

    print('>> read audiobooks from: ' + currentDialogContext.currentRootPath)

    currentDialogContext.folderDetails[currentDialogContext.currentRootPath] = computeFolders(
        currentDialogContext.currentRootPath)
    currentDialogContext.folderDetails[currentDialogContext.currentRootPath] = sortFolderList(currentDialogContext.currentFolderDetails())


def loadSingleAudiobookDetails(currentDialogContext):
    currentDialogContext.currentRootPath = currentDialogContext.systemProperties[
        SYSTEM_PROPERTIES.LAST_AUDIOBOOK_ROOT_FOLDER]
    directory = currentDialogContext.systemProperties[
        SYSTEM_PROPERTIES.LAST_AUDIOBOOK_ROOD_DIRECTORY]
    print('read single audiobook from: ' +
          currentDialogContext.currentRootPath + ' at: ' + directory)

    currentDialogContext.folderDetails[currentDialogContext.currentRootPath] = [
        getFolderDetails(currentDialogContext.currentRootPath, directory)]


def saveProgress(currentDialogContext):
    currentBook = currentDialogContext.currentlySelectedAudiobook()
    progressFilePath = currentDialogContext.getCurrentAudiobookProgressFilePath()

    updatePropertyFile(progressFilePath,
                       CONSTANTS.PROGRESS_MP3_KEY,
                       currentBook[FD.CURRENT_MP3],
                       CONSTANTS.PROGRESS_SECOND_KEY,
                       currentBook[FD.CURRENT_MP3_PROGRESS])


def sortFolderList(folderListToBeSorted):
    def compare(folder1, folder2):
        if folder1[FD.PERCENTAGE] > folder2[FD.PERCENTAGE]:
            return 1
        if folder1[FD.PERCENTAGE] == folder2[FD.PERCENTAGE]:
            f1Len = len(folder1[FD.MP3_FILES])
            f2Len = len(folder2[FD.MP3_FILES])
            if f1Len == f2Len:
                return folder1[FD.FOLDER] > folder1[FD.FOLDER]
            return f1Len - f2Len
        return -1

    return sorted(folderListToBeSorted, key=functools.cmp_to_key(compare))
