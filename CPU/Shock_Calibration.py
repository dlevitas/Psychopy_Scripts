00#Shock Calibration

from psychopy import locale_setup, visual, core, event, data, gui, sound, parallel
import os, platform, shlex, shutil

exp = 'beh'
#Set up parallel port:
if exp == 'beh':
    parallel.setPortAddress(address=0xD070) #address for the BioPack in BPS0125
    parallel.setData(0)
    
else:
    from jkpsycho import *
    scanner_coms = ScannerComs(port=3, timeout=0.001, baudrate=19200, keyboard=True)
    parallel.setPortAddress(address=0xD010) #address for the BioPack at MNC
    parallel.setData(0)
    
shockTimer = core.Clock()    
win = visual.Window(fullscr=True, pos=(0,0), units='norm', color='Black')
event.Mouse(visible=False)
text = visual.TextStim(win = win, text = '', height = 0.1, pos = (0,0), color="White")

def Text_on_Screen(str, time):
    text.text = str
    theseKeys = event.clearEvents(eventType = "keyboard")
    text.draw()
    win.flip()
    if time == 'beg':
        while True:
            theseKeys = event.getKeys(keyList=['escape','space'])
            if "escape" in theseKeys:
                core.quit()
            if len(theseKeys):
                break
    else:
        core.wait(2.0)

continueTest = 'True'
while continueTest == 'True':
    Text_on_Screen('Please wait for shock', 'beg')
    
    shockTimer.reset()
    while shockTimer.getTime() < 0.5:
        parallel.setData(192)
        
    parallel.setData(0)
        
    Text_on_Screen('How was that shock level?','end')
