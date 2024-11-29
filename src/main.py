from RPLCD.i2c import CharLCD
import DialogContext
import dialogs as DIALOGS
import time
import buttonshim
from constants import BUTTONS

# driver constants:
I2C_UC='PCF8574'
I2C_ADDRESS=0x27
I2C_PORT=1
LCD_COLS=20
LCD_ROWS=4
LCD_DOTSIZE=8
LCD_CHARMAP='A02'
LCD_AUTOLINEBREAKS=True
LCD_BACKLIGHTENABLED=True

#TODO - HOLD!

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
currentDialogContext = DialogContext()
currentDialogContext.currentDialog = DIALOGS.WELCOME(gui)

currentDialogContext.currentDialog.displayDialog(currentDialogContext)

while True:
   time.sleep(.5)
   # Button press implies potential action ...
   if pressedButton != 'null':
       currentDialogContext = currentDialogContext.currentDialog.handleButton(currentDialogContext, pressedButton)
       pressedButton = 'null'

   while currentDialogContext.action.empty() == False:   
       action = currentDialogContext.action.get()
       currentDialogContext = action(currentDialogContext)

   currentDialogContext.currentDialog.displayDialog(currentDialogContext)
