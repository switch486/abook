
import DialogContext as dc
import dialogs as DIALOGS
import actions as ACTIONS
import time
from gui import Gui
import buttonshim
import filesystem
from constants import BUTTONS


# default property file path
PROPERTY_FILE_PATH = './general.properties'


@buttonshim.on_hold(buttonshim.BUTTON_E, hold_time=1)
def hold_handler_e(button):
    global heldButton
    heldButton = BUTTONS.HOLD_BUTTON_E


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
heldButton = 'null'

gui = Gui()

currentDialogContext = dc.DialogContext()
currentDialogContext.systemPropertiesPath = PROPERTY_FILE_PATH

currentDialogContext.systemProperties = filesystem.loadSystemProperties(
    currentDialogContext)
currentDialogContext.currentDialog = DIALOGS.WELCOME(gui)

currentDialogContext.currentDialog.displayDialog(currentDialogContext)
currentDialogContext.actions.put(ACTIONS.LOAD_CAST_DEVICES)

while True:
    repaintNeeded = False
    time.sleep(.5)
    # Button press implies potential action ...
    if pressedButton != 'null':
        currentDialogContext = currentDialogContext.handleButton(pressedButton)
        repaintNeeded = True
        pressedButton = 'null'

    while currentDialogContext.actions.empty() == False:
        action = currentDialogContext.actions.get()
        action(currentDialogContext)
        repaintNeeded = True

    if repaintNeeded or currentDialogContext.repaintParts:
        print('--Repaint')
        currentDialogContext.paintDialog()
