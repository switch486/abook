# TODO load MP3 folders, with their metadata if present
# TODO - load folder MP3s to be played
# TODO load property files for last cast device, volume settings, audiobook played
# TODO save property files with updated values
# TODO HTTP server setting 

# TODO - read file -- https://blog.finxter.com/python-read-and-write-to-a-properties-file/


def updateSystemProperty(propertyName, propertyValue):
    print('update Property: ' + propertyName + ' with value: ' + propertyValue)
    # TODO - update property
    
def loadSystemProperties(file_path):
    print('read properties from: ' + file_path)
    properties = {}
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('#') or not line.strip():
                continue  # Skip comments and blank lines
            key, value = line.strip().split('=', 1)
            properties[key] = value
    return properties
    




## read details of the MP3s with audiobooks
# //bash command
# mp3info -p "%f: %m:%02s\n" *.mp3
# Titanic cz.2.mp3: 46:49
#
#


## list detailed contents of the file
# import os
# os.listdir('/Users/apuchalski/Downloads/-kidsSongs')
#
#
#


