
from constants import DIALOGS, BUTTONS, ACTIONS

def handleButtonPress(currentDialogContext, pressedButton):
    print ('Dialog: ' + currentDialogContext.currentDialogName)

    if currentDialogContext.currentDialogName == DIALOGS.WELCOME:
        return handleButtonPress_Welcome(currentDialogContext, pressedButton)
    elif currentDialogContext.currentDialogName == DIALOGS.CHOOSE_CAST:
        return handleButtonPress_ChooseCast(currentDialogContext, pressedButton)
    elif currentDialogContext.currentDialogName == DIALOGS.CHOOSE_AUDIOBOOK:
        return handleButtonPress_ChooseAudiobook(currentDialogContext, pressedButton)
    elif currentDialogContext.currentDialogName == DIALOGS.AUDIOBOOK_PLAY:
        return handleButtonPress_AudiobookPlay(currentDialogContext, pressedButton)
    
    return handleButtonPress_Test(currentDialogContext, pressedButton)

def handleButtonPress_Welcome(currentDialogContext, pressedButton):
    print ('Handle Button' + pressedButton)
    # any button navigates further
    currentDialogContext.currentDialogName = DIALOGS.CHOOSE_CAST
    currentDialogContext.action = ACTIONS.NAVIGATE
    return currentDialogContext

def handleButtonPress_ChooseCast(currentDialogContext, pressedButton):
    print ('ChooseCast')
    # navigation within options here
    if pressedButton == BUTTONS.BUTTON_A:
       # UP
       if currentDialogContext.menu_chooseCast_CursorLocationAbsolute > 0:
           currentDialogContext.menu_chooseCast_CursorLocationAbsolute -= 1
           return currentDialogContext
    elif pressedButton == BUTTONS.BUTTON_B:
       #DOWN
       if currentDialogContext.menu_chooseCast_CursorLocationAbsolute < len(currentDialogContext.chromecastDevices)-1:
           currentDialogContext.menu_chooseCast_CursorLocationAbsolute += 1
           return currentDialogContext
    elif pressedButton == BUTTONS.BUTTON_E: 
       # accept cast Device at cursor 
       currentDialogContext.lastCastDevice = currentDialogContext.chromecastDevices[currentDialogContext.menu_chooseCast_CursorLocationAbsolute]
       currentDialogContext.currentDialogName = DIALOGS.CHOOSE_AUDIOBOOK
       currentDialogContext.action = ACTIONS.NAVIGATE
       return currentDialogContext

def handleButtonPress_ChooseAudiobook(currentDialogContext, pressedButton):
    print ('TBD, Choose Audiobook')
    #TODO Implement
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
    return currentDialogContext
    
def handleButtonPress_AudiobookPlay(currentDialogContext, pressedButton):
    print ('TBD, Audiobook play')
    #TODO Implement
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
    return currentDialogContext

def handleButtonPress_Test(currentDialogContext, pressedButton):
    print ('TBD, Test')
    #TODO Implement
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
    return currentDialogContext