
#PNL Priming fMRI/Behavioral Task

from __future__ import division
from psychopy import locale_setup, visual, core, event, data, gui, parallel
import pandas as pd
import os, time, platform
import subprocess as subp
import shlex

#--------Check before running---------#
run_type = "scan"   #either 'scan' or 'beh'

#parallel.setPortAddress(address=0xD070) address for the BioPack in BPS0125
parallel.setPortAddress(address=0xD010) #address for the BioPack at MNC
parallel.setData(0)

nRuns = 6
nConditions = 6
pairs = 324

if run_type == 'scan':
    from jkpsycho import *
    scanner_coms = ScannerComs(port=3, timeout=0.001, baudrate=19200, keyboard=True)
else:
    pass

#Set directory:
cwd = os.path.dirname(__file__)


#Determine Monitor Resolution:
if platform.system() == "Windows":
    from win32api import GetSystemMetrics
    width, height = GetSystemMetrics(0), GetSystemMetrics(1)
elif platform.system() == "Darwin":
    p = subp.Popen(shlex.split("system_profiler SPDisplaysDataType"), stdout=subp.PIPE)
    output = subp.check_output(('grep', 'Resolution'), stdin=p.stdout)
    width, height = [int(x.strip(' ')) for x in output.split(':')[-1].split(' x ')]
   
#Create GUI:
expName = "UPN"
expInfo = {"participant ID": "", "run": ""}
dlg = gui.DlgFromDict(dictionary = expInfo, title = expName, order = ["participant ID","run"])
if dlg.OK == False:
    core.quit()  
 
run = expInfo['run']
    
#Saved Files:    
fileLocation = os.path.join(cwd + "/Data/%s") %expInfo["participant ID"]
fileName = "Run%s.csv" %(expInfo["run"])

if not os.path.exists(fileLocation):
    os.makedirs(fileLocation)
os.chdir(fileLocation)
if os.path.isfile(fileName):
    raise ValueError("This run has already been completed")
os.chdir(cwd)

#Window:
win = visual.Window(size = (width, height), fullscr = True, pos = (0,0), units = "norm", color = "Black")

#Turn off Mouse
event.Mouse(visible = False)

#Timers:
timer = core.Clock() #Basic timer for moving from one trial component to the next 
trialTimer = core.Clock()
cumulativeTrialTimer = core.Clock()

#Functions:   
def Instructions(str):
    text.text = str
    theseKeys = event.clearEvents(eventType = "keyboard")
    theseKeys = []
    text.draw()
    win.flip()
    while True:
        theseKeys = event.getKeys(keyList=["return","escape"])
        if "escape" in theseKeys:
            core.quit()
        if run_type == 'beh':
            if len(theseKeys):
                break
        else:
            if "6" in scanner_coms.messages():
                break 
            
def fixation(pause):     
    if 'escape' in event.getKeys():
        core.quit()
    
    timer.reset()
    fixation_start = timer.getTime()
    
    text.text = "+"
    text.height = 0.2
    text.pos = (0,0)
    text.draw()
    win.flip()
    while timer.getTime() < pause + fixation_start:
        pass
    fixation_end = timer.getTime()
    
    return fixation_start, fixation_end

def Parameters(nRuns, nConditions, pairs):
    nTrials = int(pairs/nRuns)
    nTrials_per_Cond = nTrials/nConditions

    return nTrials, nTrials_per_Cond
    
nTrials, nTrials_per_Cond = Parameters(nRuns, nConditions, pairs)      
    
def Picture(file, type):
    if 'escape' in event.getKeys():
        core.quit()
    
    timer.reset()    
    if type == "Prime":
        prime_start = timer.getTime()
        target_start = "N/A"
        image.image = file
        image.draw()
        win.flip()
        
        while timer.getTime() < 1.0 + prime_start:
            pass
        prime_end = timer.getTime()
        target_end = "N/A"    
    else:
        target_start = timer.getTime()
        prime_start = "N/A"
        image.image = file
        image.draw()
        win.flip()
        
        while timer.getTime() < 1.0 + target_start:
            pass
        target_end = timer.getTime()
        prime_end = "N/A"
        
    return prime_start, prime_end, target_start, target_end    
    
