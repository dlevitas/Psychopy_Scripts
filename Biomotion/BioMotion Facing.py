#BioMotion Facing Task 

from __future__ import division
from psychopy import locale_setup, visual, core, event, data, gui
import numpy as np
import pandas as pd
import os, csv, time, random, platform
import subprocess as subp
import shlex

#Directory:
cwd = os.path.dirname(__file__)

# Get monitor resolution, based on computer's operating system:
if platform.system() == "Windows":
    from win32api import GetSystemMetrics
    width, height = GetSystemMetrics(0), GetSystemMetrics(1)
elif platform.system() == "Darwin":
    p = subp.Popen(shlex.split("system_profiler SPDisplaysDataType"), stdout=subp.PIPE)
    output = subp.check_output(('grep', 'Resolution'), stdin=p.stdout).strip()
 
    if "Retina" in output:
        width = 1920
        height = 1080
    else:    
        width, height, hz = [int(x) for x in output.split() if x.isdigit()]
        
#Create GUI:
expInfo = {"Subject ID":"","Run": "1","All": "No"} #Run 1 = Right vs Left; Run 2 = Forward vs Backward

dlg = gui.DlgFromDict(dictionary = expInfo, order = ["Subject ID","Run","All"])
if dlg.OK == False:
    core.quit()
if expInfo["Subject ID"] == "" or expInfo["Run"] == "" or expInfo["All"] == "" or expInfo["All"] == "":
    raise ValueError("Please be sure to fill in information")
if expInfo["Run"] > "2":
    raise ValueError("Run number should either be 1 or 2")
expInfo["Date"] = data.getDateStr()
    
#Determine if Running entire script or only portion:
if expInfo["All"] == str("Yes"):
    options = [1,2]
    RunList =  [int(expInfo["Run"]), list(set(options) - set([int(expInfo["Run"])]))[0]]
else:
    RunList = [int(expInfo["Run"])]     
    
#Create directory for data, if it doesn't exist, and check for duplicate files:
fileLocation = os.path.join(cwd + "/Data")
pracfileName = "DATA.%s.practice.%s.csv" %(expInfo["Subject ID"], expInfo["Date"])
fileName = "DATA.%s.%s.csv" %(expInfo["Subject ID"], expInfo["Date"])
statfileName1 = "DATA.%s.lvr.csv" %expInfo["Subject ID"]
statfileName2 = "DATA.%s.fvb.csv" %expInfo["Subject ID"]

if not os.path.exists(fileLocation):
    os.makedirs(fileLocation)
os.chdir(fileLocation)
if os.path.isfile(pracfileName):
    os.remove(pracfileName)
elif os.path.isfile(fileName):
    os.remove(fileName)  
else:
    os.chdir(cwd)
    
#Window:
win = visual.Window(size = (width, height), fullscr = True, pos = (0,0), units = 'norm', color = 'Black')    

#Timer:
timer = core.Clock()

#Turn Mouse Off:
event.Mouse(visible=False) 

#Text Stimulus:
text = visual.TextStim(win = win, text = '', height = 0.1, pos = (0,0), color="White", alignHoriz="center", alignVert="center")

#Get Frame Rate:
fr = win.getActualFrameRate()
if fr == None:
    print "Couldn't measure a consistent frame rate. Setting to default (60)"
    fr = 100

#Get frame rate speed:
if platform.system() == "Windows":
    speed = 0.95/fr
elif platform.system() == "Darwin":
    speed = 0.9/fr

#Defining all Functions: This is where the real magic happens
#Function 1: Determine which walkerType to use for specific trial. Each file contains different (x,y) coordinates, which determine stick figure movement
def walkerType(walkertype):
    if walkertype == 0:
        dotsloc = pd.read_csv('WalkerLeftForward.walker.csv', header=None)
        dotschange = pd.read_csv('WalkerLeftForward.changer.csv',header=None)
    elif walkertype == 1:
        dotsloc = pd.read_csv('WalkerLeftBackward.walker.csv',header=None)
        dotschange = pd.read_csv('WalkerLeftBackward.changer.csv',header=None)
    elif walkertype == 2:
        dotsloc = pd.read_csv('WalkerRightForward.walker.csv',header=None)
        dotschange = pd.read_csv('WalkerRightForward.changer.csv',header=None)
    elif walkertype == 3:
        dotsloc = pd.read_csv('WalkerRightBackward.walker.csv',header=None)
        dotschange = pd.read_csv('WalkerRightBackward.changer.csv',header=None)
    else:
        raise ValueError("Number not supported")
        
    return dotsloc, dotschange
        
