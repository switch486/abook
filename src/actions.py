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
    resumeAudiobookOnCastDevice(currentDialogContext)


def resumeAudiobookOnCastDevice(currentDialogContext):
    mc = currentDialogContext.chromecast_device.media_controller

    port = currentDialogContext.systemProperties[
        SYSTEM_PROPERTIES.HTTP_STARTUP_PORT]
    currentBook = currentDialogContext.currentlySelectedAudiobook()

    trackUrl = ''.join(['http://localhost:', port, '/',
                       currentBook['folder'], '/', currentBook['currentMp3']])
    contentType = 'audio/mp3'
    title = currentBook['folder']
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


def CHECK_PLAY_STATUS(currentDialogContext):
    print('CHECK_PLAY_STATUS')
    # TODO get current play time
    # TODO in case idle, add next track
    # TODO add paint actions depending on state
    # TODO update progress of audiobook
    # TODO save progress of audiobook


def VOL_UP(currentDialogContext):
    # TODO implement
    print('volume up')


def VOL_DOWN(currentDialogContext):
    # TODO implement
    print('volume down')
