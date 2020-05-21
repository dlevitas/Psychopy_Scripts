#Theory of Mind Behavioral Script for adults:

#Create data files, and check for duplicates/override incomplete data:
fileName = "%s_ToM_%s.csv" %(subjID, currentTime)

if not os.path.exists(Data_dir):
    os.makedirs(Data_dir)
    
#Window:
win = visual.Window(fullscr = True, pos = (0,0), units = "norm", color = "Black")

#Turn off Mouse
event.Mouse(visible = False)

#Timers:
timer = core.Clock() 
cumulativeTimer = core.Clock()

#Stim_file:
stim_df = pd.read_csv('ToM_Stim_List.csv', index_col=0)

#Data List File:
run_param_list = []
header = ['Audio_File','Choice1','Choice2','Correct Statement','Correct Response','Response','ACC','RT','Degree Difficulty']

#Stimuli:
text = visual.TextStim(win, text='',height=0.08, pos=(0,0), color="White")
inst1 = visual.TextStim(win, text='Please listen carefully to the following stories.', height=0.08, pos=(0,0.4), wrapWidth=2, color="White")
inst2 = visual.TextStim(win, text='Following each story you will see two statements.', height=0.08, pos=(0,0.3), wrapWidth=2, color="White")
inst3 = visual.TextStim(win, text='Only one of the statements is true.', height=0.08, pos=(0,0.2), color="White")
inst4 = visual.TextStim(win, text='Press the left arrow key if the statement on the LEFT is true.', height=0.08, pos=(0,-0.1), wrapWidth=2, color="White")
inst5 = visual.TextStim(win, text='Press the right arrow key if the statment on the RIGHT is true.', height=0.08, pos=(0,-0.2), wrapWidth=2, color="White")
inst6 = visual.TextStim(win, text='Press the enter key to begin', height=0.08, pos=(0,-0.4), color="White")
choice_inst = visual.TextStim(win, text='',height=0.08, pos=(0,0.2), color="White")
choice1 = visual.TextStim(win, text='',height=0.08, pos=(0,0), wrapWidth=0.6, color="White")
choice2 = visual.TextStim(win, text='',height=0.08, pos=(0,0), wrapWidth=0.6, color="White")
resp_box = visual.Rect(win, width = 0.3, height = 0.1, pos = (0,0))
end1 = visual.TextStim(win, text='Thank you for participating.', height=0.08, pos=(0,0.1), wrapWidth=2, color="White")
end2 = visual.TextStim(win, text='Please let the experimenter that this task has been completed.', height=0.08, pos=(0,-0.1), wrapWidth=2, color="White")

audio_files = stim_df['Audio_file'].unique()

#Define Functions for Experiment:
def randomize(data,index):
    choices = np.random.permutation(data.ix[index][2:4])
    return choices[0], choices[1]
    
def ACC(data, choice1, index, response):
    if choice1 == data['Correct'][index]:
        corr_resp = 'left'
        if response == corr_resp:
            acc=1
        else:
            acc=0
    else:
        corr_resp = 'right'
        if response == corr_resp:
            acc=1
        else:
            acc=0
            
    return corr_resp, acc
    
#Experiment Instructions:
inst1.draw()
inst2.draw()
inst3.draw()
inst4.draw()
inst5.draw()
inst6.draw()
win.flip()

while True:
    eventKeys = event.getKeys(keyList=['escape','return'])
    if 'escape' in eventKeys:
        core.quit()
    elif 'return' in eventKeys:
        break
    else:
        pass
        
#2 sec blank screen for participants to get ready before the experiment starts:(See if Dustin is ok with this)
timer.reset()
cumulativeTimer.reset()
win.flip()
while timer.getTime() < 0.5:
    pass       

#Begin Experiment:
for i in audio_files:
    exp_start = cumulativeTimer.getTime()
    response = []
    
    if event.getKeys(keyList = ["escape"]):
        core.quit()
    timer.reset() 
    
    #0.5 sec instruction delay time before audio onset:
    i_start = timer.getTime()
    text.text = 'Listen to the story'
    text.draw()
    win.flip()
    
    while timer.getTime() < 0.5 + i_start:
        pass
    timer.reset()
    
    #Play audio:
    os.chdir(Audio_dir)
    audio = sound.Sound(value=i)
    audio.play()
    while timer.getTime() < audio.getDuration():
        if event.getKeys(keyList = ["escape"]):
            core.quit()
        else:
            pass
    audio.stop()
    timer.reset()

    #1 sec fixation delay between end of story and the onset of the choices:
    f_start = timer.getTime()
    text.text = "+"
    text.draw()
    win.flip()
    while timer.getTime() < 1.0 + f_start:
        pass
    timer.reset()
    
    #Prepare the choice statements for each audio file:
    audio_questions = stim_df[stim_df['Audio_file'] == i].reset_index()
    for k in range(len(audio_questions)):     
        #Randomize choices, then present them on screen:
        choice1.text, choice2.text = randomize(audio_questions,k)
        choice1.pos = (-0.5, -0.3)
        choice1.setAutoDraw(True)
        
        choice2.pos = (0.5, -0.3)
        choice2.setAutoDraw(True)
        
        choice_inst.text = 'Which statement is true?'
        choice_inst.setAutoDraw(True)
        
        win.flip()
        
        #Get response and feedback:
        RT = "N/A"
        response = event.clearEvents(eventType = "keyboard")
        timer.reset()
        while True:
            if event.getKeys(keyList = ["escape"]):
                core.quit()
                
            response = event.getKeys(keyList = ["left","right"])
            if len(response):
                RT = timer.getTime()
                corr_resp, acc = ACC(audio_questions, choice1.text, k, response[0])
                
                run_param_list.append([i, choice1.text, choice2.text, audio_questions['Correct'][k], corr_resp, response[0], acc, RT, audio_questions['Degree Difficulty'][k]])
                fid = pd.DataFrame(run_param_list, columns = header)
                os.chdir(Data_dir)
                fid.to_csv(fileName, header = True)
                
                if response[0] == "left":
                    resp_box.pos = (-0.5, -0.3)
                    resp_box.width = (choice1.boundingBox[0]/width)*scale
                    resp_box.height = (choice1.boundingBox[1]/height)*scale
                elif response[0] == "right":
                    resp_box.pos = (0.5, -0.3)
                    resp_box.width = (choice2.boundingBox[0]/width)*scale
                    resp_box.height = (choice2.boundingBox[1]/height)*scale

                else:
                    pass
                    
                resp_box.draw()
                r_time = timer.getTime()
                win.flip()
                #Give 0.5 sec for participants to see what they chose, before moving on:
                while timer.getTime() < 0.5 + r_time:
                    pass
                    
                break
        choice1.setAutoDraw(False)
        choice2.setAutoDraw(False)
        choice_inst.setAutoDraw(False)
        
    exp_end = cumulativeTimer.getTime()
    
end1.draw()
end2.draw()
win.flip()
core.wait(2.0)

print "ToM experiment lasted %s min" %round((exp_end - exp_start)/60,2)