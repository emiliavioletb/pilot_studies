#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 25 20:37:00 2021

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

#%% Boston naming task

# Setting up trial components 
BNT_clock = core.Clock()
BNTimage_clock = core.Clock()
BNTrest_clock = core.Clock()
BNTword_clock = core.Clock()
BNT_rest = TextStim(win, text=REST, height=0.3)
BNT_instr = TextStim(win, text = BOSTONNAMINGTASK_INSTRUCTIONS1, wrapWidth = 1.5)

# Load in stimuli
stimulus_set = 'white'
filename_stimuli = '/Users/emilia/Documents/Pilot study' + stimulus_set + '/BNT_images.csv'
images_list = pd.read_csv('BNT_images.csv')['images'].tolist()
images = list(chunks(images_list, 4)) 

words = pd.read_csv('BNT_words.csv')['words'].tolist()

# Instructions
BNT_instr.draw()
win.flip()
psychopy.event.waitKeys()
if kb.getKeys(keyList=['escape']):
    shutdown()

blank(0.5)

# Begin images trials
for j in images:
    BNT_start = datetime.now()
    fixation_cross(1)
    
    blank(0.5)

    win.callOnFlip(port.write,'N'.encode()) 

    for i in j: 
        if kb.getKeys(keyList=['escape']):
            shutdown()

        BNT_image_index = j.index(i)
        BNT_image = ImageStim(win, image=i, units='norm', size=(0.6, 0.9))

        win.callOnFlip(port.write, 'D'.encode())
        BNT_clock.reset()

        while BNT_clock.getTime() < 2:
            BNT_image.draw()
            win.flip()

        port.write('d'.encode()) 

        blank(0.5)

        port.write('x'.encode())

        # Data saving
        thisExp.addData('Image shown',i)
        thisExp.addData('Image index',BNT_image_index)
        thisExp.nextEntry()

    port.write('n'.encode()) 

    # Ten seconds of rest
    fixation_cross(1)

    blank(0.5)

    win.callOnFlip(port.write, 'H'.encode())

    BNTrest_clock.reset()

    while BNTrest_clock.getTime() < 10: 
        BNT_rest.draw()
        win.flip()

    # End trigger
    port.write('h'.encode())
    
    blank(1)

    # Data saving
    thisExp.addData('BNT start',BNT_start)
    thisExp.nextEntry()

# Break
takebreak()

# Instructions 
showtext(win, BOSTONNAMINGTASK_INSTRUCTIONS2)
psychopy.event.waitKeys()
if kb.getKeys(keyList=['escape']):
    shutdown()

# Text presentation
for j in words:

    BNT_start = datetime.now()

    if kb.getKeys(keyList=['escape']):
        shutdown()

    BNT_word_index = words.index(j)
    word_presented = TextStim(win, text = j, height=0.2)

    # Is the word sensical or nonsensical?
    if BNT_word_index in [0, 1, 3, 4, 7]:
        word = 'sensical'
        trigger_start_BNT = 'E'
        trigger_stop_BNT = 'e'

    else:
        word = 'non-sensical'
        trigger_start_BNT = 'I'
        trigger_stop_BNT = 'i'

    fixation_cross(1)

    # Present word
    win.callOnFlip(port.write, trigger_start_BNT.encode())
    BNTword_clock.reset()

    while BNTword_clock.getTime() < 10:
        word_presented.draw()
        win.flip()

    # End trigger
    port.write(trigger_stop_BNT.encode())

    # Data saving
    thisExp.addData('Word presented',j)
    thisExp.addData('Type of word presented',word)
    thisExp.addData('Word index',BNT_word_index)
    thisExp.addData('BNT start',BNT_start)
    thisExp.nextEntry()

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