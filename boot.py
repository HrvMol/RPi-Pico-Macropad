import storage, usb_cdc
import board, digitalio

btn = digitalio.DigitalInOut(board.GP3)
btn.direction = digitalio.Direction.INPUT
btn.pull = digitalio.Pull.DOWN

if not btn.value:
    storage.disable_usb_drive()
    usb_cdc.disable()
else:
    storage.enable_usb_drive()
    usb_cdc.enable()