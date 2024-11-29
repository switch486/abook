# TODO - list available cast devices
# connect , play , 
# volume up, volume down


import time
import pychromecast
import zeroconf

def connectToCastDevice (currentDialogContext):
    chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=[currentDialogContext.lastCastDevice])
    currentDialogContext.chromecast_device = chromecasts[0]
    currentDialogContext.chromecast_device.wait()

def getAvailableChromecasts(currentDialogContext):
    devices, browser = pychromecast.discovery.discover_chromecasts()
    # Shut down discovery
    browser.stop_discovery()
    
    print(f"Discovered {len(devices)} device(s):")
    for device in devices:
        print(
            f"  '{device.friendly_name}' ({device.model_name}) @ {device.host}:{device.port} uuid: {device.uuid}"
        )

    return list(map(lambda o: o.friendly_name, devices))
    
# TODO - sort list alphabetically so that the lastly used is on top