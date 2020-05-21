#CMNT Experiment:

from __future__ import division
from psychopy import locale_setup, visual, core, event, data, gui
from jkpsycho import *
import numpy as np
import pandas as pd
import sys, os, csv, time, random, unicodedata, platform
import subprocess as subp
import shlex

#Set directory:
cwd = os.path.dirname(__file__)

#Connect to Scanner:
scanner_coms = ScannerComs(port=3, timeout=0.001, baudrate=19200, keyboard=True)

#Determine Monitor Resolution:
if platform.system() == "Windows":
    from win32api import GetSystemMetrics
    width, height = GetSystemMetrics(0), GetSystemMetrics(1)
elif platform.system() == "Darwin":
    p = subp.Popen(shlex.split("system_profiler SPDisplaysDataType"), stdout=subp.PIPE)
    output = subp.check_output(('grep', 'Resolution'), stdin=p.stdout)
    width, height = [int(x.strip(' ')) for x in output.split(':')[-1].split(' x ')]

#Create GUI:
expName = "CMNT"
expInfo = {"participant ID": "", "run": "", "condition": ""} #Condition Files: F1, F2, M1, M2
dlg = gui.DlgFromDict(dictionary = expInfo, title = expName, order = ["participant ID","run"])
if dlg.OK == False:
    core.quit()
if expInfo["participant ID"] == "" or expInfo["run"] == "":
    raise ValueError ("Participant ID and run number boxes must contain numerical value")
if expInfo["run"] > '4':
    raise valueError ("Please enter appropriate run number")
if expInfo["condition"] not in ["F1", "F2", "M1", "M2"]:
    raise ValueError ("Condition must be F1, F2, M1 or M2")
conditionFile = expInfo["condition"]

#Output Directory and checking for duplicate files:
fileLocation = os.path.join(cwd + "/%s_data" %(expName))
fileName = "%s_Run%s.csv" %(expInfo["participant ID"], expInfo["run"])

if not os.path.exists(fileLocation):
    os.makedirs(fileLocation)
os.chdir(fileLocation)
if os.path.isfile(fileName):
    check = pd.read_csv(fileName)
    if len(check) < 24:
        os.remove(fileName)
    else:
        raise ValueError ("A log file already exists for this run")
    
if expInfo["run"] in ["2","3","4"] and os.path.isfile("%s_Run1.csv" %(expInfo["participant ID"])) == False:
    raise ValueError("Make sure that first chat session was run")
if expInfo["run"] in ["3","4"] and os.path.isfile("%s_Run2.csv" %(expInfo["participant ID"])) == False:
    raise ValueError("Make sure the second chat session occured")
if expInfo["run"] == "4" and os.path.isfile("%s_Run3.csv" %(expInfo["participant ID"])) == False:
    raise ValueError("Make sure that all other chat sessions have occurred")

#Determine which run to present:
if expInfo["run"] == '1':
    block_start = 0
    block_end = 24
elif expInfo["run"] == '2':
    block_start = 24
    block_end = 48
elif expInfo["run"] == '3':
    block_start = 48
    block_end = 72
elif expInfo["run"] == '4':
    block_start = 72
    block_end = 96

#Window:
win = visual.Window(size = (width, height), fullscr = True, pos = (0,0), units = "norm", color = [-1,-1,-1])

#Turn off Mouse
event.Mouse(visible = False)

#Timers:
timer = core.Clock() #Basic timer for moving from one trial component to the next 
cumulativeTimer = core.Clock()
trialTimer = core.Clock() #Records time of a single trial, but does so in a cumulative manner 
expTimer = core.Clock() #Records time of the entire run 
"""
Load ouput file from pickPartner script, and randomize data. 
This will randomize for the experiment right before run1. The stim file will not change for subsequent runs.
This means the stimulus file will not be constantly re-randomized for each run, which would cause previously
seen trials to appear in upcoming runs.
"""
partnerFileLoc = os.path.join(cwd + "/CMNT.pickPartner_data")
partnerFile = "%s_pickPartner.csv" %(expInfo["participant ID"])
os.chdir(partnerFileLoc)

