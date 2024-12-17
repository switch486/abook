from constants import SYSTEM_PROPERTIES, MS, PA as paintAction, FD, CONSTANTS
import chromecast
import filesystem
import httpServer
from os import popen


def LOAD_CAST_DEVICES(currentDialogContext):
    currentDialogContext.lastCastDevice = currentDialogContext.systemProperties[
        SYSTEM_PROPERTIES.LAST_CAST_DEVICE]
    currentDialogContext.chromecastDevices = chromecast.getAvailableChromecasts(
        currentDialogContext)
    print('Last Cast Device: ' + currentDialogContext.lastCastDevice)
    print(currentDialogContext.chromecastDevices)
    if currentDialogContext.lastCastDevice in currentDialogContext.chromecastDevices:
        currentDialogContext.menu_chooseCast_CursorLocationAbsolute = currentDialogContext.chromecastDevices.index(
            currentDialogContext.lastCastDevice)


def CONNECT_TO_CAST_DEVICE(currentDialogContext):
    print('CONNECT_TO_CAST_DEVICE')
    chromecast.connectToCastDevice(currentDialogContext)


def LOAD_AUDIOBOOKS(currentDialogContext):
    print('LOAD_AUDIOBOOKS')
    filesystem.loadAudiobooks(currentDialogContext)


def stopHttpServer(currentDialogContext):
    if currentDialogContext.httpServer != None:
        print('Stopping HTTP Server')
        httpServer.stopHttpServer(httpServer)
        currentDialogContext.httpServer = None


def PLAY_AUDIOBOOK(currentDialogContext):
    print('PLAY_AUDIOBOOK_PAINT')
    currentDialogContext.repaintParts.append(paintAction.ALL)
    stopHttpServer(currentDialogContext)
    startHttpServer(currentDialogContext)
    playPassedAudiobook(
        currentDialogContext, currentDialogContext.currentlySelectedAudiobook())


def getIPOfCurrentMachine():
    ipAddress = popen(
        'ip -f inet addr show wlan0 | grep -Po \'inet \K[\d.]+\'').read()
    print('IP ADDRESS: ' + ipAddress)
    return ipAddress.strip()


def playPassedAudiobook(currentDialogContext, currentBook):
    mc = currentDialogContext.chromecast_device.media_controller

    port = currentDialogContext.systemProperties[
        SYSTEM_PROPERTIES.HTTP_STARTUP_PORT]

    currentIP = getIPOfCurrentMachine()

    trackUrl = ''.join([CONSTANTS.HTTP_STRING, currentIP, CONSTANTS.COLON, port, CONSTANTS.URL_DIR_SEPARATOR,
                       currentBook[FD.FOLDER], CONSTANTS.URL_DIR_SEPARATOR, currentBook[FD.CURRENT_MP3]])
    contentType = CONSTANTS.CONTENT_TYPE
    title = currentBook[FD.FOLDER]
    current_time = currentBook[FD.CURRENT_MP3_PROGRESS]
    if current_time > 5:
        current_time -= 5
    stream_type = CONSTANTS.STREAM_TYPE_BUFFERED

    mc.play_media(url=trackUrl, content_type=contentType, title=title,
                  current_time=current_time, stream_type=stream_type)
    mc.block_until_active()
    mc.play()


def startHttpServer(currentDialogContext):
    print('Start HTTP Server')
    currentDialogContext.httpServer = httpServer.launchHttpServerInDirectory(
        getIPOfCurrentMachine(),
        currentDialogContext.systemProperties[SYSTEM_PROPERTIES.HTTP_STARTUP_PORT],
        currentDialogContext.currentRootPath)


def PLAY_PAUSE(currentDialogContext):
    print('play/pause')
    mc = currentDialogContext.chromecast_device.media_controller
    if mc.status.player_is_playing:
        mc.pause()
    else:
        mc.play()


def PAUSE(currentDialogContext):
    print('pause')
    mc = currentDialogContext.chromecast_device.media_controller
    mc.pause()


def CHECK_PLAY_STATUS(currentDialogContext):
    print('CHECK_PLAY_STATUS')
    mc = currentDialogContext.chromecast_device.media_controller

    if not mc.status.player_is_playing:
        # in case idle, add next track
        NEXT_TRACK(currentDialogContext)

    elif mc.status.player_is_playing:
        CURRENT_TRACK(currentDialogContext, mc.status.adjusted_current_time)


def CURRENT_TRACK(currentDialogContext, duration):
    currentTrackTime = duration
    currentDialogContext.updateTrackCalculateAudiobook(currentTrackTime)
    currentDialogContext.repaintParts.append(
        paintAction.AUDIOBOOK_TIME_NUMBERS)
    currentDialogContext.repaintParts.append(
        paintAction.AUDIOBOOK_PERCENTAGE)
    saveAudiobookProgress(currentDialogContext)


def VOL_UP(currentDialogContext):
    print('volume up')
    currentDialogContext.chromecast_device.volume_up(0.1)


def VOL_DOWN(currentDialogContext):
    print('volume down')
    currentDialogContext.chromecast_device.volume_down(0.1)


def NEXT_TRACK(currentDialogContext):
    print('NEXT_TRACK')
    audiobook = currentDialogContext.moveAudiobookPointerAndGet(1)
    playPassedAudiobook(currentDialogContext, audiobook)
    currentDialogContext.repaintParts.append(paintAction.ALL)
    saveAudiobookProgress(currentDialogContext)


def PREVIOUS_TRACK(currentDialogContext):
    print('PREVIOUS_TRACK')
    audiobook = currentDialogContext.moveAudiobookPointerAndGet(-1)
    playPassedAudiobook(currentDialogContext, audiobook)
    currentDialogContext.repaintParts.append(paintAction.ALL)
    saveAudiobookProgress(currentDialogContext)


def saveAudiobookProgress(currentDialogContext):
    if currentDialogContext.progressSaveEveryXPaints <= currentDialogContext.progressSaveCounter:
        print('Save Progress of Audiobook')
        currentDialogContext.progressSaveCounter = 0
        filesystem.saveProgress(currentDialogContext)
    else:
        currentDialogContext.progressSaveCounter += 1


def UPDATE_LAST_CAST_DEVICE(currentDialogContext, deviceName):
    print('Update last cast device to: ' + deviceName)
    filesystem.updateSystemProperty(
        currentDialogContext, SYSTEM_PROPERTIES.LAST_CAST_DEVICE, deviceName)
