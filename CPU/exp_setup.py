#Controllability Study
#SCR codes onset:offset
#    practice = 1:11
#    run1 = 2:12
#    run2 = 3:13
#    run3 = 4:14
#    run4 = 5:15

from __future__ import division
from psychopy import prefs
prefs.general['audioLib'] = ['pygame']
from psychopy import locale_setup, visual, core, event, data, gui, sound, parallel
import pandas as pd
import numpy as np
import os, platform, shlex, shutil
import subprocess as subp

#Experiment Parameters (Change them if needed):
exp = 'beh'   # beh or scan
num_runs, num_prac_blocks, num_blocks, stress_time, threat_cue_time = [4,4,6,5,3] #Stress_time must not exceed 5 seconds
shock_pat = np.cumsum([1, 0.2, 1, 0.2, 1, 0.2, 1, 0.4]) #Length of shocks and breaks. Shocks last 1-sec, followed by 200-ms offset
escape_presses_needed_total_list = [1, 1, 1, 2, 2, 3, 3, 3, 4, 5, 5, 5, 5, 6, 6, 7, 7, 7, 8, 8, 9, 10] 

#######################################DO NOT CHANGE BELOW HERE ###################################################

#Set up parallel port:
if exp == 'beh':
    parallel.setPortAddress(address=0xD070) #address for the BioPack in BPS0125
    parallel.setData(0)
    
    begin_delay = 2 #Delay period at beginning of each run
    end_delay = 0 #For behavioral, delay at end of run not neccessary, so set to zero
else:
    from jkpsycho import *
    scanner_coms = ScannerComs(port=3, timeout=0.001, baudrate=19200, keyboard=True)
    parallel.setPortAddress(address=0xD010) #address for the BioPack at MNC
    parallel.setData(0)
    
    begin_delay = 6 #Delay period at beginning of each run
    end_delay = 15 #Delay period at end of each run (to ensure brain activity returns to baseline)

#Set up path directories:
cwd = os.path.dirname(__file__)
Audio_dir = os.path.join(cwd + "/Sounds")

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

#Make sure file pathways are set up properly:
if not os.path.exists(cwd + '/Data'):
    os.makedirs(cwd + '/Data/')
if not os.path.exists(cwd + '/Data/Control') or not os.path.exists(cwd + '/Data/Uncontrol') or not os.path.exists(cwd + '/Data/None'):
    os.makedirs(cwd + '/Data/Control')
    os.makedirs(cwd + '/Data/Uncontrol')
    os.makedirs(cwd + '/Data/None')

#Create GUI and ensure correct information is entered:
expName = "Controllability Behavioral Study"
expInfo = {"participant ID":"", "Run": "", "Group":"", "R": "", "Shock Lvl" : ""}
dlg = gui.DlgFromDict(dictionary = expInfo, title = expName, order=['participant ID','Run','Group','Shock Lvl','R'])
if dlg.OK == False:
    core.quit()
if expInfo["participant ID"] == "":
    raise ValueError ("Please enter a Participant ID") 
if expInfo['Shock Lvl'] == "":
    raise ValueError('Please enter shock level.')  
if expInfo['Group'] not in ['CS','US','NS']:
    raise ValueError ('Please select a proper group code: [CS, US, NS]')
if expInfo['Group'] == 'US' and len(os.listdir(os.path.join(cwd + '/Data/Control'))) == 0:
    raise ValueError ('Please select a proper group code')
if expInfo['R'] == '' and expInfo['Group'] == 'US':
    raise ValueError('Please select number')
if expInfo['Group'] == 'US' and int(expInfo['R'])/10 >= 1:
    yoked_participant = 'CPU_0' + expInfo['R']
else:
    yoked_participant = 'CPU_00' + expInfo['R']
if expInfo['Group'] == 'CS':
    yoked_participant = 'NA'
