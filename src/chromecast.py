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
    currentDialogContext.zeroconf = zeroconf.Zeroconf()
    browser = pychromecast.CastBrowser(
        pychromecast.SimpleCastListener(
            lambda uuid, 
            service: print(browser.devices[uuid].friendly_name)), 
        currentDialogContext.zeroconf)
    browser.start_discovery()
    #TODO - somehow gather the serach results
    pychromecast.discovery.stop_discovery(browser)
    return 'some List'


#TODO - test it!

#https://github.com/home-assistant-libs/pychromecast/blob/master/examples/discovery_example2.py
#devices, browser = pychromecast.discovery.discover_chromecasts(
#    known_hosts=args.known_host
#)
## Shut down discovery
#browser.stop_discovery()
#
#print(f"Discovered {len(devices)} device(s):")
#for device in devices:
#    print(
#        f"  '{device.friendly_name}' ({device.model_name}) @ {device.host}:{device.port} uuid: {device.uuid}"
#    )
#    if args.verbose:
#        print(f"  service: {device}")


# TODO - sort list alphabetically so that the lastly used is on top