# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 17:28:08 2017

Controllability Predictable Unpredictable (CPU) Analysis
"""

from __future__ import division
import pandas as pd
import os

cwd = os.path.dirname(__file__)
expected_data = [0,1,2,3,4]
output_list = []
header = ['Subject', 'Avg Predictable Anxiety','Avg Unpredictable Anxiety', 
          'Avg Predictable Perceived Control','Avg Unpredictable Perceived Control']

def ratingData(cond) :
    if cond == 'Control':
        data_dir = os.path.join(cwd + '/Data/Control/')
    elif cond == 'Uncontrol':
        data_dir = os.path.join(cwd + '/Data/Uncontrol/')
    else:
        raise ValueError('Please select a proper condition: Control or Uncontrol')
        
    for i in os.listdir(data_dir):
        i = str(i)
        expected_data = [i+'_'+ str(x) + '.csv' for x in xrange(5)]
        
        subj_data = [str(x) for x in os.listdir(os.path.join(data_dir + i))]
        missing_data = [x for x in expected_data if x not in subj_data]
        
        if len(missing_data):
            print "Subject %s missing runs: %s" %(i, ','.join(missing_data))
        else:
            print "Subject %s missing runs: None" %i
            
        if i+'_1.csv' in subj_data:
            run1 = pd.read_csv(os.path.join(data_dir + i + '/' + expected_data[1]))
        else:
            run1 = pd.DataFrame()
        
        if i+'_2.csv' in subj_data:
            run2 = pd.read_csv(os.path.join(data_dir + i + '/' + expected_data[2]))
        else:
            run2 = pd.DataFrame()
    
        if i+'_3.csv' in subj_data:
            run3 = pd.read_csv(os.path.join(data_dir + i + '/' + expected_data[3]))
        else:
            run3 = pd.DataFrame()
            
        if i+'_4.csv' in subj_data:
            run4 = pd.read_csv(os.path.join(data_dir + i + '/' + expected_data[4]))
        else:
            run4 = pd.DataFrame()
            
        data = pd.concat([run1, run2, run3, run4], axis=0, ignore_index=True)
        
        P_data = data[data['Threat_Predictability'] == 'P']
        U_data = data[data['Threat_Predictability'] == 'U']
        
        Avg_P_Anxiety = round(P_data['Anxiety_Rating'].mean(),2)
        Avg_U_Anxiety = round(U_data['Anxiety_Rating'].mean(),2)
        
        Avg_P_Control = round(P_data['Perceived_Control_Rating'].mean(),2)
        Avg_U_Control = round(U_data['Perceived_Control_Rating'].mean(),2)
     
        output_list.append([i, Avg_P_Anxiety, Avg_U_Anxiety, Avg_P_Control, Avg_U_Control])
        fid = pd.DataFrame(output_list, columns=header)
        
        if cond == 'Control':
            fid.to_csv('Control Behavioral Ratings.csv', header=True, index=False)
        elif cond == 'Uncontrol':
            fid.to_csv('Uncontrol Behavioral Ratings.csv', header=True, index=False)
        else:
            raise ValueError('Please select a proper condition: Control or Uncontrol')
    
ratingData('Control') 
print "" 
ratingData('Uncontrol')  
