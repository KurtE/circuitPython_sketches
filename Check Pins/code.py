import board, busio, digitalio, time, supervisor
from microcontroller import Pin
from digitalio import DigitalInOut, Direction, Pull

#led = digitalio.DigitalInOut(board.LED)
#led.direction = digitalio.Direction.OUTPUT

# lets first get a list of the boards pins
# temporary exclude led
exclude = ['USB_HOST_DM', 'USB_HOST_DP', 'USB_HOST_POWER', 'LED']
all_pins = {}
print_progress_dots = False

pull_up_or_down = Pull.UP  #default first pass to do Pullup


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
    if pull_up_or_down == Pull.UP:
        print("Setting all pins to PULL up - so test by jumpering pins to GND")
        last_check = True
    else:
        print("Setting all pins to PULL down - so test by jumpering pins to +3.3v")
        last_check = False
    for pin_entry in all_pins:
        pny = all_pins[pin_entry]
        pny.pin.pull = pull_up_or_down
        pny.last_check = last_check
    time.sleep(0.25)

for board_item in dir(board):
    if board_item not in exclude:
        item_attr = getattr(board, board_item)
        if isinstance(item_attr, Pin):
            #print("Check pin: ", board_item, "(",item_attr, ")")
            pin_str = str(item_attr)
            #has names like: board.D33
            pin_str = pin_str[6:] #remove board.
            if pin_str in all_pins:
                if pin_str != board_item:
                    pnr = all_pins[pin_str]
                    pnr.pin_names = pnr.pin_names + ' ' + board_item
                    all_pins[pin_str] = pnr
                    #print("\tDup: ", pnr.pin_names)
            else:
                # new one
                iopin = DigitalInOut(item_attr)
                iopin.direction = Direction.INPUT
                iopin.pull = Pull.UP
                if board_item == pin_str:
                    add_str = board_item
                else:
                    add_str = pin_str + ' ' + board_item
                pnr = pinNamesRecord(iopin, add_str)
                all_pins[pin_str] = pnr
                #print("\tnew: ", pnr.pin_names)
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
    if supervisor.runtime.serial_bytes_available:
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
            if pull_up_or_down == Pull.UP:
                pull_up_or_down = Pull.DOWN
            else:
                pull_up_or_down = Pull.UP

            UpdatePullUpDown()
    # scan the pins
    pin_changed = False
    for pin_entry in all_pins:
        pny = all_pins[pin_entry]
        new_pin_value = pny.pin.value
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
