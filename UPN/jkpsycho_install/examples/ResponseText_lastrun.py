#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy2 Experiment Builder (v1.82.01), July 09, 2015, at 11:18
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
expName = 'ResponseText'  # from the Builder filename that created this script
expInfo = {u'session': u'001', u'participant': u''}
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + 'data/%s_%s_%s' %(expInfo['participant'], expName, expInfo['date'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath='G:\\Workspace\\jkpsycho_install\\examples\\ResponseText.psyexp',
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

# Initialize components for Routine "intro"
introClock = core.Clock()
intro_text = visual.TextStim(win=win, ori=0, name='intro_text',
    text="You'll get to type a few responses and see them all at the end.\n\nPress enter to continue",    font='Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0)

# Initialize components for Routine "trial"
trialClock = core.Clock()
ISI = core.StaticPeriod(win=win, screenHz=expInfo['frameRate'], name='ISI')


######################################################################
## text_response - initialize ########################################
######################################################################
text_response=CompDetails()
######################################################################


what_am_i_typing = visual.TextStim(win=win, ori=0, name='what_am_i_typing',
    text='default text',    font='Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-2.0)
# no responses yet, just started
responses=[]

# Initialize components for Routine "ending"
endingClock = core.Clock()
show_all_responses = visual.TextStim(win=win, ori=0, name='show_all_responses',
    text='default text',    font='Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0)

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

#------Prepare to start Routine "intro"-------
t = 0
introClock.reset()  # clock 
frameN = -1
# update component parameters for each repeat
start_on_enter = event.BuilderKeyResponse()  # create an object of type KeyResponse
start_on_enter.status = NOT_STARTED
# keep track of which components have finished
introComponents = []
introComponents.append(intro_text)
introComponents.append(start_on_enter)
for thisComponent in introComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

#-------Start Routine "intro"-------
continueRoutine = True
while continueRoutine:
    # get current time
    t = introClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *intro_text* updates
    if t >= 0.0 and intro_text.status == NOT_STARTED:
        # keep track of start time/frame for later
        intro_text.tStart = t  # underestimates by a little under one frame
        intro_text.frameNStart = frameN  # exact frame index
        intro_text.setAutoDraw(True)
    
    # *start_on_enter* updates
    if t >= 0.0 and start_on_enter.status == NOT_STARTED:
        # keep track of start time/frame for later
        start_on_enter.tStart = t  # underestimates by a little under one frame
        start_on_enter.frameNStart = frameN  # exact frame index
        start_on_enter.status = STARTED
        # keyboard checking is just starting
        start_on_enter.clock.reset()  # now t=0
        event.clearEvents(eventType='keyboard')
    if start_on_enter.status == STARTED:
        theseKeys = event.getKeys(keyList=['return'])
        
        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            start_on_enter.keys = theseKeys[-1]  # just the last key pressed
            start_on_enter.rt = start_on_enter.clock.getTime()
            # a response ends the routine
            continueRoutine = False
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in introComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

#-------Ending Routine "intro"-------
for thisComponent in introComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if start_on_enter.keys in ['', [], None]:  # No response was made
   start_on_enter.keys=None
# store data for thisExp (ExperimentHandler)
thisExp.addData('start_on_enter.keys',start_on_enter.keys)
if start_on_enter.keys != None:  # we had a response
    thisExp.addData('start_on_enter.rt', start_on_enter.rt)
thisExp.nextEntry()
# the Routine "intro" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
trials = data.TrialHandler(nReps=3, method='random', 
    extraInfo=expInfo, originPath='G:\\Workspace\\jkpsycho_install\\examples\\ResponseText.psyexp',
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
    
    #------Prepare to start Routine "trial"-------
    t = 0
    trialClock.reset()  # clock 
    frameN = -1
    # update component parameters for each repeat
    
    
    ######################################################################
    ## text_response - pre-routine #######################################
    ######################################################################
    text_response = TextGrabber(txt='', multiline=False) # will automatically start when status set to STARTED, else will be stopped.  Usage here is a bit wacky due to constraints of PsychoPy code generation.
    ######################################################################
    
    
    submit_on_enter = event.BuilderKeyResponse()  # create an object of type KeyResponse
    submit_on_enter.status = NOT_STARTED
    
    # keep track of which components have finished
    trialComponents = []
    trialComponents.append(ISI)
    trialComponents.append(text_response)
    trialComponents.append(what_am_i_typing)
    trialComponents.append(submit_on_enter)
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
        ## text_response - frame updates #####################################
        ######################################################################
        # timing logic
        if t >= 0.0 and text_response.status == NOT_STARTED:
            # keep track of start time/frame for later
            text_response.tStart = t  # underestimates by a little under one frame
            text_response.frameNStart = frameN  # exact frame index
            text_response.status=STARTED
        ######################################################################
        
        
        
        # *what_am_i_typing* updates
        if t >= 0.0 and what_am_i_typing.status == NOT_STARTED:
            # keep track of start time/frame for later
            what_am_i_typing.tStart = t  # underestimates by a little under one frame
            what_am_i_typing.frameNStart = frameN  # exact frame index
            what_am_i_typing.setAutoDraw(True)
        if what_am_i_typing.status == STARTED:  # only update if being drawn
            what_am_i_typing.setText('what do you have to say?:\n\n' + text_response.text, log=False)
        
        # *submit_on_enter* updates
        if t >= 0.0 and submit_on_enter.status == NOT_STARTED:
            # keep track of start time/frame for later
            submit_on_enter.tStart = t  # underestimates by a little under one frame
            submit_on_enter.frameNStart = frameN  # exact frame index
            submit_on_enter.status = STARTED
            # keyboard checking is just starting
            submit_on_enter.clock.reset()  # now t=0
            event.clearEvents(eventType='keyboard')
        if submit_on_enter.status == STARTED:
            theseKeys = event.getKeys(keyList=['return'])
            
            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                submit_on_enter.keys = theseKeys[-1]  # just the last key pressed
                submit_on_enter.rt = submit_on_enter.clock.getTime()
                # a response ends the routine
                continueRoutine = False
        
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
    
    
    ######################################################################
    ## text_response - post-routine ######################################
    ######################################################################
    text_response.stop()
    ######################################################################
    
    
    # check responses
    if submit_on_enter.keys in ['', [], None]:  # No response was made
       submit_on_enter.keys=None
    # store data for trials (TrialHandler)
    trials.addData('submit_on_enter.keys',submit_on_enter.keys)
    if submit_on_enter.keys != None:  # we had a response
        trials.addData('submit_on_enter.rt', submit_on_enter.rt)
    # save the response
    responses.append(text_response.text)
    # the Routine "trial" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()
    
# completed 3 repeats of 'trials'


#------Prepare to start Routine "ending"-------
t = 0
endingClock.reset()  # clock 
frameN = -1
# update component parameters for each repeat
show_all_responses.setText('Your responses:\n\n{}'.format('\n\n'.join(responses)))
finish_on_enter = event.BuilderKeyResponse()  # create an object of type KeyResponse
finish_on_enter.status = NOT_STARTED
# keep track of which components have finished
endingComponents = []
endingComponents.append(show_all_responses)
endingComponents.append(finish_on_enter)
for thisComponent in endingComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

#-------Start Routine "ending"-------
continueRoutine = True
while continueRoutine:
    # get current time
    t = endingClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *show_all_responses* updates
    if t >= 0.0 and show_all_responses.status == NOT_STARTED:
        # keep track of start time/frame for later
        show_all_responses.tStart = t  # underestimates by a little under one frame
        show_all_responses.frameNStart = frameN  # exact frame index
        show_all_responses.setAutoDraw(True)
    
    # *finish_on_enter* updates
    if t >= 0.0 and finish_on_enter.status == NOT_STARTED:
        # keep track of start time/frame for later
        finish_on_enter.tStart = t  # underestimates by a little under one frame
        finish_on_enter.frameNStart = frameN  # exact frame index
        finish_on_enter.status = STARTED
        # keyboard checking is just starting
        finish_on_enter.clock.reset()  # now t=0
        event.clearEvents(eventType='keyboard')
    if finish_on_enter.status == STARTED:
        theseKeys = event.getKeys(keyList=['return'])
        
        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            finish_on_enter.keys = theseKeys[-1]  # just the last key pressed
            finish_on_enter.rt = finish_on_enter.clock.getTime()
            # a response ends the routine
            continueRoutine = False
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in endingComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

#-------Ending Routine "ending"-------
for thisComponent in endingComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if finish_on_enter.keys in ['', [], None]:  # No response was made
   finish_on_enter.keys=None
# store data for thisExp (ExperimentHandler)
thisExp.addData('finish_on_enter.keys',finish_on_enter.keys)
if finish_on_enter.keys != None:  # we had a response
    thisExp.addData('finish_on_enter.rt', finish_on_enter.rt)
thisExp.nextEntry()
# the Routine "ending" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

win.close()
core.quit()
