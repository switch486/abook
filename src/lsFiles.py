from os import listdir, popen
from os.path import isdir, isfile, join, expanduser
from filesystem import loadPropertyFile

audiobookFolder = expanduser('~/Downloads/-kidsSongs/')


def isMp3File(filepath):
    return filepath.endswith('.mp3')


def isAbookProgress(filepath):
    return filepath.endswith('abook.progress')


def sublist_up_to(lst, element):
    try:
        index = lst.index(element)
        return lst[:index]
    except ValueError:
        return []


def calculateTime(mp3Files, mp3Lengths):
    time = 0
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

    progressDetails = None
    if progressFile != None:
        progressDetails = loadPropertyFile(join(joinedPath, progressFile))

    mp3Lengths = None
    if containsMp3Files:
        resultRows = popen('cd "' + joinedPath +
                           '" && mp3info -p "%f#%S\n" *.mp3').read().splitlines()
        mp3Lengths = {}
        for line in resultRows:
            key, value = line.strip().split('#', 1)
            mp3Lengths[key] = value

    totalTime = calculateTime(mp3Files, mp3Lengths)
    elapsedTime = 0

    if progressDetails != None:
        elapsedTime = calculateTime(sublist_up_to(
            mp3Files, progressDetails['currentMp3']), mp3Lengths)
        elapsedTime += int(progressDetails['second'])

    return {'rootPath': rootPath,
            'folder': folder,
            'mp3Files': mp3Files,
            'mp3Lengths': mp3Lengths,
            'progressDetails': progressDetails,
            'totalTime': totalTime,
            'elapsedTime': elapsedTime}


print('read audiobooks from: ' + audiobookFolder)
dirs = [f for f in listdir(audiobookFolder) if isdir(join(audiobookFolder, f))]

for folder in dirs:
    folderDetails = getFolderDetails(audiobookFolder, folder)
    f = folderDetails['folder']
    e = int(folderDetails['elapsedTime'])
    t = int(folderDetails['totalTime'])
    p = 0
    if t!=0 :
        p = int((100*e)/t)
    
    print(f'Folder: {f}, percentage: {p}%')
