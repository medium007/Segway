import pygame as pg
import time

print("Hello, this is branch")

pg.init()
pg.joystick.init()

js = pg.joystick.Joystick(0)
js.init()
print(js.get_name())

joystick_count = pg.joystick.get_count()

print("Number of joysticks: {}".format(joystick_count))

buttons = js.get_numbuttons()
print("Number of buttons: {}".format(buttons))

time.sleep(3)


while(1):
    for event in pg.event.get():
        axis = js.get_numaxes()
        for i in range(buttons):
            button = js.get_button(i)
            print("Button {:>2} value: {}".format(i, button))
        for i in range(axis):
            ax = js.get_axis(i)
            print("Axis {} value: {:>6.3f}".format(i, ax))
        print("\n")