partner = pd.read_csv("%s_pickPartner.csv" %(expInfo["participant ID"]))
      
chatBuddy = partner["PartnerName"][0]
chatBuddyPic = partner["PartnerPicture"][0]
promptNames = ["Caitlyn","Mia","Andrew","Sam","Ben"]
newName = partner["PromptName"][0]
conditionFile = partner["Condition"][0]

if expInfo["run"] == '1':
    def randomize(df):
        return df.reindex(np.random.permutation(df.index))
        
    os.chdir(cwd)
      
    df = pd.read_csv("conditions_%s.csv" %conditionFile)
    df.index = range(len(df))
    order = pd.read_csv("CMNTorder.csv", header=None)
    order.columns = ["MentalState"]   
    jitterTimes = pd.read_csv("Block_jittertimes.csv")
    columns = ["MentalState", "questionType", "questionVoice", "speaker", "prompt", "question",
              "answerA", "answerB", "corrAnswer","block"]   
    df["MentalState"] = np.nan

    for j in range(len(df)):
        if df["questionType"][j] == "Mental" and df["questionVoice"][j] == "first":
            df.loc[j, "MentalState"] = "PeerMental"
        elif df["questionType"][j] == "Mental" and df["questionVoice"][j] == "third":
            df.loc[j, "MentalState"] = "CompMental"
        elif df["questionType"][j] == "Physical" and df["questionVoice"][j] == "first":
            df.loc[j, "MentalState"] = "PeerNM"
        elif df["questionType"][j] == "Physical" and df["questionVoice"][j] == "third":
            df.loc[j, "MentalState"] = "CompNM"

    df = randomize(df)                                                                                         
    df_final = pd.DataFrame()

    CM_count = 0
    CNM_count = 0
    PM_count = 0
    PNM_count = 0

    CM_frame = df.query('questionType == "Mental" and questionVoice == "third"')
    PM_frame = df.query('questionType == "Mental" and questionVoice == "first"')
    CNM_frame = df.query('questionType == "Physical" and questionVoice == "third"')
    PNM_frame = df.query('questionType == "Physical" and questionVoice == "first"')

    CM_frame.index = range(len(CM_frame))
    CNM_frame.index = range(len(CNM_frame))
    PM_frame.index = range(len(PM_frame))
    PNM_frame.index = range(len(PNM_frame))

    for i in range(len(df)):
        if order["MentalState"][i] == "CompMental":
            df_final = df_final.append(CM_frame.ix[CM_count,columns])
            CM_count += 1
        elif order["MentalState"][i] == "CompNM":
            df_final = df_final.append(CNM_frame.ix[CNM_count,columns])
            CNM_count += 1
        elif order["MentalState"][i] == "PeerMental":
            df_final = df_final.append(PM_frame.ix[PM_count,columns])
            PM_count += 1
        elif order["MentalState"][i] == "PeerNM":
            df_final = df_final.append(PNM_frame.ix[PNM_count,columns])
            PNM_count += 1
        else:
            raise ValueError("%s is not any of the Mental States" % order["MentalState"][i])

    blocks = np.repeat(np.array([["A","B"],["C","D"]]), 24)
    df_final["block"] = blocks
    index = pd.Index(range(len(df_final)))
    df_final = df_final.set_index(index)
    df_final = df_final[columns]

    df_final = pd.concat([df_final, jitterTimes], axis=1)

    b1 = df_final.loc[df_final["block"] == "A"]
    b2 = df_final.loc[df_final["block"] == "B"]
    b3 = df_final.loc[df_final["block"] == "C"]
    b4 = df_final.loc[df_final["block"] == "D"]

    lis = [b1, b2, b3, b4]
    random.shuffle(lis)
    stim_df = pd.concat(lis) 

    for i in xrange(len(stim_df)):
        if stim_df["speaker"][i] != "Computer":
            stim_df["speaker"][i] = chatBuddy
        else:
            name = [name for name in promptNames if name in stim_df["prompt"][i]]
            stim_df["prompt"][i] = stim_df["prompt"][i].replace("".join(name), newName)
            
    stim_df.to_csv("exp_stimuli.csv", index=False)

