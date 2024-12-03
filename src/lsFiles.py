from os import listdir, popen
from os.path import isdir, isfile, join, expanduser
from filesystem import loadPropertyFile

audiobookFolder = expanduser('~/Downloads/-kidsSongs/')


def isMp3File(filepath):
    return filepath.endswith('.mp3')


def isAbookProgress(filepath):
    return filepath.endswith('abook.progress')


def getFolderDetails(rootPath, folder):
    joinedPath = join(rootPath, folder)
    print('check Folder for file contents: ' + joinedPath)

    files = [f for f in listdir(joinedPath) if isfile(join(joinedPath, f))]

    containsMp3Files = any(map(isMp3File, files))
    print('containsMp3s: ' + str(containsMp3Files))
    mp3Files = [x for x in files if isMp3File(x)]

    progressFiles = [x for x in files if isAbookProgress(x)]
    progressFile = progressFiles[0] if len(progressFiles) > 0 else None
    print('progressFile: ' + str(progressFile))

    progressDetails = None
    if progressFile != None:
        progressDetails = loadPropertyFile(join(joinedPath, progressFile))

    mp3Lengths=None
    if containsMp3Files:
        resultRows = popen('cd "' + joinedPath + '" && mp3info -p "%f#%S\n" *.mp3').read().splitlines()
        mp3Lengths = {}
        for line in resultRows:
            key, value = line.strip().split('#', 1)
            mp3Lengths[key] = value
    # calculateProgress and add to result structure

    mp3Files.sort()

    return {'rootPath': rootPath, 'folder': folder, 'mp3Files': mp3Files, 'mp3Lengths': mp3Lengths, 'progressDetails': progressDetails}


print('read audiobooks from: ' + audiobookFolder)
dirs = [f for f in listdir(audiobookFolder) if isdir(join(audiobookFolder, f))]

for folder in dirs:
    folderDetails = getFolderDetails(audiobookFolder, folder)
    print(folderDetails)
