from constants import BUTTONS
import actions as ACTIONS

# BUTTONS                 E   D    C    B    A
# Headers
# Template              'X   X    X    X    X'
CHOOSE_CAST_HEADER = ' | UP  DOWN       OK'
CHOOSE_AUDIOBOOK_HEADER = '<| UP  DOWN       OK'
# TODO - back option on hold?
PLAY_AUDIOBOOK_HEADER = '<| [<  >]  - V + ||>'


def trunc20(stringToCut):
    return (stringToCut[:18] + '..') if len(stringToCut) > 20 else stringToCut


class WELCOME:
    def __init__(self, lcd):
        self.lcd = lcd

    def handleButton(self, currentDialogContext, pressedButton):
        print('Handle Button ' + pressedButton)
        # any button navigates further
        currentDialogContext.currentDialog = CHOOSE_CAST(self.lcd)
        return currentDialogContext

    def displayDialog(self, currentDialogContext):
        print('Dialog: Welcome ')
        self.lcd.clear()
        self.lcd.write_string('* Welcome to abook *\n\rthe audiobook reader')


class CHOOSE_CAST:
    def __init__(self, lcd):
        self.lcd = lcd

    def handleButton(self, currentDialogContext, pressedButton):
        print('ChooseCast ' + pressedButton)
        # navigation within options here
        if pressedButton == BUTTONS.BUTTON_E:
            # UP
            if currentDialogContext.menu_chooseCast_CursorLocationAbsolute > 0:
                currentDialogContext.menu_chooseCast_CursorLocationAbsolute -= 1
                return currentDialogContext
        elif pressedButton == BUTTONS.BUTTON_D:
            # DOWN
            if currentDialogContext.menu_chooseCast_CursorLocationAbsolute < len(currentDialogContext.chromecastDevices)-1:
                currentDialogContext.menu_chooseCast_CursorLocationAbsolute += 1
                return currentDialogContext
        elif pressedButton == BUTTONS.BUTTON_A:
            # accept cast Device at cursor
            currentDialogContext.lastCastDevice = currentDialogContext.chromecastDevices[
                currentDialogContext.menu_chooseCast_CursorLocationAbsolute]
            currentDialogContext.currentDialog = CHOOSE_AUDIOBOOK(self.lcd)
            currentDialogContext.actions.put(ACTIONS.CONNECT_TO_CAST_DEVICE)
            currentDialogContext.actions.put(ACTIONS.LOAD_AUDIOBOOKS)
            return currentDialogContext
        return currentDialogContext

    def displayDialog(self, currentDialogContext):
        print('Dialog: Choose Cast ')
        self.lcd.clear()
        self.lcd.write_string(CHOOSE_CAST_HEADER)
        castOptionRows = self.getViewportCastDevicesFormatted(
            currentDialogContext, currentDialogContext.menu_chooseCast_CursorLocationAbsolute)
        self.lcd.write_string(castOptionRows[0] + '\n\r')
        self.lcd.write_string(castOptionRows[1] + '\n\r')
        self.lcd.write_string(castOptionRows[2] + '\n\r')

    def getViewportCastDevicesFormatted(self, currentDialogContext, selectedIndex):
        startIndex = 0
        endIndex = 2

        if startIndex > selectedIndex:
            startIndex = selectedIndex
            endIndex = startIndex + 2
        elif endIndex < selectedIndex:
            endIndex = selectedIndex
            startIndex = endIndex - 2

        return [
            trunc20(''.join(['> ' if startIndex == selectedIndex else '  ',
                    currentDialogContext.chromecastDevices[startIndex]])),
            trunc20(''.join(['> ' if startIndex + 1 == selectedIndex else '  ',
                    currentDialogContext.chromecastDevices[startIndex + 1]])),
            trunc20(''.join(['> ' if startIndex + 2 == selectedIndex else '  ', 
                    currentDialogContext.chromecastDevices[startIndex + 2]]))]


class CHOOSE_AUDIOBOOK:
    def __init__(self, lcd):
        self.lcd = lcd

    def handleButton(currentDialogContext, pressedButton):
        print('TBD, Choose Audiobook')
        # TODO Implement
        # navigation within options here
        if pressedButton == BUTTONS.BUTTON_A:
            print('A')
        elif pressedButton == BUTTONS.BUTTON_B:
            print('B')
        elif pressedButton == BUTTONS.BUTTON_C:
            print('C')
        elif pressedButton == BUTTONS.BUTTON_D:
            print('D')
        elif pressedButton == BUTTONS.BUTTON_E:
            print('E')
        return currentDialogContext

    def displayDialog(self, currentDialogContext):
        print('Dialog: Choose Audiobook ')
        self.lcd.clear()
        self.lcd.write_string(CHOOSE_AUDIOBOOK_HEADER)
        print('TBD, Choose Audiobook')


class AUDIOBOOK_PLAY:
    def __init__(self, lcd):
        self.lcd = lcd

    def handleButton(currentDialogContext, pressedButton):
        print('TBD, Audiobook play')
        # TODO Implement
        # formulate action and pass further
        if pressedButton == BUTTONS.BUTTON_A:
            print('A')
        elif pressedButton == BUTTONS.BUTTON_B:
            print('B')
        elif pressedButton == BUTTONS.BUTTON_C:
            print('C')
        elif pressedButton == BUTTONS.BUTTON_D:
            print('D')
        elif pressedButton == BUTTONS.BUTTON_E:
            print('E')
        return currentDialogContext

    def displayDialog(self, currentDialogContext):
        print('TBD, Choose Audiobook')


class TEST:
    def __init__(self, lcd):
        self.lcd = lcd

    def TEST(currentDialogContext, pressedButton):
        print('TBD, Test')
        # TODO Implement
        if pressedButton == BUTTONS.BUTTON_A:
            print('A')
        elif pressedButton == BUTTONS.BUTTON_B:
            print('B')
        elif pressedButton == BUTTONS.BUTTON_C:
            print('C')
        elif pressedButton == BUTTONS.BUTTON_D:
            print('D')
        elif pressedButton == BUTTONS.BUTTON_E:
            print('E')
        return currentDialogContext

    def displayDialog(self, currentDialogContext):
        print('TBD, Choose Audiobook')
