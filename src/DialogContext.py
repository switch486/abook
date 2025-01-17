import queue
from calculator import calculateTimes
from constants import CONSTANTS, FD


class DialogContext:
    currentDialog = None
    actions = queue.Queue()
    systemPropertiesPath = None
    systemProperties = {}
    
    chromecastDevices = ''

    lastVersionChangeDate = ''

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

    progressSaveEveryXPaints = 10  # about 5 seconds
    progressSaveCounter = 0

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
        currentAudiobookDetails = self.currentlySelectedAudiobook()

        currentMp3Idx = currentAudiobookDetails[FD.CURRENT_MP3_IDX]
        if currentMp3Idx == 0 and jump < 0:
            return
        if currentMp3Idx == len(currentAudiobookDetails[FD.AUDIOBOOK_DETAILS_KEY][CONSTANTS.MP3_FILES]) + 1 and jump > 0:
            return

        currentMp3Idx += jump
        playpointMp3Name = currentAudiobookDetails[FD.AUDIOBOOK_DETAILS_KEY][CONSTANTS.MP3_FILES][currentMp3Idx]
        currentAudiobookDetails[FD.AUDIOBOOK_DETAILS_KEY][CONSTANTS.PROGRESS_MP3_KEY] = playpointMp3Name
        currentAudiobookDetails[FD.AUDIOBOOK_DETAILS_KEY][CONSTANTS.PROGRESS_SECOND_KEY] = 0
        currentAudiobookDetails[FD.CURRENT_MP3_IDX] = currentMp3Idx

        self.updateCurrentFolderProgress(currentAudiobookDetails)

        return self.currentlySelectedAudiobook()

    def updateCurrentFolderProgress(self, currentAudiobookDetails):
        totalTime, elapsedTime, percentage = calculateTimes(
            currentAudiobookDetails[FD.AUDIOBOOK_DETAILS_KEY])

        currentAudiobookDetails[FD.TOTAL_TIME] = totalTime
        currentAudiobookDetails[FD.ELAPSED_TIME] = elapsedTime
        currentAudiobookDetails[FD.PERCENTAGE] = percentage

    def updateTrackCalculateAudiobook(self, currentMp3Progress):
        currentAudiobookDetails = self.currentlySelectedAudiobook()
        
        currentAudiobookDetails[FD.AUDIOBOOK_DETAILS_KEY][CONSTANTS.PROGRESS_SECOND_KEY] = currentMp3Progress

        self.updateCurrentFolderProgress(currentAudiobookDetails)

        return self.currentlySelectedAudiobook()

    def getCurrentAudiobookDetailsFilePath(self):
        book = self.currentlySelectedAudiobook()
        return ''.join([book[FD.ROOT_PATH], FD.PATH_SEPARATOR, book[FD.FOLDER], FD.PATH_SEPARATOR, CONSTANTS.PROGRESS_FILE])
