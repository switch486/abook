from constants import BUTTONS, PA as paintAction, FD, SYSTEM_PROPERTIES, CONSTANTS
import actions as ACTIONS
from os.path import join
from pathlib import PurePosixPath

# BUTTONS                  E   D    C    B    A
# Headers
# Template                'X   X    X    X    X'
CHOOSE_CAST_HEADER = ' | UP  DOWN       OK'
CHOOSE_AUDIOBOOK_HEADER = '<| UP  DOWN       OK'
PLAY_AUDIOBOOK_HEADER = '<| [<  >]  - V + ||>'


def selectionIndicator(startIndex, selectedIndex):
    return '> ' if startIndex == selectedIndex else '  '


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

    result = [
        [selectionIndicator(startIndex, selectedIndex), list[startIndex]]]

    if len(list) > startIndex + 1:
        result.append([selectionIndicator(startIndex + 1, selectedIndex),
                       list[startIndex + 1]])
    if len(list) > startIndex + 2:
        result.append([selectionIndicator(startIndex + 2, selectedIndex),
                       list[startIndex + 2]])

    return result


class WELCOME:

    def __init__(self, lcd):
        self.lcd = lcd

    def handleButton(self, currentDialogContext, pressedButton):
        print('Handle Button ' + pressedButton)
        if pressedButton == BUTTONS.BUTTON_A:
            print('short circuit logic - last audiobook')
            currentDialogContext.currentDialog = AUDIOBOOK_PLAY(self.lcd)
            currentDialogContext.actions.put(ACTIONS.CONNECT_TO_CAST_DEVICE)
            currentDialogContext.actions.put(
                ACTIONS.LOAD_SINGLE_AUDIOBOOK_DETAILS)
            currentDialogContext.actions.put(ACTIONS.PLAY_AUDIOBOOK)
            currentDialogContext.actions.put(
                ACTIONS.UPDATE_LAST_PLAYED_AUDIOBOOK)

        else:
            print('standard navigation case')
            currentDialogContext.currentDialog = CHOOSE_CAST(self.lcd)
        return currentDialogContext

    def displayDialog(self, currentDialogContext):
        print('Dialog: Welcome ')
        self.lcd.clear()
        lastAudiobookFolder = currentDialogContext.systemProperties[
            SYSTEM_PROPERTIES.DEFAULT_AUDIOBOOK_ROOT_FOLDER]

        self.lcd.write(0, 0, '-OK-', 4)
        if lastAudiobookFolder is not None:
            self.lcd.write(0, 11, '-RESUME-', 8)
        self.lcd.write(1, 0, '* Welcome to abook *', 20)
        self.lcd.write(2, 0, currentDialogContext.lastVersionChangeDate, 20)
        self.lcd.write(3, 0, 'Select option above^', 20)
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
            currentDialogContext.systemProperties[SYSTEM_PROPERTIES.LAST_CAST_DEVICE] = currentDialogContext.chromecastDevices[
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
            book = currentDialogContext.currentlySelectedAudiobook()
            print(currentDialogContext.currentRootPath)
            print(book)
            if len(book[FD.AUDIOBOOK_DETAILS_KEY][CONSTANTS.MP3_FILES]) > 0:
                # if audiobook selected - play
                currentDialogContext.currentDialog = AUDIOBOOK_PLAY(self.lcd)
                currentDialogContext.actions.put(ACTIONS.PLAY_AUDIOBOOK)
                currentDialogContext.actions.put(
                    ACTIONS.UPDATE_LAST_PLAYED_AUDIOBOOK)
            else:
                # if folder selected - load audiobooks in it
                currentDialogContext.currentRootPath = join(
                    currentDialogContext.currentRootPath, book[FD.FOLDER])
                currentDialogContext.actions.put(ACTIONS.LOAD_AUDIOBOOKS)
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
            defaultPath = currentDialogContext.systemProperties[
                SYSTEM_PROPERTIES.DEFAULT_AUDIOBOOK_ROOT_FOLDER]
            currentPath = currentDialogContext.currentRootPath
            if defaultPath == currentPath:
                # we are at root, change dialog
                currentDialogContext.currentDialog = CHOOSE_CAST(self.lcd)
            else:
                # we are not at root, navigate up in the folder structure
                currentDialogContext.currentRootPath = PurePosixPath(
                    currentPath).parent.as_posix()
        return currentDialogContext

    def displayDialog(self, currentDialogContext):
        print('Dialog: Choose Audiobook at: ' +
              currentDialogContext.currentRootPath)
        self.lcd.clear()
        self.lcd.writeHeader(CHOOSE_AUDIOBOOK_HEADER)
        castOptionRows = getViewportListFormatted(
            currentDialogContext.currentFolderDetails(),
            currentDialogContext.menu_chooseAudiobook_CursorLocationAbsolute)

        for index in range(len(castOptionRows)):
            i = index + 1
            # selectionMarker
            self.lcd.write(i, 0, castOptionRows[index][0], 2)
            # folderName
            self.lcd.write(i, 2, castOptionRows[index][1][FD.FOLDER], 15)
            # percentage
            if len(castOptionRows[index][1][FD.AUDIOBOOK_DETAILS_KEY][CONSTANTS.MP3_FILES]) > 0:
                self.lcd.write(i, 17, formatPercentage3(
                    castOptionRows[index][1][FD.AUDIOBOOK_DETAILS_KEY][FD.PERCENTAGE]), 3)

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
            print('E - RR - previous track')
            currentDialogContext.actions.put(ACTIONS.PREVIOUS_TRACK)
        elif pressedButton == BUTTONS.HOLD_BUTTON_E:
            print('Hold E - pause and return to audiobook choose')
            currentDialogContext.actions.put(ACTIONS.PAUSE)
            currentDialogContext.currentDialog = CHOOSE_AUDIOBOOK(self.lcd)

        return currentDialogContext

    def displayDialog(self, currentDialogContext):
        mc = currentDialogContext.chromecast_device.media_controller
        if not mc.status.player_is_playing:
            print('Dialog: Play Audiobook - paused')
            return

        print('Dialog: Play Audiobook ')
        # TODO V2 - painting should be animated:
        # -- scroll titles / folders if they are too long
        # -- switch between track time / total time
        # -- add easteregg?
        # -- -- animated equalizer?
        if shouldPaint(paintAction.ALL, currentDialogContext):
            self.lcd.clear()

        if shouldPaint(paintAction.HEADER, currentDialogContext):
            self.lcd.writeHeader(PLAY_AUDIOBOOK_HEADER)

        book = currentDialogContext.currentlySelectedAudiobook()
        bookDetails = book[FD.AUDIOBOOK_DETAILS_KEY]

        if shouldPaint(paintAction.AUDIOBOOK_TITLE, currentDialogContext):
            self.lcd.write(1, 0, book[FD.FOLDER], 17)  # folderName

        if shouldPaint(paintAction.AUDIOBOOK_PERCENTAGE, currentDialogContext):
            self.lcd.write(1, 17, formatPercentage3(
                bookDetails[FD.PERCENTAGE]), 3)  # percentage

        if shouldPaint(paintAction.AUDIOBOOK_TRACK_NAME, currentDialogContext):
            self.lcd.write(
                2, 0, bookDetails[CONSTANTS.PROGRESS_MP3_KEY], 20)  # mp3Name

        if shouldPaint(paintAction.AUDIOBOOK_TRACK_NUMBERS, currentDialogContext):
            # TrackNo/TrackCount
            self.lcd.write(
                3, 0, str(book[FD.CURRENT_MP3_IDX]) + '/' + str(len(bookDetails[CONSTANTS.MP3_FILES])), 7)

        if shouldPaint(paintAction.AUDIOBOOK_TIME_NUMBERS, currentDialogContext):
            # currentTrackTime / totalTrackTime
            mc, sc = divmod(bookDetails[CONSTANTS.PROGRESS_SECOND_KEY], 60)
            mt, st = divmod(
                int(bookDetails[CONSTANTS.MP3_DURATIONS][
                    bookDetails[CONSTANTS.PROGRESS_MP3_KEY]
                ]), 60)
            timeStatus = '{0:02d}:{1:02d}/{2:02d}:{3:02d}'.format(
                mc, sc, mt, st)

            self.lcd.write(3, 7, timeStatus, 13)

        currentDialogContext.clearRepaintParts()

        currentDialogContext.actions.put(ACTIONS.CHECK_PLAY_STATUS)


class EXCEPTION:

    def __init__(self, lcd):
        self.lcd = lcd

    def handleButton(self, currentDialogContext, pressedButton):
        print('Handle Button ' + pressedButton)
        return currentDialogContext

    def displayDialog(self, currentDialogContext):
        print('Dialog: Exception ')
        self.lcd.clear()

        self.lcd.write(0, 0, 'EXCEPTION CAUGTH', 20)
        self.lcd.write(2, 0, 'Let Your dad know', 20)
        self.lcd.write(3, 5, 'sorry', 15)
        currentDialogContext.clearRepaintParts()
