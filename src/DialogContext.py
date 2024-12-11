import queue
from calculator import calculateTimes
from constants import CONSTANTS, FD


class DialogContext:
    currentDialog = None
    actions = queue.Queue()
    systemPropertiesPath = None

    lastCastDevice = ''
    chromecastDevices = ''

    # helper variables
    menu_chooseCast_CursorLocationAbsolute = 0

    menu_chooseAudiobook_CursorLocationAbsolute = 0

    chromecast_device = None

    folderDetails = {}
    currentRootPath = ''

    currentAudiobook = None

    httpServer = None

    # repaint fields in the dialog, handled by its own dialog and cleared after repaint.
    repaintParts = []

    def clearRepaintParts(self):
        self.repaintParts = []

    def paintDialog(self):
        self.currentDialog.displayDialog(self)

    def currentFolderDetails(self):
        return self.folderDetails[self.currentRootPath]

    def currentlySelectedAudiobook(self):
        return self.currentFolderDetails()[self.menu_chooseAudiobook_CursorLocationAbsolute]

    def handleButton(self, pressedButton):
        return self.currentDialog.handleButton(self, pressedButton)

    def moveAudiobookPointerAndGet(self, jump):
        currentBook = self.currentlySelectedAudiobook()

        currentMp3Idx = currentBook['currentMp3Idx']
        if currentMp3Idx == 0 and jump < 0:
            return
        if currentMp3Idx == len(currentBook['mp3Files']) + 1 and jump > 0:
            return

        currentMp3Idx += jump
        playpointMp3Name = currentBook['mp3Files'][currentMp3Idx]

        # replace currentBook properties completely with new properties:
        self.setCurrentFolderProgress(self.calculateCurrentFolderProgress(
            currentMp3Idx, playpointMp3Name, 0, currentBook))

        return self.currentlySelectedAudiobook()

    def setCurrentFolderProgress(self, newFolderDetails):
        self.currentFolderDetails()[
            self.menu_chooseAudiobook_CursorLocationAbsolute] = newFolderDetails

    def calculateCurrentFolderProgress(self, currentMp3Idx, playpointMp3Name, playpointMp3Seconds, currentBook):
        # total and elapsed times
        totalTime, elapsedTime, previousMp3Progress, currentMp3Progress, percentage = calculateTimes(
            playpointMp3Name, playpointMp3Seconds, currentBook['mp3Files'], currentBook['mp3Lengths'])

        # replace currentBook properties completely with new properties:
        return {FD.ROOT_PATH: currentBook[FD.ROOT_PATH],
                FD.FOLDER: currentBook[FD.FOLDER],
                FD.MP3_FILES: currentBook[FD.MP3_FILES],
                FD.MP3_LENGTHS: currentBook[FD.MP3_LENGTHS],
                FD.CURRENT_MP3: playpointMp3Name,
                FD.CURRENT_MP3_IDX: currentMp3Idx,
                FD.TOTAL_TIME: totalTime,
                FD.ELAPSED_TIME: elapsedTime,
                FD.PREVIOS_MP3_PROGRESS: previousMp3Progress,
                FD.CURRENT_MP3_PROGRESS: currentMp3Progress,
                FD.PERCENTAGE: percentage}

    def updateTrackCalculateAudiobook(self, currentMp3Progress):
        currentBook = self.currentlySelectedAudiobook()

        # replace currentBook properties completely with new properties:
        self.setCurrentFolderProgress(self.calculateCurrentFolderProgress(
            currentBook['currentMp3Idx'], currentBook['currentMp3'], currentMp3Progress, currentBook))

        return self.currentlySelectedAudiobook()

    def getCurrentAudiobookProgressFilePath(self):
        book = self.currentlySelectedAudiobook()
        return ''.join([book['rootPath'], '/', book['folder'], '/', CONSTANTS.PROGRESS_FILE])
