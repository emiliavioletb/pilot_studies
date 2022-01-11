# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
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

port = serial.Serial('/dev/cu.usbserial-FTBXN67J', baudrate=9600)

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

EXPERIMENT_END_TEXT = 'Task finished. \nPlease take a break and press any key to continue when you are ready...'

STUDY_END_TEXT = 'Study finished. \nPress any key to exit.'

PRESS_ANY_KEY = 'Take a break and press any key to continue when you are ready.'

MOTOR_TASKS = '''Before the experiment begins, you will be asked to perform various motor actions to calibrate the device.
    \nThis will include continuously nodding your head, shaking your head, tapping your index finger and a rest period.
    \nEach movement will be performed for 10 seconds. 
    \nPress any key to begin.''' 

NODDING = 'Nod'

SHAKING = 'Shake your head'

FINGER_TAPPING = 'Tap your index finger'

REST = 'Rest'

RESTINGSTATE_INSTRUCTIONS = '''The first part of this study is a resting state period in which you are not required to do a task and will not be presented with a stimulus.
    \nThis will last for approximately 60 seconds during which you can keep your eyes open or closed.
            \nA sound will play when the 60 seconds is over. \nPress any key to begin.'''

VFT_INSTRUCTIONS = '''In the next task, you will be given a category and have to come up with as many words (excluding the names of people or places) within that category as you can in 60 seconds.
        \nPlease say the words aloud as your answers will be recorded.
        \nPlease try to restrict hand and head movements during the task.
            \nPress any key to begin.'''

BOSTONNAMINGTASK_INSTRUCTIONS1 = '''In the next task you will be required to name the stimulus presented when it appears on screen. 
\nPlease say your answers aloud as they are being recorded.
\nFollowing each 10 second block of word repetition, there will be 10 seconds of rest. 
\n Please stay still as still as possible during rest periods.
        \nPress any key to begin.'''

BOSTONNAMINGTASK_INSTRUCTIONS2 = '''In the next section of the task you will be required to continously repeat the word shown on the screen for 10 seconds. 
        \nPress any key to begin.'''

NBACKTASK_INSTRUCTIONS1 = '''In the next task you will be presented with a sequence of letters.
    \nFor each letter presented, you must decide if you saw the current letter in the previous trial. 
        \nPress any key to continue to the next set of instructions.'''

NBACKTASK_INSTRUCTIONS2 = '''Upon presentation of a letter, please select whether the current letter is the same or different to the previous letter. 
\nPress the SPACEBAR if the letter is the same, otherwise do not respond. 
\nPress any key to begin the practice trials.'''

NBACK_BEGIN = 'Practice trials over. Press any key to begin the testing trials.'
        
NBACKTASK_INSTRUCTIONS3 = '''In the next section of the task, you will repeat the same task but instead of deciding whether the current letter is the same as the previous, you must decide if you saw the current letter 2 trials ago. 
\nPress the LEFT arrow for YES and the RIGHT arrow for NO. 
\nPress any key to begin.'''

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
    
    
#%% WELCOME SCREEN

# Instructions
showtext(win, WELCOME)
psychopy.event.waitKeys()
if kb.getKeys(keyList=['escape']):
    shutdown()
    
showtext(win, REMAIN_STILL)
psychopy.event.waitKeys()
if kb.getKeys(keyList=['escape']):
    shutdown()

#%% Finger tapping & nodding

# Set up trial components 
nodding_clock = core.Clock()
tapping_clock = core.Clock()
shaking_clock = core.Clock()
rest_clock = core.Clock()

nodding_text = TextStim(win, text=NODDING, height=0.2)
shaking_text = TextStim(win, text=SHAKING, height=0.2)
tapping_text = TextStim(win, text=FINGER_TAPPING, height=0.2)
rest_text = TextStim(win, REST, height=0.2)
motor_break_text = TextStim(win, PRESS_ANY_KEY, height=0.2)
num_trials = 3

# Instructions
showtext(win, MOTOR_TASKS)
key = psychopy.event.waitKeys()
if kb.getKeys(keyList=['escape']):
    shutdown()