#Function 2: Draws a Stick Figure, excluding noise dots
rate = 0.0 
frame_time = core.Clock()  
dot_xys1 = []
def stickFig(dotsloc):
    playcounter = 0

    for z in xrange(int(len(dotsloc)/2)): #Total of 122 rows, but 61 rows are x-coords, and 61 are y-coords, so iterating 61 times
        frame_time.reset()
        theseKeys = event.getKeys()
        if "escape" in theseKeys:
            core.quit()

        for j in xrange(int(len(dotsloc.columns.values))): #13 columns = 13 dots
        
            dot_xys1.append([dotsloc.ix[playcounter:playcounter+1,j][playcounter]/(-width/2), 
                        dotsloc.ix[playcounter:playcounter+1,j][playcounter+1]/(-height/2)])
                       
        dot_stim1 = visual.ElementArrayStim(win, units="norm",nElements = 13, sizes= (0.013,0.02), xys = dot_xys1, elementMask = "circle", elementTex=None)           
        dot_stim1.draw()
        
        playcounter += 2
        
        while frame_time.getTime() < 3 * speed:
            if 'escape' in event.getKeys():
                core.quit()
                
        win.flip()        
                            
        del dot_xys1[:]

#Function 3: Sets the parameters that determine how many noise dots are presented, and where: 
def setBlockParams(RunType, NoiseDotsStartLvl, Multiplier, Run):            
    if RunType == "Tutorial":
        Multiplier = 0
         
    elif RunType == "Practice":
        NoiseDotsNum=Multiplier*NoiseDotsStartLvl
        if Run == 1:
            taskInstructions = 'Press the "z" button if the person is facing to the left,\n\nand press the "m" button if the person is facing to the right.\n\nWe will get started with some practice!'
            triallist = pd.read_csv("triallist_practice.Run1.csv")
            responseInstructions = "\t\t\tFacing?\n\n <- Left     or     Right->"
        else:
            taskInstructions = 'Press the "z" button if the person is walking forward,\n\nand press the "m" button if the person is walking backward.\n\nWe will get started with some practice!'
            triallist = pd.read_csv("triallist_practice.Run2.csv")
            responseInstructions = "\t\t\tDirection?\n\n Forward     or     Backward"
         
    elif RunType == "MainRun":
        if NoiseDotsStartLvl <= 6:
            NoiseDotsNum=Multiplier*NoiseDotsStartLvl
        else:
            NoiseDotsNum = 12
            
        if Run == 1:
            taskInstructions = 'Press the "z" button if the person is facing to the left,\n\nand press the "m" button if the person is facing to the right.\n\nWe will get started soon!'
            triallist = pd.read_csv("triallist_Run1.csv")
            responseInstructions = "\t\t\tFacing?\n\n <- Left     or     Right->"
        else:
            taskInstructions = 'Press the "z" button if the person is walking forward,\n\nand press the "m" button if the person is walking backward.\n\nWe will get started soon!'
            triallist = pd.read_csv("triallist_Run2.csv")
            responseInstructions = "\t\t\tDirection?\n\n Forward     or     Backward"         
    else:
        raise ValueError("RunType should be 'Tutorial', 'Practice', or 'MainRun'.")
        
    return NoiseDotsStartLvl, NoiseDotsNum, taskInstructions, triallist, responseInstructions

