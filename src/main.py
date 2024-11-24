import gui_lib
import DialogContext
import logic
import time
import buttonshim
import constants.BUTTONS as BUTTONS

@buttonshim.on_press(buttonshim.BUTTON_A)
def button_a(button, pressed):
    global pressedButton
    pressedButton = BUTTONS.BUTTON_A
    
@buttonshim.on_press(buttonshim.BUTTON_B)
def button_b(button, pressed):
    global pressedButton
    pressedButton = BUTTONS.BUTTON_B
    
@buttonshim.on_press(buttonshim.BUTTON_C)
def button_c(button, pressed):
    global pressedButton
    pressedButton = BUTTONS.BUTTON_C

@buttonshim.on_press(buttonshim.BUTTON_D)
def button_d(button, pressed):
    global pressedButton
    pressedButton = BUTTONS.BUTTON_D

@buttonshim.on_press(buttonshim.BUTTON_E)
def button_e(button, pressed):    
    global pressedButton
    pressedButton = BUTTONS.BUTTON_E

pressedButton = "null" 

gui = gui_lib.LCD()
currentDialogContext = DialogContext()
currentDialogContext.dialogName = gui_lib.DIALOGS.WELCOME

gui.display(currentDialog)




# read property file containing last cast device

while True:
   time.sleep(.5)
   if pressedButton != "null":
       currentDialog = logic.handleButtonPress(currentDialog, pressedButton)










   if pressedButton == BUTTONS.BUTTON_A:
       buttonshim.set_pixel(0x94, 0x00, 0xd3)
   elif pressedButton == BUTTONS.BUTTON_B:
       buttonshim.set_pixel(0x00, 0x00, 0xff)
   elif pressedButton == BUTTONS.BUTTON_C:    
       buttonshim.set_pixel(0x00, 0xff, 0x00)
   elif pressedButton == BUTTONS.BUTTON_D:       
       buttonshim.set_pixel(0xff, 0xff, 0x00)
   elif pressedButton == BUTTONS.BUTTON_E:   
       buttonshim.set_pixel(0xff, 0x00, 0x00)
   pressedButton = "null"





# TODO - loop consisting of: display and wait for input

# gui.display(gui_lib.DIALOGS.CHOOSE_CAST, castDevices)
## update last cast device!
# gui.display(gui_lib.DIALOGS.CHOOSE_WIFI, wifiConnections)
# gui.display(gui_lib.DIALOGS.CHOOSE_AUDIOBOOK, audiobookFolderDetails)
# gui.display(gui_lib.DIALOGS.AUDIOBOOK_PLAY, playDetails)



# loop over menu entries after a button press
## when playing update the view every x seconds based on multimedia state