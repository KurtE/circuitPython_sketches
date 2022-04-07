import board, busio, digitalio, time
from microcontroller import Pin
from digitalio import DigitalInOut, Direction, Pull

#led = digitalio.DigitalInOut(board.LED)
#led.direction = digitalio.Direction.OUTPUT

# lets first get a list of the boards pins
# temporary exclude led
exclude = ['USB_HOST_DM', 'USB_HOST_DP', 'USB_HOST_POWER', 'LED']

class pinNamesRecord(object):
    def __init__(self, pin, pin_name):
        self.pin = pin
        self.pin_names = pin_name
        self.last_check = False


print("check for all Pins")

all_pins = {}
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

print("\nEnum pin list")
for pin_entry in all_pins:
    pny = all_pins[pin_entry]
    print(pin_entry, "\t", pny.last_check, "\t", pny.pin_names)





loop_count_no_changes = 0
while True:
    pin_changed = False
    for pin_entry in all_pins:
        pny = all_pins[pin_entry]
        new_pin_value = pny.pin.value
        if new_pin_value != pny.last_check:
            if loop_count_no_changes:
                loop_count_no_changes = 0
                print()

            pny.last_check = new_pin_value
            print(pin_entry, "\t", pny.last_check, "\t", pny.pin_names)
            pin_changed = True
    if pin_changed == False:
        loop_count_no_changes += 1
        if loop_count_no_changes < 320:
            if (loop_count_no_changes & 7) == 0:
                print('.', end='')
        else:
            print('.')
            loop_count_no_changes = 0

    time.sleep(0.25)
