from psychopy.app.builder.components._base import *
from os import path
from psychopy.app.builder.experiment import Param, IndentingBuffer
from psychopy import core
#fixme: need to test the param settings.  PsychoPy's stuff didn't make full sense on the first pass, need to check that I provided a good interface and that I'm using it correctly for my own components    

#idea: code component with timing constraints?


'''
* don't name anything to end with 'Component' unless you want PsychoPy finding it and making
  it a component
  
* you must end component classes with 'Component'

* can have multiple components per file, but then not sure how to set their icons and such...

* need to restart PsychoPy to have code changed take effect when developing components

* psychopy saves the Param results rather than Param inputs in psyexp.  This can cause
  unexpected problems if you have a Param with a fixed (no dropdown) valType and later
  change that valType.  PsychoPy will load up the old valType without a care...
  At least if you have a dropdown, you can open the settings dialog again and adjust
  as needed.  But without one, it is just broken forever.

* Not sure how reusable a component can be.  no system in place for chaining write methods,
  hard to even know who writes what.  Since the timing control system for components is a mess,
  many components add the timing stff themselves... more repeated code.  For example, it seriously
  isn't worthwhile from what I can tell to make a new text component type that continues on key press.
  With my custom base class, that's 4 types fighting over the writing.  Fastest approach is to derive from
  TextComponent and then recreate KeyboardComponent .  call both writer methods each time, repeat the timing
  info for Keyboardcomponent.  What a mess.  Would have been far more reusable if each component class
  was in charge of 'finalizing' itself by writing out the implementation per slot.  Then all related
  implementations can be joined together and put under common code as needed (for example timing stuff).
  
      Can't remove features for superclasses... very annoying when superclasses often
      implement their own timing nonsense and will raise exceptions when they can't find
      the timing params anymore.
'''

#idea: request feature in PsychoPy.  requirePsychoPyLibs is a good feature, but I want it for non-psychopy libs!!

# doesn't work, can rebuild the experiment without reimporting this... so the flag is never reset.
'''
jkpsycho_already_imported = False
def import_jkpsycho(comp):
    global jkpsycho_already_imported
    if not jkpsycho_already_imported:
        jkpsycho_already_imported=True
        comp('\n# at least one component used in this experiment requires jkpsycho\nfrom jkpsycho import *')
'''

#total hack... the Experiment class uses this  _numpyRandomImports module constant
# to add some imports to the top of the script.  I want my module added there too, but
# no current support for that.  Only other things that uses this constant that I can
# see is Namespace, also in the Experiment module...
# ', '.join(_numpyRandomImports) is used for the import from list, so just import
# a dud and start new line for the final thing to be "joined".  classic hack...
from psychopy.app.builder import experiment
_hacky_import = 'np\nfrom jkpsycho import *'
if experiment._numpyRandomImports[-1]!=_hacky_import:
    try:
        experiment._numpyRandomImports.remove(_hacky_import) # to be slightly safer?
    except ValueError:
        pass
    experiment._numpyRandomImports.append(_hacky_import)

timed_param_names = ['startType', 'startVal', 'startEstim', 'stopVal', 'stopType', 'durationEstim']    
code_slots = [n+'_code' for n in 'init start frame stop close'.split()]
write_methods = 'writeInitCode writeRoutineStartCode writeFrameCode writeRoutineEndCode writeExperimentEndCode'.split()

def dumpComp(comp):
    ret=dict()
    for name,meth in zip(code_slots,write_methods):
        buff = IndentingBuffer()
        getattr(comp,meth)(buff)
        val = buff.getvalue()
        #print('dump {}.{}'.format(comp,meth))
        #print(val)
        ret[name]=val
        buff.close()
    return ret


translation_cache=dict()
def translate(txt, _cache=dict()):
    '''
    memoized translator.  Easier to use than the _localized dict thing in PsychoPy
    by default
    '''
    ret=_cache.get(txt,None)
    if ret is None:
        _cache[txt]=ret=_translate(txt)
    return ret
    
