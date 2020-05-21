#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy2 Experiment Builder (v1.82.01), February 26, 2015, at 14:01
If you publish work using this script please cite the relevant PsychoPy publications
  Peirce, JW (2007) PsychoPy - Psychophysics software in Python. Journal of Neuroscience Methods, 162(1-2), 8-13.
  Peirce, JW (2009) Generating stimuli for neuroscience using PsychoPy. Frontiers in Neuroinformatics, 2:10. doi: 10.3389/neuro.11.010.2008
"""

from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
from psychopy import visual, core, data, event, logging, sound, gui
from psychopy.constants import *  # things like STARTED, FINISHED
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import sin, cos, tan, log, log10, pi, average, sqrt, std, deg2rad, rad2deg, linspace, asarray
from numpy.random import random, randint, normal, shuffle, np
from jkpsycho import *
import os  # handy system and path functions

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# Store info about the experiment session
expName = 'ScannerComsTest'  # from the Builder filename that created this script
expInfo = {u'session': u'001', u'participant': u''}
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + 'data/%s_%s_%s' %(expInfo['participant'], expName, expInfo['date'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath=u'G:\\jkpsycho_install\\tests\\ScannerComsTest.psyexp',
    savePickle=True, saveWideText=True,
    dataFileName=filename)
#save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp

# Start Code - component code to be run before the window creation

# Setup the Window
win = visual.Window(size=(1920, 1080), fullscr=True, screen=0, allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True,
    )
# store frame rate of monitor if we can measure it successfully
expInfo['frameRate']=win.getActualFrameRate()
if expInfo['frameRate']!=None:
    frameDur = 1.0/round(expInfo['frameRate'])
else:
    frameDur = 1.0/60.0 # couldn't get a reliable measure so guess

# Initialize components for Routine "trial"
trialClock = core.Clock()
ISI = core.StaticPeriod(win=win, screenHz=expInfo['frameRate'], name='ISI')


######################################################################
## scanner_coms_connect - initialize #################################
######################################################################
scanner_coms_connect=CompDetails()
scanner_coms = ScannerComs(port=2, timeout=0.001, baudrate=19200, keyboard=True)
######################################################################


pause_text = visual.TextStim(win=win, ori=0, name='pause_text',
    text='default text',    font='Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-2.0)

# Initialize components for Routine "test"
testClock = core.Clock()


######################################################################
## coms - initialize #################################################
######################################################################
coms=CompDetails()
######################################################################



text = visual.TextStim(win=win, ori=0, name='text',
    text=None,    font=u'Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color=u'white', colorSpace='rgb', opacity=1,
    depth=-2.0)

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

#------Prepare to start Routine "trial"-------
t = 0
trialClock.reset()  # clock 
frameN = -1
# update component parameters for each repeat
pause_text.setText('instructions go here')
event.clearEvents(eventType='keyboard')

_text = 'instructions go here'+'\n\n'
_kf=pause_text.keyfilter = KeyFilter(None,'escape')

if _kf.include:
    _text+='press a key to continue:\n'+str(_kf.include)[1:-1]
elif _kf.exclude:
    _text+='press a key to continue, except:\n'+str(_kf.exclude)[1:-1]
else:
    _text+='press any key to continue'

pause_text.setText(_text)

# keep track of which components have finished
trialComponents = []
trialComponents.append(ISI)
trialComponents.append(pause_text)
for thisComponent in trialComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

#-------Start Routine "trial"-------
continueRoutine = True
while continueRoutine:
    # get current time
    t = trialClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    
    ######################################################################
    ## scanner_coms_connect - frame updates ##############################
    ######################################################################
    # timing logic
    if scanner_coms_connect.status==NOT_STARTED: scanner_coms_connect.status=STARTED
    ######################################################################
    
    
    
    # *pause_text* updates
    if t >= 0.0 and pause_text.status == NOT_STARTED:
        # keep track of start time/frame for later
        pause_text.tStart = t  # underestimates by a little under one frame
        pause_text.frameNStart = frameN  # exact frame index
        pause_text.setAutoDraw(True)
    # stop routine if pause_text's buttons are pressed
    if pause_text.status==STARTED:
        if event.getKeys(keyList=pause_text.keyfilter): stopRoutine()
    # *ISI* period
    if t >= 0.0 and ISI.status == NOT_STARTED:
        # keep track of start time/frame for later
        ISI.tStart = t  # underestimates by a little under one frame
        ISI.frameNStart = frameN  # exact frame index
        ISI.start(0.5)
    elif ISI.status == STARTED: #one frame should pass before updating params and completing
        ISI.complete() #finish the static period
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in trialComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

#-------Ending Routine "trial"-------
for thisComponent in trialComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# the Routine "trial" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

#------Prepare to start Routine "test"-------
t = 0
testClock.reset()  # clock 
frameN = -1
# update component parameters for each repeat


######################################################################
## coms - pre-routine ################################################
######################################################################
coms = makeScannerComsAccess(scanner_coms,False,False)
######################################################################


cur_text=old_text=new_text=''
# keep track of which components have finished
testComponents = []
testComponents.append(coms)
testComponents.append(text)
for thisComponent in testComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

#-------Start Routine "test"-------
continueRoutine = True
while continueRoutine:
    # get current time
    t = testClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    
    ######################################################################
    ## coms - frame updates ##############################################
    ######################################################################
    # timing logic
    if t >= 0.0 and coms.status == NOT_STARTED:
        # keep track of start time/frame for later
        coms.tStart = t  # underestimates by a little under one frame
        coms.frameNStart = frameN  # exact frame index
        coms.status=STARTED
    # update
    if coms.status == STARTED:
        coms._update()
    ######################################################################
    
    
    if coms.status==STARTED:
        new_text=', '.join(coms)
    else:
        new_text = 'not active'
    
    if new_text!=old_text:
        cur_text = old_text = new_text
        text.setText(cur_text)
    elif not cur_text.endswith('*'):
        cur_text+='*'
        text.setText(cur_text)
    else:
        pass
    
    # start experiment
    num_correct_reward_trails = 0
    trials_correct = []
    #reward_trials = []
    
    # start routine
    correct_button = '1' if corAns=='right' else '0'
    #reward_trials.append(spcue==1)
    
    already_responded = False
    correct = False
    
    # each frame
    if buttons_pressed and not already_responded:
        already_responded = True
        if correct_button in buttons_pressed:
            correct = True
    
    # end routine
    if correct and spcue==1:
        num_correct_reward_trails+=1
    trials_correct.append(correct)
    
    
    if correct in coms:
        log_correct()
    elif '2' in coms:
        log_incorrect()
    
    # *text* updates
    if t >= 0.0 and text.status == NOT_STARTED:
        # keep track of start time/frame for later
        text.tStart = t  # underestimates by a little under one frame
        text.frameNStart = frameN  # exact frame index
        text.setAutoDraw(True)
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in testComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

#-------Ending Routine "test"-------
for thisComponent in testComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)

# the Routine "test" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()


######################################################################
## scanner_coms_connect - cleanup ####################################
######################################################################
scanner_coms.close()
######################################################################



win.close()
core.quit()