def Rating(type, trial_num):    
    timer.reset()
    
    os.chdir(fileLocation)
    if trial_num not in [0, nTrials, nTrials*2, nTrials*3, nTrials*4, nTrials*5]:
        file = pd.read_csv(fileName)
    else:
        file = None
    
    """This big if else loop is all to try to make timing issues a bit better. As it currently stands
        there an extra 1.3 seconds from the intensity/valence ratings sections"""
    if type == "intensity":
        text.text = "Rating #1: Please rate the INTENSITY"
        label = ['1','2','3','4','5','6','7','8','9']
        scales = '1=Extremely Weak,   9=Extremely Strong'
        
        if os.path.isfile(str(file)):
            extra_time = file["Intensity Rating Time"][trial_num]
        else:
            extra_time = 0
    else:
        text.text = "Rating #2: Please rate the PLEASANTNESS"
        label = ['1','2','3','4','5','6','7','8','9']
        scales = '1=Extremely Unpleasant,   9=Extremely Pleasant'
        
        if os.path.isfile(str(file)):
            extra_time = file["Valence Rating Time"][trial_num]
        else:
            extra_time = 0
    
    scale = visual.RatingScale(win, low=1, high=9, pos=(0,0), size=1.5, marker=visual.TextStim(win, text="", units="norm"), noMouse=True, tickMarks = label,
            textSize = 0.7, respKeys = ['num_1','num_2','num_3','num_4','num_5','num_6','num_7','num_8','num_9'], minTime=0.0, scale = scales,
            showAccept = False,labels = label, textColor="White", stretch=1.5)
    
    text.pos = (0.0, 0.7)
    text.height = 0.07
    text.setAutoDraw(True)
    
    rate_start = timer.getTime()
    while timer.getTime() < 4.0 + rate_start - extra_time:
        if 'escape' in event.getKeys(keyList=['escape']):
            core.quit()
            
        scale.draw()
        win.flip()  
        if scale.getRating():
            break   
    text.setAutoDraw(False)
        
    output = scale.getHistory()
    if len(output) == 1:
        rating, RT = ["N/A","N/A"]
    else:
        rating = scale.getHistory()[1][0]
        RT = scale.getHistory()[1][1]
        
    rate_end = timer.getTime()
    os.chdir(cwd)           
    return rating, RT, rate_start, rate_end

#Make Paramater File:
run_param_list = []
if run_type == "beh":
    header= ["Cumulative Trial Start","Trial Start","Fixation Time","Prime Picture Time",
            "Target Picture Time", "Intensity Rating Time", "Valence Rating Time","ITI Time","Trial End","Cumulative Trial End","Prime Picture",
            "Target Picture", 'Intensity Rating','Intensity RT','Valence Rating','Valence RT',"Condition"]
else:
    header= ["Cumulative Trial Start","Trial Start","Fixation Time","Prime Picture Time",
            "Target Picture Time","ITI Time","Trial End","Cumulative Trial End","Prime Picture","Target Picture","Condition"]
        
#Text Stimuli:
text = visual.TextStim(win = win, text = '', height = 0.1, pos = (0,0), color="White")
 
#Determine which sections to run:
if expInfo["run"] == 'practice':
    stim_df = pd.read_csv("prac_stimuli.csv")
    block_start, block_end = [0,len(stim_df)]
    if run_type == 'beh':
        Instructions("Get ready to begin the practice section\n\nPress the ENTER key to start")
    else:
        Instructions("Get ready to begin the practice\n\nPlease wait for the scanner")
else:
    stim_df = pd.read_csv("exp_stimuli.csv")
    run_list = range(1,nRuns+1)
    run = int(expInfo["run"])
    if run in run_list:
        if run == 1:
            block_start, block_end = [0,nTrials]
        elif run == 2:
            block_start, block_end = [nTrials, nTrials*2]
        elif run == 3:
            block_start, block_end = [nTrials*2, nTrials*3]
        elif run == 4:
            block_start, block_end = [nTrials*3, nTrials*4]
        elif run == 5:
            block_start, block_end = [nTrials*4, nTrials*5]
        elif run == 6:
            block_start, block_end = [nTrials*5, nTrials*6]
    else:
        raise ValueError("Select correct run")
    
    if run_type == 'beh':
        Instructions('Get ready to begin!\n\nPress the ENTER key to start')
    else:
        Instructions("Get ready!\nPay attention to the pictures")
 
#Image stimuli:
#image = visual.ImageStim(win = win, pos = (0,0), size = (0.7,0.7), image = stim_df.ix[0][0])
image = visual.ImageStim(win = win, pos = (0,0), image = stim_df.ix[0][0])

#Begin Experiment:
if run == 'practice':
    parallel.setData(7)
    core.wait(0.5)
    parallel.setData(0)
elif run == 1:
    parallel.setData(1)
    core.wait(0.5)
    parallel.setData(0)
elif run == 2:
    parallel.setData(2)
    core.wait(0.5)
    parallel.setData(0)  
elif run == 3:
    parallel.setData(3)
    core.wait(0.5)
    parallel.setData(0)
elif run == 4:
    parallel.setData(4)
    core.wait(0.5)
    parallel.setData(0)