class MyParam(object):
    '''
    I used this once for debugging a Param.  Good Python, concepts better than
    interfaces so frequently!
    '''
    def __init__(self,*args,**kwargs):
        self._param = Param(*args,**kwargs)
    def __getattr__(self,attr):
        if attr.startswith('_'):
            return object.__getattribute__(self,attr)
        #print('getattr {}'.format(attr))
        return getattr(self._param,attr)
    def __setattr__(self,attr,val):
        if attr.startswith('_'):
            object.__setattr__(self,attr,val)
        else:
            import traceback
            traceback.print_stack()
            print('setattr {} = {}\n\n\n'.format(attr,val))
            setattr(self._param,attr,val)
    
    def __repr__(self):
        return 'MyParam'



import sys
def Comp(tooltip,icon_file=None):
    '''
    decorate your Component class with this to add in the icon, tooltip, and help text automatically
    help text comes from the docstring of the decorated component class.
    
    Had more planned for this, but stopped short.  
    '''
    def modifier(cls):
        # find the module
        name = cls.__module__
        mod = sys.modules[name]
        # find the path
        folder = path.abspath(path.dirname(mod.__file__))
        # extract proper name, minus the component suffix
        name=cls.__name__
        name=name.split('.')[-1]
        t='Component'
        assert(name.endswith(t))
        name=name[:-len(t)]
        '''
        # default url and default documentation html file
        #style: is this how I want it?  need to delete the file whenever I want
        # changes to be applied.  Might be simpler to just do the html documentation
        # by hand.  Isn't like the component class needs inline documentation anyways.
        if not hasattr(cls,'url'):
            cls.url = path.join(folder,name+'.html')
            if not path.exists(cls.url) and cls.__doc__:
                with open(cls.url,'w') as f:
                    from docutils.core import publish_string
                    f.write(publish_string(cls.__doc__,writer_name='html'))
        '''
        #simpler approach, just set the url to a local help file if it exists
        if not hasattr(cls,'url'):
            url = path.join(folder,name+'.html')
            if path.exists(url):
                cls.url=url
        
        # apply the tooltip
        mod.tooltip=translate(tooltip)
        
        # default icon path
        if not hasattr(mod,'iconFile'):
            iconFile=icon_file
            if iconFile is None:
                iconFile=name+'.png'
            iconFile=path.join(folder,iconFile)
            mod.iconFile=iconFile
        # oops, no icon there... unset it
        if not path.exists(mod.iconFile):
            delattr(mod,'iconFile')
            
        
        # doesn't work for some reason...
        #cls.__name__=comp_name
        
        # too far?  just want a dynamic superclass...  and auto intherit __init__ chain.
        '''
        retcls=type(name,(BaseComp,), cls.__dict__)
        class Decorated(_Comp):
            __name__=name
        ''' 
        return cls
    return modifier

'''
Probably messy legacy, surely can't be intentional.  PsychoPy seems to have ambiguous
terminology sometimes.

There is an assumption that all components have a representative object in the global
namespace.  most of these objects have a 'status' member defined that is used
... often by many components to figure out when to be active.  But it isn't enforced,
and is only partially supported by the general experiment code...  

Not at all sure if this is something that users can safely rely on, or if I should
rely on it or even support it.  But for now, I'll support it.

The pattern I've been using is to have a separate component object that manipulates
a more conveniently named object with the actual desired data.  It would be bad
to force extra data members on those used objects.

NOT_STARTED: beginning state.  not active each frame, but eligable to be STARTED
STARTED: should be active each frame
STOPPED: should not be active each frame
FINISHED: mysterious state, if all active components are FINISHED then the routine
will be stopped forcefully.  Not sure if ever actually used.  Not sure if it can be used
reliably, since it requires consensus.  really strange...  The better approach seems
to be not setting an end time and having other components potentially set continueRoutine
to False.
'''
class CompDetails(object):
    '''
    Contains timing details for the related PsychoPy component.  You may set
    status yourself to STOPPED to force the component to stop updating every frame.
    Also set it back to NOT_STARTED if you really want to (it'll get STARTED again
    next frame if conditions are right, and tStart + frameNStart will be updated).
    '''
    def __init__(self):
        self.init(self)
    @classmethod
    def init(cls,obj):
        obj.status = NOT_STARTED
        obj.tStart = None
        obj.frameNStart = None


