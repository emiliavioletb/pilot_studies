#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 25 20:35:31 2021

@author: emilia
"""

from psychopy import visual, core, sound, data, gui, logging
from psychopy.visual import TextStim, ImageStim
from psychopy.hardware import keyboard 
import psychopy.event

import pandas as pd
from datetime import datetime
import os
import serial

#%% Path directories

_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

#%% Setting up the experiment

experimentName = 'Pilot study'
experimentInfo = {'Participant': ''}
dlg = gui.DlgFromDict(dictionary=experimentInfo, sortKeys=False, title=experimentName)
if not dlg.OK:
    print("User pressed 'Cancel'!")
    core.quit()

experimentInfo['date'] = data.getDateStr()
experimentInfo['expName'] = experimentName
experimentInfo['psychopyVersion'] = '2021.2.3'
filename = _thisDir + os.sep + u'data/%s_%s_%s' % (experimentInfo['Participant'], 
                                                  experimentName, experimentInfo['date'])

thisExp = data.ExperimentHandler(name=experimentName, extraInfo=experimentInfo,
                                 originPath='C:/Users/emilia/Desktop/Experiment.py',
                                 savePickle=True, saveWideText=True,
                                 dataFileName=filename)
# Setting up a log file
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)

endExpNow = False  
frameTolerance = 0.001

#%% Event triggers 

port = serial.Serial('/dev/tty.usbserial-FTBXN67J', baudrate=9600)

#%% Setting up parameters

# Key inputs
kb = keyboard.Keyboard()
trial_timer = core.CountdownTimer()

# Set up window
win = visual.Window([1440,900], color=[-1,-1,-1], fullscr=True)

# Monitor frame rate
experimentInfo['frameRate'] = win.getActualFrameRate()
if experimentInfo['frameRate'] != None:
    frameDur = 1.0 / round(experimentInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0

# Hide mouse
win.mouseVisible = False

#%% Text of the various instructions 

WELCOME =   '''Thank you for taking part in this study.
            \nYou shall now complete a series of tasks inbetween which you will be able to take breaks.
            \nPlease press any key to continue.'''

REMAIN_STILL = '''Throughout the experiment, please try to keep your head and forehead as still as possible unless otherwise asked to.
    \nPress any key to begin.'''

EXPERIMENT_END_TEXT = 'Task finished. \n\nPlease take a break and press any key to continue when you are ready...'

STUDY_END_TEXT = 'Study finished. \nPress any key to exit.'

PRESS_ANY_KEY = 'Take a break and press any key to continue when you are ready...'

MOTOR_TASKS = '''Before the experiment begins, you will be asked to perform various motor actions to calibrate the device.
    \nThis will include continuously nodding your head, shaking your head, tapping your index finger and a rest period.
    \nEach movement will be performed continuously for 10 seconds. 
    \nPress any key to begin.''' 

NODDING = 'Nod'

SHAKING = 'Shake your head'

FINGER_TAPPING = 'Tap your index finger'

REST = 'Rest'

RESTINGSTATE_INSTRUCTIONS = '''The first part of this study is a resting state period in which you are not required to do a task and will not be presented with a stimulus.
    \nThis will last for approximately 60 seconds during which you can keep your eyes open or closed.
            \nA sound will play when the 60 seconds is over. \n\nPress any key to begin.'''

VFT_INSTRUCTIONS = '''In the next task, you will be given a category and have to come up with as many words (excluding the names of people or places) within that category as you can in 60 seconds.
        \nPlease say the words aloud as your answers will be recorded.
        \nPlease try to restrict hand and head movements during the task.
            \nPress any key to begin.'''

BOSTONNAMINGTASK_INSTRUCTIONS1 = '''In the next task you will be required to name the stimulus presented when it appears on screen. 
\nPlease say your answers aloud as they are being recorded.
\nFollowing each 10 second block of image naming, there will be 10 seconds of rest. 
\n Please stay as still as possible during rest periods.
        \nPress any key to begin.'''

BOSTONNAMINGTASK_INSTRUCTIONS2 = '''In the next section of the task you will be required to continously repeat the word shown on the screen for 10 seconds. 
\nSome words will be sensical and some will be non-sesical so do not worry about pronounciation. 
       \nPress any key to begin.'''

NBACKTASK_INSTRUCTIONS1 = '''In the final task you will be presented with a sequence of letters.
    \nFor each letter presented, you must decide if you saw the current letter in the previous trial. 
        \nPress any key to continue to the next set of instructions.'''

NBACKTASK_INSTRUCTIONS2 = '''Upon presentation of a letter, please select whether the current letter is the same or different to the letter shown just before. 
\nPress the SPACEBAR if the letter is the same, otherwise do not respond. 
\nPress any key to begin the practice trials.'''

NBACK_BEGIN = '''The practice trials are now over. 
\nThere will now be 3 blocks of testing trials.
\nPress any key to begin.'''

NBACKTASK_INSTRUCTIONS3 = 'nbacktaskinstructions.png'

#%% Some functions

def fixation_cross(duration):
    cross = TextStim(win, text = '+', height=0.3, color=(1, 1, 1))
    cross.draw()
    win.flip()
    core.wait(duration)

def blank(duration):
    blank = TextStim(win, text='')
    blank.draw()
    win.flip()
    core.wait(duration)

def showtext(window, text):
    message = visual.TextStim(window, text=text, wrapWidth = 1.5)
    message.size = 0.5
    message.draw()
    window.flip()

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def takebreak():
    showtext(win, PRESS_ANY_KEY)
    psychopy.event.waitKeys()

def expend():
    showtext(win, EXPERIMENT_END_TEXT)
    psychopy.event.waitKeys()
    if kb.getKeys(keyList=['escape']):
        shutdown()

def shutdown():
    win.close()
    core.quit()

blank_ = TextStim(win, text='')

#%% Verbal-fluency task

# Set up trial components
VFT_clock = core.Clock()
VFT_kb = keyboard.Keyboard()

# Instructions for the VFT experimental blocks
VFT_BLOCK1 = 'Please list all the animals that you can think of.'
VFT_BLOCK2 = 'Please list all the words that you can think of beginning with the letter A.'
VFT_BLOCK3 = 'Please list all the fruits that you can think of.'
VFT_BLOCK4 = 'Please list all the words that you can think of beginning with the letter F.'

all_VFT_instructions = [VFT_BLOCK1, VFT_BLOCK2, VFT_BLOCK3, VFT_BLOCK4]

# Instructions
showtext(win, VFT_INSTRUCTIONS)
psychopy.event.waitKeys()
if kb.getKeys(keyList=['escape']):
    shutdown()

# Begin trial
for j in all_VFT_instructions:

    VFT_start = datetime.now()

    if kb.getKeys(keyList=['escape']):
        shutdown()

    VFT_index = all_VFT_instructions.index(j)    
    presented_category = TextStim(win, text='', height=0.2, wrapWidth=1.5)

    # Identify trial for trigger
    if VFT_index == 0 or VFT_index == 2:
        category = 'semantic fluency'
        trigger_start = 'B'
        trigger_stop = 'b'

    elif VFT_index == 1 or VFT_index == 3:
        category = 'phonemic fluency'
        trigger_start = 'C'
        trigger_stop = 'c'

    fixation_cross(1)

    VFT_clock.reset()

    VFT_start = core.getAbsTime()

    win.callOnFlip(port.write, trigger_start.encode())

    while VFT_clock.getTime() < 60:
        presented_category.text = j + '\n\n' + str(int(60-VFT_clock.getTime()))
        presented_category.draw()
        win.flip()

    port.write(trigger_stop.encode())

    blank(1)

    # Data saving
    thisExp.addData('VFT start',VFT_start)
    thisExp.addData('VFT category', (category + ' ' + str(VFT_index)))
    thisExp.addData('Stimulus',j)
    thisExp.nextEntry()

    if VFT_index != 3:
        takebreak() 
        blank(2)

# Task end 
expend()

win.mouseVisible = True

win.flip()

thisExp.saveAsWideText(filename+'.csv', delim='auto')

thisExp.saveAsPickle(filename)

logging.flush()

# make sure everything is closed down
thisExp.abort()

port.close()

win.close()

core.quit()