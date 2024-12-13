
import types

# button constants
BUTTONS = types.SimpleNamespace()
BUTTONS.BUTTON_A = 'BUTTON_A'
BUTTONS.BUTTON_B = 'BUTTON_B'
BUTTONS.BUTTON_C = 'BUTTON_C'
BUTTONS.BUTTON_D = 'BUTTON_D'
BUTTONS.BUTTON_E = 'BUTTON_E'

BUTTONS.HOLD_BUTTON_E = 'HOLD_BUTTON_E'

# SYSTEM PROPERTIES
SYSTEM_PROPERTIES = types.SimpleNamespace()
SYSTEM_PROPERTIES.LAST_CAST_DEVICE = 'last-cast-device'
SYSTEM_PROPERTIES.LAST_AUDIOBOOK_ROOT_FOLDER = 'last-audiobook-root-folder'
SYSTEM_PROPERTIES.HTTP_STARTUP_PORT = 'http-startup-port'

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

# MEDIA PLAYER STATUSES
MS = types.SimpleNamespace()
MS.PLAYING = 'PLAYING'

# Filehandling
CONSTANTS = types.SimpleNamespace()
CONSTANTS.PROGRESS_FILE = 'abook.progress'
CONSTANTS.PROGRESS_MP3_KEY = 'currentMp3'
CONSTANTS.PROGRESS_SECOND_KEY = 'second'
CONSTANTS.CONTENT_TYPE = 'audio/mp3'
CONSTANTS.STREAM_TYPE_BUFFERED = 'STREAM_TYPE_BUFFERED'
CONSTANTS.LOCALHOST_URL_PART = 'http://localhost:'
CONSTANTS.MP3_FILETYPE = '.mp3'
CONSTANTS.URL_DIR_SEPARATOR = '/'

# FOLER DETAILS KEYS
FD = types.SimpleNamespace()
FD.ROOT_PATH = 'rootPath'
FD.FOLDER = 'folder'
FD.MP3_FILES = 'mp3Files'
FD.MP3_LENGTHS = 'mp3Lengths'
FD.CURRENT_MP3 = 'currentMp3'
FD.CURRENT_MP3_IDX = 'currentMp3Idx'
FD.TOTAL_TIME = 'totalTime'
FD.ELAPSED_TIME = 'elapsedTime'
FD.PREVIOS_MP3_PROGRESS = 'previousMp3Progress'
FD.CURRENT_MP3_PROGRESS = 'currentMp3Progress'
FD.PERCENTAGE = 'percentage'
FD.PATH_SEPARATOR = '/'

# File Open Actions
FO = types.SimpleNamespace()
FO.READ = 'r'
FO.WRITE_CREATE = 'w+'
FO.WRITE = 'w'
FO.COMMENT = '#'
FO.EQUALS = '='
FO.NEWLINE = '\n'
