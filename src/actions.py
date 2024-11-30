from constants import SYSTEM_PROPERTIES
import chromecast
import filesystem

def LOAD_CAST_DEVICES(currentDialogContext) : 
    currentDialogContext.lastCastDevice = currentDialogContext.systemProperties[SYSTEM_PROPERTIES.LAST_CAST_DEVICE]
    currentDialogContext.chromecastDevices = chromecast.getAvailableChromecasts(currentDialogContext)
    print('Last Cast Device: ' + currentDialogContext.lastCastDevice)
    print(currentDialogContext.chromecastDevices)
    if currentDialogContext.lastCastDevice in currentDialogContext.chromecastDevices:
        currentDialogContext.menu_chooseCast_CursorLocationAbsolute = currentDialogContext.chromecastDevices.index(currentDialogContext.lastCastDevice)

def CONNECT_TO_CAST_DEVICE(currentDialogContext):
    print('CONNECT_TO_CAST_DEVICE')
    chromecast.connectToCastDevice(currentDialogContext)
    
def LOAD_AUDIOBOOKS(currentDialogContext): 
    print('LOAD_AUDIOBOOKS')
    currentDialogContext = filesystem.loadAudiobooks(currentDialogContext)
        
def VOL_UP(currentDialogContext): 
    # TODO implement
    print('volume up')
        
def VOL_DOWN(currentDialogContext): 
    # TODO implement
    print('volume down')