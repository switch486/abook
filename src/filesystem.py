import os
from constants import SYSTEM_PROPERTIES, CONSTANTS, FD, FO
from os import listdir, popen
from os.path import isdir, isfile, join
from calculator import calculateTimes
import functools
import json


def loadSystemProperties(currentDialogContext):
    return loadProperties(currentDialogContext.systemPropertiesPath)


def loadProperties(path):
    print('read properties from: ' + path)
    return json.load(open(path))


def updateProperties(path, properties):
    json.dump(properties, open(path, 'w'))


def updateSystemProperties(currentDialogContext):
    updateProperties(
        currentDialogContext.systemPropertiesPath, currentDialogContext.systemProperties)


def isMp3File(filepath):
    return filepath.endswith(CONSTANTS.MP3_FILETYPE)


def isAbookDetailsFile(filepath):
    return filepath.endswith(CONSTANTS.PROGRESS_FILE)


def getFolderDetails(rootPath, folder):
    joinedPath = join(rootPath, folder)
    print('check Folder for file contents: ' + joinedPath)

    files = [f for f in listdir(joinedPath) if isfile(join(joinedPath, f))]

    # Fallback if data has been acquired earlier
    audiobookDetailFilenames = [x for x in files if isAbookDetailsFile(x)]
    audiobookDetailFilename = audiobookDetailFilenames[0] if len(
        audiobookDetailFilenames) > 0 else None
    print('audiobookDetails: ' + str(audiobookDetailFilename))

    audiobookDetails = {}
    if audiobookDetailFilename != None:
        audiobookDetails = loadProperties(
            join(joinedPath, audiobookDetailFilename))

    else:
        audiobookDetails[CONSTANTS.PROGRESS_MP3_KEY] = ''
        audiobookDetails[CONSTANTS.PROGRESS_SECOND_KEY] = 0

        containsMp3Files = any(map(isMp3File, files))
        print('containsMp3s: ' + str(containsMp3Files))
        audiobookDetails[CONSTANTS.MP3_FILES] = [
            x for x in files if isMp3File(x)]
        audiobookDetails[CONSTANTS.MP3_FILES].sort()
        audiobookDetails[CONSTANTS.MP3_DURATIONS] = {}

        if containsMp3Files:
            resultRows = popen('cd "' + joinedPath +
                               '" && mp3info -p "%f#%S\n" *.mp3').read().splitlines()
            for line in resultRows:
                key, value = line.strip().split('#', 1)
                audiobookDetails[CONSTANTS.MP3_DURATIONS][key] = value

    # set startup if no progress
    currentMp3Idx = 0
    if audiobookDetails[CONSTANTS.PROGRESS_MP3_KEY] == '' and len(audiobookDetails[CONSTANTS.MP3_FILES]) > 0:
        audiobookDetails[CONSTANTS.PROGRESS_MP3_KEY] = audiobookDetails[CONSTANTS.MP3_FILES][0]
    elif len(audiobookDetails[CONSTANTS.MP3_FILES]) > 0:
        currentMp3Idx = audiobookDetails[CONSTANTS.MP3_FILES].index(
            audiobookDetails[CONSTANTS.PROGRESS_MP3_KEY])

    # total and elapsed times
    totalTime, elapsedTime, percentage = calculateTimes(audiobookDetails)

    return {FD.ROOT_PATH: rootPath,
            FD.FOLDER: folder,
            FD.AUDIOBOOK_DETAILS_KEY: audiobookDetails,
            FD.CURRENT_MP3_IDX: currentMp3Idx,
            FD.TOTAL_TIME: totalTime,
            FD.ELAPSED_TIME: elapsedTime,
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
    currentDialogContext.folderDetails[currentDialogContext.currentRootPath] = sortFolderList(
        currentDialogContext.currentFolderDetails())


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
    audiobookDetailsFilepath = currentDialogContext.getCurrentAudiobookDetailsFilePath()

    updateProperties(audiobookDetailsFilepath,
                     currentBook[FD.AUDIOBOOK_DETAILS_KEY])


def sortFolderList(folderListToBeSorted):
    def compare(folder1, folder2):
        if folder1[FD.AUDIOBOOK_DETAILS_KEY][FD.PERCENTAGE] > folder2[FD.AUDIOBOOK_DETAILS_KEY][FD.PERCENTAGE]:
            return -1
        if folder1[FD.AUDIOBOOK_DETAILS_KEY][FD.PERCENTAGE] == folder2[FD.AUDIOBOOK_DETAILS_KEY][FD.PERCENTAGE]:
            f1Len = len(folder1[FD.AUDIOBOOK_DETAILS_KEY][CONSTANTS.MP3_FILES])
            f2Len = len(folder2[FD.AUDIOBOOK_DETAILS_KEY][CONSTANTS.MP3_FILES])
            if f1Len == f2Len:
                return folder1[FD.FOLDER] < folder1[FD.FOLDER]
            return f2Len - f1Len
        return 1

    return sorted(folderListToBeSorted, key=functools.cmp_to_key(compare))