# base class provided by PsychoPy was neither basic enough nor convenient enough.  This class
# will aim to be very flexible and provide support for all the common stuff you might want in a
# custom component.

class CompTools(object):
    def _initialize(self):
        # attributes for code patterns, simple
        for name in code_slots:
            setattr(self,name,'')
        self._finalized=False
    def _remove_timed_params(self):
        for pname in timed_param_names:
            try:
                del self.params[pname]
                self.order.remove(pname)
            except ValueError:
                pass
    # doesn't work!
    def _hide_timed_params(self):
        for pname in timed_param_names:
            try:
                self.order.remove(pname)
            except ValueError:
                pass
        self.params['startType'].val='time (s)'
        self.params['stopType'].val='duration (s)'
        self.params['startVal'].val=0.0
        self.params['stopVal'].val=''
        self.params['startEstim'].val=0.0
        self.params['durationEstim'].val=1.0
    def _endless(self):
        self.params['startType'].val='time (s)'
        self.params['stopType'].val='duration (s)'
        self.params['startVal'].val=0.0
        self.params['stopVal'].val=''
        self.params['startEstim'].val=0.0
        self.params['durationEstim'].val=1.0
    
    def _finalize(self):
        if not self._finalized:
            # give derived object a chance to finish a few things...
            # like the params may not have been fully configured until just now
            self._finalized=True
            self.finalize()
            
            # not doing super methods anymore, not worth it...
            return
    
    def finalize(self):
        '''
        reimplement this method yourself to have one last chance to configure
        stuff before the _code stuff is written out!
        '''
        pass
    
    class WithBuff:
        def __init__(self,comp,buff):
            self.comp=comp
            self.buff=buff
        def __enter__(self):
            self.comp._buff=self.buff
        def __exit__(self,e_ty,e_val,tb):
            delattr(self.comp,'_buff')
    def buff(self,buff):
        return self.WithBuff(self,buff)
        

    def _indent(self, i, relative=True):
        self._buff.setIndentLevel(i,relative=relative)
    def _write(self,pat, indent=0):        
        if not pat:
            return
        s=pat.format(**self.params)
        s=unicode(s+'\n')
        #print(s)
        self._buff.setIndentLevel(indent, relative=True)
        try:
            self._buff.writeIndentedLines(s)
        finally:
            self._buff.setIndentLevel(-indent, relative=True)
        return len(s)-1
    __call__=_write
    
    class _Header:
        def __init__(self,comp,post=None):
            txt='{name}'
            if post is not None:
                txt+=' - '+post
            self.txt=txt
            self.comp=comp
        def __enter__(self):
            line='## {} ##'.format(self.txt)
            line=line.format(**self.comp.params)
            n=70-len(line)
            if n>0:
                line+='#'*n
            self.N = len(line)
            xx='#'*self.N
            self.comp('\n'.join(('\n',xx,line,xx)))
        def __exit__(self,e_ty,e_val,tb):
            self.comp('#'*self.N+'\n\n')
    def _header(self,post=None):
        return self._Header(self,post)

    def param(self, name, val, valType='code', hint=None, label=None, updates='constant', categ="Basic", dropdownVals=None, dropdownTypes=None, dropdownUpdates=None, readOnly=False):
        '''
            name
                the param name
            val
                the value for the param
            valType='code'
                ('num','str','code','bool') how to interpret the value
            hint=name
                simple description
            label=name
                name presented in settings dialog
            categ="Basic"
                don't know, unused by me
            updates='constant'
                when is the param value updated ('constant','experiment', 'routine', 'set every frame')
            
            dropdownVals=None
                provide a sequence of valid values to restrict given vals to those vals (and provide dropdown list to choose from)
            dropdownTypes=None
                "if other types are allowed then this is the possible types this parameter can have (e.g. rgb can be 'red' or [1,0,1])"
                dropdown list of valid options if provided
            dropdownUpdates=None
                dropdown options for valid update settings ['constant', 'routine', 'set every frame'].  Supply True to have it filled with the
                common types.
        '''
        if dropdownTypes:
            allowedTypes=dropdownTypes
        else:
            allowedTypes=[]
        if dropdownVals:
            allowedVals=dropdownVals
        else:
            allowedVals=[]
        if dropdownUpdates is True:
            allowedUpdates=['constant','experiment', 'routine', 'set every frame']
        elif dropdownUpdates:
            allowedUpdates=dropdownUpdates
        else:
            allowedUpdates=[]
        
        if label is None:
            label = name
        if hint is None:
            hint = name
        
        label=translate(label)
        hint=translate(hint)
                
        param=Param(val,valType=valType, allowedVals=allowedVals, allowedTypes=allowedTypes, updates=updates, allowedUpdates=allowedUpdates, hint=hint, label=label, categ=categ )
        param.readOnly=readOnly
        
        self.params[name]=param
        self.order.append(name)


