import pychromecast


def connectToCastDevice(currentDialogContext):
    chromecasts, browser = pychromecast.get_listed_chromecasts(
        friendly_names=[currentDialogContext.lastCastDevice])
    currentDialogContext.chromecast_device = chromecasts[0]
    currentDialogContext.chromecast_device.wait()


def getAvailableChromecasts(currentDialogContext):
    print('Chromecast - start discovery')
    devices, browser = pychromecast.discovery.discover_chromecasts()
    browser.stop_discovery()
    print('Chromecast - stop discovery')

    print(f"Discovered {len(devices)} device(s):")
    for device in devices:
        print(
            f"  '{device.friendly_name}' ({device.model_name}) @ {device.host}:{device.port} uuid: {device.uuid}"
        )

    return list(map(lambda o: o.friendly_name, devices))
