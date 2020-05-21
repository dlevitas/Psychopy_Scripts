from _comp import *

#idea: endExpNow also a thing

@Comp("Exit the routine when a condition is True")
class StopRoutineComponent(BaseComp):
    def __init__(self, exp, parentName, name='routine_stopper', condition='False'):
        BaseComp.__init__(self,exp,parentName,name, timed_component=True)
        
        self.param('condition',condition, hint = "If expression evaluates to True the routine will stop.  example to stop if buttons 1,2,or 5 were pressed:  any(b in buttons for b in ('1','2','5'))", label="stop condition")
        self.frame_code='if {condition}: stopRoutine()'


def stopRoutine():
    '''
    in PsychoPy, you can set continueRoutine to False to cause the routine
    to stop.  Or call this function.
    
    I prefer this to be done via a function, so that if the PychoPy implementation
    ever changes I can just update this one function and all the old code will still work.
    '''
    #global continueRoutine
    #continueRoutine=False
    
    # I think this is needed when debugging in Spyder, UMD reloader might
    # otherwise invalidate sys module
    import sys
    
    sys.modules['__main__'].continueRoutine=False

