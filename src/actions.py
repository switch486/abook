from constants import SYSTEM_PROPERTIES
import chromecast

def LOAD_CAST_DEVICES(currentDialogContext) : 
    currentDialogContext.lastCastDevice = currentDialogContext.systemProperties[SYSTEM_PROPERTIES.LAST_CAST_DEVICE]
    currentDialogContext.chromecastDevices = chromecast.getAvailableChromecasts(currentDialogContext)
    print('Last Cast Device: ' + currentDialogContext.lastCastDevice)
    print(currentDialogContext.chromecastDevices)
    if currentDialogContext.lastCastDevice in currentDialogContext.chromecastDevices:
        currentDialogContext.menu_chooseCast_CursorLocationAbsolute = currentDialogContext.chromecastDevices.index(currentDialogContext.lastCastDevice)
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