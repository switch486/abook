import buttonshim
import time



button_was_held = False


@buttonshim.on_press(buttonshim.BUTTON_A)
def press_handler(button, pressed):
    print('press A')


@buttonshim.on_release(buttonshim.BUTTON_A)
def release_handler(button, pressed):
    print('release A')


@buttonshim.on_hold(buttonshim.BUTTON_A, hold_time=1)
def hold_handler(button):
    print('hold A')


    time.sleep(15)