#Function #4: Creates stick figure with varying noise dots floating in space
def StickFigNoise(dotsloc, dotschange, NoiseDotsNum, RunType, NoiseDotsStartLvl):
    
    xmin = min(dotsloc.ix[0])
    xmax = max(dotsloc.ix[0])
    ymin = min(dotsloc.ix[1])
    ymax = max(dotsloc.ix[1])

    XNoiseDots = range(-100,101)
    random.shuffle(XNoiseDots)
    finalrXNoiseDots = pd.DataFrame(XNoiseDots[0:NoiseDotsNum])

    YNoiseDots = range(int(ymin),int(ymax+1))
    random.shuffle(YNoiseDots)
    finalrYNoiseDots = pd.DataFrame(YNoiseDots[0:NoiseDotsNum])

    finalnoiseloc = pd.concat([finalrXNoiseDots, finalrYNoiseDots], axis=1) 
   
    playcounter = 0
    
    rcols = range(dotschange.shape[1])
    random.shuffle(rcols)
    curchange = dotschange.copy().ix[:,rcols]
    
    timer.reset()
    stim_onset_time = timer.getTime()
    
    dot_xys1 = []
    dot_xys2 = []
    
    rate = 0.0
    
    frame_time = core.Clock()
    for z in xrange(int(len(dotsloc)/2)): #Total of 122 rows, but 61 rows are x-coords, and 61 are y-coords, so iterating 61 times
        frame_time.reset()
        theseKeys = event.getKeys()
        if "escape" in theseKeys:
            core.quit()
        
        for j in xrange(int(len(dotsloc.columns.values))): #13 columns = 13 dots

            dot_xys1.append([dotsloc.ix[playcounter:playcounter+1,j][playcounter]/(-width/2), 
                        dotsloc.ix[playcounter:playcounter+1,j][playcounter+1]/(-height/2)])
                       
        dot_stim1 = visual.ElementArrayStim(win, units="norm",nElements = 13, sizes= (0.013,0.02), xys = dot_xys1, elementMask = "circle", elementTex=None)           
        dot_stim1.draw()           
            
        for j in xrange(finalnoiseloc.shape[0]):
            trialchanger = (curchange.iloc[playcounter:playcounter+2,j][playcounter],
                            curchange.iloc[playcounter:playcounter+2,j][playcounter+1])
            finalnoiseloc[j:j+1] += np.array(trialchanger)
            truefinalnoiseloc = np.array(finalnoiseloc[j:j+1])
            
            dot_xys2.append([truefinalnoiseloc[0][0]/(-width/2), truefinalnoiseloc[0][1]/(-height/2)])
        dot_stim2 = visual.ElementArrayStim(win, units="norm",nElements = NoiseDotsNum, sizes= (0.013,0.02), xys = dot_xys2, elementMask = "circle", elementTex=None)            
        dot_stim2.draw()
        
        playcounter += 2

        while frame_time.getTime() < 3 * speed:
            if 'escape' in event.getKeys():
                core.quit()
                
        win.flip()        
                            
        del dot_xys1[:]
        del dot_xys2[:]

    stim_offset_time = timer.getTime()
    
    return stim_onset_time, stim_offset_time   
                
#Function #5: Gets Button Response and Reaction Time (only first response recorded)
def ButtonResponse():
    event_press = event.clearEvents(eventType = "keyboard")
    event_press = []
    response = None
    timer.reset()
    while True:
        event_press = event.getKeys(keyList = ["z","m","escape"])
        if "escape" in event_press:
            core.quit()
        if len(event_press) and not response:
            RT = timer.getTime()
            response = event_press[0]
        if response:
            break
            
    return response, RT

#Function #6: Checks Accuracy on Practice and Main Runs
def AccuracyCheck(response, Run):
    acc, corrAns = [0,0]
    if Run == 1:
        if response == "z":
            if triallist["Facing"][i] == "Left":
                acc = 1
                corrAns = "z"
            else:
                acc = 0
                corrAns = "m"
        elif response == "m":
            if triallist["Facing"][i] == "Right":
                acc = 1
                corrAns = "m"
            else:
                acc = 0
                corrAns = "z"
    else:
        if response == "z":
            if triallist["Direction"][i] == "Forward":
                acc = 1
                corrAns = "z"
            else:
                acc = 0
                corrAns = "m"
        elif response == "m":
            if triallist["Direction"][i] == "Backward":
                acc = 1
                corrAns = "m"
            else:
                acc = 0
                corrAns = "z"
              
    return acc, corrAns
    
