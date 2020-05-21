#TOM-STOMP Tasks Wrapper Script:

from __future__ import division
from psychopy import prefs
prefs.general['audioLib'] = ['pygame']
from psychopy import locale_setup, visual, core, event, data, gui, sound
import pandas as pd
import numpy as np
import os, platform, shlex, sys, time
import subprocess as subp

#Set up path directories:
cwd = os.path.dirname(__file__)
Movie_dir = os.path.join(cwd + "/Stimuli")
Audio_dir = os.path.join(cwd + "/Stories")
Data_dir = os.path.join(cwd + "/Data")

#Determine Monitor Resolution:
if platform.system() == "Windows":
    from win32api import GetSystemMetrics
    width, height = GetSystemMetrics(0), GetSystemMetrics(1)
elif platform.system() == "Darwin":
    p = subp.Popen(shlex.split("system_profiler SPDisplaysDataType"), stdout=subp.PIPE)
    output = subp.check_output(('grep', 'Resolution'), stdin=p.stdout)
    if output[-7:] != 'Retina\n':
        width, height = [int(x.strip('.')) for x in output.split(':')[-1].split('x')]
    else:
        width =  int([x.strip('.') for x in output.split(':')[-1].split('x')][0])
        height = int([x.strip('.') for x in output.split(':')[-1].split('x')][1][:-8])
scale = (width*0.0015) + 0.05

#Create GUI:
expInfo = {"Participant ID":""}
dlg = gui.DlgFromDict(dictionary = expInfo)
if dlg.OK == False:
    core.quit()
if expInfo["Participant ID"] == "":
    raise ValueError ("Please enter a Participant ID")
 
subjID = expInfo['Participant ID']
currentTime = time.strftime("%m%d%Y_%H.%M.%S")

#Run the two task scripts:
execfile('STOMP.py')
execfile('ToM.py')

#Close Python
win.close()
core.quit()