# Begin trials
for i in range(0, num_trials):
    
    Motor_clock = datetime.now()
    
    if kb.getKeys(keyList=['escape']):
        shutdown()
        
    # Nodding trials
    fixation_cross(1)
    nodding_text.draw()
    if kb.getKeys(keyList=['escape']):
        shutdown()
    win.callOnFlip(port.write, 'J'.encode())
    nodding_clock.reset()
    
    while nodding_clock.getTime() < 10:
          nodding_text.draw()
          win.flip()
    
    port.write('j'.encode())
    
    blank(1)
    
    # Tapping
    fixation_cross(1)
    tapping_text.draw()
    if kb.getKeys(keyList=['escape']):
        shutdown()
    win.callOnFlip(port.write, 'K'.encode())
    tapping_clock.reset()
    
    while tapping_clock.getTime() < 10:
          tapping_text.draw()
          win.flip()    
          
    port.write('k'.encode())
    
    blank(1)
    
    # Rest
    fixation_cross(1)
    rest_text.draw()
    if kb.getKeys(keyList=['escape']):
        shutdown()
    win.callOnFlip(port.write, 'L'.encode())
    rest_clock.reset()
    
    while rest_clock.getTime() < 10:
          rest_text.draw()
          win.flip() 
    
    port.write('l'.encode())
    
    blank(1)
    
    # Shaking
    fixation_cross(1)
    shaking_text.draw()
    if kb.getKeys(keyList=['escape']):
        shutdown()
    win.callOnFlip(port.write, 'M'.encode())
    shaking_clock.reset()
        
    while shaking_clock.getTime() < 10:
          shaking_text.draw()
          win.flip()

    port.write('m'.encode())
    
    blank(1)
    
    if i != 2:
        motor_break_text.draw()
        win.flip()
        
        psychopy.event.waitKeys()
        
        blank(2)
    
    # Data saving
    thisExp.addData('Motor start',Motor_clock)
    thisExp.nextEntry()
    
# Task end
expend()

#%% Resting state instructions

# Set up trial components
restingstate_clock = core.Clock()
restingstate_sound = sound.Sound('beep.wav')
blank_ = TextStim(win, text='')

# Instructions

showtext(win, RESTINGSTATE_INSTRUCTIONS)
psychopy.event.waitKeys()
if kb.getKeys(keyList=['escape']):
    shutdown()

fixation_cross(1)

restingstate_clock.reset()
blank_.draw()
win.callOnFlip(port.write, 'A'.encode())
restingstate_start = datetime.now()

while restingstate_clock.getTime() < 60:    
    
    if kb.getKeys(keyList=['escape']):
        shutdown()
        
    blank_.draw()
    win.flip()
        
port.write('a'.encode()) 

restingstate_stop = datetime.now()
restingstate_sound.play()

# Data saving
thisExp.addData('Resting state start',restingstate_start)
thisExp.addData('Resting state stop',restingstate_stop)
thisExp.nextEntry()

# Task end
expend()

#%% Verbal-fluency task

# Set up trial components
VFT_clock = core.Clock()
VFT_kb = keyboard.Keyboard()

# Instructions for the VFT experimental blocks
VFT_BLOCK1 = 'Please list all the animals that you can think of.'
VFT_BLOCK2 = 'Please list all the words that you can think of beginning with the letter A.'
VFT_BLOCK3 = 'Please list all the fruits that you can think of.'
VFT_BLOCK4 = 'Please list all the words that you can think of which begin with the letter F.'

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

fixation_cross(1)

# Begin images trials
for j in images:
    
    BNT_start = datetime.now()
    fixation_cross(1)
    
    win.callOnFlip(port.write,'N'.encode()) 
    
    for i in j: 
        
        if kb.getKeys(keyList=['escape']):
            shutdown()
        
        BNT_image_index = j.index(i)
        BNT_image = ImageStim(win, image=i, units='norm', size=(0.6, 0.9))
        if kb.getKeys(keyList=['escape']):
            shutdown()

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
    blank(1)
    
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
    
#%% N-back task

# Setting up trial components
nback_clock = core.Clock()
nback_clock2 = core.Clock()

nback_kb1 = keyboard.Keyboard()
nback_kb2 = keyboard.Keyboard()
fix_cros = TextStim(win, text='+', height=0.15)

# Loading stimuli
nback_letters1 = pd.read_csv('nback_letters1.csv')['letters'].tolist()
nback_corrAns1 = pd.read_csv('nback_letters1.csv')['corrAns'].tolist()
nback_letters2 = pd.read_csv('nback_letters2.csv')['letters'].tolist()
nback_corrAns2 = pd.read_csv('nback_letters2.csv')['corrAns'].tolist()
practice_letters = pd.read_csv('nback_practice.csv')['letters'].tolist()

