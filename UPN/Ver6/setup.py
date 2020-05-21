# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 17:25:03 2016

@author: Daniel
"""

from __future__ import division
import os, random
import pandas as pd
import numpy as np
#from stat_formulas import *

nRuns = 6
pairs = 324
Types = 9
nConditions = 4

cwd = os.path.dirname(__file__)
base_dir = os.path.dirname(cwd)

os.chdir(base_dir)

NegNames = [base_dir +"/NegativePics_216/" + str(x) for x in os.listdir(os.path.join(base_dir + "/NegativePics_216/"))[:-1]]
PosNames = [base_dir +"/PositivePics_216/" + str(x) for x in os.listdir(os.path.join(base_dir + "/PositivePics_216/"))[:-1]]
NeutNames = [base_dir +"/NeutralPics_216/" + str(x) for x in os.listdir(os.path.join(base_dir + "/NeutralPics_216/"))[:-1]]

random.shuffle(NeutNames)
random.shuffle(PosNames)
random.shuffle(NegNames)

df = pd.concat([pd.DataFrame(NegNames), pd.DataFrame(PosNames), pd.DataFrame(NeutNames)],
            axis=1, ignore_index=True).sample(frac=1).reset_index(drop=True)
df.columns = ["Negative","Positive","Neutral"]

for i in xrange(1, Types+1):
    if i == 1:
        type1 = pd.DataFrame((54*"neut_neut.").split("."))[:-1]
        prime1 = pd.DataFrame(NeutNames[0:54])
        target1 = pd.DataFrame(NeutNames[54:108])
        condition = pd.DataFrame(list("1"*len(type1)))
        neut_neut = pd.concat([prime1, target1, type1, condition], axis=1, ignore_index=True)
    elif i == 2:
        type2 = pd.DataFrame((54*"pos_pos.").split("."))[:-1]
        prime2 = pd.DataFrame(PosNames[0:54])
        target2 = pd.DataFrame(PosNames[54:108])
        condition = pd.DataFrame(list("2"*len(type2)))
        pos_pos = pd.concat([prime2, target2, type2, condition], axis=1, ignore_index=True)
    elif i == 3:
        type3 = pd.DataFrame((54*"neg_neg.").split("."))[:-1]  
        prime3 = pd.DataFrame(NegNames[0:54])
        target3 = pd.DataFrame(NegNames[54:108])
        condition = pd.DataFrame(list("3"*len(type3)))
        neg_neg = pd.concat([prime3, target3, type3, condition], axis=1, ignore_index=True)
    elif i == 4:
        type4 = pd.DataFrame((27*"neut_pos.").split("."))[:-1]
        prime4 = pd.DataFrame(NeutNames[108:135])
        target4 = pd.DataFrame(PosNames[108:135])
        condition = pd.DataFrame(list("4"*len(type4)))
        neut_pos = pd.concat([prime4, target4, type4, condition], axis=1, ignore_index=True)
    elif i == 5:
        type5 = pd.DataFrame((27*"pos_neut.").split("."))[:-1]   
        prime5 = pd.DataFrame(PosNames[135:162])
        target5 = pd.DataFrame(NeutNames[135:162])
        condition = pd.DataFrame(list("4"*len(type5)))
        pos_neut = pd.concat([prime5, target5, type5, condition], axis=1, ignore_index=True)
    elif i == 6:
        type6 = pd.DataFrame((27*"neut_neg.").split("."))[:-1]
        prime6 = pd.DataFrame(NeutNames[162:189])
        target6 = pd.DataFrame(NegNames[108:135])
        condition = pd.DataFrame(list("5"*len(type6)))
        neut_neg = pd.concat([prime6, target6, type6, condition], axis=1, ignore_index=True)
    elif i == 7:
        type7 = pd.DataFrame((27*"neg_neut.").split("."))[:-1]  
        prime7 = pd.DataFrame(NegNames[135:162])
        target7 = pd.DataFrame(NeutNames[189:216])
        condition = pd.DataFrame(list("5"*len(type7)))
        neg_neut = pd.concat([prime7, target7, type7, condition], axis=1, ignore_index=True)
    elif i == 8:
        type8 = pd.DataFrame((27*"pos_neg.").split("."))[:-1]  
        prime8 = pd.DataFrame(PosNames[162:189])
        target8 = pd.DataFrame(NegNames[162:189]) 
        condition = pd.DataFrame(list("6"*len(type8)))
        pos_neg = pd.concat([prime8, target8, type8, condition], axis=1, ignore_index=True)
    elif i == 9:
        type9 = pd.DataFrame((27*"neg_pos.").split("."))[:-1]
        prime9 = pd.DataFrame(NegNames[189:216])
        target9 = pd.DataFrame(PosNames[189:216]) 
        condition = pd.DataFrame(list("6"*len(type9)))
        neg_pos = pd.concat([prime9, target9, type9, condition], axis=1, ignore_index=True)
    else:
        pass
    
"""run1_list"""
run1_list = pd.concat([neut_neut[0:9], pos_pos[0:9], neg_neg[0:9], pos_neg[0:5],
                      neg_pos[0:4], neut_pos[0:5], pos_neut[0:4], neg_neut[0:5], 
                      neut_neg[0:4]], axis=0, ignore_index=True)
run1_list.columns = ["Prime","Target","Type","Condition"] 
                     
neut_neut = neut_neut.drop(neut_neut.head(9).index)
pos_pos = pos_pos.drop(pos_pos.head(9).index)
neg_neg = neg_neg.drop(neg_neg.head(9).index)
pos_neg = pos_neg.drop(pos_neg.head(5).index)
neg_pos = neg_pos.drop(neg_pos.head(4).index)
neut_pos = neut_pos.drop(neut_pos.head(5).index)
pos_neut = pos_neut.drop(pos_neut.head(4).index)
neg_neut = neg_neut.drop(neg_neut.head(5).index)
neut_neg = neut_neg.drop(neut_neg.head(4).index)

"""run2_list"""
run2_list = pd.concat([neut_neut[0:9], pos_pos[0:9], neg_neg[0:9], pos_neg[0:4],
                      neg_pos[0:5], neut_pos[0:4], pos_neut[0:5], neg_neut[0:4], 
                      neut_neg[0:5]], axis=0, ignore_index=True)
run2_list.columns = ["Prime","Target","Type","Condition"] 
                    
neut_neut = neut_neut.drop(neut_neut.head(9).index)
pos_pos = pos_pos.drop(pos_pos.head(9).index)
neg_neg = neg_neg.drop(neg_neg.head(9).index)
pos_neg = pos_neg.drop(pos_neg.head(4).index)
neg_pos = neg_pos.drop(neg_pos.head(5).index)
neut_pos = neut_pos.drop(neut_pos.head(4).index)
pos_neut = pos_neut.drop(pos_neut.head(5).index)
neg_neut = neg_neut.drop(neg_neut.head(4).index)
neut_neg = neut_neg.drop(neut_neg.head(5).index)

"""run3_list"""
run3_list = pd.concat([neut_neut[0:9], pos_pos[0:9], neg_neg[0:9], pos_neg[0:5],
                      neg_pos[0:4], neut_pos[0:5], pos_neut[0:4], neg_neut[0:5], 
                      neut_neg[0:4]], axis=0, ignore_index=True)
run3_list.columns = ["Prime","Target","Type","Condition"] 
                      
neut_neut = neut_neut.drop(neut_neut.head(9).index)
pos_pos = pos_pos.drop(pos_pos.head(9).index)
neg_neg = neg_neg.drop(neg_neg.head(9).index)
pos_neg = pos_neg.drop(pos_neg.head(5).index)
neg_pos = neg_pos.drop(neg_pos.head(4).index)
neut_pos = neut_pos.drop(neut_pos.head(5).index)
pos_neut = pos_neut.drop(pos_neut.head(4).index)
neg_neut = neg_neut.drop(neg_neut.head(5).index)
neut_neg = neut_neg.drop(neut_neg.head(4).index)

"""run4_list"""
run4_list = pd.concat([neut_neut[0:9], pos_pos[0:9], neg_neg[0:9], pos_neg[0:4],
                      neg_pos[0:5], neut_pos[0:4], pos_neut[0:5], neg_neut[0:4], 
                      neut_neg[0:5]], axis=0, ignore_index=True)
run4_list.columns = ["Prime","Target","Type","Condition"] 
                      
neut_neut = neut_neut.drop(neut_neut.head(9).index)
pos_pos = pos_pos.drop(pos_pos.head(9).index)
neg_neg = neg_neg.drop(neg_neg.head(9).index)
pos_neg = pos_neg.drop(pos_neg.head(4).index)
neg_pos = neg_pos.drop(neg_pos.head(5).index)
neut_pos = neut_pos.drop(neut_pos.head(4).index)
pos_neut = pos_neut.drop(pos_neut.head(5).index)
neg_neut = neg_neut.drop(neg_neut.head(4).index)
neut_neg = neut_neg.drop(neut_neg.head(5).index)

"""run5_list"""
run5_list = pd.concat([neut_neut[0:9], pos_pos[0:9], neg_neg[0:9], pos_neg[0:5],
                      neg_pos[0:4], neut_pos[0:5], pos_neut[0:4], neg_neut[0:5], 
                      neut_neg[0:4]], axis=0, ignore_index=True)
run5_list.columns = ["Prime","Target","Type","Condition"] 
                      
neut_neut = neut_neut.drop(neut_neut.head(9).index)
pos_pos = pos_pos.drop(pos_pos.head(9).index)
neg_neg = neg_neg.drop(neg_neg.head(9).index)
pos_neg = pos_neg.drop(pos_neg.head(5).index)
neg_pos = neg_pos.drop(neg_pos.head(4).index)
neut_pos = neut_pos.drop(neut_pos.head(5).index)
pos_neut = pos_neut.drop(pos_neut.head(4).index)
neg_neut = neg_neut.drop(neg_neut.head(5).index)
neut_neg = neut_neg.drop(neut_neg.head(4).index)

"""run6_list"""
run6_list = pd.concat([neut_neut[0:9], pos_pos[0:9], neg_neg[0:9], pos_neg[0:4],
                      neg_pos[0:5], neut_pos[0:4], pos_neut[0:5], neg_neut[0:4], 
                      neut_neg[0:5]], axis=0, ignore_index=True)
run6_list.columns = ["Prime","Target","Type","Condition"] 
                      
neut_neut = neut_neut.drop(neut_neut.head(9).index)
pos_pos = pos_pos.drop(pos_pos.head(9).index)
neg_neg = neg_neg.drop(neg_neg.head(9).index)
pos_neg = pos_neg.drop(pos_neg.head(4).index)
neg_pos = neg_pos.drop(neg_pos.head(5).index)
neut_pos = neut_pos.drop(neut_pos.head(4).index)
pos_neut = pos_neut.drop(pos_neut.head(5).index)
neg_neut = neg_neut.drop(neg_neut.head(4).index)
neut_neg = neut_neg.drop(neut_neg.head(5).index)


def triplet_checker(run):
    run.index = range(len(run))
    ind = list(range(len(run)))
    shuffled = []
    pick = random.sample(ind,2)
    shuffled += pick
    ind.remove(pick[0])
    ind.remove(pick[1])
    last2_same = run['Condition'].values[pick[0]] == run['Condition'].values[pick[1]]
    last_cond = run['Condition'].values[pick[1]]
    while len(ind):
        if last2_same:
            ind_last_cond = set(run[run['Condition'] == last_cond].index.tolist())
            ind_no_last_cond = set(ind) - ind_last_cond
            pick = list(random.sample(ind_no_last_cond,1))
            shuffled += pick
            ind.remove(pick[0])  
            last_cond = run['Condition'].values[pick[0]]
            last2_same = False
        else:
            pick = random.sample(ind,1)
            shuffled += pick
            ind.remove(pick[0])
            last2_same = run['Condition'].values[pick[0]] == last_cond
            last_cond = run['Condition'].values[pick[0]]
    
    return run.ix[shuffled, :]
    
run1 = triplet_checker(run1_list)  
run2 = triplet_checker(run2_list) 
run3 = triplet_checker(run3_list) 
run4 = triplet_checker(run4_list) 
run5 = triplet_checker(run5_list) 
run6 = triplet_checker(run6_list)   

stim_df = pd.concat([run1, run2, run3, run4, run5, run6], axis=0, ignore_index=True)
stim_df.to_csv("exp_stimuli.csv", index=False)

vals = stim_df['Condition'].values
triples = any([vals[i-1] == vals[i] == vals[i+1] for i in range(1, len(vals) - 1)])
print triples
     
def randomize(df):
    return df.reindex(np.random.permutation(df.index))
os.chdir(cwd)
order_file1 = pd.read_csv("ITI.csv")   
order_file2 = randomize(pd.read_csv("ITI.csv"))   
order_file3 = randomize(pd.read_csv("ITI.csv"))   
order_file4 = randomize(pd.read_csv("ITI.csv")) 
order_file5 = randomize(pd.read_csv("ITI.csv")) 
order_file6 = randomize(pd.read_csv("ITI.csv")) 

order_file = pd.concat([order_file1, order_file2, order_file3, order_file4,
            order_file5, order_file6], axis=0, ignore_index=True) + 0.440329

stim_df.index = range(len(stim_df))
ITI = order_file["ITI"]

stim_df = pd.concat([stim_df, ITI], axis=1)

TotalTrialTime = []
for i in stim_df["ITI"]:
    TotalTrialTime.append(i+1)
TotalTrialTime = pd.DataFrame(TotalTrialTime, columns=["TotalTrialTime"])

stim_df = pd.concat([stim_df, TotalTrialTime], axis=1)

stim_df.to_csv("exp_stimuli.csv", index=False)
























