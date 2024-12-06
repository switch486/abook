from RPLCD.i2c import CharLCD
import DialogContext as dc
import dialogs as DIALOGS
import actions as ACTIONS
import time
import buttonshim
import filesystem
from constants import BUTTONS

# driver constants:
I2C_UC = 'PCF8574'
I2C_ADDRESS = 0x27
I2C_PORT = 1
LCD_COLS = 20
LCD_ROWS = 4
LCD_DOTSIZE = 8
LCD_CHARMAP = 'A02'
LCD_AUTOLINEBREAKS = True
LCD_BACKLIGHTENABLED = True

# default property file path
PROPERTY_FILE_PATH = './general.properties'

# TODO - HOLD!


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

gui = CharLCD(i2c_expander=I2C_UC,
              address=I2C_ADDRESS,
              port=I2C_PORT,
              cols=LCD_COLS,
              rows=LCD_ROWS,
              dotsize=LCD_DOTSIZE,
              charmap=LCD_CHARMAP,
              auto_linebreaks=LCD_AUTOLINEBREAKS,
              backlight_enabled=LCD_BACKLIGHTENABLED)
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

    if (repaintNeeded):
        print('--Repaint')
        currentDialogContext.paintDialog()
