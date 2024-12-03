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

    def paintDialog(self):
        self.currentDialog.displayDialog(self)
        
    def currentFolderDetails(self): 
       return self.folderDetails[self.currentRootPath]
