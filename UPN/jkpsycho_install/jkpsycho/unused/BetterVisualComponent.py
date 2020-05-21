from _comp import *



'''
class BetterVisualComponent(BaseComp):
    categories = ['Custom']
    def __init__(self, exp, parentName, name='', units='from exp settings', color='$[1,1,1]',
                pos=[0,0], size=[0,0], ori=0 , colorSpace='rgb', opacity=1, **kwargs):
        BaseComp.__init__(self,exp,parentName,name,**kwargs)
        
        self.psychopyLibs=['visual']#needs this psychopy lib to operate
        self.param('units',units,'str', dropdownVals=['from exp settings', 'deg', 'cm', 'pix', 'norm']
            ,hint="Units of dimensions for this stimulus")
        self.param('color',color',str',dropdownUpdates=['constant','set every repeat','set every frame']
            ,hint="Color of this stimulus (e.g. $[1,1,0], red ); Right-click to bring up a color-picker (rgb only)")
        self.param('opacity',)
        self.params['opacity']=Param(opacity, valType='code', allowedTypes=[],
            updates='constant', allowedUpdates=['constant','set every repeat','set every frame'],
            hint=_translate("Opacity of the stimulus (1=opaque, 0=fully transparent, 0.5=translucent)"),
            label=_localized['opacity'])
        self.params['colorSpace']=Param(colorSpace, valType='str', allowedVals=['rgb','dkl','lms','hsv'],
            updates='constant',
            hint=_translate("Choice of color space for the color (rgb, dkl, lms, hsv)"),
            label=_localized['colorSpace'])
        self.params['pos']=Param(pos, valType='code', allowedTypes=[],
            updates='constant', allowedUpdates=['constant','set every repeat','set every frame'],
            hint=_translate("Position of this stimulus (e.g. [1,2] )"),
            label=_localized['pos'])
        self.params['size']=Param(size, valType='code', allowedTypes=[],
            updates='constant', allowedUpdates=['constant','set every repeat','set every frame'],
            hint=_translate("Size of this stimulus (either a single value or x,y pair, e.g. 2.5, [1,2] "),
            label=_localized['size'])
        self.params['ori']=Param(ori, valType='code', allowedTypes=[],
            updates='constant', allowedUpdates=['constant','set every repeat','set every frame'],
            hint=_translate("Orientation of this stimulus (in deg)"),
            label=_localized['ori'])
    def writeFrameCode(self,buff):
        """Write the code that will be called every frame
        """
        buff.writeIndented("\n")
        buff.writeIndented("# *%s* updates\n" %(self.params['name']))
        self.writeStartTestCode(buff)#writes an if statement to determine whether to draw etc
        buff.writeIndented("%(name)s.setAutoDraw(True)\n" %(self.params))
        buff.setIndentLevel(-1, relative=True)#to get out of the if statement
        #test for stop (only if there was some setting for duration or stop)
        if self.params['stopVal'].val not in ['', None, -1, 'None']:
            self.writeStopTestCode(buff)#writes an if statement to determine whether to draw etc
            buff.writeIndented("%(name)s.setAutoDraw(False)\n" %(self.params))
            buff.setIndentLevel(-1, relative=True)#to get out of the if statement
        #set parameters that need updating every frame
        if self.checkNeedToUpdate('set every frame'):#do any params need updating? (this method inherited from _base)
            buff.writeIndented("if %(name)s.status == STARTED:  # only update if being drawn\n" %(self.params))
            buff.setIndentLevel(+1, relative=True)#to enter the if block
            self.writeParamUpdates(buff, 'set every frame')
            buff.setIndentLevel(-1, relative=True)#to exit the if block
'''