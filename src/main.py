import gui_lib
import time
import buttonshim

@buttonshim.on_press(buttonshim.BUTTON_A)
def button_a(button, pressed):
    global pressedButton
    pressedButton = button
    
@buttonshim.on_press(buttonshim.BUTTON_B)
def button_b(button, pressed):
    global pressedButton
    pressedButton = button
    
@buttonshim.on_press(buttonshim.BUTTON_C)
def button_c(button, pressed):
    global pressedButton
    pressedButton = button

@buttonshim.on_press(buttonshim.BUTTON_D)
def button_d(button, pressed):
    global pressedButton
    pressedButton = button

@buttonshim.on_press(buttonshim.BUTTON_E)
def button_e(button, pressed):    
    global pressedButton
    pressedButton = button

pressedButton = "null" 



gui = gui_lib.LCD()
currentDialog = gui_lib.DIALOGS.WELCOME

gui.display(currentDialog)

# read property file containing last cast device

while True:
   time.sleep(.1)
   if pressedButton == "button_1":
       buttonshim.set_pixel(0x94, 0x00, 0xd3)
       pressedButton = "null"
   elif pressedButton == "button_2":
       buttonshim.set_pixel(0x00, 0x00, 0xff)
       pressedButton = "null"
   elif pressedButton == "button_3":    
       buttonshim.set_pixel(0x00, 0xff, 0x00)
       pressedButton = "null"
   elif pressedButton == "button_4":       
       buttonshim.set_pixel(0xff, 0xff, 0x00)
       pressedButton = "null"
   elif pressedButton == "button_5":   
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