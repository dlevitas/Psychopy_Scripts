from _comp import *
from psychopy import event


'''
def checkQuit():
    if not sys.modules['__main__'].endExpNow:
        sys.modules['__main__'].endExpNow = 
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
'''

class NegativeKeyList(object):
    def __init__(self,*exclude):
        self._exclude=exclude
    def __contains__(self,what):
        return (what not in self._exclude)
        
def xor(a,b):
    return bool(a) != bool(b)

#fixme: will this ever fail??
try:
    import pyglet
except:
    pass


# centralized object for managing multiple hooks to the
# pyglet text methods that PsychoPy uses.  While it is somewhat rare
# that there would be a real need for many callbacks, it is safer to
# be prepared.  And centralized version is easier to maintain than
# a linked-list style approach.
class PygletTextHooks(object):
    def __init__(self,win):
        self.win=win
        self._text=[]
        self._motion=[]
        self.register_text(win.winHandle.on_text)
        if hasattr(win.winHandle,'on_text_motion'):
            self.register_motion(win.winHandle.on_text_motion)
        
        win.winHandle.on_text_motion=self.on_motion
        win.winHandle.on_text=self.on_text
        win._jkpsycho_hooked = self
        
    def on_motion(self,motion):
        for fn in self._motion:
            fn(motion)
    def on_text(self,text,emulated=False):
        for fn in self._text:
            fn(text,emulated)
    
    def register_motion(self,fn):
        self._motion.append(fn)
        #print(self)
    def unregister_motion(self,fn):
        self._motion.remove(fn)
        #print(self)
    def register_text(self,fn):
        self._text.append(fn)
        #print(self)
    def unregister_text(self,fn):
        self._text.remove(fn)
        #print(self)
    
    def __str__(self):
        return 'PygletHooks: {} for text, {} for motion'.format(len(self._text),len(self._motion))


def _hooked():
    main = sys.modules['__main__']
    win=main.win #how brittle is this approach?, looking it up via __main__?
    
    ret=getattr(win,'_jkpsycho_hooked',None)
    if not ret:
        ret = PygletTextHooks(win)
    return ret

def hook_motion(fn):
    _hooked().register_motion(fn)
def unhook_motion(fn):
    _hooked().unregister_motion(fn)
def hook_text(fn):
    _hooked().register_text(fn)
def unhook_text(fn):
    _hooked().unregister_text(fn)

