from constants import SYSTEM_PROPERTIES, PA as paintAction
import chromecast
import filesystem
import httpServer


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


def playPassedAudiobook(currentDialogContext, currentBook):
    mc = currentDialogContext.chromecast_device.media_controller

    port = currentDialogContext.systemProperties[
        SYSTEM_PROPERTIES.HTTP_STARTUP_PORT]

    trackUrl = ''.join(['http://localhost:', port, '/',
                       currentBook['folder'], '/', currentBook['currentMp3']])
    contentType = 'audio/mp3'
    title = currentBook['folder']
    # TODO - rewind 5 seconds of audiobook at resume start
    current_time = currentBook['currentMp3Progress']
    stream_type = 'STREAM_TYPE_BUFFERED'

    mc.play_media(url=trackUrl, content_type=contentType, title=title,
                  current_time=current_time, stream_type=stream_type)
    mc.block_until_active()
    mc.play()


def startHttpServer(currentDialogContext):
    print('Start HTTP Server')
    currentDialogContext.httpServer = httpServer.launchHttpServerInDirectory(currentDialogContext.systemProperties[
        SYSTEM_PROPERTIES.HTTP_STARTUP_PORT], currentDialogContext.currentRootPath)


def PLAY_PAUSE(currentDialogContext):
    print('play/pause')
    # mc = curre™ntDialogContext.chromecast_device.media_controller
    # mc.play()
    # mc.pause()
    # TODO implement


def CHECK_PLAY_STATUS(currentDialogContext):
    print('CHECK_PLAY_STATUS')
    # TODO get current play time
    # TODO in case idle, add next track
    # TODO add paint actions depending on state
    # TODO update progress of audiobook
    # TODO save progress of audiobook


def VOL_UP(currentDialogContext):
    print('volume up')
    currentDialogContext.chromecast_device.volume_up(0.1)


def VOL_DOWN(currentDialogContext):
    print('volume down')
    currentDialogContext.chromecast_device.volume_down(0.1)


def NEXT_TRACK(currentDialogContext):
    print('NEXT_TRACK')
    # TODO - move currentAudiobook +1 and reset time to 0
    audiobook = currentDialogContext.currentlySelectedAudiobook()
    playPassedAudiobook(
        currentDialogContext, audiobook)


def PREVIOUS_TRACK(currentDialogContext):
    print('PREVIOUS_TRACK')
    # TODO - move currentAudiobook -1 and reset time to 0 -- at start of chapter first
    audiobook = currentDialogContext.currentlySelectedAudiobook()
    playPassedAudiobook(
        currentDialogContext, audiobook)
