# -*- coding: utf-8 -*-
from __future__ import division

"""
Created on Thu Aug 25 12:58:30 2016

@author: Daniel
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 17:25:03 2016

@author: Daniel
"""
import os, random
import pandas as pd
import numpy as np
#from stat_formulas import *

nRuns = 1
pairs = 12
Types = 9
nConditions = 4

cwd = os.path.dirname(__file__)
print cwd
#base_dir = os.path.dirname(cwd)

#os.chdir(base_dir)


Pos = os.listdir(os.path.join(cwd + '/PositivePics_8/'))[:-1]
Neg= os.listdir(os.path.join(cwd + '/NegativePics_8/'))[:-1]
Neut = os.listdir(os.path.join(cwd + '/NeutralPics_8/'))[:-1]

NegNames = []
PosNames = []
NeutNames = []

for i in Pos:
    PosNames.append(os.path.join(cwd + '/PositivePics_8/' + i))
for i in Neg:
    NegNames.append(os.path.join(cwd + '/NegativePics_8/' + i))
for i in Neut:
    NeutNames.append(os.path.join(cwd + '/NeutralPics_8/' + i))

df = pd.concat([pd.DataFrame(NegNames), pd.DataFrame(PosNames), pd.DataFrame(NeutNames)],
            axis=1, ignore_index=True).sample(frac=1).reset_index(drop=True)
df.columns = ["Negative","Positive","Neutral"]

for i in xrange(1, Types+1):
    if i == 1:
        type1 = pd.DataFrame((2*"neut_neut.").split("."))[:-1]
        prime1 = pd.DataFrame(NeutNames[0:2])
        target1 = pd.DataFrame(NeutNames[2:4])
        condition = pd.DataFrame(list("1"*len(type1)))
        neut_neut = pd.concat([prime1, target1, type1, condition], axis=1, ignore_index=True)
    elif i == 2:
        type2 = pd.DataFrame((2*"pos_pos.").split("."))[:-1]
        prime2 = pd.DataFrame(PosNames[0:2])
        target2 = pd.DataFrame(PosNames[2:4])
        condition = pd.DataFrame(list("2"*len(type2)))
        pos_pos = pd.concat([prime2, target2, type2, condition], axis=1, ignore_index=True)
    elif i == 3:
        type3 = pd.DataFrame((2*"neg_neg.").split("."))[:-1]  
        prime3 = pd.DataFrame(NegNames[0:2])
        target3 = pd.DataFrame(NegNames[2:4])
        condition = pd.DataFrame(list("3"*len(type3)))
        neg_neg = pd.concat([prime3, target3, type3, condition], axis=1, ignore_index=True)
    elif i == 4:
        type4 = pd.DataFrame((1*"neut_pos.").split("."))[:-1]
        prime4 = pd.DataFrame(NeutNames[4:5])
        target4 = pd.DataFrame(PosNames[4:5])
        condition = pd.DataFrame(list("4"*len(type4)))
        neut_pos = pd.concat([prime4, target4, type4, condition], axis=1, ignore_index=True)
    elif i == 5:
        type5 = pd.DataFrame((1*"pos_neut.").split("."))[:-1]   
        prime5 = pd.DataFrame(PosNames[5:6])
        target5 = pd.DataFrame(NeutNames[5:6])
        condition = pd.DataFrame(list("4"*len(type5)))
        pos_neut = pd.concat([prime5, target5, type5, condition], axis=1, ignore_index=True)
    elif i == 6:
        type6 = pd.DataFrame((1*"neut_neg.").split("."))[:-1]
        prime6 = pd.DataFrame(NeutNames[6:7])
        target6 = pd.DataFrame(NegNames[4:5])
        condition = pd.DataFrame(list("5"*len(type6)))
        neut_neg = pd.concat([prime6, target6, type6, condition], axis=1, ignore_index=True)
    elif i == 7:
        type7 = pd.DataFrame((1*"neg_neut.").split("."))[:-1]  
        prime7 = pd.DataFrame(NegNames[5:6])
        target7 = pd.DataFrame(NeutNames[7:8])
        condition = pd.DataFrame(list("5"*len(type7)))
        neg_neut = pd.concat([prime7, target7, type7, condition], axis=1, ignore_index=True)
    elif i == 8:
        type8 = pd.DataFrame((1*"pos_neg.").split("."))[:-1]  
        prime8 = pd.DataFrame(PosNames[6:7])
        target8 = pd.DataFrame(NegNames[6:7]) 
        condition = pd.DataFrame(list("6"*len(type8)))
        pos_neg = pd.concat([prime8, target8, type8, condition], axis=1, ignore_index=True)
    elif i == 9:
        type9 = pd.DataFrame((1*"neg_pos.").split("."))[:-1]
        prime9 = pd.DataFrame(NegNames[7:8])
        target9 = pd.DataFrame(PosNames[7:8]) 
        condition = pd.DataFrame(list("6"*len(type9)))
        neg_pos = pd.concat([prime9, target9, type9, condition], axis=1, ignore_index=True)
    else:
        pass

ITI = pd.DataFrame([3.5]*12)
TotalTrialTime = pd.DataFrame([4.5]*12)

run_list = pd.concat([neut_neut, pos_pos, neg_neg, pos_neg,
                      neg_pos, neut_pos, pos_neut, neg_neut, 
                      neut_neg], axis=0, ignore_index=True)
run_list = pd.concat([run_list, ITI, TotalTrialTime], axis =1, ignore_index=True)
run_list.columns = ["Prime","Target","Type","Condition","ITI","TotalTrialTime"] 



run_list = run_list.sample(frac=1).reset_index(drop=True)
run_list.to_csv("prac_stimuli.csv", index=False)