# something to provide access to raw text as entered
#opt: probably just my test code or machine... but it can get laggy
class RawText(object):
    def __init__(self,text='', chain=True, start=True):
        self.cursor=0
        self.text=text
        self._chain=chain        
        self._move=False        
        self._active=False
        self.changed=False
        
        if start:
            self.start()
    '''
    def start(self):
        if self._active:
            return
        self._active=True
        try:
            main = sys.modules['__main__']
            win=main.win #how brittle is this approach?
        except Exception as e:
            print(e)
            print('will not have access to the raw text, is this an error??') #fixme: well, is it an error??
            return
        self._win = win
        self._prev_text = win.winHandle.on_text
        # psychopy doesn't currently use this hook, so need to take care
        self._prev_motion = getattr(win.winHandle,'on_text_motion',None)
        win.winHandle.on_text=self._text
        win.winHandle.on_text_motion=self._motion
    def stop(self):
        if not self._active:
            return
        self._active=False
        
        self._win.winHandle.on_text = self._prev_text
        if self._prev_motion is not None:
            self._win.winHandle.on_text_motion = self._prev_motion
        else:
            delattr(self._win.winHandle,'on_text_motion')
    '''
    def start(self):
        if self._active:
            return
        self._active=True
        hook_motion(self._motion)
        hook_text(self._text)
    def stop(self):
        if not self._active:
            return
        self._active=False
        unhook_motion(self._motion)
        unhook_text(self._text)
    
    def clear(self):
        self.text=''
        self.cursor=0
        self.changed=True
    
    def close(self):
        self.stop()
    def __enter__(self):
        self.start()
        return self
    def __exit__(self,e_ty,e_val,tb):
        self.stop()
    
    @perr
    def _text(self,text,emulated=False):
        #if '\r' in text or '\n' in text:
        #    text = os.linesep
        if '\r' in text: #what???  maybe psychopy only accepts \n for some reason?
            txt='\n'
        else:
            txt=text
        
        self.text = self.text[:self.cursor]+txt+self.text[self.cursor:]
        self.cursor+=len(txt)
        self.changed=True
        
        #return self._chain_text(text,emulated)
    '''
    def _chain_text(self,text,emulated):
        if self._chain:
            return self._prev_text(text,emulated=emulated)
    def _chain_motion(self,motion):
        if self._chain and self._prev_motion is not None:
            return self._prev_motion(motion)
    '''
    @perr
    def _motion(self,motion):
        #print(motion)
        #print('and::::',pyglet.window.key.MOTION_BACKSPACE)
        #print(motion==pyglet.window.key.MOTION_BACKSPACE)
        #print(type(motion))
        
        # would require the user of this class to provide some edit cursor,
        # else moving things about is frustrating.
        if self._move:
            if motion == pyglet.window.key.MOTION_LEFT:
                self.cursor-=1
            elif motion == pyglet.window.key.MOTION_RIGHT:
                self.cursor+=1
            #impl: many other movements to implement later, if they are requested
            # would find nearby newlines, adjust cursor based on that.  same
            # with moving to words, find nearest... space?  hmmm.... may need to do
            # line splitting and regex in this case.  yuck.
        
        # deletions (single characters, no concept of selections)
        if motion == pyglet.window.key.MOTION_DELETE:
            self.text=self.text[:self.cursor]+self.text[self.cursor+1:]
        elif motion == pyglet.window.key.MOTION_BACKSPACE:
            self.text=self.text[:self.cursor-1]+self.text[self.cursor:]
            self.cursor-=1
        
        # catch-all for invalid cursor positions
        if self.cursor<0:
            self.cursor=0
        else:
            N=len(self.text)
            if self.cursor>N:
                self.cursor=N
        
        self.changed=True
        
        #return self._chain_motion(motion)

class TextGrabber(RawText):
    def __init__(self,txt='',multiline=False):
        RawText.__init__(self,txt,start=False)
        self.multiline=multiline
        
        # timing details, to follow ComDetails concept
        self._status = NOT_STARTED
        self.tStart = None
        self.frameNStart = None
    
    # use a property to catch starts and stops
    @property
    def status(self):
        return self._status
    @status.setter
    def status(self,new_status):
        if new_status==self._status:
            return
        if new_status==STARTED:
            self.start()
        else:
            self.stop()
        self._status=new_status
    
    @perr
    def _text(self,text,emulated=False):
        if not self.multiline and '\r' in text:
            return
        RawText._text(self,text,emulated)
        
        '''
        if not self.multiline and '\r' in text:
            # just immediately pass it on to any other registered grabbers
            return self._chain_text(text,emulated)
        else:
            return RawText._text(self,text,emulated)
        '''
    def __repr__(self):
        r='TextGrabber("""{}""", multiline={})'.format(self.text,self.multiline)
        if self.status==STARTED:
            r='Active '+r
        else:
            r='Inactive '+r
        return r
    
    __str__=__repr__

@Comp("Let the user input text freely using a keyboard")
class TextResponseComponent(BaseComp):
    categories = ['Responses']
    def __init__(self, exp, parentName, name='text_response', multiline=False):
        BaseComp.__init__(self,exp,parentName,name, timed_component=True)
        
        #self.param('init_txt', init_txt, valType='str', hint="this text will already be entered for the user",label="initial text")
        self.param('multiline',multiline,hint='if True, the user can press return to start a new line',label='multiline?')
        #self.param('backspace',backspace,hint='if True, user will be able to press backspace to delete already entered text',label='backspace?')
        #self.param('eat_keys',eat_keys,hint="if False, any keys used for typing text will still be available to other components in this Routine.",label='eat keys?')
        
        self.start_code="{name} = TextGrabber(txt='', multiline={multiline}) # will automatically start when status set to STARTED, else will be stopped.  Usage here is a bit wacky due to constraints of PsychoPy code generation."
        self.stop_code="{name}.stop()"