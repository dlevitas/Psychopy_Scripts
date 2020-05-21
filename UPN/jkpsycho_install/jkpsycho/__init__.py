from __future__ import division
import numpy as np
from random import random
import warnings
import sys

# mostly copies from my jkpy package.  A common Psychopy related library, though
# just a very rough draft.

class KeyFilter(object):
    def __init__(self, include, exclude):
        if hasattr(include,'capitalize'):
            include=[include]
        if hasattr(exclude,'capitalize'):
            exclude=[exclude]
        
        self.include=include
        self.exclude=exclude
    def __contains__(self,key):
        if self.include and key not in self.include:
            return False
        if self.exclude and key in self.exclude:
            return False
        return True


def center_text(txt):
    lines=txt.split('\n')
    width=max(len(line) for line in lines)
    lines=[line.center(width) for line in lines]
    return '\n'.join(lines)

def isstr(thing):
    try:
        return thing==(thing+'')
    except:
        return False

def sjoin(delim):
    def helper(vals):
        return delim.join(map(str,vals))
    return helper

def _str1D(*args):
    npoint=len(args[0])
    npart=len(args)
    arr=np.empty((npoint,npart),dtype=object)
    for i,arg in enumerate(args):
        arr[:,i]=arg
    return ' '.join(map(''.join,arr.astype(str)))

def np_in(thing,possibilities):
    #numpy future warning that arr==None will be elementwise in the future
    # I assumed it was that way already?  but it doesn't matter either way.
    # I only expect single None's for thing, any array of Nones can be whatever...
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for p in possibilities:
            if np.all(thing==p):
                return True
    return False

def str1D(onset,dm=None,am=None, multi=False):
    if multi:
        nrun=len(onset)
        if dm is None:
            dm=[None]*nrun
        if am is None:
            am=[None]*nrun
        
        lines=[]
        for i in xrange(nrun):
            lines.append(str1D(onset[i],dm=dm[i],am=am[i]))
        return '\n'.join(lines)
    
    if np_in(onset,['*',None,False]):
        return '*'
    try:
        if not len(onset):
            return '*'
    except:
        return '*'
    
    args=[onset]
    if am is not None:
        am=map(sjoin(','),am)
        args.extend(['*',am])
    if dm is not None:
        args.extend([':',dm])
    return _str1D(*args)


def round_to(value, nearest=1.0):
    '''
    rounds the value <value> to the nearest <nearest>
     
    default nearest=1:  round to nearest whole number
    nearest=0.1: round to nearest tenth
    '''
    value=np.asarray(value,dtype=float)
    nearest*=1.0
    bump=np.sign(value)/2.0
    return np.trunc(value/nearest+bump) * nearest

def rnd(lo,hi,nearest):
    return round_to(random()*(hi-lo)+lo, nearest)








def constrained_sort(counts,max_consec=1):
    '''
    res=constrained_sort(counts,max_consec=1)
    
    Generates a np.array of length sum(counts) that meets the given constraints.
    The result is 'sorted', in that it is a predictable order.  More numerous
    values are placed preferentially, interrupted only by the constraints.
    If there were no constraints, you'd just get argsort(counts) ordering.
    
    Useful way to determine if there exists at least one valid ordering for
    the given constraints.  At least I think so.  May have missed a corner
    case?  Works so far.
    
    Arguments
    ---------------
        
        counts: sequence of integers
            Describes the distribution of values in the resulting array.  
            sum(res==i)==counts[i] always.
        
        max_consec: single integer or sequence of integers
            Limit on the maximum number of consecutive values.  0 doesn't make
            sense, 1 means no immediate repeats.  
    '''
    if not hasattr(max_consec,'__len__'):
        max_consec=(max_consec,)*len(counts)
    
    N=sum(counts)
    counts=-np.array(counts)
    consec_count=1
    consec_val=-1
    
    x=np.zeros(N,dtype=int)
    for i in range(N):
        # if not limited, just pick the most plentiful remaining
        if consec_count!=max_consec[consec_val]:
            j=np.argmin(counts)
        # may be limited, so have a backup 
        else:
            js=np.argsort(counts)
            if js[0]!=consec_val:
                j=js[0]
            else:
                j=js[1]
        x[i]=j
        counts[j]+=1
        if j==consec_val:
            consec_count+=1
        else:
            consec_count=1
            consec_val=j
        
    if np.any(counts):
        raise RuntimeError('unable to generate valid ordering')
    return x
from itertools import izip_longest
def paste(*columns,**kwargs):
    align=kwargs.get('align','left')
    delim=kwargs.get('delim',' ')
    #idea: column widths can be specified manually
    #idea: pass in sequences (non-str) that are interpreted as pre-split lines
    
    if align=='left':
        def pad(s,w):
            return s+' '*(w-len(s))
    elif align=='right':
        def pad(s,w):
            return ' '*(w-len(s))+s
    elif align=='center':
        def pad(s,w):
            return s.center(w)
    else:
        raise ValueError("invalid alignment type '{}'".format(align))
    
    table=list(izip_longest(*[column.split('\n') for column in columns],fillvalue=''))
    ncol=len(columns)
    widths=[0]*ncol
    for row in table:
        for i,cell in enumerate(row):
            widths[i]=max(widths[i],len(cell))
    
    lines=[]
    for row in table:
        line=delim.join(pad(cell,w) for (cell,w) in zip(row,widths))
        lines.append(line)
    txt='\n'.join(lines)
    return txt


