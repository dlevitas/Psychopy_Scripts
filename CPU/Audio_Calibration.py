#Audio Calibration

from psychopy import prefs
prefs.general['audioLib'] = ['pygame']
from psychopy import locale_setup, visual, core, event, data, gui, sound
import os, platform, shlex, shutil

exp = 'beh'

cwd = os.path.dirname(__file__)
if exp == 'beh':
    pass
else:
    from jkpsycho import *
    scanner_coms = ScannerComs(port=3, timeout=0.001, baudrate=19200, keyboard=True)
    
audioTimer = core.Clock()    
win = visual.Window(fullscr=True, pos=(0,0), units='norm', color='Black')
event.Mouse(visible=False)
text = visual.TextStim(win = win, text = '', height = 0.1, pos = (0,0), color="White")
audio = sound.Sound(value=os.path.join(cwd + '/Sounds/bell.wav'))

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

while True:
    
    Text_on_Screen('Please wait for the audio', 'beg')
    
    audioTimer.reset()
    while audioTimer.getTime() < 2.0:
        audio.play()
    audio.stop()
    
    Text_on_Screen('How was that volume level?','end')
