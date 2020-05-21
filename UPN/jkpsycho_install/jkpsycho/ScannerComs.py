from _comp import *
from psychopy import event

# Should perhaps
# generalize the STARTED/STOPPED things like I do for TextResponse.
# but it is hard to generalize...  may want to redo the BaseComp and Comp thing
# to more return the needed materials.  A base class for the component and
# for the details class.


def makeScannerComsAccess(scanner_coms, as_set, clear_every_frame):
    if as_set:
        Base = set
    else:
        Base = list
    class ScannerComsAccess(Base):
        def __init__(self):
            Base.__init__(self)
            
            self._clear_every_frame = clear_every_frame
            self._as_set = as_set
            self._active = False
            self._coms = scanner_coms
            
            # timing details, to follow ComDetails concept
            self._status = NOT_STARTED
            self.tStart = None
            self.frameNStart = None
        
        def _update(self):
            if not self._active:
                return
            # optionally discard previous messages
            if self._clear_every_frame:
                self._clear()
            # grab new messages
            _new_messages = self._coms.messages(clear_after=True, as_set=self._as_set)
            if self._as_set:
                self.update(_new_messages)
            else:
                self.extend(_new_messages)
                
        def _clear(self):
            if self._as_set:
                self.clear()
            else:
                self[:]=[]
        
        #NOTE: depending on how PsychoPy orders the code when building, this might
        # miss the first frame when 'active'.  But I don't see that as a real problem.
        # what sort of use do you have for this Component if you are trying to
        # activate and then read on the very same frame??
        #style: if I make the start/stop methods more generic, expose them... then
        # one would expect them to also change the status.  But that gets messy.
        def _start(self):
            if self._active:
                return
            self._active = True
            # always clear coms when starting, avoid previous junk
            self._coms.clear()
            # not sure if this makes more sense to clear or not here.  Currently,
            # I'm viewing 'starting' as a brand new use of the object.  So any
            # previous state should be discarded.
            self._clear()
        def _stop(self):
            if not self._active:
                return
            self._active = False
        
        # use a property to catch starts and stops
        @property
        def status(self):
            return self._status
        @status.setter
        def status(self,new_status):
            if new_status==self._status:
                return
            if new_status==STARTED:
                self._start()
            else:
                self._stop()
            self._status=new_status
    return ScannerComsAccess()

@Comp("communicate with scanner (trigger, buttons, etc.)")
class ScannerComsComponent(BaseComp):
    def __init__(self, exp, parentName, name='coms', as_set=True, clear_every_frame=True):
        BaseComp.__init__(self,exp,parentName,name, timed_component=True)
        
        self.param('as_set',as_set, 'bool', hint = "if True, <name> is a set.  Else, a list.", label="Store as a set?")
        self.param('clear_every_frame',clear_every_frame, 'bool', hint="If True, <name> will only give the signals that arrived since the previous frame", label="Clear every frame?")
        
        self.start_code = '{name} = makeScannerComsAccess(scanner_coms,{as_set},{clear_every_frame})'
        self.frame_code = '{name}._update()'


class ScannerComs(object):
    def __init__(self,port=3, timeout=0.001, baudrate=19200, verbose=False, keyboard=False):
        '''
        # port for scanner room seems to be 3, thought that practice room was 2.
		
        Connect to scanner coms (serial port).  Optionally use keyboard as backup (numbers
        0-9 would come through as '0'-'9' just like button box does).  Default settings
        here should work with the MNC scanner.
        
        Tests indicate that any loss of connection will result in no further messages.  So
        if the experiment machine looses connection to the button box stuff (like
        powercycle the MRA box) buttons will stop working.  I don't yet see a way around
        this, though seems like the more serious problem is loosing connection in the first
        place rather than an inability to recover from that.
        
        WARNING: While PsychoPy's mouse handling class lets you know if a certain button is CURRENTLY pressed,
        monitoring a serial port from the scanner works like PsychoPy's keyboard queue.  Care needs to be taken
        not to handle old messages by accident.  Like if the subject answers each trial with a button press and you
        fail to clear the queue at the start of each trial, extra button presses from the previous trial could be
        used to immediately answer the current trial! 
        '''
        if timeout is None:
            raise ValueError("I don't support blocking reads currently, timeout must not be None")
        if timeout<=0:
            raise ValueError("timout must be > 0")
        
        self.keyboard=keyboard
        self.verbose=verbose
        try:
            # stopbits?  bytesize?
            import serial
            self._coms = serial.Serial(port, timeout=timeout, baudrate=baudrate)
            if verbose:
                print('using serial port {}'.format(self._coms.portstr))
            self._str = 'ScannerComs(port={}, timeout={}, baudrate={})'.format(port,timeout,baudrate)
        except:
            self._coms = None
            print('could not connect to serial port.  This is OK if not hooked up to a scanner.  Else check your connections,ports,settings,etc...')
            self._str = 'Dummy ScannerComs instance, never connected properly'
        self._messages=[]
        
    def close(self):
        '''
        I don't know what happens if you don't close the serial connection.  You should probably close it.
        '''
        if self._coms:
            self._coms.close()
            self._coms=None
            self._str='closed ScannerComs instance'
    
    def clear(self):
        '''
        clear all incoming messages (keyboard included, if enabled)
        '''
        if self._coms:
            self._coms.flushInput()
        if self.keyboard:
            self._readKeys()
        self._messages=[]
    def _readKeys(self):
        # reads numeric keys, removes from keyboard buffer
        return event.getKeys(keyList=map(str,range(10)))
    def _read(self):
        if self._coms:
            while True:
                msg = self._coms.read()
                if not msg:
                    break
                self._messages.append(msg)
        if self.keyboard:
            self._messages.extend(self._readKeys())
            #event.clearEvents(eventType="keyboard")
    #impl: make new component instead, or an option for the existing component
    # waiting like done here won't let the routine loop, so isn't very useful in 
    # PsychoPy.  Was already reported as a bug.
    """
    def wait_for_message(self,*valid_messages):
        '''
        waits until any of the valid messages are encountered.
        
        clears existing messages first
        
        returns True whenever a valid message is encountered.  All messages encountered
        (potentially including those that arrive after the first valid message)
        are discarded.
        
        returns False immediately if no connection and no keyboard
        
        '''
        if not self._coms and not self.keyboard:
            return False
        self.clear()
        while True:
            for msg in self.messages():
                if msg in valid_messages:
                    return True
    """
    def messages(self, clear_after=True, as_set=True):
        '''
        returns a set (or list) of messages that have been gathered since
        last cleared.  By default, will clear the messages after returning them.        
        '''
        if self._coms or self.keyboard:
            self._read()
            ret = self._messages
        else:
            ret=[]
        
        if as_set:
            ret=set(ret)
        if clear_after:
            self._messages=[]
        return ret
    
    def connected_to_serial(self):
        return bool(self._coms)
    def connected_to_keyboard(self):
        return bool(self.keyboard)    
    #clean: repr not as complete after keyboard option added
    def __repr__(self):
        return self._str
    __str__=__repr__
    
    #idea: any way to detect if the coms get closed externally?  It didn't seem like
    # pyserial had anything for that...

