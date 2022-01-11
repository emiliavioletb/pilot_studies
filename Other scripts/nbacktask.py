#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 24 10:58:41 2021

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
    \nPress any key to start.'''

EXPERIMENT_END_TEXT = 'Task finished. \n\nPlease take a break and press any key to continue when you are ready...'

STUDY_END_TEXT = 'Study finished. \nPress any key to exit.'

PRESS_ANY_KEY = 'Take a break and press any key to continue when you are ready...'

MOTOR_TASKS = '''Before the experiment begins, you will be asked to perform various motor actions to calibrate the device.
    \nThis will include continuously nodding your head, shaking your head, tapping your index finger and a rest period.
    \nEach movement will be performed continuously for 10 seconds. 
    \nPress any key to start.''' 

NODDING = 'Nod'

SHAKING = 'Shake your head'

FINGER_TAPPING = 'Tap your index finger'

REST = 'Rest'

RESTINGSTATE_INSTRUCTIONS = '''The first part of this study is a resting state period in which you are not required to do a task and will not be presented with a stimulus.
    \nThis will last for approximately 60 seconds during which you can keep your eyes open or closed.
            \nA sound will play when the 60 seconds is over. \n\nPress any key to start.'''

VFT_INSTRUCTIONS = '''In the next task, you will be given a category and have to come up with as many words (excluding the names of people or places) within that category as you can in 60 seconds.
        \nPlease say the words aloud as your answers will be recorded.
        \nPlease try to restrict hand and head movements during the task.
            \nPress any key to start.'''

BOSTONNAMINGTASK_INSTRUCTIONS1 = '''In the next task you will be required to name the stimulus presented when it appears on screen. 
\nPlease say your answers aloud as they are being recorded.
\nFollowing each 10 second block of image naming, there will be 10 seconds of rest. 
\n Please stay as still as possible during rest periods.
        \nPress any key to start.'''

BOSTONNAMINGTASK_INSTRUCTIONS2 = '''In the next section of the task you will be required to continously repeat the word shown on the screen for 10 seconds. 
\nSome words will be sensical and some will be non-sesical so do not worry about pronounciation. 
       \nPress any key to start.'''

NBACKTASK_INSTRUCTIONS1 = '''In the final task you will be presented with a sequence of letters.
    \nFor each letter presented, you must decide if you saw the current letter in the previous trial. 
        \nPress any key to continue to the next set of instructions.'''

NBACKTASK_INSTRUCTIONS2 = 'nbacktaskinstructions1.png'

NBACK_BEGIN = '''The practice trials are now over. 
\nThere will now be 3 blocks of testing trials.
\nPress any key to start.'''

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

#%% N-back task

# Setting up trial components
nback_clock = core.Clock()
nback_clock2 = core.Clock()

nback_kb1 = keyboard.Keyboard()
nback_kb2 = keyboard.Keyboard()

# Loading stimuli
nback_letters1 = pd.read_csv('nback_letters1.csv')['letters'].tolist()
nback_corrAns1 = pd.read_csv('nback_letters1.csv')['corrAns'].tolist()
nback_letters2 = pd.read_csv('nback_letters2.csv')['letters'].tolist()
nback_corrAns2 = pd.read_csv('nback_letters2.csv')['corrAns'].tolist()
practice_letters = pd.read_csv('nback_practice.csv')['letters'].tolist()

nback_list1 = list(chunks(nback_letters1, 30)) 
nback_corrAns = list(chunks(nback_corrAns1, 30)) 

nback_list2 = list(chunks(nback_letters2, 30)) 
nback_corrAns_ = list(chunks(nback_corrAns2, 30))

# Data saving
nback_results = pd.DataFrame(columns = ['Trial number', 
                                        'Block number',
                                        'Stimulus presented', 
                                        'Key pressed', 
                                        'Correct answer', 
                                        'Response', 
                                        'Reaction time'])

nback_results2 = pd.DataFrame(columns = ['Trial number', 
                                         'Block number',
                                        'Stimulus presented', 
                                        'Key pressed', 
                                        'Correct answer', 
                                        'Response', 
                                        'Reaction time'])

# Instructions 
showtext(win, NBACKTASK_INSTRUCTIONS1)
psychopy.event.waitKeys()
if kb.getKeys(keyList=['escape']):
    shutdown()
    
instructions5 = ImageStim(win, image=NBACKTASK_INSTRUCTIONS2, units='norm', size=(1.7, 1.8))
instructions5.draw()
win.flip()
psychopy.event.waitKeys()
if kb.getKeys(keyList=['escape']):
    shutdown()

# Begin practice
for h in practice_letters:

    if kb.getKeys(keyList=['escape']):
        shutdown()

    practice_present = TextStim(win, text=h, height=0.5)

    fixation_cross(0.5)

    practice_present.draw()

    win.flip()

    core.wait(0.5)

    blank(2)

# Start testing trials 
showtext(win, NBACK_BEGIN)
psychopy.event.waitKeys()

# Begin trials for n-back 1 
for (a,b) in zip(nback_list1, nback_corrAns):
    block_number = nback_list1.index(a)
    for j in range(0, len(a)):

        nback1_start = datetime.now()

        if kb.getKeys(keyList=['escape']):
            shutdown()

        corrAns = b[j]
        thisLetter = a[j]
        letter_present = TextStim(win, text=a[j], height=0.5)

        fixation_cross(0.5)
        
        # Use clock-based timing
        nback_clock.reset()

        start_marker_sent = False
        key_pressed = False
        win.callOnFlip(nback_kb1.clock.reset)

        while nback_clock.getTime() < 2.5:
            if nback_clock.getTime() < 0.5:
                letter_present.draw()
                if start_marker_sent == False:
                    win.callOnFlip(port.write, 'F'.encode())
                    start_marker_sent = True
            else:
                blank_.draw()

            win.flip()

            if key_pressed == False:
                keys_n = nback_kb1.getKeys(keyList = ['space'], waitRelease=False) 
                if len(keys_n) > 0:
                    key_pressed = True

        port.write('f'.encode())

        if key_pressed == False:
            response = 'none'
            RT = '0'
            if str(corrAns) == 'none':
                answer = 1
            else:
                answer = 0

        elif key_pressed == True:
            response = str(keys_n[-1].name)
            RT = str(keys_n[-1].rt)
            if str(corrAns) == response:
                answer = 1
            elif str(corrAns) != response:
                answer = 0                          

        else:
            answer = 'error'

        # Saving trial data
        thisExp.addData('N back RT',RT)
        thisExp.addData('Stimulus presented',thisLetter)
        thisExp.addData('N back response',answer)
        thisExp.addData('N back start',nback1_start)
        thisExp.addData('Key pressed', response)
        thisExp.addData('Trial number', j)
        thisExp.addData('Block number', block_number)
        thisExp.nextEntry()

        # Saving response data
        nback_results = nback_results.append({'Trial number': j, 
                                              'Block number': block_number,
                                                'Stimulus presented': thisLetter,
                                                'Key pressed': response,
                                                'Correct answer': str(corrAns),
                                                'Response': answer,
                                                'Reaction time': RT}, ignore_index=True)

    if block_number != 2:
        takebreak() 
        blank(2)

# Save results to CSV
nback_filename1 = 'P' + experimentInfo['Participant'] +'_nbackresults1.csv'
nback_results.to_csv(nback_filename1, header=True)

# Instructions
instructions3 = ImageStim(win, image=NBACKTASK_INSTRUCTIONS3, units='norm', size=(1.7, 1.9))
instructions3.draw()
win.flip()
psychopy.event.waitKeys()
if kb.getKeys(keyList=['escape']):
    shutdown()

# Begin trials for n-back 2
for (a,b) in zip(nback_list2, nback_corrAns_):
    
    block_number = nback_list2.index(a)
    
    for j in range(0, len(a)):

        nback2_start = datetime.now()

        if kb.getKeys(keyList=['escape']):
            shutdown()

        corrAns2 = b[j]
        thisLetter2 = a[j]
        letter_present2 = TextStim(win, text=a[j], height=0.5)

        fixation_cross(0.5)
        
        # Use clock-based timing
        nback_clock.reset()

        start_marker_sent2 = False

        key_pressed2 = False

        win.callOnFlip(nback_kb2.clock.reset)

        while nback_clock.getTime() < 2.5:
            if nback_clock.getTime() < 0.5:
                letter_present2.draw()
                if start_marker_sent2 == False:
                    win.callOnFlip(port.write, 'F'.encode())
                    start_marker_sent2 = True
            else:
                blank_.draw()

            win.flip()

            if key_pressed2 == False:
                keys_n2 = nback_kb2.getKeys(keyList = ['space'], waitRelease=False) 
                if len(keys_n2) > 0:
                    key_pressed2 = True

        port.write('f'.encode())

        if key_pressed2 == False:
            response2 = 'none'
            RT2 = '0'
            if str(corrAns2) == 'none':
                answer2 = 1
            else:
                answer2 = 0

        elif key_pressed2 == True:
            response2 = str(keys_n2[-1].name)
            RT2 = str(keys_n2[-1].rt)
            if str(corrAns2) == response2:
                answer2 = 1
            elif str(corrAns2) != response2:
                answer2 = 0                          
        else:
            answer2 = 'error'

        # Saving trial data
        thisExp.addData('N back RT',RT2)
        thisExp.addData('Stimulus presented',thisLetter2)
        thisExp.addData('N back response',answer2)
        thisExp.addData('N back start',nback2_start)
        thisExp.addData('Key pressed', response2)
        thisExp.addData('Trial number', j)
        thisExp.addData('Block number', block_number)
        thisExp.nextEntry()

        # Saving response data
        nback_results2 = nback_results2.append({'Trial number': j, 
                                              'Block number': block_number,
                                                'Stimulus presented': thisLetter2,
                                                'Key pressed': response2,
                                                'Correct answer': str(corrAns2),
                                                'Response': answer2,
                                                'Reaction time': RT2}, ignore_index=True)

    if block_number != 2:
        takebreak() 
        blank(2)

# Save results to CSV
nback_filename2 = 'P' + experimentInfo['Participant'] +'_nbackresults2.csv'
nback_results2.to_csv(nback_filename2)

#%% Ending the study
showtext(win, STUDY_END_TEXT)

core.wait(5)

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