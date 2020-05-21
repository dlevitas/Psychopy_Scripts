#STOMP Behavioral Script for adults:

#Create data files, and check for duplicates/override incomplete data:
fileName = "%s_STOMP_%s.csv" %(subjID, currentTime)

if not os.path.exists(Data_dir):
    os.makedirs(Data_dir)

 

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
    eventKeys = event.getKeys(keyList=['escape','return'])
    if 'escape' in eventKeys:
        core.quit()
    elif 'return' in eventKeys:
        break
    else:
        pass

#Begin Experiment:
exp_start = cumulativeTimer.getTime()
for i in movie_list:
    #2 sec blank screen for participants to get ready before the experiment starts:(See if Dustin is ok with this)
    timer.reset()
    win.flip()
    while timer.getTime() < 2.0:
        pass  
    
    if event.getKeys(keyList = ["escape"]):
        core.quit()
        
    #Play Movie
    movie.loadMovie(os.path.join(cwd +'/Stimuli/' + i))
    movie.setAutoDraw(True) 
    while movie.status != visual.FINISHED:
    #while timer.getTime() < 3.0:
        if 'escape' in event.getKeys(keyList=['escape']):
            core.quit()
        movie.play()
        win.flip()
    movie.setAutoDraw(False)
        
    text.text = 'Have you seen this movie before? (yes/no). When you are finished, press the enter key.'
    text.pos = (0,0.8)
    text.setAutoDraw(True)
    win.flip()
    
    current = ''
    answer = ''
    caps = 'False'
    while True:
        response = event.getKeys()
        if len(response):
            keys = response[0]
                
            if keys in chars:
                current = keys

            elif keys == 'space':
                current = ' '

            elif keys == 'backspace' and len(answer) > 0:
                answer = answer[:-1]
                
            elif keys == 'comma':
                current = ','
                
            elif keys =='period':
                current = '.'
                
            elif keys =='apostrophe':
                current =  "'"
                
            elif keys == 'lshift' or keys == 'rshift':
                caps = 'True'
                continue

            elif keys == 'return':
                break
             
            elif keys == 'escape':
                run_param_list.append([expInfo['Participant ID'], i, fr0.text, fr1.text])
                fid = pd.DataFrame(run_param_list, columns = header)
                os.chdir(Data_dir)
                fid.to_csv(fileName, header = True)
                core.quit()
                
            else:
                pass
                
            if caps == 'True':
                if keys == 'backspace':
                    answer = answer
                
                else:
                    answer += current.upper()
            else:
                if keys == 'backspace':
                    answer = answer

                else:
                    answer += current.lower()
                
            fr0.text = answer
            fr0.draw()
            win.flip()
            caps = 'False'  
            
    fr0.setAutoDraw(False)
    text.setAutoDraw(False)

    
    text.text = 'Please describe this scene. Your response should be 7-10 lines. When you are finished, press the enter key.'
    text.pos = (0,0.8)
    text.setAutoDraw(True)
    win.flip()
    
    
    current = ''
    answer = ''
    caps = 'False'
    while True:
        response = event.getKeys()
        if len(response):
            key = response[0]
                
            if key in chars:
                current = key

            elif key == 'space':
                current = ' '

            elif key == 'backspace' and len(answer) > 0:
                answer = answer[:-1]
                
            elif key == 'comma':
                current = ','
                
            elif key =='period':
                current = '.'
                
            elif key =='apostrophe':
                current =  "'"
                
            elif key == 'lshift' or key == 'rshift':
                caps = 'True'
                continue

            elif key == 'return':
                break
             
            elif key == 'escape':
                run_param_list.append([expInfo['Participant ID'], i, fr0.text, fr1.text])
                fid = pd.DataFrame(run_param_list, columns = header)
                os.chdir(Data_dir)
                fid.to_csv(fileName, header = True)
                core.quit()
                
            else:
                pass
                
            if caps == 'True':
                if key == 'backspace':
                    answer = answer
                else:
                    answer += current.upper()
            else:
                if key == 'backspace':
                    answer = answer
                else:
                    answer += current.lower()
                
            fr1.text = answer
            fr1.draw()
            win.flip()
            caps = 'False'  
            
    fr1.setAutoDraw(False)
    text.setAutoDraw(False)
        
    run_param_list.append([expInfo['Participant ID'], i, fr0.text, fr1.text])
    fid = pd.DataFrame(run_param_list, columns = header)
    os.chdir(Data_dir)
    fid.to_csv(fileName, header = True)
            
exp_end = cumulativeTimer.getTime()
os.chdir(cwd)
print "STOMP experiment lasted %s seconds, or %s min" %((exp_end - exp_start),round(((exp_end - exp_start)/60),2))