nback_list1 = list(chunks(nback_letters1, 48)) 
nback_corrAns = list(chunks(nback_corrAns1, 48)) 

nback_list2 = list(chunks(nback_letters2, 48)) 
nback_corrAns_ = list(chunks(nback_corrAns2, 48)) 

# Data saving
nback_results = pd.DataFrame(columns = ['Trial number', 
                                        'Stimulus presented', 
                                        'Key pressed', 
                                        'Correct answer', 
                                        'Response', 
                                        'Reaction time'])

nback_results2 = pd.DataFrame(columns = ['Trial number', 
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
    
showtext(win, NBACKTASK_INSTRUCTIONS2)
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
        
        if j != 0:
                          
            # Use clock-based timing
            nback_clock.reset()
            
            start_marker_sent = False
            tStart =nback_clock.getTime()
            nback_kb1.clock.reset()
            
            while nback_clock.getTime() < 2.5:
                if nback_clock.getTime() < 0.5:
                    letter_present.draw()
                    if start_marker_sent == False:
                        win.callOnFlip(port.write, 'F'.encode())
                        start_marker_sent = True
                else:
                    blank_.draw()
        
                win.flip()
                      
                keys_n = nback_kb1.getKeys(keyList = ['space'], waitRelease=False) 
                
                tResp = nback_clock.getTime()
                response = 'None' if not keys_n else keys_n[-1]
            
            port.write('f'.encode())
                            
            # Get responses 
            if keys_n:
                RT = (tResp - tStart)-0.5
                if corrAns == response or str(corrAns) == response:
                    answer = 1
                elif corrAns != response:
                    answer = 0
                    
            elif response == 'None':
                RT = 0
                if corrAns == '' or corrAns == [] or corrAns == None or corrAns == 'None':
                    answer = 1
                else:
                    answer = 0
            
            else:
                answer = 'error'
            
            # Saving trial data
            thisExp.addData('N back RT',RT)
            thisExp.addData('Stimulus presented',thisLetter)
            thisExp.addData('N back response',answer)
            thisExp.addData('N back start',nback1_start)
            thisExp.addData('Key pressed', response)
            thisExp.addData('Trial number', j),
            thisExp.addData('Block number', block_number)
            thisExp.nextEntry()
            
            # Saving response data
            nback_results = nback_results.append({'Trial number': j, 
                                                    'Stimulus presented': thisLetter,
                                                    'Key pressed': response,
                                                    'Response': answer,
                                                    'Reaction time': RT}, ignore_index=True)
                        
        else:
            nback_clock.reset()
            while nback_clock.getTime() < 2.5:
                if nback_clock.getTime() < 0.5:
                    letter_present.draw()
                else:
                    blank_.draw()
                win.flip()
            


# Save results to CSV
nback_filename1 = 'P' + experimentInfo['Participant'] +'_nbackresults1.csv'
nback_results.to_csv(nback_filename1, header=True)

# Instructions
showtext(win, NBACKTASK_INSTRUCTIONS3)
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
            
        thisLetter2 = a[j]
        corrAns2 = b[j]
        letter_present2 = TextStim(win, text=a[j], height=0.5)

        fixation_cross(0.5)

        # Use clock-based timing
        start_marker_sent2 = False 
        nback_clock.reset()
        win.callOnFlip(nback_kb2.clock.reset) 
        key_pressed2 = False

    
        while nback_clock.getTime() < 2.5:
            if nback_clock.getTime() < 0.5:
               letter_present2.draw()
               if start_marker_sent2 == False:
                   win.callOnFlip(port.write, 'G'.encode())
                   start_marker_sent2 = True
            else:
                blank_.draw()

            win.flip()

            if key_pressed2 == False: 
                keys_n2 = nback_kb2.getKeys(keyList=['space'], waitRelease=False) 
                if len(keys_n2) > 0:
                    key_pressed = True
                    
        port.write('g'.encode())

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
        thisExp.addData('N back2 RT', RT2)
        thisExp.addData('Stimulus presented2', thisLetter2)
        thisExp.addData('N back2 response', answer2)
        thisExp.addData('N back2 start', nback2_start)
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

    if block_number != 3:

        takebreak() 

        blank(2)

# Save results to CSV
nback_filename2 = 'P' + experimentInfo['Participant'] +'_nbackresults2.csv'
nback_results.to_csv(nback_filename2)

# Task end
expend()

#%% Ending the study

showtext(win, EXPERIMENT_END_TEXT)

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