if not yoked_participant in os.listdir(str(os.path.join(cwd + '/Data/Control'))) and expInfo['Group'] == 'US':
    raise ValueError ('Please use proper number for this experiment')
   
#Set up Condition Parameters:
if os.path.isfile(cwd + '/US_exp_file.csv'): #Don't need this file if we're running a Controllabile condition participant
    os.remove('US_exp_file.csv')
    
fileName = "%s_%s.csv" %(expInfo["participant ID"], expInfo['Run']) #Output file

if expInfo['Group'] == 'CS':
    #List of whether threat blocks will be predictable or unpredictable
    P_U = ['P','U'] + ['P']*int(num_blocks/2) + ['U']*int(num_blocks/2) + ['P']*int(num_blocks/2) + ['U']*int(num_blocks/2) #First letter is practice, the rest refer to the main runs
    
    if not os.path.exists(cwd + '/Data/Control/' + expInfo['participant ID']):
        os.makedirs(cwd + '/Data/Control/' + expInfo['participant ID'])

    Data_dir = os.path.join(cwd + '/Data/Control/' + expInfo['participant ID'])
    stim_df = pd.read_csv('exp_file.csv')
    audio_time_limit = pd.Series(['[5,5,5]']*(num_runs*num_blocks+num_prac_blocks))
    
    #Counter balance the predictable and unpredictable threat periods
    if len(os.listdir(os.path.join(cwd + '/Data/Control'))) % 2:
        k=1
        while k < int(num_blocks/2) + 1:
            P_U += [P_U.pop(2)]
            k += 1

elif expInfo['Group'] == 'US':
    if not os.path.exists(cwd + '/Data/Uncontrol/' + expInfo['participant ID']):
        os.makedirs(cwd + '/Data/Uncontrol/' + expInfo['participant ID'])
    
    #if os.path.isfile('Escape_Presses_Needed_Tracker.txt'):
        #os.remove('Escape_Presses_Needed_Tracker.txt')
    if os.path.isfile(os.path.join(cwd +'/Data/Control/US_exp_file.csv')): #Sometimes thie US_exp_file gets left in this folder if script fails early. Making sure it won't be an issue
        os.remove(os.path.join(cwd +'/Data/Control/US_exp_file.csv'))
        
    #yoked_participant = expInfo['R']
        
    ###if len(os.listdir(os.path.join(cwd + '/Data/Control/' + yoked_participant))) != num_runs+1: #Make sure the CS partner at least has the practice and 4 main runs, otherwise the uncontrollable participant can't be yoked to partner 
    ###    raise ValueError('The CS participant is missing run files')
    
    if len(os.listdir(os.path.join(cwd + '/Data/Control/' + yoked_participant))) < num_runs:
        raise ValueError('The CS participant does not have all 4 main runs')
    else:
        Data_dir = os.path.join(cwd + '/Data/Uncontrol/' + expInfo['participant ID'])
        os.chdir(os.path.join(cwd + '/Data/Control/' + yoked_participant))
        
        #Creating the yoked partner file for US participants
        fout=open("US_exp_file.csv","a") #create a blank .csv file
        for line in open(yoked_participant + '_0' +'.csv'): #open practice run from yoked CS partner
            fout.write(line) #copy practice data from partner to the US_exp_file
        for num in range(1, num_runs+1):
            f = open(yoked_participant + "_" + str(num) + ".csv")
            f.next() # skip the header
            for line in f:
                 fout.write(line) #copy main runs data from yoked CS partner to US_exp_file
        fout.close()
            
        shutil.move('US_exp_file.csv', cwd + '/US_exp_file.csv') #move US_exp_file to main directory
        os.chdir(cwd)
        
        stim_df = pd.read_csv('US_exp_file.csv')
        P_U = stim_df['Threat_Predictability'].dropna().tolist() #List of whether threat blocks will be predictable or unpredictable
        
        #Yokes CS participant escape times to US participant
        #audio_time_limit_prac = stim_df['Escape_Times'][0:num_prac_blocks]
        #audio_time_limit_main = stim_df['Escape_Times'][num_prac_blocks:]
        #audio_time_limit = pd.concat([audio_time_limit_prac, audio_time_limit_main], axis=0, ignore_index=True)
        audio_time_limit = stim_df['Escape_Times']

        #Individual button presses from yoked participant
        ind_button_presses = stim_df['Individual_Button_Presses']
