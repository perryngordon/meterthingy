#!/usr/local/bin/python
##
# mt-calibrate.py
# Copyright: 2019 Perryn Gordon
# License: MIT
# Calibrate meter to align settings with needle positions.
# Creates the mt.calibration file
##

import RPi.GPIO as GPIO
import time

rpigpio_version = GPIO.VERSION
rpi_info = GPIO.RPI_INFO
rpi_revision = str((GPIO.RPI_INFO['P1_REVISION']))
print("RPi.GPIO v"+rpigpio_version+" running on RPi "+rpi_info['TYPE']+" rev"+rpi_revision)

pwmoutpin = 18
run = True
meter_calibration = {}

GPIO.setmode(GPIO.BOARD)
GPIO.setup(pwmoutpin,GPIO.OUT)

dc = 0
p = GPIO.PWM(pwmoutpin,50)

while run:
        inp = raw_input()
        if len(inp) == 0:

                if dc == 0:
                        dc = 1
                        p.start(dc)
                        p.ChangeDutyCycle(dc)
                        continue

                if dc < 100:
			dc = dc + 1

                p.ChangeDutyCycle(dc)
                continue

        if inp == 'x':
                run = False
                continue

        if int(inp) in range(1,101,1):
                print("adding calibration item")
                meter_calibration[inp] = dc


print(meter_calibration)
with open('mt.calibration','w') as file:
        file.write(str(meter_calibration))



p.stop()
GPIO.cleanup()