os.chdir(cwd)

stim_df = pd.read_csv("exp_stimuli.csv", nrows = 97) #The stimuli file that's used in the experiment
#chatBuddy = stim_df["speaker"]

#List and Panda File Header 
run_param_list = []
header = ["CumulativeTrialStart","TrialStart","Block","MentalState", "Condition", "Speaker","Prompt", "PromptOnset", "PromptEnd", "ChoiceOnset", 
"ChoiceEnd", "RespButton", "CorrAnswer", "ButtonPressTime", "RT(sec)", "ACC", "ISI_Onset", "ISI_End", "FeedbackOnset", "FeedbackEnd", 
"ITI_Onset", "ITI_End", "TrialEnd","CumulativeTrialEnd"]

#Define text and image stimuli
text = visual.TextStim(win = win, text = '', height = 0.1, pos = (0,0), color="White")
text1 = visual.TextStim(win = win, text = '', height = 0.1, pos = (0,0), color="White")
text2 = visual.TextStim(win = win, text = '', height = 0.1, pos = (0,0), color="#99CCFF")
text3 = visual.TextStim(win = win, text = '', height = 0.1, pos = (0,0), color="White")
text4 = visual.TextStim(win = win, text = '', height = 0.1, pos = (0,0), color="White")

image = visual.ImageStim(win = win, pos = (0,0), size = (0.1,0.1), image = os.path.join(cwd + "/Stimuli/grayBlue.png"))
rect = visual.Rect(win=win, width = 0.3, height = 0.2, pos = (0,0))
    
#Run Instruction Page:
text.text = '\t\tREMEMBER:\n\t\tAnswer each question using the \n\t\tLEFT button for OPTION 1 and \n\t\tthe RIGHT button for OPTION 2.\n\n\t\t Please wait for the scanner.'
text.height = 0.1
text.draw()
win.flip()
while True:
    theseKeys = event.getKeys()
    if "escape" in theseKeys:
        core.quit() 
    """if "space" in theseKeys:
        break"""
    if "6" in scanner_coms.messages():
        break 
    
cumulativeTimer.reset()
#10-second fixation:
tstart = timer.getTime()
text.text = "+"
text.height = 0.25
text.draw()
win.flip()
while timer.getTime() < 10 + tstart:
    pass
    