elif run == 5:
    parallel.setData(5)
    core.wait(0.5)
    parallel.setData(0)
elif run == 6:
    parallel.setData(6)
    core.wait(0.5)
    parallel.setData(0)

cumulativeTrialTimer.reset()
#6.6-second fixation (b/c TR = 2.2 sec):
tstart = timer.getTime()
text.text = " "
text.draw()
win.flip()
if run_type == 'scan':
    while timer.getTime() < 6.6 + tstart:
        pass
else:
    while timer.getTime() < 2.5 + tstart:
        pass
timer.reset()

for i in xrange(block_start, block_end):
    trialTimer.reset()
    trial_start = trialTimer.getTime()
    cumulativeTrialStart = cumulativeTrialTimer.getTime()
    
    #Present Fixation for 200 ms:
    fixation_start, fixation_end = fixation(0.2)
    fixation_time = fixation_end - fixation_start
    
    #Present Prime picture 400 ms:
    prime_start, prime_end = Picture(stim_df["Prime"][i], "Prime")[0:2]
    prime_time = prime_end - prime_start
    
    #Present Target picture 400 ms:
    target_start, target_end = Picture(stim_df["Target"][i], "Target")[2:4]
    target_time = target_end - target_start
    
    if run_type == 'beh':
        #Intensity and Valence Ratings:
        intensity_rating, intensity_RT, intensity_rate_start, intensity_rate_end = Rating("intensity", i)
        valence_rating, valence_RT, valence_rate_start, valence_rate_end= Rating("valence", i)
        
        intensity_rating_time = intensity_rate_end - intensity_rate_start
        valence_rating_time = valence_rate_end - valence_rate_start
    else:
        pass
    
    #Present ITI fixation:
    timer.reset()
    ITI_start = timer.getTime()
    text.text = " "
    text.draw()
    win.flip()
    
    while timer.getTime() < (stim_df["ITI"][i] + ITI_start):
        if 'escape' in event.getKeys():
            core.quit()
        
        if run_type == 'beh':
            if (stim_df["TotalTrialTime"][i] + intensity_rating_time + valence_rating_time) <= trialTimer.getTime():
                break
        else:
            if (stim_df["TotalTrialTime"][i]) <= trialTimer.getTime():
                break
    ITI_end = timer.getTime()
    trial_end = trialTimer.getTime()
    cumulativeTrialEnd = cumulativeTrialTimer.getTime()
    
    #Panda Output File
    if run_type == 'beh':
        run_param_list.append([cumulativeTrialStart, trial_start, fixation_time, prime_time, 
            target_time, intensity_rating_time, valence_rating_time, (ITI_end - ITI_start), trial_end, cumulativeTrialEnd, stim_df["Prime"][i][-11:], 
            stim_df["Target"][i][-11:], intensity_rating, intensity_RT, valence_rating, valence_RT, stim_df["Condition"][i]])
    else:
        run_param_list.append([cumulativeTrialStart, trial_start, fixation_time, prime_time, 
            target_time, (ITI_end - ITI_start), trial_end, cumulativeTrialEnd, stim_df["Prime"][i][-11:], stim_df["Target"][i][-11:], stim_df["Condition"][i]])
    
    os.chdir(fileLocation)
    fid = pd.DataFrame(run_param_list, columns = header)
    fid.to_csv(fileName, header = True)
    os.chdir(cwd)

if run_type == "scan":
    #11-second fixation:
    tend = timer.getTime()
    text.text = " "
    text.draw()
    win.flip()
    while timer.getTime() < 11 + tend:
        pass 
else:
    pass

if run == 'practice':
    parallel.setData(17)
    core.wait(0.5)
    parallel.setData(0)
elif run == 1:
    parallel.setData(11)
    core.wait(0.5)
    parallel.setData(0)
elif run == 2:
    parallel.setData(12)
    core.wait(0.5)
    parallel.setData(0)  
elif run == 3:
    parallel.setData(13)
    core.wait(0.5)
    parallel.setData(0)
elif run == 4:
    parallel.setData(14)
    core.wait(0.5)
    parallel.setData(0)
elif run == 5:
    parallel.setData(15)
    core.wait(0.5)
    parallel.setData(0)
elif run == 6:
    parallel.setData(16)
    core.wait(0.5)
    parallel.setData(0)



if expInfo['run'] == 'practice':
    text.text = 'End of practice'
else:
    text.text = "End of run %s" %expInfo["run"]    
text.pos = (0,0)
text.draw()
win.flip()

"""
parallel.setData(18)
core.wait(0.5)
parallel.setData(0)
"""

while True:
    theseKeys = event.getKeys()
    if "escape" in theseKeys:
        core.quit()
    if "space" in theseKeys:
        break

#Finished:
win.close()
core.quit()