def writer(method):
    def helper(self,buff):
        with self.buff(buff):
            self._finalize()
            method(self)
    return helper
    
class BaseComp(CompTools,BaseComponent):
    categories=['Custom']
    def __init__(self, exp, parentName, name, **kwargs):
        '''
        A better BaseComponent class than is provided by PsychoPy (that's the goal, anyway).
        Extends BaseComponent.
        
        Code related data members:
            Now much simpler to provide the code that will be written to a compiled PsychoPy
            experiment script.  Simply set the relevant data members to be a formattable string, 
            and all the remaining work is done for you.  Use named fields to be replaced by param values.
            The old way was to implement methods like "writeInitCode"... I do that for you.
            
            init_code   - put at the start of the script
            start_code  - put right before the routine starts
            frame_code  - run every frame within the routine (though timing controls may modify this, like if you set an onset and duration)
            stop_code   - run after the routine ends
            close_code  - put at the every end of the script
            
            
            #not implemented:
            #started_code - only meaningful for timed components (see timed_component param).  run when the status is changed to STARTED due to timing settings
            #stopped_code - only meaningful for timed components (see timed_component param).  run when the status is changed to STOPPED due to timing settings (not guaranteed to run, so often safe to use both this and stop_code for cleanups)
            
            Example: 
                
                self.init_code="print('the name of this script is {name}')"
                # name will be replaced with str(self.params[name]) and that code placed
                # at the start of the script.
        
        Simpler Params:
            Rather than messing with the Param objects and translating things and all that
            pain, just use the more convenient param method.  Params are added in order
            that you supply, automatically translated, the options are reworded/renamed
            to make more sense (to me at least), and there are better defaults.
        
        Consistent timing and status details:
            An object like CompDetails will be created automatically and assigned
            the name {name}.  The primary use of this object is for timing control.
            So most features won't be used unless you have timed_component=True.
            
            Your frame_code will be run whenever {name}.status==STARTED.  status will
            be changed automatically by the timing control logic.  Additionally, anyone
            can set {name}.status=STOPPED to stop your component.  That's useful if the
            component should be stopped in response to some external event.
            
            You may supply your own CompDetails-like object to overwrite the default one
            in your own init_code.
        
        #disabled:
        #if requires_jkpsycho=True (default), jkpsycho will be imported automatically as needed
        
        NEW PARAMS:
        --------------------------
            
            timed_component=False
                If True, you'll get the default timing control params ['startType', 'startVal', 'startEstim', 'stopVal', 'stopType', 'durationEstim']
                and all the timing logic that should come with it.  If False, those params aren't added (so you don't have to manually remove them anymore!)
        
        '''
        self._timed_component = kwargs.pop('timed_component',False)
        #self._requires_jkpsycho = kwargs.pop('requires_jkpsycho',True)
        #idea: convert camel case to _ postfix _component for default name
        super(BaseComp, self).__init__(exp, parentName, name, **kwargs)
        self.type=str(type(self)).replace('Component','')
        self.categories=['misc']
                    
        if not self._timed_component:
            self._remove_timed_params()
        
        self._initialize()
    
    ##########################################################################################
    ## helper methods for writing implementation to compiled script
    ##########################################################################################
    #idea: bring dedent and clean_code functions from jkpy?
    
    ##########################################################################################    
    ## BaseComponent methods for writing the various implementation sections
    ##########################################################################################
    
    # top of script
    @writer
    def writeInitCode(self):
        #if self._requires_jkpsycho:
        #    import_jkpsycho(self)
        
        # the {name} is used to store timing and status details for the component
        # as seems to be a partial convention in PsychoPy.  Derived components
        # may replace {name} with whatever object they wish in their own init code,
        # but it must follow the CompDetails interface
        with self._header('initialize'):
            self('{name}=CompDetails()')
            if self.init_code:
                self(self.init_code)
    
    # before routine loop
    @writer
    def writeRoutineStartCode(self):
        # if timed, let the timing logic figure out when to start it
        '''
        if self._timed_component:
            self('{name}.status = NOT_STARTED')
        # otherwise just run it immediately from the start of the routine
        else:
            self('{name}.status = STARTED')
        '''
        #PychoPy currently does this itself, though it forces everything to be NOT_STARTED.
        # can't overwrite it.  so even untimed components will need in-frame code
        # to set STARTED if I'm using CompDetails.
        if self.start_code:
            with self._header('pre-routine'):
                self(self.start_code)
    
    # every frame in routine loop
    @writer
    def writeFrameCode(self):
        with self._header('frame updates'):
            # logic to change status NOT_STARTED->STARTED->STOPPED
            self('# timing logic')
            if self._timed_component:
                # write logic to set status=STARTED at the appropriate time
                self.writeStartTestCode(self._buff) #WARNING: shifts indent up
                self('{name}.status=STARTED')
                #if self.started_code:
                #    self(self.started_code)
                self._indent(-1);
                
                # write logic to set status=STOPPED at the appropriate time
                if self.params['stopVal'].val not in ['',None,-1,'None']:
                    self.writeStopTestCode(self._buff) #WARNING: shifts indent up
                    self('{name}.status = STOPPED')
                    #if self.stopped_code:
                    #    self(self.stopped_code)
                    self._indent(-1)
            else:
                self('if {name}.status==NOT_STARTED: {name}.status=STARTED')
            
            if self.frame_code:
                self('# update')
                # always let user have the ability to stopp the component manually by
                # setting status=STOPPED (or FINISHED, but FINISHED seems useless)
                self('if {name}.status == STARTED:')
                self(self.frame_code, indent=1)
    
    # after routine loop
    @writer
    def writeRoutineEndCode(self):
        if self.stop_code:
            with self._header('post-routine'):
                self(self.stop_code)
    
    # end of script
    @writer
    def writeExperimentEndCode(self):
        if self.close_code:
            with self._header('cleanup'):
                self(self.close_code)


import functools
def perr(fn):
    '''
    decorator that prints any exceptions, good where exceptions
    would otherwise be eaten (async callbacks?).  Works as long as printing
    works.
    '''
    @functools.wraps(fn)
    def helper(*args,**kwargs):
        try:
            return fn(*args,**kwargs)
        except:
            import traceback
            traceback.print_exc()
            raise
    return helper