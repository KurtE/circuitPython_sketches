import digitalio, analogio, board

pot = analogio.AnalogIn(board.A9)
for i in range(10):
    print(pot.value)
pot.deinit()

print("try the digital")
pot = digitalio.DigitalInOut(board.D23)
pot.direction = digitalio.Direction.OUTPUT
pot.deinit()
pot = analogio.AnalogIn(board.A9)
for i in range(10):
    print(pot.value)
