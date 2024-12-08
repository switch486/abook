from constants import BUTTONS
import actions as ACTIONS

# BUTTONS                  E   D    C    B    A
# Headers
# Template                'X   X    X    X    X'
CHOOSE_CAST_HEADER = ' | UP  DOWN       OK'
CHOOSE_AUDIOBOOK_HEADER = '<| UP  DOWN       OK'
# TODO - back option on hold?
PLAY_AUDIOBOOK_HEADER = '<| [<  >]  - V + ||>'


def selectionIndicator(startIndex, selectedIndex):
    return '> ' if startIndex == selectedIndex else '  '


def join(str1, str2, str3='', str4=''):
    return ''.join([str1, str2, str3, str4])


def formatPercentage3(string):
    number = int(string)
    return f"{number:02}%"


def formatStringForAudiobooksDisplay(selectionMarker, title, percentage):
    title = ''.join([selectionMarker, trunc(title, 15)])
    percentage = formatPercentage3(percentage)
    spacesBetween = 20 - len(title) - len(percentage)
    return ''.join([title, ' ' * spacesBetween, percentage, '\n\r'])


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
        self.lcd.write(1, 0, ''.join(castOptionRows[0]))
        self.lcd.write(2, 0, ''.join(castOptionRows[1]))
        self.lcd.write(3, 0, ''.join(castOptionRows[2]))


class CHOOSE_AUDIOBOOK:
    def __init__(self, lcd):
        self.lcd = lcd

    def handleButton(self, currentDialogContext, pressedButton):
        print('ChooseAudiobook ' + pressedButton)
        if pressedButton == BUTTONS.BUTTON_A:
            # play audiobook
            currentDialogContext.currentDialog = AUDIOBOOK_PLAY(self.lcd)
            # TODO - add action to setup the HTTP server for playing
            # TODO - add action to trigger the play of the audiobook selected at the specific place, with the specific title, ...
        elif pressedButton == BUTTONS.BUTTON_D:
            # DOWN
            if currentDialogContext.menu_chooseAudiobook_CursorLocationAbsolute < len(currentDialogContext.currentFolderDetails())-1:
                currentDialogContext.menu_chooseAudiobook_CursorLocationAbsolute += 1
        elif pressedButton == BUTTONS.BUTTON_E:
            # UP
            if currentDialogContext.menu_chooseAudiobook_CursorLocationAbsolute > 0:
                currentDialogContext.menu_chooseAudiobook_CursorLocationAbsolute -= 1
        return currentDialogContext

    def displayDialog(self, currentDialogContext):
        print('Dialog: Choose Audiobook ')
        self.lcd.clear()
        self.lcd.writeHeader(CHOOSE_AUDIOBOOK_HEADER)
        castOptionRows = getViewportListFormatted(
            currentDialogContext.currentFolderDetails(),
            currentDialogContext.menu_chooseAudiobook_CursorLocationAbsolute)

        self.lcd.write(1, 0, castOptionRows[0][0], 2) # selectionMarker
        self.lcd.write(1, 2, castOptionRows[0][1]['folder'], 15) # folderName
        self.lcd.write(1, 17, castOptionRows[0][1]['percentage'], 3) # percentage
        
        self.lcd.write(2, 0, castOptionRows[1][0], 2) # selectionMarker
        self.lcd.write(2, 2, castOptionRows[1][1]['folder'], 15) # folderName
        self.lcd.write(2, 17, castOptionRows[1][1]['percentage'], 3) # percentage
        
        self.lcd.write(3, 0, castOptionRows[2][0], 2) # selectionMarker
        self.lcd.write(3, 2, castOptionRows[2][1]['folder'], 15) # folderName
        self.lcd.write(3, 17, castOptionRows[2][1]['percentage'], 3) # percentage


class AUDIOBOOK_PLAY:
    def __init__(self, lcd):
        self.lcd = lcd

    def handleButton(self, currentDialogContext, pressedButton):
        print('Audiobook play: handle button action ' + pressedButton)
        # TODO Implement
        if pressedButton == BUTTONS.BUTTON_A:
            print('A - Play/pause')
        elif pressedButton == BUTTONS.BUTTON_B:
            print('B - volup')
        elif pressedButton == BUTTONS.BUTTON_C:
            print('C - voldown')
        elif pressedButton == BUTTONS.BUTTON_D:
            print('D - FF - next track')
        elif pressedButton == BUTTONS.BUTTON_E:
            print('E - RR - previous track /// back on hold')
        return currentDialogContext

    def displayDialog(self, currentDialogContext):
        print('Dialog: Play Audiobook ')
        # TODO - painting should be animated:
        # -- scroll titles / folders if they are too long
        # -- switch between track time / total time
        # -- add easteregg?
        # -- -- animated equalizer?
        #TODO - conditionally repaint everything
        self.lcd.clear()
        self.lcd.writeHeader(PLAY_AUDIOBOOK_HEADER)
        book = currentDialogContext.currentlySelectedAudiobook()
        
        self.lcd.write(1, 0, book['folder'], 17) # folderName
        self.lcd.write(1, 17, formatPercentage3(book['percentage']), 3) # percentage
        self.lcd.write(2, 0, book['currentMp3'], 20) # mp3Name
        
        # TrackNo/TrackCount 
        self.lcd.write(3, 0, str(book['currentMp3Idx']) + '/' + str(len(book['mp3Files'])), 7)
        
        # currentTrackTime / totalTrackTime
        mc, sc = divmod(book['currentMp3Progress'], 60)
        mt, st = divmod(int(book['mp3Lengths'][book['currentMp3']]), 60)
        timeStatus = '{0:02d}:{1:02d}/{2:02d}:{3:02d}'.format(mc, sc, mt, st)

        self.lcd.write(3, 7, timeStatus, 13)

        # TODO - add action to get current play time from cast device and update the current state
        # TODO - add action to see if the track is not finished
        #currentDialogContext.actions.put(
        #    ACTIONS.PLAY_AUDIOBOOK_PAINT(self.displayDialog))


class TEST:
    def __init__(self, lcd):
        self.lcd = lcd

    def handleButton(self, currentDialogContext, pressedButton):
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
