from constants import BUTTONS, PA as paintAction, FD
import actions as ACTIONS

# BUTTONS                  E   D    C    B    A
# Headers
# Template                'X   X    X    X    X'
CHOOSE_CAST_HEADER = ' | UP  DOWN       OK'
CHOOSE_AUDIOBOOK_HEADER = '<| UP  DOWN       OK'
PLAY_AUDIOBOOK_HEADER = '<| [<  >]  - V + ||>'


def selectionIndicator(startIndex, selectedIndex):
    return '> ' if startIndex == selectedIndex else '  '


def join(str1, str2, str3='', str4=''):
    return ''.join([str1, str2, str3, str4])


def formatPercentage3(string):
    number = int(string)
    return f"{number:02}%"


def shouldPaint(actionValue, currentDialogContext):
    return actionValue in currentDialogContext.repaintParts or paintAction.ALL in currentDialogContext.repaintParts


def getViewportListFormatted(list, selectedIndex):
    startIndex = 0
    endIndex = 2

    if startIndex > selectedIndex:
        startIndex = selectedIndex
        endIndex = startIndex + 2
    elif endIndex < selectedIndex:
        endIndex = selectedIndex
        startIndex = endIndex - 2

    return [
        [selectionIndicator(startIndex, selectedIndex), list[startIndex]],
        [selectionIndicator(startIndex + 1, selectedIndex),
         list[startIndex + 1]],
        [selectionIndicator(startIndex + 2, selectedIndex), list[startIndex + 2]]]


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
        self.lcd.writeHeader(
            '* Welcome to abook *\n\rthe audiobook reader\n\n\r')
        self.lcd.write(3, 4, 'press any key...', 16)
        currentDialogContext.clearRepaintParts()


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
        self.lcd.writeHeader(CHOOSE_CAST_HEADER)
        castOptionRows = getViewportListFormatted(
            currentDialogContext.chromecastDevices,
            currentDialogContext.menu_chooseCast_CursorLocationAbsolute)
        self.lcd.write(1, 0, ''.join(castOptionRows[0]), 20)
        self.lcd.write(2, 0, ''.join(castOptionRows[1]), 20)
        self.lcd.write(3, 0, ''.join(castOptionRows[2]), 20)
        currentDialogContext.clearRepaintParts()


class CHOOSE_AUDIOBOOK:
    def __init__(self, lcd):
        self.lcd = lcd

    def handleButton(self, currentDialogContext, pressedButton):
        print('ChooseAudiobook ' + pressedButton)
        if pressedButton == BUTTONS.BUTTON_A:
            # play audiobook
            currentDialogContext.currentDialog = AUDIOBOOK_PLAY(self.lcd)
            currentDialogContext.actions.put(ACTIONS.PLAY_AUDIOBOOK)
        elif pressedButton == BUTTONS.BUTTON_D:
            # DOWN
            if currentDialogContext.menu_chooseAudiobook_CursorLocationAbsolute < len(currentDialogContext.currentFolderDetails())-1:
                currentDialogContext.menu_chooseAudiobook_CursorLocationAbsolute += 1
        elif pressedButton == BUTTONS.BUTTON_E:
            # UP
            if currentDialogContext.menu_chooseAudiobook_CursorLocationAbsolute > 0:
                currentDialogContext.menu_chooseAudiobook_CursorLocationAbsolute -= 1
        elif pressedButton == BUTTONS.HOLD_BUTTON_E:
            # Hold E -> Back to previous dialog
            currentDialogContext.currentDialog = CHOOSE_CAST(self.lcd)
        return currentDialogContext

    def displayDialog(self, currentDialogContext):
        print('Dialog: Choose Audiobook ')
        self.lcd.clear()
        self.lcd.writeHeader(CHOOSE_AUDIOBOOK_HEADER)
        castOptionRows = getViewportListFormatted(
            currentDialogContext.currentFolderDetails(),
            currentDialogContext.menu_chooseAudiobook_CursorLocationAbsolute)
        # TODO do not show percentage on folders without MP3s

        self.lcd.write(1, 0, castOptionRows[0][0], 2)  # selectionMarker
        self.lcd.write(1, 2, castOptionRows[0][1][FD.FOLDER], 15)  # folderName
        # percentage
        self.lcd.write(1, 17, formatPercentage3(
            castOptionRows[0][1][FD.PERCENTAGE]), 3)

        self.lcd.write(2, 0, castOptionRows[1][0], 2)  # selectionMarker
        self.lcd.write(2, 2, castOptionRows[1][1][FD.FOLDER], 15)  # folderName
        # percentage
        self.lcd.write(2, 17, formatPercentage3(
            castOptionRows[1][1][FD.PERCENTAGE]), 3)

        self.lcd.write(3, 0, castOptionRows[2][0], 2)  # selectionMarker
        self.lcd.write(3, 2, castOptionRows[2][1][FD.FOLDER], 15)  # folderName
        # percentage
        self.lcd.write(3, 17, formatPercentage3(
            castOptionRows[2][1][FD.PERCENTAGE]), 3)

        currentDialogContext.clearRepaintParts()


