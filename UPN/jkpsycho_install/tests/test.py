#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy2 Experiment Builder (v1.81.03), February 24, 2015, at 13:33
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
expName = 'test'  # from the Builder filename that created this script
expInfo = {}
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data' + os.sep + u'psychopy_data_' + data.getDateStr()

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath=None,
    savePickle=True, saveWideText=False,
    dataFileName=filename)
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

# Initialize components for Routine "init"
initClock = core.Clock()


######################################################################
## scanner_coms_connect - initialize #################################
######################################################################
scanner_coms_connect=CompDetails()
scanner_coms = ScannerComs(port=3, timeout=0.001, baudrate=19200, keyboard=True)
######################################################################


pause_text_2 = visual.TextStim(win=win, ori=0, name='pause_text_2',
    text='default text',    font='Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0)

# Initialize components for Routine "test_response_test"
test_response_testClock = core.Clock()


######################################################################
## tr1 - initialize ##################################################
######################################################################
tr1=CompDetails()
######################################################################




######################################################################
## tr2 - initialize ##################################################
######################################################################
tr2=CompDetails()
######################################################################


text_3 = visual.TextStim(win=win, ori=0, name='text_3',
    text='default text',    font=u'Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color=u'white', colorSpace='rgb', opacity=1,
    depth=-2.0)

# Initialize components for Routine "instr"
instrClock = core.Clock()
pause_text = visual.TextStim(win=win, ori=0, name='pause_text',
    text="Next, you will have 10 seconds to press buttons.  You'll see a list of presses on screen.  An * will be appended on subsequent frames to show that you have't pressed anything since last time.",    font='Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0)

_text = "Next, you will have 10 seconds to press buttons.  You'll see a list of presses on screen.  An * will be appended on subsequent frames to show that you have't pressed anything since last time."+'\n\n'
if ['1','2','5']:
    _text+='press a key to continue:\n'+str(list(['1','2','5']))[1:-1]
else:
    _text+='press any key to continue'
pause_text.setText(_text)


# Initialize components for Routine "simple_coms_test"
simple_coms_testClock = core.Clock()

button_display = visual.TextStim(win=win, ori=0, name='button_display',
    text='default text',    font='Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0)

# Initialize components for Routine "trial"
trialClock = core.Clock()
ISI = core.StaticPeriod(win=win, screenHz=expInfo['frameRate'], name='ISI')


######################################################################
## scanner_coms_use - initialize #####################################
######################################################################
scanner_coms_use=CompDetails()
######################################################################



text = visual.TextStim(win=win, ori=0, name='text',
    text='default text',    font='Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-3.0)


######################################################################
## routine_stopper - initialize ######################################
######################################################################
routine_stopper=CompDetails()
######################################################################



# Initialize components for Routine "TableLooperTest"
TableLooperTestClock = core.Clock()


######################################################################
## scanner_coms_use_2 - initialize ###################################
######################################################################
scanner_coms_use_2=CompDetails()
######################################################################




######################################################################
## table_looper - initialize #########################################
######################################################################
table_looper=CompDetails()
trial=TableLooper(u'conds.csv')
######################################################################


row_printer = visual.TextStim(win=win, ori=0, name='row_printer',
    text='default text',    font=u'Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color=u'white', colorSpace='rgb', opacity=1,
    depth=-2.0)
do_table_looper_test = True

# Initialize components for Routine "done"
doneClock = core.Clock()
pause_text_3 = visual.TextStim(win=win, ori=0, name='pause_text_3',
    text='default text',    font=u'Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color=u'white', colorSpace='rgb', opacity=1,
    depth=0.0)

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

#------Prepare to start Routine "init"-------
t = 0
initClock.reset()  # clock 
frameN = -1
# update component parameters for each repeat
pause_text_2.setText('''This is the test suite for JkPsycho Components

Follow instructions to thoroughly test the components.  If there is a problem, contact me (Josh Kinnison) and I'll fix it as soon as possible.

Scanner Coms connected?: {}'''.format(scanner_coms.connected_to_serial()))
event.clearEvents(eventType='keyboard')

_text = '''This is the test suite for JkPsycho Components

Follow instructions to thoroughly test the components.  If there is a problem, contact me (Josh Kinnison) and I'll fix it as soon as possible.

Scanner Coms connected?: {}'''.format(scanner_coms.connected_to_serial())+'\n\n'
if None:
    _text+='press a key to continue:\n'+str(list(None))[1:-1]
else:
    _text+='press any key to continue'
pause_text_2.setText(_text)

# keep track of which components have finished
initComponents = []
initComponents.append(pause_text_2)
for thisComponent in initComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

#-------Start Routine "init"-------
continueRoutine = True
while continueRoutine:
    # get current time
    t = initClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    
    ######################################################################
    ## scanner_coms_connect - frame updates ##############################
    ######################################################################
    # timing logic
    if scanner_coms_connect.status==NOT_STARTED: scanner_coms_connect.status=STARTED
    ######################################################################
    
    
    
    # *pause_text_2* updates
    if t >= 0.0 and pause_text_2.status == NOT_STARTED:
        # keep track of start time/frame for later
        pause_text_2.tStart = t  # underestimates by a little under one frame
        pause_text_2.frameNStart = frameN  # exact frame index
        pause_text_2.setAutoDraw(True)
    # stop routine if pause_text_2's buttons are pressed
    if pause_text_2.status==STARTED:
        if event.getKeys(keyList=None): stopRoutine()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        routineTimer.reset()  # if we abort early the non-slip timer needs reset
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in initComponents:
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

#-------Ending Routine "init"-------
for thisComponent in initComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)

#------Prepare to start Routine "test_response_test"-------
t = 0
test_response_testClock.reset()  # clock 
frameN = -1
routineTimer.add(20.000000)
# update component parameters for each repeat


######################################################################
## tr1 - pre-routine #################################################
######################################################################
tr1 = TextGrabber(txt='', multiline=False) # will automatically start when status set to STARTED, else will be stopped.  Usage here is a bit wacky due to constraints of PsychoPy code generation.
######################################################################




######################################################################
## tr2 - pre-routine #################################################
######################################################################
tr2 = TextGrabber(txt='', multiline=True) # will automatically start when status set to STARTED, else will be stopped.  Usage here is a bit wacky due to constraints of PsychoPy code generation.
######################################################################


# keep track of which components have finished
test_response_testComponents = []
test_response_testComponents.append(tr1)
test_response_testComponents.append(tr2)
test_response_testComponents.append(text_3)
for thisComponent in test_response_testComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

#-------Start Routine "test_response_test"-------
continueRoutine = True
while continueRoutine and routineTimer.getTime() > 0:
    # get current time
    t = test_response_testClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    
    ######################################################################
    ## tr1 - frame updates ###############################################
    ######################################################################
    # timing logic
    if t >= 2 and tr1.status == NOT_STARTED:
        # keep track of start time/frame for later
        tr1.tStart = t  # underestimates by a little under one frame
        tr1.frameNStart = frameN  # exact frame index
        tr1.status=STARTED
    if tr1.status == STARTED and t >= (2 + (8-win.monitorFramePeriod*0.75)): #most of one frame period left
        tr1.status = STOPPED
    ######################################################################
    
    
    
    
    ######################################################################
    ## tr2 - frame updates ###############################################
    ######################################################################
    # timing logic
    if t >= 10 and tr2.status == NOT_STARTED:
        # keep track of start time/frame for later
        tr2.tStart = t  # underestimates by a little under one frame
        tr2.frameNStart = frameN  # exact frame index
        tr2.status=STARTED
    if tr2.status == STARTED and t >= (10 + (8-win.monitorFramePeriod*0.75)): #most of one frame period left
        tr2.status = STOPPED
    ######################################################################
    
    
    
    # *text_3* updates
    if t >= 0.0 and text_3.status == NOT_STARTED:
        # keep track of start time/frame for later
        text_3.tStart = t  # underestimates by a little under one frame
        text_3.frameNStart = frameN  # exact frame index
        text_3.setAutoDraw(True)
    if text_3.status == STARTED and t >= (0.0 + (20-win.monitorFramePeriod*0.75)): #most of one frame period left
        text_3.setAutoDraw(False)
    if text_3.status == STARTED:  # only update if being drawn
        text_3.setText("{}\none line 2-10 seconds: {}\nmulti-line 10-18 seconds:{}".format(t,tr1.text,tr2.text), log=False)
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        routineTimer.reset()  # if we abort early the non-slip timer needs reset
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in test_response_testComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

#-------Ending Routine "test_response_test"-------
for thisComponent in test_response_testComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)


######################################################################
## tr1 - post-routine ################################################
######################################################################
tr1.stop()
######################################################################




######################################################################
## tr2 - post-routine ################################################
######################################################################
tr2.stop()
######################################################################



#------Prepare to start Routine "instr"-------
t = 0
instrClock.reset()  # clock 
frameN = -1
# update component parameters for each repeat
event.clearEvents(eventType='keyboard')
# keep track of which components have finished
instrComponents = []
instrComponents.append(pause_text)
for thisComponent in instrComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

#-------Start Routine "instr"-------
continueRoutine = True
while continueRoutine:
    # get current time
    t = instrClock.getTime()
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
        if event.getKeys(keyList=['1','2','5']): stopRoutine()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        routineTimer.reset()  # if we abort early the non-slip timer needs reset
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in instrComponents:
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

#-------Ending Routine "instr"-------
for thisComponent in instrComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)

#------Prepare to start Routine "simple_coms_test"-------
t = 0
simple_coms_testClock.reset()  # clock 
frameN = -1
# update component parameters for each repeat
msgs=''
# keep track of which components have finished
simple_coms_testComponents = []
simple_coms_testComponents.append(button_display)
for thisComponent in simple_coms_testComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

#-------Start Routine "simple_coms_test"-------
continueRoutine = True
while continueRoutine:
    # get current time
    t = simple_coms_testClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    new_msgs = scanner_coms.messages()
    if new_msgs:
        msgs=', '.join(new_msgs)
    elif not msgs.endswith('*'):
        msgs+='*'
    
    
    # *button_display* updates
    if t >= 0.0 and button_display.status == NOT_STARTED:
        # keep track of start time/frame for later
        button_display.tStart = t  # underestimates by a little under one frame
        button_display.frameNStart = frameN  # exact frame index
        button_display.setAutoDraw(True)
    if button_display.status == STARTED and t >= (0.0 + (0-win.monitorFramePeriod*0.75)): #most of one frame period left
        button_display.setAutoDraw(False)
    if button_display.status == STARTED:  # only update if being drawn
        button_display.setText('{}\n{:02.2f}'.format(msgs,t), log=False)
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        routineTimer.reset()  # if we abort early the non-slip timer needs reset
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in simple_coms_testComponents:
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

#-------Ending Routine "simple_coms_test"-------
for thisComponent in simple_coms_testComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)


