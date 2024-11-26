import gui_lib
import DialogContext
import logic
import time
import buttonshim
import mechanics
from constants import BUTTONS
from constants import DIALOGS

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

pressedButton = 'null' 

gui = gui_lib.LCD()
currentDialogContext = DialogContext()
currentDialogContext.currentDialogName = DIALOGS.WELCOME

gui.display(currentDialogContext)

while True:
   time.sleep(.5)
   # Button press implies potential action ...
   if pressedButton != 'null':
       currentDialogContext = logic.handleButtonPress(currentDialogContext, pressedButton)
       pressedButton = 'null'

   if currentDialogContext.action != 'null':   
       currentDialogContext = mechanics.handleAction(currentDialogContext)
       currentDialogContext.action = 'null'

   gui.display(currentDialogContext)