class AUDIOBOOK_PLAY:
    def __init__(self, lcd):
        self.lcd = lcd

    def handleButton(self, currentDialogContext, pressedButton):
        print('Audiobook play: handle button action ' + pressedButton)
        if pressedButton == BUTTONS.BUTTON_A:
            print('A - Play/pause')
            currentDialogContext.actions.put(ACTIONS.PLAY_PAUSE)
        elif pressedButton == BUTTONS.BUTTON_B:
            print('B - volup')
            currentDialogContext.actions.put(ACTIONS.VOL_UP)
        elif pressedButton == BUTTONS.BUTTON_C:
            print('C - voldown')
            currentDialogContext.actions.put(ACTIONS.VOL_DOWN)
        elif pressedButton == BUTTONS.BUTTON_D:
            print('D - FF - next track')
            currentDialogContext.actions.put(ACTIONS.NEXT_TRACK)
        elif pressedButton == BUTTONS.BUTTON_E:
            print('E - RR - previous track /// back on hold')
            currentDialogContext.actions.put(ACTIONS.PREVIOUS_TRACK)
        elif pressedButton == BUTTONS.HOLD_BUTTON_E:
            # Hold E -> Back to previous dialog
            currentDialogContext.actions.put(ACTIONS.PAUSE)
            currentDialogContext.currentDialog = AUDIOBOOK_PLAY(self.lcd)

        return currentDialogContext

    def displayDialog(self, currentDialogContext):
        print('Dialog: Play Audiobook ')
        # TODO - painting should be animated:
        # -- scroll titles / folders if they are too long
        # -- switch between track time / total time
        # -- add easteregg?
        # -- -- animated equalizer?
        if shouldPaint(paintAction.ALL, currentDialogContext):
            self.lcd.clear()

        if shouldPaint(paintAction.HEADER, currentDialogContext):
            self.lcd.writeHeader(PLAY_AUDIOBOOK_HEADER)

        book = currentDialogContext.currentlySelectedAudiobook()

        if shouldPaint(paintAction.AUDIOBOOK_TITLE, currentDialogContext):
            self.lcd.write(1, 0, book[FD.FOLDER], 17)  # folderName

        if shouldPaint(paintAction.AUDIOBOOK_PERCENTAGE, currentDialogContext):
            self.lcd.write(1, 17, formatPercentage3(
                book[FD.PERCENTAGE]), 3)  # percentage

        if shouldPaint(paintAction.AUDIOBOOK_TRACK_NAME, currentDialogContext):
            self.lcd.write(2, 0, book[FD.CURRENT_MP3], 20)  # mp3Name

        if shouldPaint(paintAction.AUDIOBOOK_TRACK_NUMBERS, currentDialogContext):
            # TrackNo/TrackCount
            self.lcd.write(
                3, 0, str(book[FD.CURRENT_MP3_IDX]) + '/' + str(len(book[FD.MP3_FILES])), 7)

        if shouldPaint(paintAction.AUDIOBOOK_TIME_NUMBERS, currentDialogContext):
            # currentTrackTime / totalTrackTime
            mc, sc = divmod(book[FD.CURRENT_MP3_PROGRESS], 60)
            mt, st = divmod(
                int(book[FD.MP3_LENGTHS][book[FD.CURRENT_MP3]]), 60)
            timeStatus = '{0:02d}:{1:02d}/{2:02d}:{3:02d}'.format(
                mc, sc, mt, st)

            self.lcd.write(3, 7, timeStatus, 13)

        currentDialogContext.clearRepaintParts()

        currentDialogContext.actions.put(ACTIONS.CHECK_PLAY_STATUS)