#Function #7: Gets the TrialSigns (3 correct in a row = "+", and an incorrect = "-", but only if NoiseDotsStartLvl > 1)
def TrialSign(acc, NoiseDotsStartLvl, correctcounter, incorrectcounter, RunType):
    if acc == 1:
        correctcounter += 1
        if correctcounter > 2:
            NoiseDotsStartLvl += 1
            correctcounter = 0
            TrialSigns.append("+")
        if RunType == "Practice":
            Instructions("\t\tCorrect")
    else:
        correctcounter = 0
        incorrectcounter = 1
        if incorrectcounter == 1 and NoiseDotsStartLvl > 1:
            NoiseDotsStartLvl -= 1
            TrialSigns.append("-")
        else:
            pass
        if RunType == "Practice":
            Instructions("\t\tIncorrect")
        
    return TrialSigns, NoiseDotsStartLvl, correctcounter, incorrectcounter
    
#Function #8: Keeps track of reversals:
def Reversal(TrialSigns, reversals, targetreversals):
    reversals = 0
    if len(TrialSigns) > 1:
        for t in range(len(TrialSigns)):
            if t == 0:
                pass
            else:
                if TrialSigns[t] != TrialSigns[t-1]:
                    reversals += 1 
    return reversals

#Function #9: Draws fixation cross on screen for 0.5 sec       
def fixation():
    t0 = timer.getTime()    
    text.text = "+"
    text.draw()
    win.flip()
    while timer.getTime() < 0.5 + t0:
        pass
    timer.reset()    
    
#Function #10: Presents Instructions  
def Instructions(str):
    text.text = str
    theseKeys = event.clearEvents(eventType = "keyboard")
    theseKeys = []
    text.draw()
    win.flip()
    while True:
        theseKeys = event.getKeys(keyList=['escape','space'])
        if "escape" in theseKeys:
            core.quit()
        if len(theseKeys):
            break
                     
#Create parameter lists for practice and main run outputs:
prac_param_list = []
run_param_list = []
header = ["Run","Stimulus Onset Time","Stimulus Offset Time","Response","Correct Response","Accuracy","RT","Num Noise Dots","Trial Noise Level","Trial Signs","Reversals"]
      
#================== Begin Tutorial: Display Instructions and Stick Figure Examples ==================

RunType = "Tutorial"

Instructions("Today you will see some videos of dots\n\tin the shape of a person")
Instructions('\t\t\tIn this game\nyou will see the person walking.\n\t(press space to continue)')

#Forward walking while facing right:
Instructions('Sometimes he is walking\n\t\t\tforwards.')
stickFig(pd.read_csv('WalkerRightForward.walker.csv', header=None))

#Walking backward while facing right:
Instructions('Sometimes he is walking backwards')
stickFig(pd.read_csv('WalkerRightBackward.walker.csv',header=None))

#Walking forward while facing left:
Instructions('Sometimes he is facing left.')
stickFig(pd.read_csv('WalkerLeftForward.walker.csv',header=None))
        
#Walking forward while facing right:
Instructions('Sometimes he is facing right')
stickFig(pd.read_csv('WalkerRightForward.walker.csv', header=None))
          
Instructions('Your job is to tell me\n\twhat direction\n\the is facing')

NoiseDotsStartLvl = 3
NoiseDotsNum = 12

Instructions('Sometimes it will look\n\tlike this...')
StickFigNoise(pd.read_csv("WalkerRightBackward.walker.csv", header=None), pd.read_csv("WalkerRightBackward.changer.csv", header=None), NoiseDotsNum, RunType, NoiseDotsStartLvl)

Instructions('Try your best\nbut if you are unsure\njust guess!')
     
