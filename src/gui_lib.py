from RPLCD.i2c import CharLCD
from constants import DIALOGS

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

# Headers
# Template              'X   X    X    X    X'
CHOOSE_CAST_HEADER=     ' | UP  DOWN       OK'
CHOOSE_AUDIOBOOK_HEADER='<| UP  DOWN       OK'
#TODO - back option on hold?
PLAY_AUDIOBOOK_HEADER=  '<| [<  >]  - V + ||>'

class LCD:
    def __init__(self):
        self.lcd = CharLCD(i2c_expander=I2C_UC, 
                    address=I2C_ADDRESS, 
                    port=I2C_PORT, 
                    cols=LCD_COLS, 
                    rows=LCD_ROWS, 
                    dotsize=LCD_DOTSIZE,
                    charmap=LCD_CHARMAP, 
                    auto_linebreaks=LCD_AUTOLINEBREAKS, 
                    backlight_enabled=LCD_BACKLIGHTENABLED)
        self.lcd.clear()

    def displayWelcome(self):
        self.lcd.write_string('* Welcome to abook *\n\rthe audiobook reader')
        
    def displayChooseCast(self, currentDialogContext):
        self.lcd.write_string(CHOOSE_CAST_HEADER)
        castOptionRows = self.getViewportCastDevicesFormatted(currentDialogContext)
        self.lcd.write_string(castOptionRows[0] + '\n\r')
        self.lcd.write_string(castOptionRows[1] + '\n\r')
        self.lcd.write_string(castOptionRows[2] + '\n\r')
        
    def getViewportCastDevicesFormatted(self, currentDialogContext):
        if currentDialogContext.menu_chooseCast_ViewpointStart > currentDialogContext.menu_chooseCast_CursorLocationAbsolute:
            currentDialogContext.menu_chooseCast_ViewpointStart = currentDialogContext.menu_chooseCast_CursorLocationAbsolute
            currentDialogContext.menu_chooseCast_ViewpointEnd = currentDialogContext.menu_chooseCast_ViewpointStart + 2
        elif currentDialogContext.menu_chooseCast_ViewpointEnd < currentDialogContext.menu_chooseCast_CursorLocationAbsolute:
            currentDialogContext.menu_chooseCast_ViewpointEnd = currentDialogContext.menu_chooseCast_CursorLocationAbsolute
            currentDialogContext.menu_chooseCast_ViewpointStart = currentDialogContext.menu_chooseCast_ViewpointStart - 2
        
        index = currentDialogContext.menu_chooseCast_ViewpointStart
        selected = currentDialogContext.menu_chooseCast_CursorLocationAbsolute
        
        return [
            self.trunc20(''.join(['> ' if index     == selected else '  ', currentDialogContext.chromecastDevices[index    ]])),
            self.trunc20(''.join(['> ' if index + 1 == selected else '  ', currentDialogContext.chromecastDevices[index + 1]])),
            self.trunc20(''.join(['> ' if index + 2 == selected else '  ', currentDialogContext.chromecastDevices[index + 2]]))]
         
    def trunc20(self, stringToCut):
        return (stringToCut[:18] + '..') if len(stringToCut) > 20 else stringToCut

    def display(self, currentDialogContext):
        self.lcd.clear()
        match currentDialogContext.currentDialogName:
            case DIALOGS.WELCOME:
                self.displayWelcome()
            case DIALOGS.CHOOSE_CAST:
                self.displayChooseCast(currentDialogContext)
            case DIALOGS.CHOOSE_WIFI:
                #TODO Implement
                "two"
            case DIALOGS.CHOOSE_AUDIOBOOK:
                #TODO Implement
                "two"
            case DIALOGS.AUDIOBOOK_PLAY:
                #TODO Implement
                "two"
            case default:
                #TODO Implement
                self.lcd.write_string(arguments)







