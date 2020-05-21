#!/usr/bin/env python2
from __future__ import division
from psychopy import visual, core, event, parallel, gui, monitors
#from psychopy import visual, core, event, gui
import numpy as np
import os as os
import sys
from copy import copy
from win32api import GetSystemMetrics


wwidth = GetSystemMetrics(0)
wheight = GetSystemMetrics(1)

myWin = visual.Window(size=(wwidth,wheight), allowGUI=False, color=[-1,-1,-1], fullscr=True)

fixation = visual.GratingStim(win=myWin, mask = 'cross',
                              size=[150/wwidth/2, 150/wheight/2],
                              pos=[0,0], sf=0, color=(1,1,1))
fixation.draw()
myWin.flip()

keepGoing = True
while keepGoing:
    keyList = event.getKeys(keyList=['escape'])
    if 'escape' in keyList:
        keepGoing = False

myWin.close()
core.quit()