#================== Tutorial complete. Moving to practice section ==================
repeat = 0
for x in RunList:
    Run = x
    RunType = "Practice"

    correctcounter, incorrectcounter = [0,0]
    reversals = 0
    targetreversals = 12
    Multiplier = 2
    TrialSigns = []
    NoiseDotsStartLvl, NoiseDotsStartLvl_new = [1,1]

    taskInstructions, triallist = setBlockParams(RunType, NoiseDotsStartLvl, Multiplier, Run)[2:4]

    #Display task Instructions
    Instructions(taskInstructions) 
    
    #Display 0.5 second fixation
    fixation()
    
    for i in xrange(len(triallist)):
        theseKeys = event.getKeys()
        if "escape" in theseKeys:
            core.quit()
            
        dotsloc, dotschange = walkerType(np.int(triallist["WalkerType"][i]))
        NoiseDotsStartLvl, NoiseDotsNum, responseInstructions = [setBlockParams(RunType, NoiseDotsStartLvl_new, Multiplier, Run)[x] for x in [0,1,4]]
        print NoiseDotsStartLvl
        
        #Display 0.5 second fixation
        fixation() 
        
        #Draw Stick Figure
        stim_onset_time, stim_offset_time = StickFigNoise(dotsloc, dotschange, NoiseDotsNum, RunType, NoiseDotsStartLvl)
        
        #Right or Left? Forward or Backward?
        text.text = responseInstructions
        text.draw()
        win.flip()
        
        #Record Button Response and RT
        response, RT = ButtonResponse()
               
        #Display 0.5 second fixation
        fixation()
        
        #Record Accuracy
        acc, corrAns = AccuracyCheck(response, Run)
        
        #Record trial signs ("+" or "-"), if any
        TrialSigns, NoiseDotsStartLvl_new, correctcounter, incorrectcounter = TrialSign(acc, NoiseDotsStartLvl, correctcounter, incorrectcounter, RunType)
        
        #Record reversals, if any
        reversals = Reversal(TrialSigns, reversals, targetreversals)
        
        #Output File (Practice)
        if len(TrialSigns):
            out = TrialSigns[:]
        else:
            out = []
        prac_param_list.append([Run, stim_onset_time, stim_offset_time, response, corrAns, acc, RT, NoiseDotsNum, NoiseDotsStartLvl, out, reversals])
        """Keeping this in the loop so that way if you quit early the data is still saved. A bit unorthodox. If this
            seems uneccessary than just move the next 4 lines outside of the loop"""
        os.chdir(fileLocation)
        fid = pd.DataFrame(prac_param_list, columns = header)
        fid.to_csv(pracfileName, header = True)
        os.chdir(cwd)

        if reversals >= targetreversals:
            break
    #================== End of practice. Moving to Main Run(s) ================== 
    RunType = "MainRun"
    Instructions('You have completed the practice!\n\nNow we will go on to the real game.\n\nIn the real game, it will not say if you got it right or wrong.\n\nJust do your best. The game will begin soon!')

    correctcounter, incorrectcounter = [0,0]
    reversals = 0
    targetreversals = 12
    Multiplier = 2
    TrialSigns = []
    NoiseDotsStartLvl, NoiseDotsStartLvl_new = [1,1]

    taskInstructions, triallist = setBlockParams(RunType, NoiseDotsStartLvl, Multiplier, Run)[2:4]
    
    #Display task Instructions
    Instructions(taskInstructions) 
    
    #Display 0.5 second fixation
    fixation()

    for i in xrange(len(triallist)):
        theseKeys = event.getKeys()
        if "escape" in theseKeys:
            core.quit()
            
        dotsloc, dotschange = walkerType(np.int(triallist["WalkerType"][i]))
        NoiseDotsStartLvl, NoiseDotsNum, responseInstructions = [setBlockParams(RunType, NoiseDotsStartLvl_new, Multiplier, Run)[x] for x in [0,1,4]]
        
        #Draw Stick Figure
        stim_onset_time, stim_offset_time = StickFigNoise(dotsloc, dotschange, NoiseDotsNum, RunType, NoiseDotsStartLvl)
        
        #Right or Left? Forward or Backward?
        text.text = responseInstructions
        text.draw()
        win.flip()
        
        #Record Button Response and RT
        response, RT = ButtonResponse()
               
        #Display 0.5 second fixation
        fixation()
        
        #Record Accuracy
        acc, corrAns = AccuracyCheck(response, Run)
        
        #Record trial signs ("+" or "-"), if any
        TrialSigns, NoiseDotsStartLvl_new, correctcounter, incorrectcounter = TrialSign(acc, NoiseDotsStartLvl, correctcounter, incorrectcounter, RunType)
       
        #Record reversals, if any
        reversals = Reversal(TrialSigns, reversals, targetreversals)
        
        #Output File (MainRuns)
        if len(TrialSigns):
            out = TrialSigns[:]
        else:
            out = []
        run_param_list.append([Run, stim_onset_time, stim_offset_time, response, corrAns, acc, RT, NoiseDotsNum, NoiseDotsStartLvl, out, reversals])
        """Keeping this in the loop so that way if you quit early the data is still saved. A bit unorthodox. If this
            seems uneccessary than just move the next 4 lines outside of the loop"""
        os.chdir(fileLocation)
        fid = pd.DataFrame(run_param_list, columns = header)
        fid.to_csv(fileName, header = True)
        os.chdir(cwd)

        if reversals >= targetreversals:
                break
    
    if repeat == 0 and len(RunList) > 1:
        Instructions("\t\t Great job! Please wait for more.")
        Instructions("\t In the last part\n you had to say if the person\n was facing to the left, or to the right")
        Instructions("\t This time you see the guy walking\n\t\t just like before, but your job\n\t\t\t\t is different!")
        Instructions("\tThis time, your job is to tell me\n what direction he is walking in.")
            
        #Forward walking while facing right:
        Instructions('Sometimes he is walking\n\t\t\tforwards.')
        stickFig(pd.read_csv('WalkerRightForward.walker.csv', header=None))

        #Walking backward while facing right:
        Instructions('Sometimes he is walking backwards')
        stickFig(pd.read_csv('WalkerRightBackward.walker.csv',header=None))
        Instructions("\t\t Try your best\t\n but if you are unsure\n\t\t just guess!")
        repeat += 1   
    else:
        pass
        
