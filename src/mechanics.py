from constants import ACTIONS, DIALOGS, SYSTEM_PROPERTIES
import filesystem
import chromecast

def handleAction(currentDialogContext):
    print ('Action: ' + currentDialog.action)

    if currentDialogContext.action == ACTIONS.NAVIGATE:
        return handleAction_Navigate(currentDialogContext)
    elif currentDialogContext.action == ACTIONS.VOL_UP:
        return handleAction_VolumeUp(currentDialogContext)
    elif currentDialogContext.action == ACTIONS.VOL_DOWN:
        return handleAction_VolumeDown(currentDialogContext)
    
    # fallback - no action
    return currentDialogContext

def handleAction_Navigate(currentDialogContext): 
    if currentDialogContext.currentDialogName == DIALOGS.CHOOSE_CAST:
        return handle_loadCastDevices(currentDialogContext)
    elif currentDialogContext.currentDialogName == DIALOGS.CHOOSE_AUDIOBOOK:
        return handle_loadAudiobooks(currentDialogContext)
    
def handle_loadCastDevices(currentDialogContext): 
    currentDialogContext.lastCastDevice = filesystem.loadSystemProperty(SYSTEM_PROPERTIES.LAST_CAST_DEVICE)
    currentDialogContext.chromecastDevices = chromecast.getAvailableChromecasts(currentDialogContext)
    print('load cast devices')
    
def handle_loadAudiobooks(currentDialogContext): 
    # TODO update last cast device
    print('load audiobooks')
        
def handleAction_VolumeUp(currentDialogContext): 
    # TODO implement
    print('volume up')
        
def handleAction_VolumeDown(currentDialogContext): 
    # TODO implement
    print('volume down')