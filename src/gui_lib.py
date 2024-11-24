from RPLCD.i2c import CharLCD
import types

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

# dialog constants
DIALOGS = types.SimpleNamespace()
DIALOGS.WELCOME=0
DIALOGS.CHOOSE_CAST=1
DIALOGS.CHOOSE_WIFI=2
DIALOGS.CHOOSE_AUDIOBOOK=3
DIALOGS.AUDIOBOOK_PLAY=4

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

    def display(self, dialog, arguments=''):
        match dialog:
            case DIALOGS.WELCOME:
                return self.displayWelcome()
            case DIALOGS.CHOOSE_CAST:
                return "one"
            case DIALOGS.CHOOSE_WIFI:
                return "two"
            case DIALOGS.CHOOSE_AUDIOBOOK:
                return "two"
            case DIALOGS.AUDIOBOOK_PLAY:
                return "two"
            case default:
                return "something"