#------Prepare to start Routine "trial"-------
t = 0
trialClock.reset()  # clock 
frameN = -1
# update component parameters for each repeat


######################################################################
## scanner_coms_use - pre-routine ####################################
######################################################################

# initialize storage
if True:
    coms=set([])
else:
    coms=[]

# clear old stuff (always)
scanner_coms.clear()

######################################################################


pre=''
if scanner_coms.connected_to_serial():
    pre+='serial+'
if scanner_coms.connected_to_keyboard():
    pre+='keyboard'
if not pre:
    pre='not connected to any inputs!!'
pre+='\n'

print(scanner_coms._coms)
print(bool(scanner_coms._coms))

# keep track of which components have finished
trialComponents = []
trialComponents.append(ISI)
trialComponents.append(scanner_coms_use)
trialComponents.append(text)
trialComponents.append(routine_stopper)
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
    ## scanner_coms_use - frame updates ##################################
    ######################################################################
    # timing logic
    if t >= 1 and scanner_coms_use.status == NOT_STARTED:
        # keep track of start time/frame for later
        scanner_coms_use.tStart = t  # underestimates by a little under one frame
        scanner_coms_use.frameNStart = frameN  # exact frame index
        scanner_coms_use.status=STARTED
    # update
    if scanner_coms_use.status == STARTED:
        
        # pull messages from scanner coms (maybe keyboard too)
        _new_messages = scanner_coms.messages(clear_after=True,as_set=True)
        
        # update or replace
        if True:
            coms=_new_messages
        else:
            if True:
                coms.update(_new_messages)
            else:
                coms.extend(_new_messages)
        
    ######################################################################
    
    
    
    if scanner_coms_use.status==NOT_STARTED:
        txt=pre+'not started'
    elif scanner_coms_use.status==STOPPED:
        txt=pre+'stopped'
    else:
        print(coms)
        if 'not started' in txt:
            txt=pre
        if coms:
            txt=pre+','.join(coms)
        elif not txt.endswith('*'):
            txt+='*'
    
    
    # *text* updates
    if t >= 0.0 and text.status == NOT_STARTED:
        # keep track of start time/frame for later
        text.tStart = t  # underestimates by a little under one frame
        text.frameNStart = frameN  # exact frame index
        text.setAutoDraw(True)
    if text.status == STARTED:  # only update if being drawn
        text.setText(txt, log=False)
    
    
    ######################################################################
    ## routine_stopper - frame updates ###################################
    ######################################################################
    # timing logic
    if t >= 0.0 and routine_stopper.status == NOT_STARTED:
        # keep track of start time/frame for later
        routine_stopper.tStart = t  # underestimates by a little under one frame
        routine_stopper.frameNStart = frameN  # exact frame index
        routine_stopper.status=STARTED
    # update
    if routine_stopper.status == STARTED:
        if '6' in coms: stopRoutine()
    ######################################################################
    
    
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


