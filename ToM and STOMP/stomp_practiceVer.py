#Stomp 2 Practice:

from __future__ import division
from psychopy import locale_setup, visual, core, event, data, gui
import pandas as pd
import numpy as np
import os, platform, shlex
import subprocess as subp
from psychopy.iohub import launchHubServer, EventConstants

#io=launchHubServer(experiment_code='key_evts', psychopy_monitor_name='default')
io = launchHubServer()
keyboard = io.devices.keyboard

#Set up path directories:
cwd = os.path.dirname(__file__)
Movie_dir = os.path.join(cwd + "/Stimuli")
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
expName = "STOMP"
expInfo = {"Participant ID":""}
dlg = gui.DlgFromDict(dictionary = expInfo, title = expName)
if dlg.OK == False:
    core.quit()
if expInfo["Participant ID"] == "":
    raise ValueError ("Please enter a Participant ID")

#Create data files, and check for duplicates/override incomplete data:
fileName = "%s.csv" %expInfo["Participant ID"]

if not os.path.exists(Data_dir):
    os.makedirs(Data_dir)
os.chdir(Data_dir)
if os.path.isfile(fileName):
    check = pd.read_csv(fileName)
    if len(check) < 137:
        os.remove(fileName)
    else:
        raise ValueError ("A log file already exists for this participant")
os.chdir(cwd)
        
#Window:
win = visual.Window(fullscr = True, pos = (0,0), units = "norm", color = "Black")

#Turn off Mouse
event.Mouse(visible = False)

#Timers:
timer = core.Clock() 
cumulativeTimer = core.Clock()

#Data List File:
run_param_list = []
header = ['Subject','Movie','Seen Movie?','Response']

#Stimuli:
text = visual.TextStim(win, text='',height=0.08, pos=(0,0), color="White")
movie_list = [str(x) for x in np.random.permutation(os.listdir(os.path.join(cwd + "/Stimuli")))]
movie = visual.MovieStim3(win, size=(1.5,1.5), filename = os.path.join(cwd +"/Stimuli/JohnTucker.mov"), units='norm', noAudio=True)
chars = list('1234567890abcdefghijklmnopqrstuvwxyz')
fr0 = visual.TextStim(win, text='', height=0.08, pos=(0,0.2), color='White', wrapWidth=1.5)
fr1 = visual.TextStim(win, text='', height=0.08, pos=(0,0.2), color='White', wrapWidth=1.5)

#Experiment Instructions:
text.text = 'You are going to watch a short video clip. Press the enter key to continue'
text.draw()
win.flip()

while True:
    """
    eventKeys = event.getKeys(keyList=['escape','return'])
    if 'escape' in eventKeys:
        core.quit()
    elif 'return' in eventKeys:
        break
    else:
        pass
    """
    #for event in keyboard.getEvents():
        #if event.type == EventConstants.KEYBOARD_PRESS:
    if 'escape' in keyboard.getKeys(keys='escape'):
        core.quit()
    elif 'return' in keyboard.getKeys(keys='return'):
        break
    else:
        print keyboard.getKeys(keys='escape')
        pass


#Close Psychopy:
win.close()
core.quit() 