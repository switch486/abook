import gui_lib

gui = gui_lib.LCD()

gui.display(gui_lib.DIALOGS.WELCOME)

# TODO - loop consisting of: display and wait for input

# gui.display(gui_lib.DIALOGS.CHOOSE_CAST, castDevices)
# gui.display(gui_lib.DIALOGS.CHOOSE_WIFI, wifiConnections)
# gui.display(gui_lib.DIALOGS.CHOOSE_AUDIOBOOK, audiobookFolderDetails)
# gui.display(gui_lib.DIALOGS.AUDIOBOOK_PLAY, playDetails)



# loop over menu entries after a button press
## when playing update the view every x seconds based on multimedia state