######################################################################
## scanner_coms_use - post-routine ###################################
######################################################################
scanner_coms.clear()
######################################################################




# set up handler to look after randomisation of conditions etc
trials = data.TrialHandler(nReps=500, method='random', 
    extraInfo=expInfo, originPath=None,
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
    
    #------Prepare to start Routine "TableLooperTest"-------
    t = 0
    TableLooperTestClock.reset()  # clock 
    frameN = -1
    # update component parameters for each repeat
    
    
    ######################################################################
    ## scanner_coms_use_2 - pre-routine ##################################
    ######################################################################
    
    # initialize storage
    if True:
        coms=set([])
    else:
        coms=[]
    
    # clear old stuff (always)
    scanner_coms.clear()
    
    ######################################################################
    
    
    #being routine!
    # keep track of which components have finished
    TableLooperTestComponents = []
    TableLooperTestComponents.append(scanner_coms_use_2)
    TableLooperTestComponents.append(row_printer)
    for thisComponent in TableLooperTestComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    #-------Start Routine "TableLooperTest"-------
    continueRoutine = True
    while continueRoutine:
        # get current time
        t = TableLooperTestClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        
        ######################################################################
        ## scanner_coms_use_2 - frame updates ################################
        ######################################################################
        # timing logic
        if t >= 0.0 and scanner_coms_use_2.status == NOT_STARTED:
            # keep track of start time/frame for later
            scanner_coms_use_2.tStart = t  # underestimates by a little under one frame
            scanner_coms_use_2.frameNStart = frameN  # exact frame index
            scanner_coms_use_2.status=STARTED
        # update
        if scanner_coms_use_2.status == STARTED:
            
            # pull messages from scanner coms (maybe keyboard too)
            _new_messages = scanner_coms.messages(clear_after=True,as_set=True)
            
            # update or replace
            if True:
                coms=_new_messages
            else:
                if True:
                    coms.update(_new_messages)
                else:
                    coms.extend(_new_messages)
            
        ######################################################################
        
        
        
        
        ######################################################################
        ## table_looper - frame updates ######################################
        ######################################################################
        # timing logic
        if table_looper.status==NOT_STARTED: table_looper.status=STARTED
        ######################################################################
        
        
        
        # *row_printer* updates
        if t >= 0.0 and row_printer.status == NOT_STARTED:
            # keep track of start time/frame for later
            row_printer.tStart = t  # underestimates by a little under one frame
            row_printer.frameNStart = frameN  # exact frame index
            row_printer.setAutoDraw(True)
        if row_printer.status == STARTED and t >= (0.0 + (1.0-win.monitorFramePeriod*0.75)): #most of one frame period left
            row_printer.setAutoDraw(False)
        if row_printer.status == STARTED:  # only update if being drawn
            row_printer.setText('press 5 to step, 6 to stop\n'+str(trial), log=False)
        if '5' in coms:
            stopRoutine()
        if '6' in coms:
            do_table_looper_test=False
        if not do_table_looper_test:
            stopRoutine()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineTimer.reset()  # if we abort early the non-slip timer needs reset
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in TableLooperTestComponents:
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
    
    #-------Ending Routine "TableLooperTest"-------
    for thisComponent in TableLooperTestComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    
    
    ######################################################################
    ## scanner_coms_use_2 - post-routine #################################
    ######################################################################
    scanner_coms.clear()
    ######################################################################
    
    
    
    
    ######################################################################
    ## table_looper - post-routine #######################################
    ######################################################################
    trial+=1
    ######################################################################
    
    
    
    thisExp.nextEntry()
    
# completed 500 repeats of 'trials'


#------Prepare to start Routine "done"-------
t = 0
doneClock.reset()  # clock 
frameN = -1
# update component parameters for each repeat
pause_text_3.setText(u'All Done!')
event.clearEvents(eventType='keyboard')

_text = u'All Done!'+'\n\n'
if None:
    _text+='press a key to continue:\n'+str(list(None))[1:-1]
else:
    _text+='press any key to continue'
pause_text_3.setText(_text)

# keep track of which components have finished
doneComponents = []
doneComponents.append(pause_text_3)
for thisComponent in doneComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

#-------Start Routine "done"-------
continueRoutine = True
while continueRoutine:
    # get current time
    t = doneClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *pause_text_3* updates
    if t >= 0.0 and pause_text_3.status == NOT_STARTED:
        # keep track of start time/frame for later
        pause_text_3.tStart = t  # underestimates by a little under one frame
        pause_text_3.frameNStart = frameN  # exact frame index
        pause_text_3.setAutoDraw(True)
    # stop routine if pause_text_3's buttons are pressed
    if pause_text_3.status==STARTED:
        if event.getKeys(keyList=None): stopRoutine()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        routineTimer.reset()  # if we abort early the non-slip timer needs reset
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in doneComponents:
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

#-------Ending Routine "done"-------
for thisComponent in doneComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)


######################################################################
## scanner_coms_connect - cleanup ####################################
######################################################################
scanner_coms.close()
######################################################################





win.close()
core.quit()
