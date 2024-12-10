
import types

# button constants
BUTTONS = types.SimpleNamespace()
BUTTONS.BUTTON_A = 'BUTTON_A'
BUTTONS.BUTTON_B = 'BUTTON_B'
BUTTONS.BUTTON_C = 'BUTTON_C'
BUTTONS.BUTTON_D = 'BUTTON_D'
BUTTONS.BUTTON_E = 'BUTTON_E'

# SYSTEM PROPERTIES
SYSTEM_PROPERTIES = types.SimpleNamespace()
SYSTEM_PROPERTIES.LAST_CAST_DEVICE = 'last-cast-device'
SYSTEM_PROPERTIES.LAST_AUDIOBOOK_ROOT_FOLDER = 'last-audiobook-root-folder'
SYSTEM_PROPERTIES.HTTP_STARTUP_PORT='http-startup-port'

# Play audiobook partial paint actions
PA = types.SimpleNamespace()
# 0123
PA.ALL = 'all'
# 0
PA.HEADER = 'header'
# 1
PA.AUDIOBOOK_TITLE = 'audiobook-title'
PA.AUDIOBOOK_PERCENTAGE = 'audiobook-percentage'
# 2
PA.AUDIOBOOK_TRACK_NAME = 'audiobook-track-name'
# 3
PA.AUDIOBOOK_TRACK_NUMBERS = 'audiobook-track-numbers'
PA.AUDIOBOOK_TIME_NUMBERS = 'audiobook-time-numbers'
