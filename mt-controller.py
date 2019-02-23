#!/usr/local/bin/python
##
# mt-controller.py
# Copyright: 2019 Perryn Gordon
# License: MIT
# Sets the meter needle position based on the value in the mt.setting file
# Reads the mt.calibration file and the mt.setting file
##
import os
import time
import ast
import RPi.GPIO as GPIO

setting = None
pwmoutpin = 18
loop_delay = 2

GPIO.setmode(GPIO.BOARD)
GPIO.setup(pwmoutpin,GPIO.OUT)
p = GPIO.PWM(pwmoutpin,50)

if not os.path.exists('mt.setting'):
	with open('mt.setting', 'w') as f:
		f.write('0')
		f.close() 
		os.chmod('mt.setting',0o666)

while 1:
        ## read mt.setting
        with open('mt.setting','r') as file:
                new_setting = int(float(file.read().rstrip('\n')))
                file.close()

        ## set meter if value changed
        if new_setting != setting:
                with open('mt.calibration','r') as file:
                        calibration = ast.literal_eval(file.readline())
                        file.close()

                        meter_setting = float(calibration[new_setting])
                        if setting == None:
                                p.start(meter_setting)
                        else:
                                p.ChangeDutyCycle(meter_setting)

                        setting = new_setting


        time.sleep(loop_delay)
