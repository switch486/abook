from constants import DIALOGS, SYSTEM_PROPERTIES
import filesystem
import chromecast
import types

def LOAD_CAST_DEVICES(currentDialogContext) : 
    currentDialogContext.lastCastDevice = filesystem.loadSystemProperty(SYSTEM_PROPERTIES.LAST_CAST_DEVICE)
    currentDialogContext.chromecastDevices = chromecast.getAvailableChromecasts(currentDialogContext)
    return currentDialogContext

def CONNECT_TO_CAST_DEVICE():
    #TODO implement
    print('CONNECT_TO_CAST_DEVICE')
    
def LOAD_AUDIOBOOKS(currentDialogContext): 
    # chromecast device should conditionally reconnect
    chromecast.connectToCastDevice(currentDialogContext)
    ##### filesystem.readAudiobooksOnTheDevice
    # TODO update last cast device
    print('load audiobooks')
        
def VOL_UP(currentDialogContext): 
    # TODO implement
    print('volume up')
        
def VOL_DOWN(currentDialogContext): 
    # TODO implement
    print('volume down')