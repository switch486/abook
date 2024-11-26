from constants import ACTIONS, DIALOGS, SYSTEM_PROPERTIES
import filesystem
import chromecast

def handleAction(currentDialog):
    print ('Action: ' + currentDialog.action)

    if currentDialog.action == ACTIONS.NAVIGATE:
        return handleAction_Navigate(currentDialog)
    elif currentDialog.action == ACTIONS.VOL_UP:
        return handleAction_VolumeUp(currentDialog)
    elif currentDialog.action == ACTIONS.VOL_DOWN:
        return handleAction_VolumeDown(currentDialog)
    
    # fallback - no action
    return currentDialog

def handleAction_Navigate(currentDialog): 
    if currentDialog.currentDialogName == DIALOGS.CHOOSE_CAST:
        return handle_loadCastDevices(currentDialog)
    elif currentDialog.currentDialogName == DIALOGS.CHOOSE_AUDIOBOOK:
        return handle_loadAudiobooks(currentDialog)
    
def handle_loadCastDevices(currentDialog): 
    currentDialog.lastCastDevice = filesystem.loadSystemProperty(SYSTEM_PROPERTIES.LAST_CAST_DEVICE)
    currentDialog.chromecastDevices = chromecast.getAvailableChromecasts(currentDialog)
    print('load cast devices')
    
def handle_loadAudiobooks(currentDialog): 
    print('load audiobooks')
        
def handleAction_VolumeUp(currentDialog): 
    print('volume up')
        
def handleAction_VolumeDown(currentDialog): 
    print('volume down')