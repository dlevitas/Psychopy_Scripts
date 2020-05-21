from _comp import *

@Comp("connect to scanner coms (triggers, buttons...)")
class ScannerComsConnectComponent(BaseComp):
    def __init__(self,exp, parentName, name='scanner_coms_connect',port=2, timeout=0.001, baudrate=19200, allow_keyboard=False):
        BaseComp.__init__(self,exp,parentName,name)
        
        self.param('port',port)
        self.param('timeout',timeout)
        self.param('baudrate',baudrate)
        self.param('allow_keyboard',allow_keyboard,'bool',hint="If True, keyboard messages (numbers 0-9) will be mixed in as well.  So for button 1, you can use the button or press 1 on the keyboard.")
        
        self.init_code='scanner_coms = ScannerComs(port={port}, timeout={timeout}, baudrate={baudrate}, keyboard={allow_keyboard})'
        self.close_code='scanner_coms.close()'