else:
    if not os.path.exists(cwd + '/Data/None/' + expInfo['participant ID']):
        os.makedirs(cwd + '/Data/None/' + expInfo['participant ID'])
        
    Data_dir = os.path.join(cwd + '/Data/None/' + expInfo['participant ID'])
    stim_df = pd.read_csv('exp_file.csv')
    audio_time_limit = pd.Series(['[5,5,5]']*(num_runs*num_blocks+num_prac_blocks))
 
#Make sure you don't enter a run number out of order: 
if expInfo['Run'] not in ['0','1','2','3','4']:
    raise ValueError("Please enter a valid run number")
if expInfo["Run"] in ["1","2","3","4"] and not os.path.isfile(os.path.join(Data_dir,"%s_0.csv" %(expInfo["participant ID"]))):
    raise ValueError("Make sure the practice was run")
if expInfo["Run"] in ["2","3","4"] and not os.path.isfile(os.path.join(Data_dir,"%s_1.csv" %(expInfo["participant ID"]))):
    raise ValueError("Make sure the first session was run")
if expInfo["Run"] in ["3","4"] and not os.path.isfile(os.path.join(Data_dir,"%s_2.csv" %(expInfo["participant ID"]))):
    raise ValueError("Make sure the first & second sessions were run")
if expInfo["Run"] == "4" and not os.path.isfile(os.path.join(Data_dir,"%s_3.csv" %(expInfo["participant ID"]))):
    raise ValueError("Make sure that all other sessions were run")

if os.path.isfile(os.path.join(Data_dir, fileName)):
    raise ValueError('A log file already exists for this participant')
    
#Determine which part of the experimental file to run, based on the run:
if expInfo["Run"] == '0': #Practice run
    seed_value = 0
    block_start, block_end = [0, num_prac_blocks]
    P_U_counter = 0
if expInfo["Run"] == '1': #Main run 1
    seed_value = 1
    block_start, block_end = [num_prac_blocks, num_blocks+num_prac_blocks]
    P_U_counter = 2
elif expInfo["Run"] == '2': #Main run 2
    seed_value = 2
    block_start, block_end = [num_blocks+num_prac_blocks, (num_blocks*2)+num_prac_blocks]
    P_U_counter = int(2+(num_blocks/2))
elif expInfo["Run"] == '3': #Main run 3
    seed_value = 3
    block_start, block_end = [(num_blocks*2)+num_prac_blocks, (num_blocks*3)+num_prac_blocks]
    P_U_counter = int(2+(num_blocks/2)*2)
elif expInfo["Run"] == '4': #Main run 4
    seed_value = 4
    block_start, block_end = [(num_blocks*3)+num_prac_blocks, (num_blocks*4)+num_prac_blocks]
    P_U_counter = int(2+(num_blocks/2)*3)
    
np.random.seed(seed_value)
            
#Window:
win = visual.Window(size=(width, height), fullscr = True, pos = (0,0), units = "norm", color = "Black")

#Turn off Mouse
event.Mouse(visible = False)

#Timers:
timer = core.Clock() 
shock_timer = core.Clock()
ind_timer = core.Clock()
cumulativeTimer = core.Clock()

