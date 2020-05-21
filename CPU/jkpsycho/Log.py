from _comp import *
"""


start='''
if {as_set}:
    {var_name}=set([])
else:
    {var_name}=[]
scanner_coms.clear()
'''
frame='''
_new_messages = scanner_coms.messages(clear_after=True,as_set={as_set})
if {clear_every_frame}:
    {var_name}=_new_messages
else:
    if {as_set}:
        {var_name}.update(_new_messages)
    else:
        {var_name}.append(_new_messages)
'''

#fixme: need to verify that the component time windows are applied automatically.

@Comp("communicate with scanner (trigger, buttons, etc.)")
class ScannerComsComponent(BaseComp):
    def __init__(self, exp, parentName, name='scanner_coms_use', var_name='coms', as_set=True, clear_every_frame=True):
        BaseComp.__init__(self,exp,parentName,name, timed_component=True)
        
        self.param('var_name',var_name, hint = "variable in which the received signals are listed", label="Variable name")
        self.param('as_set',as_set, 'bool', hint = "if True, <var_name> is a set.  Else, a list.", label="Store as a set?")
        self.param('clear_every_frame',clear_every_frame, 'bool', hint="If true, <var_name> will only give the signals that arrived since the previous frame", label="Clear every frame?")
        
        self.start_code=start
        self.frame_code=frame
"""



#comp: need more case studies.  Can/Should I support timing of specific events?
# perhaps with offsets?  Also full routine.  need to have only one Log defined at the start,
# not sure if I can do some neat ordering trick or if I should just have this default
# instantiated or static.
#idea: have at least 2 components.  One initializes (with settings like save prefix)
# and another that logs things.  That is a good style to follow.
from collections import defaultdict
class Log(object):
    '''
    Manually log events in your experiment, export them as csv tables and afni timing files.
    The PsychoPy logs don't necessarially reflect the regressors you actually want, and don't
    output the timings in a ready-to-use format either.  This object gives you full control
    over what events to log and how to log them, then gives you timing files that can be
    immediately used for analysis.
    
    
    Example:
        
        #initialize
        log = Log()
        
        #use
        log.start('some_event')
        # stuff happens...
        log.stop('some_event')
        # can do that multiple times, with multiple event names, overlapping events are fine...
        
        # save csv tables to files like <prefix><event_name>.csv
        log.save_csv(prefix)
        # save afni 1D timing files named like <prefix><event_name>(_dm).1D.  both just the event onsets and also duration modulated (_dm) versions.
        log.save_afni(prefix)
    
    
    for perfect timing accurracy, supply the timestamp explicitly.  For example:
    
        # eventA will start just a tiny bit before eventB
        log.start('eventA')
        log.start('eventB')
        
        # perfectionist, now both events start at exactly the same time in the logs
        time=core.getTime()
        log.start('eventA',time)
        log.start('eventB',time)
    
    '''
    def __init__(self):
        self._starts=defaultdict(list)
        self._stops=defaultdict(list)
        self._started=defaultdict(lambda:False)
        self._runs=defaultdict(list)
        self._finished=False
        self._run=-1
    def next_run(self):
        self._run+=1
    #idea: safer to pass the timein, else you have small differences where you wouldn't expect them
    # (as every line of code takes *some* time at least).  Is there a frame-time in Psychopy that would
    # be more convenient?
    def start(self,what,time=None):
        '''
        log the start of an event named <what>.  If time not supplied, it is determined by core.getTime
        '''
        if time is None:
            time=core.getTime()
        if self._finished:
            raise RuntimeError('this log is already finished, cannot add more to it!')
        if self._started[what]:
            raise RuntimeError("trying to log the start of '{}', but the last occurance hasn't ended yet!".format(what))
        self._started[what]=True
        self._starts[what].append(time)
        self._runs[what].append(self._run)
        return time
    def stop(self,what,time=None):
        '''
        log the end of an event named <what>.  If time not supplied, it is determined by core.getTime
        '''
        if time is None:
            time=core.getTime()
        if self._finished:
            raise RuntimeError('this log is already finished, cannot add more to it!')
        if not self._started[what]:
            raise RuntimeError("trying to log the end of '{}', but it hasn't been started!".format(what))
        self._started[what]=False
        self._stops[what].append(time)
        return time
    def finish(self):
        '''
        called automatically, though no harm in calling it yourself if you know everything
        is finished.  perhaps a good assertion of sorts (RuntimeErrors raised if
        any further logging attempts are made after the Log is finished).
        '''
        if not self._finished:
            self._finished=True
            self.events=dict()
            self.num_runs=self._run+1
            names=self._starts.keys()
            
            bad=[]
            for name in names:
                if self._started[name]:
                    bad.append(name)
            if bad:
                raise RuntimeError('this log was stopped before all events were stopped: {}'.format(bad))
            
            bad=dict()
            for name in names:
                starts=self._starts[name]
                stops=self._stops[name]
                run=self._runs[name]
                if len(starts)!=len(stops):
                    bad[name]=(starts,stops)
                    continue
                df=pd.DataFrame(dict(start_s=starts,stop_s=stops))
                df['duration_s'] = df.stop_s-df.start_s
                df['run']=run
                self.events[name]=df
            if bad:
                raise RuntimeError("the following events couldn't be saved because there was a mismatch in the number of start and stop times logged:\n{}".format(bad))
            
            # runs not explicitly marked by user, so default to just 1 run
            if not self.num_runs:
                for name in names:
                    self.events[name].run=0
                self.num_runs=1
            else:
                raise NotImplementedError("haven't quite gotten multiple runs working yet...")
            
    def save_csv(self,prefix):
        '''
        save csv tables for onset/duration per event
        
        for each event_name:
            save event log in <prefix><event_name>.csv
        '''
        self.finish()
        for name,df in self.events.items():
            df.to_csv(prefix+name+'.csv', index_label='index')
    def save_afni(self,prefix):
        '''
        make afni 1D files for regression!
        
        for each event_name:
            save onset times in <prefix><event_name>.1D
            save onsets and durations in <prefix><event_name>_dm.1D
        '''
        self.finish()
        for name,df in self.events.items():
            # group by run
            onsets=[]
            durations=[]
            for r in xrange(self.num_runs):
                onsets.append(df[df.run==r].start_s.values)
                durations.append(df[df.run==r].duration_s.values)
            # format and write to file
            with open(prefix+name+'.1D','w') as f:
                f.write(str1D(onsets,multi=True))
            with open(prefix+name+'_dm.1D','w') as f:
                f.write(str1D(onsets,dm=durations,multi=True))
        