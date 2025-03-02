
import DialogContext as dc
import dialogs as DIALOGS
import actions as ACTIONS
import time
from gui import Gui
import buttonshim
import filesystem
from constants import BUTTONS
import traceback


# default property file path
SYSTEM_PROPERTIES_FILE_PATH = './systemProperties.json'


@buttonshim.on_hold(buttonshim.BUTTON_E, hold_time=2)
def hold_handler_e(button):
    global heldButton
    heldButton = BUTTONS.HOLD_BUTTON_E


@buttonshim.on_hold(buttonshim.BUTTON_A, hold_time=5)
def hold_handler_a(button):
    global heldButton
    heldButton = BUTTONS.EXIT


@buttonshim.on_release(buttonshim.BUTTON_A)
def button_a(button, pressed):
    global releasedButton
    releasedButton = BUTTONS.BUTTON_A


@buttonshim.on_release(buttonshim.BUTTON_B)
def button_b(button, pressed):
    global releasedButton
    releasedButton = BUTTONS.BUTTON_B


@buttonshim.on_release(buttonshim.BUTTON_C)
def button_c(button, pressed):
    global releasedButton
    releasedButton = BUTTONS.BUTTON_C


@buttonshim.on_release(buttonshim.BUTTON_D)
def button_d(button, pressed):
    global releasedButton
    releasedButton = BUTTONS.BUTTON_D


@buttonshim.on_release(buttonshim.BUTTON_E)
def button_e(button, pressed):
    global releasedButton
    releasedButton = BUTTONS.BUTTON_E


# technical triggers
heldButton = None
releasedButton = None

# UseCase Action
buttonAction = 'null'

gui = Gui()

currentDialogContext = dc.DialogContext()
currentDialogContext.systemPropertiesPath = SYSTEM_PROPERTIES_FILE_PATH

currentDialogContext.systemProperties = filesystem.loadSystemProperties(
    currentDialogContext)
currentDialogContext.currentDialog = DIALOGS.WELCOME(gui)

currentDialogContext.currentDialog.displayDialog(currentDialogContext)
currentDialogContext.actions.put(ACTIONS.LOAD_LAST_VERSION_CHANGE_DATE)
currentDialogContext.actions.put(ACTIONS.LOAD_CAST_DEVICES)

while True:
    repaintNeeded = False
    time.sleep(.5)

    if heldButton is not None and releasedButton is not None:
        buttonAction = heldButton
        heldButton = None
        releasedButton = None
    elif heldButton is None and releasedButton is not None:
        buttonAction = releasedButton
        releasedButton = None

    # Button press implies potential action ...
    if buttonAction != 'null':
        currentDialogContext = currentDialogContext.handleButton(buttonAction)
        repaintNeeded = True
        buttonAction = 'null'

    try:
        while currentDialogContext.actions.empty() == False:
            action = currentDialogContext.actions.get()
            action(currentDialogContext)
            repaintNeeded = True
    except BaseException as err:
        print(traceback.format_exc())
        print(f">> EXCEPTION {err=}, {type(err)=}")
        currentDialogContext.currentDialog = DIALOGS.EXCEPTION(gui)

    if buttonAction == BUTTONS.EXIT:
        ACTIONS.STOP_APP(currentDialogContext)
        break

    if repaintNeeded or currentDialogContext.repaintParts:
        print('--Repaint')
        currentDialogContext.paintDialog()
