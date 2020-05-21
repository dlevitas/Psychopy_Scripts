from _base import *
from os import path

thisFolder = path.abspath(path.dirname(__file__))#the absolute path to the folder containing this path
iconFile = path.join(thisFolder,'InitJK.png')
tooltip = _translate("Initialize jkpsycho stuff")

baseFolder = path.dirname(thisFolder)

init='''
import sys
from jkpsycho import *
from jkpsycho._comp import CompDetails
'''.format(baseFolder.replace('\\','/'))

class InitJKComponent(BaseComponent):
    categories = ['Custom']
    def __init__(self, exp, parentName, name='init_jk'):
        BaseComponent.__init__(self,exp, parentName, name)
        self.type='InitJK'
        self.categories=['misc']
        self.order=[]
        self.params=dict(name=self.params['name'])
    def _write(self,buff,pat):        
        s=pat.format(**self.params)
        s=unicode(s+'\n')
        buff.writeIndentedLines(s)
    def writeInitCode(self,buff):
        self._write(buff,init)
    def writeRoutineStartCode(self,buff):
        pass
    def writeFrameCode(self,buff):
        pass
    def writeRoutineEndCode(self,buff):
        pass
    def writeExperimentEndCode(self,buff):
        pass

