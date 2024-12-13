from RPLCD.i2c import CharLCD


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

def trunc(stringToCut, maxLength):
    return (stringToCut[:maxLength-2] + '..') if len(stringToCut) > maxLength else stringToCut


class Gui:
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

    def clear(self):
        self.lcd.clear()
        
        # 0 Y....................
        # 1 Y....................
        # 2 Y....................
        # 3 Y....................
        #    XXXXXXXXXXXXXXXXXXXX
        #    123456789...
    def write(self, y, x, value, maxLength) :
        string = value
        if len(value) > maxLength :
            string = trunc(value, maxLength)
        self.lcd.cursor_pos = (y, x)
        self.lcd.write_string(string)
        
            
    def writeHeader(self, value):
        self.lcd.cursor_pos = (0, 0)
        self.lcd.write_string(value)
        
        
        