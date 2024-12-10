import queue


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
        repaintParts = []

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
        
        mp3Index = currentBook['currentMp3Idx']
        if mp3Index == 0 and jump < 0:
            return
        if mp3Index == len(currentBook['mp3Files']) + 1 and jump > 0:
            return
        
        mp3Index += jump
        
        # replace currentBook properties completely with new properties:
        self.currentFolderDetails()[self.menu_chooseAudiobook_CursorLocationAbsolute] = 
        {'rootPath': currentBook['rootPath'],
            'folder': currentBook['folder'],
            'mp3Files': currentBook['mp3Files'],
            'mp3Lengths': currentBook['mp3Lengths'],
            'currentMp3': playpointMp3Name,
            'currentMp3Idx': currentMp3Idx,
            'progressDetails': progressDetails,
            'totalTime': currentBook['totalTime'],
            'elapsedTime': elapsedTime,
            'previousMp3Progress': previousMp3Progress,
            'currentMp3Progress': currentMp3Progress,
            'percentage': percentage}
        

        
        
