# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 22:38:00 2016

@author: Daniel

Item Analysis for BP CMNT Sessions:

Note: This script only works with the current CMNT file structure in Dropbox. 
If for some unfathomable reason this changes, this script will be as worthless 
as my high school diploma
"""
from __future__ import division
import os, re
import pandas as pd
import numpy as np

cwd = os.path.dirname(__file__)

dataLoc = os.path.join(cwd + "/CMNT_data")

subj_ids = []
for i in os.listdir(dataLoc):
    subj_ids.append(re.findall(r'BP\d+', str(i)))
"""
The loop above locates the participant ID from the file pathway. This will only 
work if the ID does not contain a '_'. For example, BP111 is fine, but BP_111
won't be recorded. Need to make sure we do this properly in the PsychoPy script
GUI box when listing participant ID
"""

subj_ids = list(set([val for sublist in subj_ids for val in sublist]))
"""
The line above first takes a list of lists and combines them into a single list.
From there the set() function removes all duplciates but changes the variable type
to a set, so we convert it back into a list
"""

for j in subj_ids:
    if os.path.exists(os.path.join(dataLoc + "/RED_CMNT_" + j + "_Run1.csv")):
        run1 = pd.read_csv(os.path.join(dataLoc + "/RED_CMNT_" + j + "_Run1.csv"))
    else:
        run1 = None
    if os.path.exists(os.path.join(dataLoc + "/RED_CMNT_" + j + "_Run2.csv")):
        run2 = pd.read_csv(os.path.join(dataLoc + "/RED_CMNT_" + j + "_Run2.csv"))
    else:
        run2 = None
    if os.path.exists(os.path.join(dataLoc + "/RED_CMNT_" + j + "_Run3.csv")):
        run3 = pd.read_csv(os.path.join(dataLoc + "/RED_CMNT_" + j + "_Run3.csv"))
    else:
        run3 = None
    if os.path.exists(os.path.join(dataLoc + "/RED_CMNT_" + j + "_Run4.csv")):
        run4 = pd.read_csv(os.path.join(dataLoc + "/RED_CMNT_" + j + "_Run4.csv"))
    else:
        run4 = None
    for k in ["Run1","Run2","Run3","Run4"]:
        if not os.path.exists(os.path.join(dataLoc + "/RED_CMNT_" + j + "_" + k + ".csv")):
            print ("Data missing for %s, %s") %(j, k)
            
    data = pd.concat([run1, run2, run3, run4], axis=0)
    data = data.drop("Unnamed: 0", 1)
    data.index = range(len(data))    
    
    os.chdir(os.path.join(cwd + "/Item Analysis Data"))
    data.to_csv("FINAL_DATA_%s.csv" %j, header = True)
    os.chdir(cwd)
    
"""
The loop sequence above checks to make sure all runs are accounted for, and lets
us know if something is indeed missing. All existing run files are imported into 
the python environment as dataframes.
"""


os.chdir(os.path.join(cwd + "/Item Analysis Data"))
#if os.path.isfile(".LookOverData.csv"):
#    os.remove(".LookOverData.csv")

cols_to_keep = ["MentalState","Condition","Prompt","ACC","Repeats"]
df = pd.concat((pd.read_csv(i) for i in os.listdir(os.path.join(cwd + "/Item Analysis Data"))),
    ignore_index = True)

repeats = df.duplicated("Prompt")
df["Repeats"] = repeats
df = df[cols_to_keep]


#df.to_csv(".LookOverData.csv", header=True)

for i in range(120):
    if df.ix[i, 2] in str(df["Prompt"]):
        print "yes"