import machine
import time
import select
import sys
from machine import Pin
board = Pin.board

exclude = ['__class__ ', '__name__', '__bases__', '__dict__']
all_pins = {}
print_progress_dots = False

pull_up_or_down = Pin.PULL_UP  #default first pass to do Pullup


class pinNamesRecord(object):
    def __init__(self, pin, pin_name):
        self.pin = pin
        self.pin_names = pin_name
        self.last_check = True

def print_pin_table():
    print("\nEnum pin list")
    print("Physical Pins\tLogical Names")
    for pin_entry in all_pins:
        pny = all_pins[pin_entry]
        print(pin_entry, "\t", pny.pin_names)

def UpdatePullUpDown():
    print()
    if pull_up_or_down == Pin.PULL_UP:
        print("Setting all pins to PULL up - so test by jumpering pins to GND")
        last_check = True
    else:
        print("Setting all pins to PULL down - so test by jumpering pins to +3.3v")
        last_check = False
    for pin_entry in all_pins:
        pny = all_pins[pin_entry]
        pin = pny.pin
        pin.init( mode=Pin.IN, pull=pull_up_or_down)
        pny.last_check = last_check
    time.sleep(0.25)

for board_item in dir(board):
    if board_item not in exclude:
        item_attr = getattr(board, board_item)
        pin_str = str(item_attr)
        if pin_str.startswith("Pin("):
            #print("Check pin: ", board_item, "(",item_attr, ")")
            #has names like: board.D33
            pin_str = pin_str[4:-1] #remove PIN( and trailing)
            if pin_str in all_pins:
                pnr = all_pins[pin_str]
                pnr.pin_names = pnr.pin_names + ' ' + board_item
                all_pins[pin_str] = pnr
            else:
                # new one
                #iopin = Pin(board_item, Pin.IN Pin.PULL_UP)
                iopin = item_attr
                iopin.init( mode=Pin.IN, pull=Pin.PULL_UP)
                add_str = board_item
                pnr = pinNamesRecord(iopin, add_str)
                all_pins[pin_str] = pnr

print_pin_table()

UpdatePullUpDown()
#print_pin_table()
print("A Python version of the Pin High/Low test")
print("Simple keyboard interface")
print("\tEmpty line, will toggle between IO pins Pulled UP and Pulled Down")
print("\tp - print pin table out showing all pin names for pin")
print("\t. - will toggle printing progress dots on or off")

loop_count_no_changes = 0
while True:
    #check for User Input
    avail = select.select([sys.stdin], [], [], 0)
    if avail != ([], [], []): #supervisor.runtime.serial_bytes_available:
        text = input()
        print("*** Serial input ***", text)
        if text == 'p' or text == 'P':
            print_pin_table()
        elif text == '.':
            if print_progress_dots:
                print_progress_dots = False
                print("** Turned off progress dots ***")
            else:
                print_progress_dots = True
                print("** Turned off progress dots ***")
        else:
            if pull_up_or_down == Pin.PULL_UP:
                pull_up_or_down = Pin.PULL_DOWN
            else:
                pull_up_or_down = Pin.PULL_UP

            UpdatePullUpDown()
    # scan the pins
    pin_changed = False
    for pin_entry in all_pins:
        pny = all_pins[pin_entry]
        new_pin_value = pny.pin.value()
        if new_pin_value != pny.last_check:
            if loop_count_no_changes:
                loop_count_no_changes = 0
                if print_progress_dots:
                    print()
            pny.last_check = new_pin_value
            if pny.last_check:
                print("HIGH: ", end='')
            else:
                print("LOW: ", end='')
            print(pny.pin_names)
            pin_changed = True
    if pin_changed == False:
        loop_count_no_changes += 1
        if loop_count_no_changes < 320:
            if (loop_count_no_changes & 7) == 0:
                if print_progress_dots:
                    print('.', end='')
        else:
            if print_progress_dots:
                print('.')
            loop_count_no_changes = 0

    time.sleep(0.25)