#Output Data:
run_param_list = []
header = ['subject_ID', 'Exp_Type', 'Run', 'Threat_Predictability', 'Cumulative_Start_Time','Block', 'Block_Onset','Block_End', 'Safe_Block_Time', 'Threat_Block_Time', 'Num_Stressor_Presentations', 'Audio_Files', 'Threat_Cue_Onset_Times', 'Stressor_Onset_Times', 'Stressor_End_Times', 'Individual_Button_Presses', 'Escape_Times','Escape_Presses_Needed_List', 'Shock_Level','Cumulative_End_Time', 'Anxiety_Rating','Perceived_Control_Rating', 'Yoked_Participant']

#Functions:
def save_data(block):
    if stim_df['Block'][i] == 'safe':
        run_param_list.append([expInfo["participant ID"], exp, expInfo['Run'], 'NA', cum_start, stim_df['Block'][i], safe_block_onset, safe_block_end, (safe_block_end - safe_block_onset), 'NA', 'NA', 'NA', 'NA','NA','NA', 'NA', 'NA', 'NA', 'NA', cum_end, 'NA','NA', yoked_participant])
        fid = pd.DataFrame(run_param_list, columns = header)
        fid.to_csv(os.path.join(Data_dir,r'%s_%s.csv' %(expInfo["participant ID"],expInfo["Run"])), header=True, index=False)
    else:
        run_param_list.append([expInfo["participant ID"], exp, expInfo['Run'], P_U[P_U_counter], cum_start, stim_df['Block'][i], threat_block_onset, threat_block_end, 'NA', (threat_block_end - threat_block_onset), stim_df['Num_Stressor_Presentations'][i], audio_files_list, threat_cue_list, stressor_onset_list, stressor_end_list, button_press_RTs_all_list, escape_times_list, escape_presses_needed_block_list, expInfo['Shock Lvl'], cum_end, anxiety_rating, perceived_control_rating, yoked_participant])
        fid = pd.DataFrame(run_param_list, columns = header)
        fid.to_csv(os.path.join(Data_dir,r'%s_%s.csv' %(expInfo["participant ID"],expInfo["Run"])), header=True, index=False)

def escape_option():
    if 'escape' in event.getKeys(keyList=['escape']):
        parallel.setData(int(expInfo['Run']) + 11)
        core.wait(0.5)
        parallel.setData(0)
        core.quit()
        
def Instructions(str):
    text.text = str
    text.height = 0.1
    text.pos = (0,0)
    theseKeys = event.clearEvents(eventType = 'keyboard')
    theseKeys = []
    text.draw()
    win.flip()
    while True:
        escape_option()
        theseKeys = event.getKeys(keyList=['space'])
        if exp == 'beh':
            if len(theseKeys):
                break
        else:
            if '6' in scanner_coms.messages():
                break
        
def Rating(type):
    escape_option()
    event.clearEvents(eventType = "keyboard")
    timer.reset()
    
    if type == 'anxiety':
        text.text = 'Please rate how ANXIOUS you felt during the previous block'
        label = ['1','2','3','4','5','6','7','8','9']
        scales = '1=Low Anxiety,   9=High Anxiety'
    else:
        text.text = 'Please rate how much CONTROL you felt you had during the previous block'
        label = ['1','2','3','4','5','6','7','8','9']
        scales = '1=No Control,   9=Complete Control'
    
    scale = visual.RatingScale(win, low=1, high=9, pos=(0,0), size=1.5, marker=visual.TextStim(win, text="", units="norm"), noMouse=True, tickMarks = label,
            textSize = 0.7, respKeys = ['num_1','num_2','num_3','num_4','num_5','num_6','num_7','num_8','num_9'], minTime=0.0, scale = scales,
            showAccept = False,labels = label, textColor="White", stretch=1.5, acceptKeys = ['num_1','num_2','num_3','num_4','num_5','num_6','num_7','num_8','num_9'])
    
    text.pos = (0.0, 0.7)
    text.height = 0.07
    text.setAutoDraw(True)
    
    rate_start = timer.getTime()
    while timer.getTime() < 20:
        escape_option()
            
        scale.draw()
        win.flip() 
        
        if scale.getRating():
            break
    
    text.setAutoDraw(False)
    
    output = scale.getHistory()
    if len(output) == 1 or output[1][0] == 0:
        rating = 'NA'
    else:
        rating = scale.getHistory()[1][0]
                
    return rating

