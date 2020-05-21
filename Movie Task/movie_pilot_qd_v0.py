from __future__ import division
from psychopy import visual, core, data, event, logging, sound, gui, parallel
from psychopy.constants import *
from win32api import GetSystemMetrics
import numpy as np
from pandas import read_csv
from pandas import DataFrame
import os, sys, random
from jkpsycho import *

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
                              blendMode = 'avg' )
                              
event.Mouse(visible=False)
                              

film_desc_path = os.path.join('stimuli', "film_desc_run%s.csv" % expInfo["Run"])
film_df_generator = read_csv(film_desc_path, chunksize=1)

timing_df = DataFrame([['',0]]*8, columns=["", "time"])
time_file_path = "data/" + "subj%s_%srun%s.csv" % (expInfo['SubjNo'], 
                                                   expInfo['Counter'],
                                                   expInfo['Run'])

instr_stim = visual.TextStim(myWin, text = "Get Ready!",
                             color='white', colorSpace='rgb',
                             height = 300/wheight/2, pos = (0,0))

fixation_stim = visual.GratingStim(win=myWin, mask = 'cross',
                                   size=[150/wwidth/2, 150/wheight/2],
                                   pos=[0,0], sf=0, rgb=1)

def conds(stim=None, duration=None, start_time=None, button=None):
    if duration and not start_time:
        raise ValueError("Need both duration and start_time keywords to function!")
        
    if not len(event.getKeys(keyList=[exitexp_key])) == 0:
        myWin.close()
        core.quit()
        
    value = True
    
    if duration:
        value &= exp_clock.getTime() - start_time < duration
    elif stim:
        value &= stim.status != visual.FINISHED
    elif button:
        value &= not bool(len(event.getKeys(keyList=[button])))
        value &= not button in scanner_coms.messages()
        
    return value

def run_trial(film_dict, block_no):
    film_path = os.path.join('stimuli/clips/', film_dict["movie_path"][0])
    
    print film_dict["movie_path"][0]
    
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
        
    valence_stim.draw()
    myWin.flip()
    start_time = exp_clock.getTime()
    
    while conds(duration=1, start_time=start_time):
        pass
    
    should_flip = movie_stim.shouldDrawVideoFrame()
    movie_stim.draw()
    
    while conds(button='space'):#stim=movie_stim):
        
        if should_flip:
            myWin.flip()
        else:
            core.wait(0.001)
            
        movie_stim.draw()
        should_flip = movie_stim.shouldDrawVideoFrame()

    movie_stim.stop()

    myWin.flip()

instr_stim.draw()
myWin.flip()

while conds(button='6'):
    pass
run_start = exp_clock.getTime()
timing_df.loc[0] = ["run_start", 0]

fixation_stim.draw()
myWin.flip()

start_time = exp_clock.getTime()
while conds(duration=5*TR, start_time=start_time):
    pass

for i, film_df in enumerate(film_df_generator):
    timing_df.loc[2*i+1] = ["block%s_start" % i, exp_clock.getTime() - run_start]
    film_dict = film_df.to_dict()
    run_trial(film_dict, block_no=i)
    
    fixation_stim.draw()
    myWin.flip()

    start_time = exp_clock.getTime()
    while conds(duration=10, start_time=start_time):
        pass
    timing_df.loc[2*i+2] = ["block%s_end" % i, exp_clock.getTime() - run_start]

timing_df.loc[7] = ["run_end", exp_clock.getTime() - run_start]
timing_df.to_csv(time_file_path, index=False)

myWin.close()
core.quit()