import os
from constants import SYSTEM_PROPERTIES


# TODO load MP3 folders, with their metadata if present
# TODO - load folder MP3s to be played
# TODO load property files for last cast device, volume settings, audiobook played
# TODO save property files with updated values
# TODO HTTP server setting

# TODO - read file -- https://blog.finxter.com/python-read-and-write-to-a-properties-file/

def loadSystemProperties(currentDialogContext):
    print('read properties from: ' + currentDialogContext.systemPropertiesPath)
    properties = {}
    with open(currentDialogContext.systemPropertiesPath, 'r') as file:
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


def loadAudiobooks(currentDialogContext):
    audiobookFolder = currentDialogContext.systemProperties[
        SYSTEM_PROPERTIES.LAST_AUDIOBOOK_ROOT_FOLDER]
    print('read audiobooks from: ' + audiobookFolder)
    dirs = os.listdir(audiobookFolder)
    print(dirs)
    currentDialogContext.audiobooks = dirs


# read details of the MP3s with audiobooks
# //bash command
# mp3info -p "%f: %m:%02s\n" *.mp3
# Titanic cz.2.mp3: 46:49
#
#


# list detailed contents of the file
# import os
# os.listdir('/Users/apuchalski/Downloads/-kidsSongs')
#
#
#
