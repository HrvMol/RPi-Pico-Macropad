import time
import os
import digitalio
import board
import storage
#HID packages
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
#OLED packages
import busio
import terminalio
import displayio
from adafruit_display_text import label
import adafruit_ssd1327

#setting keyboard as a usb device
keyboard = Keyboard(usb_hid.devices)

#setting start page
f = open("home.txt","r")
keybinds = f.readlines()
f.close()
print(keybinds)

#Display setup
displayio.release_displays()

spi = busio.SPI(board.GP10, MOSI=board.GP11)
oled_cs = board.GP13
oled_dc = board.GP12
display_bus = displayio.FourWire(spi, command=oled_dc, chip_select=oled_cs, baudrate=1000000, reset=board.GP15)

WIDTH = 128
HEIGHT = 128
FONTSCALE = 1

display = adafruit_ssd1327.SSD1327(display_bus, width=WIDTH, height=HEIGHT)

# Make the display context
splash = displayio.Group()
display.show(splash)

btnMax = 5
btnCurrent = 1
lineDist = 15


def btn_settings(btn_pin):
    btn = digitalio.DigitalInOut(btn_pin)
    btn.direction = digitalio.Direction.INPUT
    btn.pull = digitalio.Pull.DOWN
    return btn

def displayOut():
    splash = displayio.Group()
    for i in range(1, 18, 2):
        try:
            print(keybinds[i])
                
            # Draw a label
            text = keybinds[i]
            text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF)
            text_width = text_area.bounding_box[2] * FONTSCALE
            text_group = displayio.Group(
                scale=FONTSCALE,
                x=0,#display.width // 2 - text_width // 2,
                y=7*i#display.height // 2,
            )
            text_group.append(text_area)  # Subgroup for text scaling
            splash.append(text_group)
        except IndexError:
            pass
    display.show(splash)
        
def changePage(page):
    global keybinds
    
    #checks if it is a txt file
    check = keybinds[page].split(".")
    if keybinds[page].count(".") >= 1:
        if check[1] == "txt\r\n":
            f = open(keybinds[page], "r")
            keybinds = f.readlines()
            f.close()
            displayOut()
            
    #pressing keys
    else:
        key = keybinds[page]
        length = key.count(",")
        if length > 0: key = keybinds[page].split(",")
        if length == 1:
            keyboard.press(int(key[0]), int(key[1]))
            time.sleep(0.1)
            keyboard.release(int(key[0]), int(key[1]))
        elif length == 2:
            keyboard.press(int(key[0]), int(key[1]), int(key[2]))
            time.sleep(0.1)
            keyboard.release(int(key[0]), int(key[1]), int(key[2]))
        else:
            keyboard.press(int(key))
            time.sleep(0.1)
            keyboard.release(int(key))
        
    
#assigning button settings
btn1 = btn_settings(board.GP2)
btn2 = btn_settings(board.GP1)
btn3 = btn_settings(board.GP9)
btn4 = btn_settings(board.GP4)
btn5 = btn_settings(board.GP5)
btn6 = btn_settings(board.GP6)
btn7 = btn_settings(board.GP7)
btn8 = btn_settings(board.GP8)
btn9 = btn_settings(board.GP3)

btn1_last = btn2_last = btn3_last = btn4_last = btn5_last = btn6_last = btn7_last = btn8_last = btn9_last = False

#refresh display on start
displayOut()

while True:
    try:      
        if btn1.value != btn1_last:
            if btn1.value:
                changePage(0)
        elif btn2.value != btn2_last:
            if btn2.value:
                changePage(2)
        elif btn3.value != btn3_last:
            if btn3.value:
                changePage(4)
        elif btn4.value != btn4_last:
            if btn4.value:
                changePage(6)
        elif btn5.value != btn5_last:
            if btn5.value:
                changePage(8)
        elif btn6.value != btn6_last:
            if btn6.value:
                changePage(10)
        elif btn7.value != btn7_last:
            if btn7.value:
                changePage(12)
        elif btn8.value != btn8_last:
            if btn8.value:
                changePage(14)
        elif btn9.value != btn9_last:
            if btn9.value:
                changePage(16)
    except IndexError:
        pass
    
    btn1_last = btn1.value
    btn2_last = btn2.value
    btn3_last = btn3.value
    btn4_last = btn4.value
    btn5_last = btn5.value
    btn6_last = btn6.value
    btn7_last = btn7.value
    btn8_last = btn8.value
    btn9_last = btn9.value
    time.sleep(0.01)