from itertools import groupby
def constrained_shuffle(order,max_consec):
    '''
    Randomization with constraints, in the following steps:
        1) numpy.random.shuffle
        2) loop through order removing each element that
           breaks the constraints
        3) for each removed element, reinsert it:
            a) randomly inspect every possible insertion point
            b) insert element at first valid position found
    
    Supported constraints:
        - max_consec
    
    inspired by make_random_timing.py
    '''
    N=len(order)
    np.random.shuffle(order)
    src=list(order)
    
    others=[]
    lst=[]
    consec_count=1
    consec_val=None
    #idea: multiple passes here might be worthwhile.  
    # could keep trying until none of the remaining can be appended
    for val in src:
        # in a run
        if val==consec_val:
            # cannot continue this run
            if consec_count==max_consec[val]:
                others.append(val)
                continue
            # still running
            consec_count+=1
        # new value, new run
        else:            
            consec_count=1
            consec_val=val
        
        # current value works fine at this spot
        lst.append(val)
    
    lst.insert(0,None)
    lst.append(None)
    while others:
        src=others
        others=[]
        for o in src:
            # precalculate consecutive lengths.  mostly for my own sanity,
            # but it is reasonable assumption that if this is taking long enough
            # to care about the constraints are likely hard to meet and so
            # it is worthwhile to calculate run lengths up front rather than
            # on-demand with overlaps.
            consecs=[]
            for (val,grp) in groupby(lst):
                N=sum(1 for _ in grp)
                consecs.extend([N]*N)
            
            N=len(lst)-2
            js=np.random.permutation(N+1)+1
            M=max_consec[o]
            for j in js:
                # max length run on the left can't extend
                if lst[j-1]==o and consecs[j-1]==M:
                    continue
                # max length run on the right can't extend
                if lst[j]==o and consecs[j]==M:
                    continue    
                
                lst.insert(j,o)
                break
            else:
                others.append(o)
    
    order[:]=lst[1:-1]
    return order

def constrained_permute(counts,max_consec=1):
    '''
    constrained_sort + constrained_shuffle.  see those
    functions for the documentation.
    '''
    if not hasattr(max_consec,'__len__'):
        max_consec=(max_consec,)*len(counts)
    order=constrained_sort(counts,max_consec)
    return constrained_shuffle(order,max_consec)

def make_random_trial_order(types, num_per_type, max_consec):
    N=len(types)
    if not hasattr(num_per_type,'__len__'):
        num_per_type=[num_per_type]*N
    if not hasattr(max_consec,'__len__'):
        max_consec=[max_consec]*N
    
    order=constrained_permute(num_per_type,max_consec)
    # paranoid validation:
    for (val,grp) in groupby(order):
        if sum(1 for _ in grp)>max_consec:
            raise RuntimeError("failed to meet max_consec constraint, this is Josh's fault...")
    # remap, just in case types weren't sequential and 0 based
    return [types[i] for i in order]


import pandas as pd

try:
    from psychopy import core
except:
    pass # not being used with PsychoPy, that's fine
else:    
    # anything here that requires PsychoPy to be loaded
    
    # code parts for the builder components.  either things of more general use,
    # or things that are needed for the generated code to work.
    from ScannerComs import ScannerComs, makeScannerComsAccess
    from Log import Log
    from TableLooper import TableLooper
    from StopRoutine import stopRoutine
    from TextResponse import TextGrabber, RawText
    from _comp import CompDetails
    
    
    
    
    
    
    
    
    test_modifiers=None
    def _save_modifiers():
        try:
            main = sys.modules['__main__']
            win=main.win
            import pyglet
        except Exception as e:
            print(e)
            print('no window?')
            #fixme: I don't think this will always be an error...
            return
        
        flags_and_names=[]
        for name in 'mod_shift mod_ctrl mod_alt mod_windows mod_command mod_option mod_capslock mod_numlock mod_scrolllock mod_accel'.split():
            enum=name.upper()
            name=name.split('_')[-1]
            flags_and_names.append( (getattr(pyglet.window.key,enum),name) )
        print(flags_and_names)
        def wrapped_onPygletKey(symbol, modifiers, emulated=False):
            #global test_modifiers
            #test_modifiers=[]
            event.modifiers=[]
            for (flag,name) in flags_and_names:
                if (flag & modifiers):
                    event.modifiers.append(name)
                #pass
                #if flag & modifiers:
                #    print(name)
            #test_modifiers = [ name for name in (flag,name) in flags_and_names if flag&modifiers ]
            #if test_modifiers:
            #    print(test_modifiers)
            #if test_modifiers:
            #    print('a')
            return event._onPygletKey(symbol,modifiers,emulated=emulated)
        
        #event.useText=True
        def wrapped_onPygletText(text, emulated=False):
            print(text)
            return event._onPygletText(text,emulated=emulated)
        
        
        win.winHandle.on_key_press = wrapped_onPygletKey
        win.winHandle.on_text = wrapped_onPygletText
    #_save_modifiers()
    
     # mostly copy/paste from quit as defined in psychopy.core
    # was having issues wrapping it for some reason... eventually need to figure
    # that out, happens occasionally in IPython + Spyder + UMD reloading thing
    def dbg_quit():
        print("custom quit routine for debug convenience, you shouldn't see this message if running an actual experiment!!")
        from psychopy import core
        core.logging.flush()
        for t in core.threading.enumerate():
            if hasattr(t,'stop') and hasattr(t,'running'):
                t.stop()
                while t.running==0:
                    pass
        
        # this is the only new part, want to close that window
        import sys
        main = sys.modules['__main__']
        main.win.close()
        
        # not really appropriate, but IPython catches it and then returns to interpreter at least.
        sys.exit(0)
    
    #idea: maybe other conveniences to consider.  Though PsychoPy unfortunately runs a number of things
    # before I have a chance to, at least using this approach.
    try:
        if __IPYTHON__:
            print('running in ipython mode, some debugging conveniences enabled!')
            core.quit = dbg_quit
    except:
        pass