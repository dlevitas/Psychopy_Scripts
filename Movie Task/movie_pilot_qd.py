from __future__ import division
from psychopy import visual, core, data, event, logging, sound, gui, parallel
from psychopy.constants import *
from win32api import GetSystemMetrics
import numpy as np
from pandas import read_csv
from pandas import DataFrame
import os, sys, random
from jkpsycho import *

from vlc import *

scanner_coms = ScannerComs(port=3, timeout=0.001, baudrate=19200, keyboard=True)

exitexp_key = "escape"
exp_clock = core.Clock()
TR = 1.25
expName = u'Movie_Pilot'  # from the Builder filename that created this script
expInfo = {'SubjNo':'', 'Run':'0', 'Counter':''}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False: core.quit()
wwidth = GetSystemMetrics(0)
wheight = GetSystemMetrics(1)

myWin = visual.Window(size = (wwidth,wheight), fullscr = True,
                              colorSpace = 'rgb', color = (-1,-1,-1),
                              blendMode = 'avg', gamma=1)
                              
event.Mouse(visible=False)
                              

film_desc_path = os.path.join('stimuli', "film_desc_run%s.csv" % expInfo["Run"])
film_df_generator = read_csv(film_desc_path, chunksize=1)

timing_df = DataFrame()
time_file_path = "data/" + "subj%s_%srun%s.csv" % (expInfo['SubjNo'], 
                                                   expInfo['Counter'],
                                                   expInfo['Run'])

instr_stim = visual.TextStim(myWin, text = "Get Ready!",
                             color='white', colorSpace='rgb',
                             height = 300/wheight/2, pos = (0,0))

fixation_stim = visual.GratingStim(win=myWin, mask = 'cross',
                                   size=[150/wwidth/2, 150/wheight/2],
                                   pos=[0,0], sf=0, rgb=1)

def conds(stim=None, duration=None, start_time=None, button=None, timing_df=None):
    if duration and not start_time:
        raise ValueError("Need both duration and start_time keywords to function!")
        
    if not len(event.getKeys(keyList=[exitexp_key])) == 0:
        timing_df = timing_df.append([["run_end", exp_clock.getTime() - run_start]])
        timing_df.columns = ['', 'time']
        timing_df.to_csv(time_file_path, index=False)
        myWin.close()
        core.quit()
        
    value = not bool(len(event.getKeys(keyList=['space'])))
    
    if duration:
        value &= exp_clock.getTime() - start_time < duration
    elif stim:
        value &= not stim.status == visual.FINISHED
    elif button:
        value &= not bool(len(event.getKeys(keyList=[button])))
        value &= not button in scanner_coms.messages()
        
    return value

def run_trial(film_dict, block_no, timing_df):
    film_path = os.path.join('stimuli/clips/', film_dict["movie_path"][0])
    valence = film_dict["valence"][0]
#    duration = film_df["duration"][0]
    if not block_no:
        global valence_stim
        valence_stim = visual.TextStim(myWin, text = valence,
                                       color='white', colorSpace='rgb',
                                       height = 300/wheight/2, pos = (0,0))
    else:
        valence_stim.text = valence
        
    movie_stim = visual.MovieStim2(myWin, film_path,
                                   size=1280, pos=(0,0),
                                   flipVert=False, flipHoriz=False,
                                   loop=False)
                                   
    vlc.movie_stim._vlc_instance, vlc.VideoAdjustOption.Gamma

        
    valence_stim.draw()
    myWin.flip()
    start_time = exp_clock.getTime()
    
    while conds(duration=1, start_time=start_time, timing_df=timing_df):
        pass
    
    should_flip = movie_stim.play()
    myWin.flip()
    timing_df = timing_df.append([['movie%s_start' % block_no, exp_clock.getTime()]])
    while conds(stim=movie_stim, timing_df=timing_df):
        
        if should_flip:
            myWin.flip()
        else:
            core.wait(0.001)
        try:    
            if not movie_stim.status == visual.FINISHED:
                should_flip = movie_stim.draw()
        except RuntimeError:
            break

    movie_stim.stop()
    myWin.flip()
    timing_df = timing_df.append([['movie%s_end' % block_no, exp_clock.getTime()]])
    
    return timing_df

instr_stim.draw()
myWin.flip()

while conds(button='6', timing_df=timing_df):
    pass
run_start = exp_clock.getTime()
timing_df = timing_df.append([["run_start", 0]])

fixation_stim.draw()
myWin.flip()

start_time = exp_clock.getTime()
while conds(duration=5*TR, start_time=start_time, timing_df=timing_df):
    pass

for i, film_df in enumerate(film_df_generator):
    timing_df = timing_df.append([["block%s_start" % i, exp_clock.getTime() - run_start]])
    film_dict = film_df.to_dict()
    timing_df = run_trial(film_dict, block_no=i, timing_df=timing_df)
    
    fixation_stim.draw()
    myWin.flip()

    start_time = exp_clock.getTime()
    while conds(duration=10, start_time=start_time):
        pass
    timing_df = timing_df.append([["block%s_end" % i, exp_clock.getTime() - run_start]])
    
extra_time = exp_clock.getTime()
start_time = exp_clock.getTime()
while conds(duration=480-exp_clock.getTime()+run_start, start_time=start_time, timing_df=timing_df):
    pass

timing_df = timing_df.append([["run_end", exp_clock.getTime() - run_start]])
timing_df.columns = ['', 'time']
timing_df.to_csv(time_file_path, index=False)

myWin.close()
core.quit()