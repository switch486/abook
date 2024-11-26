
from constants import DIALOGS
from constants import BUTTONS

def handleButtonPress(currentDialog, pressedButton):
    print ('Dialog: ' + currentDialog.currentDialogName)

    if currentDialog.currentDialogName == DIALOGS.WELCOME:
        return handleButtonPress_Welcome(currentDialog, pressedButton)
    elif currentDialog.currentDialogName == DIALOGS.CHOOSE_CAST:
        return handleButtonPress_ChooseCast(currentDialog, pressedButton)
    elif currentDialog.currentDialogName == DIALOGS.CHOOSE_AUDIOBOOK:
        return handleButtonPress_ChooseAudiobook(currentDialog, pressedButton)
    elif currentDialog.currentDialogName == DIALOGS.AUDIOBOOK_PLAY:
        return handleButtonPress_AudiobookPlay(currentDialog, pressedButton)
    
    return handleButtonPress_Test(currentDialog, pressedButton)

def handleButtonPress_Welcome(currentDialog, pressedButton):
    print ('Handle Button' + pressedButton)
    # any button navigates further
    currentDialog.currentDialogName = DIALOGS.CHOOSE_CAST
    currentDialog.dialogChanged = True
    return currentDialog

def handleButtonPress_ChooseCast(currentDialog, pressedButton):
    print ('TBD, ChooseCast')
    # navigation within options here
    if pressedButton == BUTTONS.BUTTON_A:
       print ('A')
    elif pressedButton == BUTTONS.BUTTON_B:
       print ('B')
    elif pressedButton == BUTTONS.BUTTON_C:   
       print ('C')
    elif pressedButton == BUTTONS.BUTTON_D:      
       print ('D')
    elif pressedButton == BUTTONS.BUTTON_E:  
       print ('E')
    return currentDialog

def handleButtonPress_ChooseAudiobook(currentDialog, pressedButton):
    print ('TBD, Choose Audiobook')
    #navigation within options here
    if pressedButton == BUTTONS.BUTTON_A:
       print ('A')
    elif pressedButton == BUTTONS.BUTTON_B:
       print ('B')
    elif pressedButton == BUTTONS.BUTTON_C:   
       print ('C')
    elif pressedButton == BUTTONS.BUTTON_D:      
       print ('D')
    elif pressedButton == BUTTONS.BUTTON_E:  
       print ('E')
    return currentDialog
    
def handleButtonPress_AudiobookPlay(currentDialog, pressedButton):
    print ('TBD, Audiobook play')
    # formulate action and pass further
    if pressedButton == BUTTONS.BUTTON_A:
       print ('A')
    elif pressedButton == BUTTONS.BUTTON_B:
       print ('B')
    elif pressedButton == BUTTONS.BUTTON_C:   
       print ('C')
    elif pressedButton == BUTTONS.BUTTON_D:      
       print ('D')
    elif pressedButton == BUTTONS.BUTTON_E:  
       print ('E')
    return currentDialog

def handleButtonPress_Test(currentDialog, pressedButton):
    print ('TBD, Test')
    if pressedButton == BUTTONS.BUTTON_A:
       print ('A')
    elif pressedButton == BUTTONS.BUTTON_B:
       print ('B')
    elif pressedButton == BUTTONS.BUTTON_C:   
       print ('C')
    elif pressedButton == BUTTONS.BUTTON_D:      
       print ('D')
    elif pressedButton == BUTTONS.BUTTON_E:  
       print ('E')
    return currentDialog