Instructions("\t\tEnd of experiment")        
#================== End of Experiment ==================
#Perform a simple analysis of the data (excluding practice section(s))
#lvr = Left vs Right
#fvb = Forward vs Backward
lvr_stat_param_list = []
fvb_stat_param_list = []
header = ["# Trials","Correct","Incorrect","% Correct","% Incorrect", "# Reversals", "Highest Trial Noise Level Achieved", "Final Trial Noise Level"," Avg RT"]

os.chdir(os.path.join(cwd + "/Data"))

df = pd.read_csv("DATA.%s.%s.csv" %(expInfo["Subject ID"], expInfo["Date"]))
if len(df.Run.unique()) == 2:
    lvr = df.query('Run == 1')
    fvb = df.query('Run == 2')
    
    lvr = lvr.reset_index()
    fvb = fvb.reset_index()
    
else:
    if expInfo["Run"] == '1':
        lvr = df.query('Run == 1')
        fvb = pd.DataFrame()
    else:
        fvb = df.query('Run == 2')
        lvr = pd.DataFrame()

if len(fvb) == 0:
    fvb_numTrials, fvb_Correct, fvb_Incorrect, fvb_percentCorrect, fvb_percentIncorrect, fvb_finalReversals, fvb_highestTrialNoiseLvl, fvb_finalTrialNoiseLvl, fvb_avgRT = ['N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A']
    lvr_numTrials = len(lvr)
    lvr_Correct = len(lvr.query('Accuracy == 1'))
    lvr_Incorrect = len(lvr.query('Accuracy == 0'))
    lvr_percentCorrect = round((lvr_Correct/lvr_numTrials)*100,2)
    lvr_percentIncorrect = round((lvr_Incorrect/lvr_numTrials)*100,2)
    lvr_finalReversals = max(lvr["Reversals"])
    lvr_highestTrialNoiseLvl = max(lvr["Trial Noise Level"])
    lvr_finalTrialNoiseLvl = lvr["Trial Noise Level"][len(lvr)-1]
    lvr_avgRT = pd.DataFrame.mean(pd.DataFrame(lvr["RT"]))[0]
elif len(lvr) == 0:
    lvr_numTrials, lvr_Correct, lvr_Incorrect, lvr_percentCorrect, lvr_percentIncorrect, lvr_finalReversals, lvr_highestTrialNoiseLvl, lvr_finalTrialNoiseLvl, lvr_avgRT = ['N/A','N/A', 'N/A','N/A','N/A','N/A','N/A','N/A','N/A']
    fvb_numTrials = len(fvb)
    fvb_Correct = len(fvb.query('Accuracy == 1'))
    fvb_Incorrect = len(fvb.query('Accuracy == 0'))
    fvb_percentCorrect = round((fvb_Correct/fvb_numTrials)*100,2)
    fvb_percentIncorrect = round((fvb_Incorrect/fvb_numTrials)*100,2)
    fvb_finalReversals = max(fvb["Reversals"])
    fvb_highestTrialNoiseLvl = max(fvb["Trial Noise Level"])
    fvb_finalTrialNoiseLvl = fvb["Trial Noise Level"][len(fvb)-1]
    fvb_avgRT = pd.DataFrame.mean(pd.DataFrame(fvb["RT"]))[0]        
