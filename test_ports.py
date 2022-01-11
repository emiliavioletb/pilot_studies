
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 22 11:12:45 2021

@author: Emilia
"""

import serial
from psychopy import core, visual
from psychopy.visual import TextStim


port = serial.Serial('/dev/tty.usbserial-FTBXN67J', baudrate=9600)

win = visual.Window([2560,1600], color=[-1,-1,-1], fullscr=True)
text = TextStim(win, text='Test')
text.draw()
win.flip()
port.write('T'.encode())
core.wait(5)
port.write('T'.encode())

port.close()
win.close()
core.quit()