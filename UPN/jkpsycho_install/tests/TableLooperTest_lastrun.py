#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy2 Experiment Builder (v1.81.03), February 24, 2015, at 15:37
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
expName = 'TableLooperTest'  # from the Builder filename that created this script
expInfo = {u'session': u'001', u'participant': u''}
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + 'data/%s_%s_%s' %(expInfo['participant'], expName, expInfo['date'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath='C:\\Users\\Josh\\Dropbox\\bin\\EXPLORATION\\jkpsycho_install\\TableLooperTest.psyexp',
    savePickle=True, saveWideText=True,
    dataFileName=filename)
#save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp

# Start Code - component code to be run before the window creation

# Setup the Window
win = visual.Window(size=(1680, 1050), fullscr=True, screen=0, allowGUI=False, allowStencil=False,
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
pause_text = visual.TextStim(win=win, ori=0, name='pause_text',
    text='default text',    font='Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0)

# Initialize components for Routine "test"
testClock = core.Clock()


######################################################################
## table_looper - initialize #########################################
######################################################################
table_looper=CompDetails()
trial=TableLooper('conds.csv')
######################################################################


pause_text_2 = visual.TextStim(win=win, ori=0, name='pause_text_2',
    text='default text',    font='Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0)

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

#------Prepare to start Routine "trial"-------
t = 0
trialClock.reset()  # clock 
frameN = -1
# update component parameters for each repeat
pause_text.setText('For testing the TableLooper component.  Press any key to advance to the next row.  Each row is displayed on the screen')
event.clearEvents(eventType='keyboard')

_text = 'For testing the TableLooper component.  Press any key to advance to the next row.  Each row is displayed on the screen'+'\n\n'
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
        routineTimer.reset()  # if we abort early the non-slip timer needs reset
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
    else:  # this Routine was not non-slip safe so reset non-slip timer
        routineTimer.reset()

#-------Ending Routine "trial"-------
for thisComponent in trialComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)

# set up handler to look after randomisation of conditions etc
trials = data.TrialHandler(nReps=5000, method='random', 
    extraInfo=expInfo, originPath='C:\\Users\\Josh\\Dropbox\\bin\\EXPLORATION\\jkpsycho_install\\TableLooperTest.psyexp',
    trialList=[None],
    seed=None, name='trials')
thisExp.addLoop(trials)  # add the loop to the experiment
thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb=thisTrial.rgb)
if thisTrial != None:
    for paramName in thisTrial.keys():
        exec(paramName + '= thisTrial.' + paramName)

for thisTrial in trials:
    currentLoop = trials
    # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
    if thisTrial != None:
        for paramName in thisTrial.keys():
            exec(paramName + '= thisTrial.' + paramName)
    
    #------Prepare to start Routine "test"-------
    t = 0
    testClock.reset()  # clock 
    frameN = -1
    # update component parameters for each repeat
    pause_text_2.setText(str(trial))
    event.clearEvents(eventType='keyboard')
    
    _text = str(trial)+'\n\n'
    _kf=pause_text_2.keyfilter = KeyFilter(None,'escape')
    
    if _kf.include:
        _text+='press a key to continue:\n'+str(_kf.include)[1:-1]
    elif _kf.exclude:
        _text+='press a key to continue, except:\n'+str(_kf.exclude)[1:-1]
    else:
        _text+='press any key to continue'
    
    pause_text_2.setText(_text)
    
    # keep track of which components have finished
    testComponents = []
    testComponents.append(pause_text_2)
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
        ## table_looper - frame updates ######################################
        ######################################################################
        # timing logic
        if table_looper.status==NOT_STARTED: table_looper.status=STARTED
        ######################################################################
        
        
        
        # *pause_text_2* updates
        if t >= 0.0 and pause_text_2.status == NOT_STARTED:
            # keep track of start time/frame for later
            pause_text_2.tStart = t  # underestimates by a little under one frame
            pause_text_2.frameNStart = frameN  # exact frame index
            pause_text_2.setAutoDraw(True)
        # stop routine if pause_text_2's buttons are pressed
        if pause_text_2.status==STARTED:
            if event.getKeys(keyList=pause_text_2.keyfilter): stopRoutine()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineTimer.reset()  # if we abort early the non-slip timer needs reset
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
        else:  # this Routine was not non-slip safe so reset non-slip timer
            routineTimer.reset()
    
    #-------Ending Routine "test"-------
    for thisComponent in testComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    
    
    ######################################################################
    ## table_looper - post-routine #######################################
    ######################################################################
    trial+=1
    ######################################################################
    
    
    thisExp.nextEntry()
    
# completed 5000 repeats of 'trials'

win.close()
core.quit()
