# TODO load MP3 folders, with their metadata if present
# TODO - load folder MP3s to be played
# TODO load property files for last cast device, volume settings, audiobook played
# TODO save property files with updated values
# TODO HTTP server setting 

from constants import SYSTEM_PROPERTIES

DEFAULT_CAST_DEVICE = 'Attic Hub'

def loadSystemProperty(propertyName):
    print ('loading Property: ' + propertyName)
    # TODO - read file

    return DEFAULT_CAST_DEVICE

