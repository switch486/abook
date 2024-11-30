import queue

class DialogContext:
   currentDialog = None
   actions = queue.Queue()
   
   lastCastDevice = ''
   chromecastDevices = ''
   
   # helper variables
   menu_chooseCast_ViewpointStart=0
   menu_chooseCast_ViewpointEnd=2
   menu_chooseCast_CursorLocationAbsolute=0
   
   chromecast_device=None
   
   def paintDialog(self):
      self.currentDialog.displayDialog(self)
