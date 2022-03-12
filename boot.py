import storage, usb_cdc
import board, digitalio

#button used to show the drive
btn = digitalio.DigitalInOut(board.GP9)
btn.direction = digitalio.Direction.INPUT
btn.pull = digitalio.Pull.DOWN

#shows or hides storage and cdc depending on button state
if btn.value:
    storage.enable_usb_drive()
    usb_cdc.enable()
else:
    storage.disable_usb_drive()
    usb_cdc.disable()
