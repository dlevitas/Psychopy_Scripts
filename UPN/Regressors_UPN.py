# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 12:56:03 2016

@author: Daniel

UPN Regressor Timing Files
"""
from __future__ import division
import os, re
import pandas as pd
import numpy as np

blank_array = np.empty((6,9))
blank_array[:] = np.nan
columns = [0,1,2,3,4,5,6,7,8]
index= range(6)


#########
fix_time_at_start = 6.6
#########

cwd = os.path.dirname(__file__)
expected_data = ['Run1.csv','Run2.csv','Run3.csv','Run4.csv','Run5.csv','Run6.csv']

if not os.path.isdir("Timing_Files"):
    os.mkdir("Timing_Files")
else:
    pass

for v in ['ver1', 'ver2', 'ver3', 'ver4', 'ver5', 'ver6', 'ver7', 'ver8']:
    new_dir = os.path.dirname(os.path.join(cwd + "/" + v + "/Data/"))
    subj_IDs = os.listdir(os.path.join(cwd + "/" + v + "/Data/"))
    for s in subj_IDs:
        os.chdir(os.path.join(new_dir + "/" + s + "/"))
        runs = [f for f in os.listdir(os.path.join(new_dir + "/" + s + "/")) if re.findall(r'Run\d+', f)]
        missing = [x for x in expected_data if x not in runs]

        if len(missing):
            print "Subject %s is missing %s" %(str(s), ','.join(missing))
            if 'Run1.csv' in runs:
                run1 = pd.read_csv('Run1.csv')
            else:
                run1 = pd.DataFrame()
            if 'Run2.csv' in runs:
                run2 = pd.read_csv('Run2.csv')
            else:
                run2 = pd.DataFrame()
            if 'Run3.csv' in runs:
                run3 = pd.read_csv('Run3.csv')
            else:
                run3 = pd.DataFrame()
            if 'Run4.csv' in runs:
                run4 = pd.read_csv('Run4.csv')
            else:
                run4 = pd.DataFrame()
            if 'Run5.csv' in runs:
                run5 = pd.read_csv('Run5.csv')
            else:
                run5 = pd.DataFrame()
            if 'Run6.csv' in runs:
                run6 = pd.read_csv('Run6.csv')
            else:
                run6 = pd.DataFrame()
                
        else:
            print "Subject %s is not missing any runs" %str(s)
            run1,run2,run3,run4,run5,run6 = [pd.read_csv(x) for x in runs]
            
        #Check for missing trials in each run   
        if len(run1) != 54 and len(run1) != 0:
            print "Subject %s is missing %s trial(s) in Run4" %(s, 54-len(run1))
        if len(run2) != 54 and len(run2) != 0:
            print "Subject %s is missing %s trial(s) in Run4" %(s, 54-len(run2))
        if len(run3) != 54 and len(run3) != 0:
            print "Subject %s is missing %s trial(s) in Run4" %(s, 54-len(run3))
        if len(run4) != 54 and len(run4) != 0:
            print "Subject %s is missing %s trial(s) in Run4" %(s, 54-len(run4)) 
        if len(run5) != 54 and len(run5) != 0:
            print "Subject %s is missing %s trial(s) in Run4" %(s, 54-len(run5))
        if len(run6) != 54 and len(run6) != 0:
            print "Subject %s is missing %s trial(s) in Run4" %(s, 54-len(run6)) 
        
        con1_1, con2_1, con3_1, con4_1, con5_1, con6_1 = [[], [], [], [], [], []]
        con1_2, con2_2, con3_2, con4_2, con5_2, con6_2 = [[], [], [], [], [], []]
        con1_3, con2_3, con3_3, con4_3, con5_3, con6_3 = [[], [], [], [], [], []]
        con1_4, con2_4, con3_4, con4_4, con5_4, con6_4 = [[], [], [], [], [], []]
        con1_5, con2_5, con3_5, con4_5, con5_5, con6_5 = [[], [], [], [], [], []]
        con1_6, con2_6, con3_6, con4_6, con5_6, con6_6 = [[], [], [], [], [], []]
        
        for k in run1.index:
            if run1.Condition[k] == 1:
                con1_1.append(run1["Cumulative Trial Start"][k] - fix_time_at_start + run1["Fixation Time"][k])
            elif run1.Condition[k] == 2:
                con2_1.append(run1["Cumulative Trial Start"][k] - fix_time_at_start + run1["Fixation Time"][k])
            elif run1.Condition[k] == 3:
                con3_1.append(run1["Cumulative Trial Start"][k] - fix_time_at_start + run1["Fixation Time"][k])
            elif run1.Condition[k] == 4:
                con4_1.append(run1["Cumulative Trial Start"][k] - fix_time_at_start + run1["Fixation Time"][k])
            elif run1.Condition[k] == 5:
                con5_1.append(run1["Cumulative Trial Start"][k] - fix_time_at_start + run1["Fixation Time"][k])
            elif run1.Condition[k] == 6:
                con6_1.append(run1["Cumulative Trial Start"][k] - fix_time_at_start + run1["Fixation Time"][k])
            else:
                pass

        for k in run2.index:
            if run2.Condition[k] == 1:
                con1_2.append(run2["Cumulative Trial Start"][k] - fix_time_at_start + run2["Fixation Time"][k])
            elif run2.Condition[k] == 2:
                con2_2.append(run2["Cumulative Trial Start"][k] - fix_time_at_start + run2["Fixation Time"][k])
            elif run2.Condition[k] == 3:
                con3_2.append(run2["Cumulative Trial Start"][k] - fix_time_at_start + run2["Fixation Time"][k])
            elif run2.Condition[k] == 4:
                con4_2.append(run2["Cumulative Trial Start"][k] - fix_time_at_start + run2["Fixation Time"][k])
            elif run2.Condition[k] == 5:
                con5_2.append(run2["Cumulative Trial Start"][k] - fix_time_at_start + run2["Fixation Time"][k])
            elif run2.Condition[k] == 6:
                con6_2.append(run2["Cumulative Trial Start"][k] - fix_time_at_start + run2["Fixation Time"][k])
            else:
                pass

        for k in run3.index:
            if run3.Condition[k] == 1:
                con1_3.append(run3["Cumulative Trial Start"][k] - fix_time_at_start + run3["Fixation Time"][k])
            elif run3.Condition[k] == 2:
                con2_3.append(run3["Cumulative Trial Start"][k] - fix_time_at_start + run3["Fixation Time"][k])
            elif run3.Condition[k] == 3:
                con3_3.append(run3["Cumulative Trial Start"][k] - fix_time_at_start + run3["Fixation Time"][k])
            elif run3.Condition[k] == 4:
                con4_3.append(run3["Cumulative Trial Start"][k] - fix_time_at_start + run3["Fixation Time"][k])
            elif run3.Condition[k] == 5:
                con5_3.append(run3["Cumulative Trial Start"][k] - fix_time_at_start + run3["Fixation Time"][k])
            elif run3.Condition[k] == 6:
                con6_3.append(run3["Cumulative Trial Start"][k] - fix_time_at_start + run3["Fixation Time"][k])
            else:
                pass

        for k in run4.index:
            if run4.Condition[k] == 1:
                con1_4.append(run4["Cumulative Trial Start"][k] - fix_time_at_start + run4["Fixation Time"][k])
            elif run4.Condition[k] == 2:
                con2_4.append(run4["Cumulative Trial Start"][k] - fix_time_at_start + run4["Fixation Time"][k])
            elif run4.Condition[k] == 3:
                con3_4.append(run4["Cumulative Trial Start"][k] - fix_time_at_start + run4["Fixation Time"][k])
            elif run4.Condition[k] == 4:
                con4_4.append(run4["Cumulative Trial Start"][k] - fix_time_at_start + run4["Fixation Time"][k])
            elif run4.Condition[k] == 5:
                con5_4.append(run4["Cumulative Trial Start"][k] - fix_time_at_start + run4["Fixation Time"][k])
            elif run4.Condition[k] == 6:
                con6_4.append(run4["Cumulative Trial Start"][k] - fix_time_at_start + run4["Fixation Time"][k])
            else:
                pass

        for k in run5.index:
            if run5.Condition[k] == 1:
                con1_5.append(run5["Cumulative Trial Start"][k] - fix_time_at_start + run5["Fixation Time"][k])
            elif run5.Condition[k] == 2:
                con2_5.append(run5["Cumulative Trial Start"][k] - fix_time_at_start + run5["Fixation Time"][k])
            elif run5.Condition[k] == 3:
                con3_5.append(run5["Cumulative Trial Start"][k] - fix_time_at_start + run5["Fixation Time"][k])
            elif run5.Condition[k] == 4:
                con4_5.append(run5["Cumulative Trial Start"][k] - fix_time_at_start + run5["Fixation Time"][k])
            elif run5.Condition[k] == 5:
                con5_5.append(run5["Cumulative Trial Start"][k] - fix_time_at_start + run5["Fixation Time"][k])
            elif run5.Condition[k] == 6:
                con6_5.append(run5["Cumulative Trial Start"][k] - fix_time_at_start + run5["Fixation Time"][k])
            else:
                pass

        for k in run6.index:
            if run6.Condition[k] == 1:
                con1_6.append(run6["Cumulative Trial Start"][k] - fix_time_at_start + run6["Fixation Time"][k])
            elif run6.Condition[k] == 2:
                con2_6.append(run6["Cumulative Trial Start"][k] - fix_time_at_start + run6["Fixation Time"][k])
            elif run6.Condition[k] == 3:
                con3_6.append(run6["Cumulative Trial Start"][k] - fix_time_at_start + run6["Fixation Time"][k])
            elif run6.Condition[k] == 4:
                con4_6.append(run6["Cumulative Trial Start"][k] - fix_time_at_start + run6["Fixation Time"][k])
            elif run6.Condition[k] == 5:
                con5_6.append(run6["Cumulative Trial Start"][k] - fix_time_at_start + run6["Fixation Time"][k])
            elif run6.Condition[k] == 6:
                con6_6.append(run6["Cumulative Trial Start"][k] - fix_time_at_start + run6["Fixation Time"][k])
            else:
                pass       
            
        total_con1_onset = []
        total_con2_onset = []
        total_con3_onset = []
        total_con4_onset = []
        total_con5_onset = []
        total_con6_onset = []
        
        for j in (con1_1, con1_2, con1_3, con1_4, con1_5, con1_6):
            total_con1_onset.append(j)
        for j in (con2_1, con2_2, con2_3, con2_4, con2_5, con2_6):
            total_con2_onset.append(j)
        for j in (con3_1, con3_2, con3_3, con3_4, con3_5, con3_6):
            total_con3_onset.append(j)
        for j in (con4_1, con4_2, con4_3, con4_4, con4_5, con4_6):
            total_con4_onset.append(j)
        for j in (con5_1, con5_2, con5_3, con5_4, con5_5, con5_6):
            total_con5_onset.append(j)
        for j in (con6_1, con6_2, con6_3, con6_4, con6_5, con6_6):
            total_con6_onset.append(j)
        
        total_con1_onset = pd.DataFrame(total_con1_onset)
        total_con2_onset = pd.DataFrame(total_con2_onset)
        total_con3_onset = pd.DataFrame(total_con3_onset)
        total_con4_onset = pd.DataFrame(total_con4_onset)
        total_con5_onset = pd.DataFrame(total_con5_onset)
        total_con6_onset = pd.DataFrame(total_con6_onset)
        
        #Go to Timing_Files directory and put data there
        os.chdir(os.path.join(cwd + "/Timing_Files/"))
        if not os.path.isdir(s):
            os.mkdir(s)
        else:
            pass
        os.chdir(os.path.join(cwd + "/Timing_Files/" + s + "/"))
        
        '''
        total_con1_onset.to_csv('NN.csv', index=False, header=False)
        total_con2_onset.to_csv('PP.csv', index=False, header=False)
        total_con3_onset.to_csv('UU.csv', index=False, header=False)
        total_con4_onset.to_csv('NP_PN.csv', index=False, header=False)
        total_con5_onset.to_csv('NU_UN.csv', index=False, header=False)
        total_con6_onset.to_csv('PU_UP.csv', index=False, header=False)
        '''
        np.savetxt("NN.txt", total_con1_onset.values, fmt='%s')
        np.savetxt("PP.txt", total_con2_onset.values, fmt='%s')
        np.savetxt("UU.txt", total_con3_onset.values, fmt='%s')
        np.savetxt("NP_PN.txt", total_con4_onset.values, fmt='%s')
        np.savetxt("NU_UN.txt", total_con5_onset.values, fmt='%s')
        np.savetxt("PU_UP.txt", total_con6_onset.values, fmt='%s')

    
    
        
        

            
            
            
            
            
            
            
            
            
            
    

