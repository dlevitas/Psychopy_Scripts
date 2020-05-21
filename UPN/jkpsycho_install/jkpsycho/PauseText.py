from _comp import *
'''
Don't get hopes up for PsychoPy component inheritance.  even for simple things,
it takes some care...
'''

#idea: perhaps a multiComponent class would be a better approach.  use separate
# tabs in the config dialog.  


from psychopy.app.builder.components.text import TextComponent as TextComp
"""
update_filter=r'''
_text = {text}+'\n\n'
if {keyFilter}:
    _text+='press a key to continue:\n'+str(list({keyFilter}))[1:-1]
else:
    _text+='press any key to continue'
{name}.setText(_text)
'''
"""

update_filter=r'''
_text = {text}+'\n\n'
_kf={name}.keyfilter = KeyFilter({include_keys},{exclude_keys})

if _kf.include:
    _text+='press a key to continue:\n'+str(_kf.include)[1:-1]
elif _kf.exclude:
    _text+='press a key to continue, except:\n'+str(_kf.exclude)[1:-1]
else:
    _text+='press any key to continue'

{name}.setText(_text)
'''


@Comp("show some text and wait for key press to continue, just intended for debugging!")
class PauseTextComponent(CompTools,TextComp):
    def __init__(self, exp, parentName, name='pause_text', **kwargs):
        include_keys=kwargs.pop('include_keys',None)
        exclude_keys=kwargs.pop('exclude_keys',"'escape'")
        
        #keyFilter=kwargs.pop('keyFilter',None)
        TextComp.__init__(self,exp,parentName,name,**kwargs)
        self._endless()
        self.params['text'].updates='set every repeat'
        self.param('include_keys',include_keys,'code',label='Only these keys',hint="end the routine if one of these keys is pressed (ex: 'space','enter').  Quote the key names, and separate them with commas.  use None to use everything.")
        self.param('exclude_keys',exclude_keys,'code',label='Never these keys',hint="don't pay attention to any of these keys.  use None to respond to everything")
        
        #self.param('keyFilter',keyFilter,'code', label='Key Filter'
        #, hint="Only end the routine if one of these keys is pressed (ex: ['space','enter']).  use None to continue on any key.")
        
    def writeInitCode(self,buff):
        TextComp.writeInitCode(self,buff)
        with self.buff(buff):
            if self.params['text'].updates=='constant':
                self(update_filter)
    def writeRoutineStartCode(self,buff):
        TextComp.writeRoutineStartCode(self,buff)
        with self.buff(buff):
            self("event.clearEvents(eventType='keyboard')")
            if self.params['text'].updates=='set every repeat':
                self(update_filter)
    def writeFrameCode(self,buff):
        TextComp.writeFrameCode(self,buff)
        with self.buff(buff):
            self("# stop routine if {name}'s buttons are pressed")
            self('if {name}.status==STARTED:')
            if self.params['text'].updates=='set every frame':
                self(update_filter,1)    
            self('if event.getKeys(keyList={name}.keyfilter): stopRoutine()',1)