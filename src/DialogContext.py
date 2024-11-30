import queue


class DialogContext:
    currentDialog = None
    actions = queue.Queue()
    systemPropertiesPath = None

    lastCastDevice = ''
    chromecastDevices = ''

    lastAudiobook = ''
    audiobooks = ''

    # helper variables
    menu_chooseCast_ViewpointStart = 0
    menu_chooseCast_ViewpointEnd = 2
    menu_chooseCast_CursorLocationAbsolute = 0
    
    menu_chooseAudiobook_CursorLocationAbsolute = 0

    chromecast_device = None

    def paintDialog(self):
        self.currentDialog.displayDialog(self)