else:
    lvr_numTrials = len(lvr)
    fvb_numTrials = len(fvb)

    lvr_Correct = len(lvr.query('Accuracy == 1'))
    fvb_Correct = len(fvb.query('Accuracy == 1'))

    lvr_Incorrect = len(lvr.query('Accuracy == 0'))
    fvb_Incorrect = len(fvb.query('Accuracy == 0'))
    
    lvr_percentCorrect = round((lvr_Correct/lvr_numTrials)*100,2)
    fvb_percentCorrect = round((fvb_Correct/fvb_numTrials)*100,2)
    
    lvr_percentIncorrect = round((lvr_Incorrect/lvr_numTrials)*100,2)
    fvb_percentIncorrect = round((fvb_Incorrect/fvb_numTrials)*100,2)

    lvr_finalReversals = max(lvr["Reversals"])
    fvb_finalReversals = max(fvb["Reversals"])

    lvr_highestTrialNoiseLvl = max(lvr["Trial Noise Level"])
    fvb_highestTrialNoiseLvl = max(fvb["Trial Noise Level"])

    lvr_finalTrialNoiseLvl = lvr["Trial Noise Level"][len(lvr)-1]
    fvb_finalTrialNoiseLvl = fvb["Trial Noise Level"][len(fvb)-1]

    lvr_avgRT = pd.DataFrame.mean(pd.DataFrame(lvr["RT"]))[0]
    fvb_avgRT = pd.DataFrame.mean(pd.DataFrame(fvb["RT"]))[0]        

if len(df.Run.unique()) == 2:
    lvr_stat_param_list.append([lvr_numTrials, lvr_Correct, lvr_Incorrect, lvr_percentCorrect, lvr_percentIncorrect, lvr_finalReversals, lvr_highestTrialNoiseLvl, lvr_finalTrialNoiseLvl, lvr_avgRT])
    fvb_stat_param_list.append([fvb_numTrials, fvb_Correct, fvb_Incorrect, fvb_percentCorrect, fvb_percentIncorrect, fvb_finalReversals, fvb_highestTrialNoiseLvl, fvb_finalTrialNoiseLvl, fvb_avgRT])   
else:
    if expInfo["Run"] == '1':
        lvr_stat_param_list.append([lvr_numTrials, lvr_Correct, lvr_Incorrect, lvr_percentCorrect, lvr_percentIncorrect, lvr_finalReversals, lvr_highestTrialNoiseLvl, lvr_finalTrialNoiseLvl, lvr_avgRT])
    else:
        fvb_stat_param_list.append([fvb_numTrials, fvb_Correct, fvb_Incorrect, fvb_percentCorrect, fvb_percentIncorrect, fvb_finalReversals, fvb_highestTrialNoiseLvl, fvb_finalTrialNoiseLvl, fvb_avgRT])   

os.chdir(cwd)
statsLocation = os.path.join(cwd + "/Analysis")
if not os.path.exists(statsLocation):
    os.mkdir(statsLocation)
os.chdir(statsLocation)
 
if len(df.Run.unique()) == 2: 
    lvr_fid = pd.DataFrame(lvr_stat_param_list, columns = header)
    fvb_fid = pd.DataFrame(fvb_stat_param_list, columns = header)
    lvr_fid.to_csv(statfileName1, header = True)  
    fvb_fid.to_csv(statfileName2, header = True)
else:
    if expInfo["Run"] == '1':
        lvr_fid = pd.DataFrame(lvr_stat_param_list, columns = header)
        lvr_fid.to_csv(statfileName1, header = True) 
    else:
        fvb_fid = pd.DataFrame(fvb_stat_param_list, columns = header)
        fvb_fid.to_csv(statfileName2, header = True)
    
#Exit PsychoPy Script:
win.close()
core.quit()

     