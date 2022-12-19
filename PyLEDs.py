import board
import neopixel
import time
import signal
from sys import exit

pixels = neopixel.NeoPixel(board.D12, 30)

def exit_handler(signal_received, frame):
    pixels.fill((0, 0, 0))
    print("Script terminated!")
    exit(0)

if __name__ == '__main__':
    # Tell Python to run the handler() function when SIGINT is recieved
    signal.signal(signal.SIGINT, exit_handler) # ctlr + c
    signal.signal(signal.SIGTSTP, exit_handler) # ctlr + z

    while True:
        print("Start blinking different colors")
        # Pass through different colors ... just for test :)
        pixels.fill((0, 0, 255))
        time.sleep(0.5)
        pixels.fill((0, 255, 0))
        time.sleep(0.5)
        pixels.fill((0, 255, 255))
        time.sleep(0.5)
        pixels.fill((255, 0, 0))
        time.sleep(0.5)
        pixels.fill((255, 0, 255))
        time.sleep(0.5)
        pixels.fill((255, 255, 0))
        time.sleep(0.5)
        pixels.fill((255, 255, 255))
        time.sleep(0.5)

else :
    print("Error: name is not main!")