timer.reset()
#Begin Trials:
for i in xrange(block_start, block_end):
    trialTimer.reset()
    cumulativeTrialStart = cumulativeTimer.getTime()
    trial_start = trialTimer.getTime()
    win.flip()
    conditionFile = partner["Condition"][0]
    
    exit_press = []
    event_press = []

    #0.5 seconds
    speaker = visual.TextStim(win, text = stim_df["speaker"][i], height = 0.1, pos = (0,0.6), color="#99CCFF")
    speaker.setAutoDraw(True)
    
    t0 = timer.getTime()

    while timer.getTime() < 0.5 + t0:
        win.flip() 
    timer.reset()
        
    #3.5 seconds
    if stim_df["speaker"][i] == "Computer":
        text.text = stim_df["prompt"][i].decode("utf8")
        text.pos = (-0.1,0)
        text.height = 0.1
        text.draw()
        text_box_length = (text.boundingBox[0]/width)*2 + 0.1
        
        image.image = os.path.join(cwd + "/Stimuli/grayBlue.png")
        image.pos = (-0.1,0)
        image.size = (text_box_length, 0.35)
        
        image.draw()
        text.draw()
    else:
        text.text = stim_df["prompt"][i].decode("utf8")
        text.pos = (-0.1,0)
        text.height = 0.1
        text.draw()
        text_box_length = (text.boundingBox[0]/(width))*2 + 0.1

        image.image = os.path.join(cwd + "/Stimuli/blue_darker.png") 
        image.pos = (-0.1,-.015)
        image.size = (text_box_length, 0.35)
        
        image.draw()
        text.draw()
        
    win.flip()
    t1 = timer.getTime()
    prompt_onset = trialTimer.getTime()
    
    while timer.getTime() < 3.5 + t1:
        exit_press += event.getKeys()
        if "escape" in exit_press:
            core.quit()
            
    prompt_end = trialTimer.getTime()
    speaker.setAutoDraw(False)
    timer.reset()
    onset_Time = timer.getTime()

    #4 seconds
    #if chatBuddy in ["Domenick","Harrison"]:
    """if chatBuddy == "Computer":
        text1.text = stim_df["question"][i]
        text1.pos = (0,0.6)
        text1.height = 0.1
        text1.setAutoDraw(True)
    else:"""
    text1.text = stim_df["question"][i]
    text1.pos = (0,0.3)
    text1.height = 0.1
    text1.setAutoDraw(True)
    
    if stim_df["speaker"][i] == chatBuddy:
        text2.text = chatBuddy
        text2.pos = (0,0.6)
        text2.height = 0.1
        text2.setAutoDraw(True)
    else:
        text2.text = "Computer"
        text2.pos = (0,0.6)
        text2.height = 0.1
        text2.setAutoDraw(True)
    
    text3.text = stim_df["answerA"][i]
    text3.pos = (-0.3, -0.3)
    text_box_length1 = (text3.boundingBox[0]/width)*2 + 0.05
    text3.setAutoDraw(True)
    
    text4.text = stim_df["answerB"][i]
    text4.pos = (0.3, -0.3)
    text4.height = 0.1
    text_box_length2 = (text4.boundingBox[0]/width)*2 + 0.05
    text4.setAutoDraw(True)
    win.flip()
        
    t3 = timer.getTime()
    choice_onset = trialTimer.getTime()
    
    event_press = event.clearEvents(eventType = "keyboard")
    RT = "N/A"
    buttonPressTime = "N/A"
    response = None
    scanner_coms.clear()
    while timer.getTime() < 4 + t3:
        if event.getKeys(keyList = ["escape"]):
            core.quit()
        """
        event_press = event.getKeys(keyList = ["1","0"])
        #event_press += [scanner_coms.read()]
        if len(event_press) and not response:
            RT = timer.getTime() - onset_Time - t3
            buttonPressTime = trialTimer.getTime() 
            response = event_press[0]
        """    
        butList = [x for x in scanner_coms.messages(as_set = False) if x in ["1","2"]]
        if len(butList) and not response:
            response = butList[0]
            RT = timer.getTime() - onset_Time - t3
            buttonPressTime = trialTimer.getTime()
            
        if response == "1":
            rect.pos = (-0.3, -0.3)
            rect.width = text_box_length1
            rect.height = 0.2
            rect.draw()
        elif response == "2":
            rect.pos = (0.3, -0.3)
            rect.width = text_box_length2
            rect.height = 0.2
            rect.draw()
        else:
            pass
            
        win.flip()
                   
    choice_end = trialTimer.getTime()
    timer.reset()
    text1.setAutoDraw(False)
    text2.setAutoDraw(False)
    text3.setAutoDraw(False)
    text4.setAutoDraw(False)
    
    #ISI time
    text.text = "+"
    text.pos = (0,0)
    text.height = 0.25
    text.draw()
    win.flip()
    
    t4 = timer.getTime()
    jitter1_onset = trialTimer.getTime()
    
    while timer.getTime() < (stim_df["jitter1"][i]/1000) + t4:
        exit_press += event.getKeys()
        if "escape" in exit_press:
            core.quit()
            
    jitter1_end = trialTimer.getTime()
    timer.reset()
    
    #Check Button Presses:
    if response == "1":
        reply = stim_df["answerA"][i]
        if reply == stim_df["corrAnswer"][i]:
            acc = 1
        else:
            acc = 0   
    elif response == "2":
        reply = stim_df["answerB"][i]
        if reply == stim_df["corrAnswer"][i]:
            acc = 1
        else:
            acc = 0
    else:
        response = 'N/A'
        reply = stim_df["corrAnswer"][i]
        acc = 0
       
    text.text = reply
    text.height = 0.1
    text.pos = (0.1,0.3)
    
    #2 seconds
    win.flip()
    if stim_df["speaker"][i] == "Computer": 
        if acc == 1:
            text.text = reply
            text.height = 0.1
            text.pos = (0.1,0.3)
            
            speaker.draw()
            text.draw()
            image.image = os.path.join(cwd + "/Stimuli/grayGreen.png")
            image.size = (text.boundingBox[0]/width*2 + 0.1, text.boundingBox[1]/height*2 + 0.1)
            image.pos = (0.1, 0.3)
            
            image.draw()
            text.draw()
            
            text.pos = (-0.1,-0.1)
            text.text = reply + u" \u2713"
            text_box_length = text.boundingBox[0]/width*2 + 0.1
            
            image.image = os.path.join(cwd + "/Stimuli/grayBlue.png")
            image.size = (text.boundingBox[0]/width*2 + 0.1, text.boundingBox[1]/height*2 + 0.1)
            image.pos = (-0.1,-0.1)
            
            image.draw()
            text.draw()
        if acc == 0:
            if response == "N/A":
                text.text = "     "
                text.height = 0.1
                text.pos = (0.1,0.3)
                
                speaker.draw()
                text.draw()
                image.image = os.path.join(cwd + "/Stimuli/grayGreen.png")
                image.size = (text.boundingBox[0]/width*2 + 0.1, text.boundingBox[1]/height*2 + 0.1)
                image.pos = (0.1, 0.3)
                
                image.draw()
                text.draw()
                
                text.pos = (-0.1,-0.1)
                text.text = stim_df["corrAnswer"][i]
                text_box_length = text.boundingBox[0]/width*2 + 0.1
                
                image.image = os.path.join(cwd + "/Stimuli/grayBlue.png")
                image.size = (text.boundingBox[0]/width*2 + 0.1, text.boundingBox[1]/height*2 + 0.1)
                image.pos = (-0.1,-0.1)
                
                image.draw()
                text.draw()
            else:
                text.text = reply
                text.height = 0.1
                text.pos = (0.1,0.3)
                
                speaker.draw()
                text.draw()
                image.image = os.path.join(cwd + "/Stimuli/grayGreen.png")
                image.size = (text.boundingBox[0]/width*2 + 0.1, text.boundingBox[1]/height*2 + 0.1)
                image.pos = (0.1, 0.3)
                
                image.draw()
                text.draw()
                
                text.pos = (-0.1,-0.1)
                text.text = stim_df["corrAnswer"][i]
                text_box_length = text.boundingBox[0]/width*2 + 0.1
                
                image.image = os.path.join(cwd + "/Stimuli/grayBlue.png")
                image.size = (text.boundingBox[0]/width*2 + 0.1, text.boundingBox[1]/height*2 + 0.1)
                image.pos = (-0.1,-0.1)
                
                image.draw()
                text.draw()
    else: 
        if acc == 1:
            text.text = reply
            text.height = 0.1
            text.pos = (0.1,0.3)
            
            speaker.draw()
            text.draw()
            image.image = os.path.join(cwd + "/Stimuli/green_darker.png")
            image.size = (text.boundingBox[0]/width*2 + 0.1, text.boundingBox[1]/height*2 + 0.1)
            image.pos = (0.1, 0.285)
            
            image.draw()
            text.draw()
            
            text.text = reply + " :)"
            text.pos = (-0.1,-0.1)
            
            image.image = os.path.join(cwd + "/Stimuli/blue_darker.png")
            image.size = (text.boundingBox[0]/width*2 + 0.1, text.boundingBox[1]/height*2.5 + 0.1)
            image.pos = (-0.1,-0.115)
            
            image.draw()
            text.draw()
            
        if acc == 0:
            if response == "N/A":
                text.text = "     "
                text.height = 0.1
                text.pos = (0.1,0.3)
                
                speaker.draw()
                text.draw()
                image.image = os.path.join(cwd + "/Stimuli/green_darker.png")
                image.size = (text.boundingBox[0]/width*2 + 0.1, text.boundingBox[1]/height*2 + 0.1)
                image.pos = (0.1, 0.285)
                
                image.draw()
                text.draw()
                
                text.text = stim_df["corrAnswer"][i]
                text.pos = (-0.1,-0.1)
                
                image.image = os.path.join(cwd + "/Stimuli/blue_darker.png")
                image.size = (text.boundingBox[0]/width*2 + 0.1, text.boundingBox[1]/height*2.5 + 0.1)
                image.pos = (-0.1,-0.115)
                
                image.draw()
                text.draw()
            else:
                text.text = reply
                text.height = 0.1
                text.pos = (0.1,0.3)
                
                speaker.draw()
                text.draw()
                image.image = os.path.join(cwd + "/Stimuli/green_darker.png")
                image.size = (text.boundingBox[0]/width*2 + 0.1, text.boundingBox[1]/height*2 + 0.1)
                image.pos = (0.1, 0.285)
                
                image.draw()
                text.draw()
                
                text.text = stim_df["corrAnswer"][i]
                text.pos = (-0.1,-0.1)
                
                image.image = os.path.join(cwd + "/Stimuli/blue_darker.png")
                image.size = (text.boundingBox[0]/width*2 + 0.1, text.boundingBox[1]/height*2.5 + 0.1)
                image.pos = (-0.1,-0.115)
                
                image.draw()
                text.draw()

    win.flip()
    
    t5 = timer.getTime()
    feedback_onset = trialTimer.getTime()
    
    while timer.getTime() < 2.0 + t5:
        exit_press += event.getKeys()
        if "escape" in exit_press:
            core.quit()
            
    feedback_end = trialTimer.getTime()
    timer.reset()
     
    #ITI time
    text.text = "+"
    text.height = 0.25
    text.pos = (0,0)
    text.draw()
    win.flip()
    
    t6 = timer.getTime()
    jitter2_onset = trialTimer.getTime()
    
    while timer.getTime() < (stim_df["jitter2"][i]/1000) + t6:
        if (stim_df["TotalTrialTime"][i]/1000) <= trialTimer.getTime():
            break
            
    jitter2_end = trialTimer.getTime()
    trial_end = trialTimer.getTime()
    cumulativeTrialEnd = cumulativeTimer.getTime()
  
    #Panda Output File
    run_param_list.append([cumulativeTrialStart, trial_start, stim_df["block"][i], stim_df["MentalState"][i], conditionFile, stim_df["speaker"][i], 
    stim_df["prompt"][i], prompt_onset, prompt_end, choice_onset, choice_end, response, stim_df["corrAnswer"][i], buttonPressTime, RT, acc, 
    jitter1_onset, jitter1_end, feedback_onset, feedback_end, jitter2_onset, jitter2_end, trial_end, cumulativeTrialEnd])
    
    os.chdir(fileLocation)
    fid = pd.DataFrame(run_param_list, columns = header)
    fid.to_csv(fileName, header = True)

#15-second fixation:
timer.reset()
tend = timer.getTime()
text.text = "+"
text.height = 0.25
text.draw()
win.flip()
while timer.getTime() < 15 + tend:
    pass

#End of Block:
text.text = "End of chat session %s" %expInfo["run"]
text.pos = (0,0)
text.height = 0.2
text.draw()
win.flip()

image.image = os.path.join(cwd + "/Stimuli/" + chatBuddyPic)
image.pos = (0, -0.2)
image.size = (0.5, 1.0)
image.draw()
win.flip()

while True:
    theseKeys = event.getKeys()
    if "escape" in theseKeys:
        core.quit()
    if "space" in theseKeys:
        break

#Goodbye:
win.close()
core.quit()