#Visual & Auditory Stimuli:
text = visual.TextStim(win = win, text = '', height = 0.1, pos = (0,0), color="White")
threat_cue = visual.ImageStim(win = win, pos = (0,0), size = (0.3,0.3), image = os.path.join(cwd + "/lightbulb.png"))
safe_square = visual.Rect(win, width=1.5, height=1.5, pos = (0,0), fillColor="Blue", lineColor="Blue")
threat_square = visual.Rect(win, width=1.5, height=1.5, pos = (0,0), fillColor="Red", lineColor="Red")
predictable_symbol = visual.ImageStim(win = win, pos = (-0.7,0.7), size = (0.08,0.08), image = os.path.join(cwd + "/lightbulb.png"))
feedback_shape = visual.Rect(win, pos=(0,0), width=threat_square.width/max(escape_presses_needed_total_list), height=threat_square.width/max(escape_presses_needed_total_list), fillColor='White', lineColor='White')
sounds = np.random.permutation([x for x in os.listdir(os.path.join(cwd + '/Sounds')) if x != 'bell.wav']) #bell.wav sound file will be used for calibration, but not the task
aud_list = [sound.Sound(value=os.path.join(Audio_dir, s)) for s in sounds]
sound_counter, US_feedback_shape_counter = [0,0]
US_feedback_shape_sizes = np.random.permutation([0.15, 0.3, 0.45, 0.6, 0.75, 0.9, 1.05, 1.2, 1.35, 1.5])
ind_counter1, ind_counter2 = [0,0]

#Instructions:
if expInfo['Run'] == '0': 
    Instructions('We will begin with two practice sections.\n\nTo clarify, a blue square represents a safe block and a red square represents a threat block. In this practice section, a cue will appear in the center of each red square 3 seconds before the sound and shocks.\n\nPress the spacebar to begin')
else:
    Instructions('Remember, a blue square represents a safe block and a red square represents a threat block.\n\nPress the spacebar to begin')

#Onset SCR codes:
if expInfo['Run'] in ['0','1','2','3','4']:
    parallel.setData(int(expInfo['Run'])+1)
    core.wait(0.5)
    parallel.setData(0)
    
#Blank screen to let participants get ready:
cumulativeTimer.reset()
tstart = timer.getTime()
text.text = '+'
text.draw()
win.flip()
while timer.getTime() < begin_delay + tstart:
    pass

