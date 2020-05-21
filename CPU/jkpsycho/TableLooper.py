from _comp import *

@Comp("simply loop through a spreadsheet")
class TableLooperComponent(BaseComp):
    def __init__(self, exp, parentName, name='table_looper', var_name='trial', source=''):
        BaseComp.__init__(self,exp,parentName,name)
        
        self.param('var_name',var_name, hint="base name through which to access the values.  For example <var_name>.<column_name>")
        self.param('source',source,'str', hint="A filename for the spreadsheet, only csv files supported currently")
        
        self.init_code='{var_name}=TableLooper({source})'
        self.stop_code='{var_name}+=1'

class TableLooper(object):
    def __init__(self,fpath):
        '''
        Workaround to read in loop variables the way you perhaps thought Psychopy
        would do automatically.
        
        
        Example:
            
            # make example data
            fpath='table_looper_example.csv'
            df=pd.DataFrame(dict(Condition=[1,2,3,2,1,3],File_name=list('aaabbb')))
            df.to_csv(fpath,index=False)
            
            # "begin experiment"
            trial=TableLooper(fpath)
            
            num_trials=10
            for i in range(num_trials):
                # access values
                print(trial)
                print((trial.File_name,trial.Condition))
                
                # "end routine"
                trial+=1
        
        '''
        #fixme: add error checking
        #idea: generic class, list with immutable contents and ability to seek?
        
        import pandas as pd
        self._df = pd.DataFrame.from_csv(fpath,index_col=None)
        self._i=0
        self._apply()
                        
    def _apply(self):
        self._i = self._i%len(self._df)
        s=self._df.iloc[self._i]
        for col in self._df.columns:
            setattr(self,col,s[col])
        self._repr = 'TrialLooper[{}]={}'.format(self._i,s.to_dict())
    def _next(self):
        self._i+=1
        self._apply()
    def _prev(self):
        self._i-=1
        self._apply()
    def _seek(self,i):
        self._i = i
        self._apply()
    def __iadd__(self,off):
        self._i+=off
        self._apply()
        return self
    def __repr__(self):
        return self._repr