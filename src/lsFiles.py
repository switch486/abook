from os import listdir
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
        # calculateProgress and add to result structure

    files.sort()

    return {'rootPath': rootPath, 'folder': folder, 'mp3Files': mp3Files, 'progressDetails': progressDetails}


print('read audiobooks from: ' + audiobookFolder)
dirs = [f for f in listdir(audiobookFolder) if isdir(join(audiobookFolder, f))]

for folder in dirs:
    folderDetails = getFolderDetails(audiobookFolder, folder)
    print(folderDetails)

# print(dirs)