#Begin Experiment:
for i in xrange(block_start, block_end):
    cum_start = cumulativeTimer.getTime()
    escape_option()
        
    if i == 2:
        Instructions('In this next practice section, there will NOT be a cue that appears shortly before the sound and shocks.\n\nPress the spacebar to begin')
        timer.reset()
        tstart = timer.getTime()
        text.text = '+'
        text.draw()
        win.flip()
        while timer.getTime() < begin_delay + tstart:
            pass
    
    if stim_df['Block'][i] == 'safe':
        timer.reset()
        safe_block_onset = timer.getTime()
        safe_square.draw()
        win.flip()
        
        while timer.getTime() < stim_df['Safe_Block_Time'][i]:
            escape_option()
            
        safe_block_end = timer.getTime()
            
        cum_end = cumulativeTimer.getTime()
        save_data(i)
        timer.reset()
        
    else:
        if i == 1:
            escape_presses_needed_counter = 0
        elif i in [4,11,17,23]: #index of the first threat period in each main run
            f = open('Escape_Presses_Needed_Tracker.txt', 'r')
            escape_presses_needed_counter = int(f.read())
            if i == 4 and escape_presses_needed_counter in [0,1,2]: #In case people don't complete all three practice escapes, change the counter to 4 for the beginning of 1st run
                escape_presses_needed_counter = 3
        else:
            escape_presses_needed_counter = escape_presses_needed_counter
            
        stress_counter, anxiety_rating = [0, 'NA']
        button_press_RTs, button_press_RTs_all_list, escape_times_list, escape_presses_needed_block_list, stressor_onset_list, stressor_end_list, audio_files_list, threat_cue_list = [[], [], [], [], [], [], [], []]
        
        timer.reset()
        threat_block_onset = timer.getTime()
        threat_square.setAutoDraw(True)
        if expInfo['Run'] == '0' and i == 1:
            predictable_symbol.setAutoDraw(True)
        
        if expInfo['Run'] in ['1','3'] and P_U[2] == 'P':
            predictable_symbol.setAutoDraw(True)
        elif expInfo['Run'] in ['2','4'] and P_U[2] == 'U':
            predictable_symbol.setAutoDraw(True)
        else:
            pass
        win.flip()

        while timer.getTime() < stim_df['Threat_Block_Time'][i]:
            escape_option()
            
            if sound_counter == len(aud_list):
                sounds, aud_list = [np.random.permutation(sounds), np.random.permutation(aud_list)]
                sound_counter = 0
            
            if P_U[P_U_counter] == 'P':
                while stress_counter < len(eval(stim_df['Stressor_Onset_Times'][i])):
                    escape_option()
                    if timer.getTime() >= eval(stim_df['Stressor_Onset_Times'][i])[stress_counter] - threat_cue_time:
                        threat_cue_list.append(timer.getTime())
                        threat_cue.setAutoDraw(True)
                        win.flip()
                        while timer.getTime() <= eval(stim_df['Stressor_Onset_Times'][i])[stress_counter]:
                            escape_option()
                        threat_cue.setAutoDraw(False)
                        win.flip()
                        break
            else:
                pass
            
            if stress_counter < len(eval(stim_df['Stressor_Onset_Times'][i])) and sound_counter < len(aud_list) and timer.getTime() >= eval(stim_df['Stressor_Onset_Times'][i])[stress_counter]:
                stressor_onset_list.append(timer.getTime())
                audio = aud_list[sound_counter]
                audio_files_list.append(sounds[sound_counter])
                event.clearEvents(eventType = "keyboard")
                feedback_shape.setAutoDraw(True)
                #feedback_shape.draw()
                if expInfo['Group'] == 'CS':
                    feedback_shape.width = threat_square.width/max(escape_presses_needed_total_list)
                    feedback_shape.height = threat_square.height/max(escape_presses_needed_total_list)
                else:
                    feedback_shape.width = US_feedback_shape_sizes[US_feedback_shape_counter]
                    feedback_shape.height = US_feedback_shape_sizes[US_feedback_shape_counter]
                win.flip()
                audio.play()
                
                parallel.setData(192)
                
                j=0
                shock_timer.reset()
                #ind_timer.reset()
                while timer.getTime() <= eval(stim_df['Stressor_Onset_Times'][i])[stress_counter] + eval(audio_time_limit[i])[stress_counter]:
                    escape_option()
                    
                    if shock_timer.getTime() >= shock_pat[j]:
                        if j % 2:
                            parallel.setData(192)
                        else:
                            parallel.setData(0)
                        j += 1
                                       
                    if expInfo['Group'] == 'CS':
                        if 'return' in event.getKeys(keyList=['return']):
                            button_press_RTs.append(timer.getTime() - eval(stim_df['Stressor_Onset_Times'][i])[stress_counter])
                            feedback_shape.width += threat_square.width/max(escape_presses_needed_total_list)
                            feedback_shape.height += threat_square.width/max(escape_presses_needed_total_list)
                            win.flip()

                            if len(button_press_RTs) == escape_presses_needed_total_list[escape_presses_needed_counter]:
                                stressor_end_list.append(timer.getTime())
                                escape_times_list.append(timer.getTime() - eval(stim_df['Stressor_Onset_Times'][i])[stress_counter])
                                escape_presses_needed_block_list.append(escape_presses_needed_total_list[escape_presses_needed_counter])
                                escape_presses_needed_counter += 1
                                #US_feedback_shape_counter += 1
                                #feedback_shape.setAutoDraw(False)
                                #win.flip()
                                break 
                    else:
                        if 'return' in event.getKeys(keyList=['return']):
                            button_press_RTs.append(timer.getTime() - eval(stim_df['Stressor_Onset_Times'][i])[stress_counter])
                        
                        if timer.getTime() >= eval(stim_df['Stressor_Onset_Times'][i])[stress_counter] + eval(ind_button_presses[i])[ind_counter1][ind_counter2]:
                            US_feedback_shape_counter += 1
                            if US_feedback_shape_counter == len(US_feedback_shape_sizes):
                                np.random.permutation(US_feedback_shape_sizes)
                                US_feedback_shape_counter = 0
                            
                            feedback_shape.width = US_feedback_shape_sizes[US_feedback_shape_counter]
                            feedback_shape.height = US_feedback_shape_sizes[US_feedback_shape_counter]
                            win.flip()
                            ind_counter2 += 1
                                
                        if ind_counter2 == len(eval(ind_button_presses[i])[ind_counter1]):
                            stressor_end_list.append(timer.getTime())
                            escape_times_list.append(stressor_end_list)
                            ind_counter1 += 1
                            ind_counter2 = 0
                            break
                
                parallel.setData(0)
                audio.stop()
                feedback_shape.setAutoDraw(False)
                win.flip()
               
                button_press_RTs_all_list.append(button_press_RTs)
                
                if expInfo['Group'] == 'US':
                    escape_presses_needed_block_list = 'NA'
                    
                if len(button_press_RTs) == 0 and expInfo['Group'] == 'CS':
                    escape_times_list.append(stress_time)
                    stressor_end_list.append(timer.getTime())
                    
                if len(button_press_RTs) == 0 and expInfo['Group'] == 'US':
                    escape_times_list = stressor_end_list
                
                button_press_RTs = [] #clear list for when there are multiple stressors in a single threat period
                stress_counter += 1
                sound_counter += 1
                
        threat_square.setAutoDraw(False)
        threat_block_end = timer.getTime()
        
        ind_counter1 = 0
        
        if expInfo['Run'] == '0' and i == 1:
            predictable_symbol.setAutoDraw(False)
        
        if expInfo['Run'] in ['1','3'] and P_U[2] == 'P':
            predictable_symbol.setAutoDraw(False)
        elif expInfo['Run'] in ['2','4'] and P_U[2] == 'U':
            predictable_symbol.setAutoDraw(False)
        else:
            pass
        
        if exp == 'beh':
            anxiety_rating = Rating('anxiety')
            perceived_control_rating = Rating('control')
            
        if not len(threat_cue_list):
            threat_cue_list = 'NA'
            
        cum_end = cumulativeTimer.getTime()
            
        save_data(i)
        
        P_U_counter += 1

if expInfo['Group'] == 'CS':
    np.savetxt('Escape_Presses_Needed_Tracker.txt', np.array([escape_presses_needed_counter]), fmt='%s')

#Blank screen at end:
tend = timer.getTime()
text.text = ''
text.draw()
win.flip()
while timer.getTime() < end_delay + tend:
    pass
    
#Offset SCR codes:
if expInfo['Run'] in ['0','1','2','3','4']:
    parallel.setData(int(expInfo['Run']) + 11)
    core.wait(0.5)
    parallel.setData(0)
 
#End of experiment:
if expInfo['Run'] == '0':
    text.text = 'Finished practice run'
else:
    text.text = 'Finished run %s' %expInfo['Run']
text.height = 0.1
text.pos=(0,0)
text.draw()
win.flip()
core.wait(2.0)

#Close Psychopy:
win.close()
core.quit()
