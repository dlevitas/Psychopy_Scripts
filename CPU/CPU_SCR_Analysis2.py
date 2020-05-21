# -*- coding: utf-8 -*-
"""
Created on Thu Apr 20 10:23:10 2017

@author: Daniel
CPU SCR Analysis
"""

from __future__ import division
import matplotlib.pyplot as plt
import scipy.io as sio
import pandas as pd
import os

cwd = os.path.dirname(__file__)
rate = 250
delay = 2
window = 12
pre = 3

all_P, all_U, all_P_regress, all_U_regress = [pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()]

for i in os.listdir(os.path.join(cwd + '/SCR/')):
    i = str(i)
    print i
    
    if i in [str(x)+'.mat' for x in os.listdir(os.path.join(cwd + '/Data/Control/'))]:
        timing_dir = os.path.join(cwd + '/Data/Control/')
    elif i in [str(x)+'.mat' for x in os.listdir(os.path.join(cwd + '/Data/Uncontrol/'))]:
        timing_dir = os.path.join(cwd + '/Data/Uncontrol/')
    else:
        raise ValueError('Data timing files are in an inproper folder')
        
    """Not sure if this if-else statement is needed"""
    if int(i[4:7]) % 2:
        predict_order = ['U','P']
    else:
        predict_order = ['P','U']
    
    data = pd.DataFrame(sio.loadmat(os.path.join(cwd + '/SCR/' + i)).values()[7]) 
    data.columns  = ['0','1','2','3','4','5','6','7','8','9']
    data = data[[0, 9]]
    index = pd.DataFrame(range(len(data)))
    data = pd.concat([index, data], axis=1)
    data.columns = ['SCR_Index','GSR','Event']
    
    codes = data.Event.unique()
    start_code = sorted(data.Event.unique())[1] #2nd number because the baseline is 0
    end_code = sorted(data.Event.unique())[-2] #2nd to last number because the shock level is 64
    
    start_exp = int(data.ix[data["Event"] == start_code][-1:].iloc[0][0])
    end_exp = int(data.ix[data["Event"] == end_code].iloc[0][0])
    
    data = data.ix[start_exp:end_exp]
    
    if 2 in codes:
        run1 = data.ix[int(data.ix[data["Event"] == 2][-1:].iloc[0][0]) + 1:int(data.ix[data["Event"] == 12].iloc[0][0]) - 1]
        run1 = run1.iloc[::rate,:].reset_index(drop=True)
        run1 = pd.concat([run1, pd.DataFrame(range(len(run1)))], axis=1)
        run1.columns = ['SCR_Index','GSR','Event', 'Timing_Index']
        run1_timing = pd.read_csv(os.path.join(timing_dir + i[:-4] + '/' + i[:-4]+'_1.csv'))
        
        run1_stress_onsets = eval(run1_timing['Stressor_Onset_Times'].dropna()[0]) + list(run1_timing['Cumulative_Start_Time'][2] + eval(run1_timing['Stressor_Onset_Times'].dropna()[2])) + list(run1_timing['Cumulative_Start_Time'][4] + eval(run1_timing['Stressor_Onset_Times'].dropna()[4]))
        
        run1_P, run1_U, run1_P_regress, run1_U_regress = [[], [], [], []]
        if run1_timing['Threat_Predictability'][0] == 'U':
            for x in range(len(run1_stress_onsets)):
                run1_U.append(run1[int(round(run1_stress_onsets[x],0)):int(round(run1_stress_onsets[x],0) + window)])
            
            run1_U = pd.concat([run1_U[0], run1_U[1], run1_U[2], run1_U[3], run1_U[4], run1_U[5]], axis=0, ignore_index=True)
            run1_U_regress = run1[~run1.Timing_Index.isin(run1_U.Timing_Index)]
            run1_P, run1_P_regress = [pd.DataFrame(), pd.DataFrame()]
        else:
            for x in range(len(run1_stress_onsets)):
                run1_P.append(run1[int(round(run1_stress_onsets[x],0)):int(round(run1_stress_onsets[x],0) + window)])
                run1_P_regress.append(run1[int(round(run1_stress_onsets[x]-pre,0)):int(round(run1_stress_onsets[x],0) + window)])
            
            run1_P = pd.concat([run1_P[0], run1_P[1], run1_P[2], run1_P[3], run1_P[4], run1_P[5]], axis=0, ignore_index=True)
            run1_P_regress = pd.concat([run1_P_regress[0], run1_P_regress[1], run1_P_regress[2], run1_P_regress[3], run1_P_regress[4], run1_P_regress[5]], axis=0, ignore_index=True)
            run1_P_regress = run1[~run1.Timing_Index.isin(run1_P.Timing_Index)]            
            run1_U, run1_U_regress = [pd.DataFrame(), pd.DataFrame()]
    else:
        print "Subject %s is missing SCR data for run 1" %(i[:-4])
        run1_P, run1_U, run1_P_regress, run1_U_regress = [pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()]
    
    if 3 in codes:
        run2 = data.ix[int(data.ix[data["Event"] == 3][-1:].iloc[0][0]) + 1:int(data.ix[data["Event"] == 13].iloc[0][0]) - 1]
        run2 = run2.iloc[::rate,:].reset_index(drop=True)
        run2 = pd.concat([run2, pd.DataFrame(range(len(run2)))], axis=1)
        run2.columns = ['SCR_Index','GSR','Event', 'Timing_Index']
        run2_timing = pd.read_csv(os.path.join(timing_dir + i[:-4] + '/' + i[:-4]+'_2.csv'))
        
        run2_stress_onsets = list(run2_timing['Cumulative_Start_Time'][1] + eval(run2_timing['Stressor_Onset_Times'].dropna()[1])) + list(run2_timing['Cumulative_Start_Time'][3] + eval(run2_timing['Stressor_Onset_Times'].dropna()[3])) + list(run2_timing['Cumulative_Start_Time'][5] + eval(run2_timing['Stressor_Onset_Times'].dropna()[5]))
        
        run2_P, run2_U, run2_P_regress, run2_U_regress = [[], [], [], []]
        if run2_timing['Threat_Predictability'][1] == 'U':
            for x in range(len(run2_stress_onsets)):
                run2_U.append(run2[int(round(run2_stress_onsets[x],0)):int(round(run2_stress_onsets[x],0) + window)])
            
            run2_U = pd.concat([run2_U[0], run2_U[1], run2_U[2], run2_U[3]], axis=0, ignore_index=True)
            run2_U_regress = run2[~run2.Timing_Index.isin(run2_U.Timing_Index)]
            run2_P, run2_P_regress = [pd.DataFrame(), pd.DataFrame()]
        else:
            for x in range(len(run2_stress_onsets)):
                run2_P.append(run2[int(round(run2_stress_onsets[x],0)):int(round(run2_stress_onsets[x],0) + window)])
                run2_P_regress.append(run2[int(round(run2_stress_onsets[x]-pre,0)):int(round(run2_stress_onsets[x],0) + window)])
            
            run2_P = pd.concat([run2_P[0], run2_P[1], run2_P[2], run2_P[3]], axis=0, ignore_index=True)
            run2_P_regress = pd.concat([run2_P_regress[0], run2_P_regress[1], run2_P_regress[2], run2_P_regress[3]], axis=0, ignore_index=True)
            run2_P_regress = run2[~run2.Timing_Index.isin(run2_P.Timing_Index)]            
            run2_U, run2_U_regress = [pd.DataFrame(), pd.DataFrame()]
                    
    else:
        print "Subject %s is missing SCR data for run 2" %i[:-4]
        run2_P, run2_U, run2_P_regress, run2_U_regress = [pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()]
        
    if 4 in codes:
        run3 = data.ix[int(data.ix[data["Event"] == 4][-1:].iloc[0][0]) + 1:int(data.ix[data["Event"] == 14].iloc[0][0]) - 1]
        run3 = run3.iloc[::rate,:].reset_index(drop=True)
        run3 = pd.concat([run3, pd.DataFrame(range(len(run3)))], axis=1)
        run3.columns = ['SCR_Index','GSR','Event', 'Timing_Index']
        run3_timing = pd.read_csv(os.path.join(timing_dir + i[:-4] + '/' + i[:-4]+'_3.csv'))
        
        run3_stress_onsets = list(run3_timing['Cumulative_Start_Time'][1] + eval(run3_timing['Stressor_Onset_Times'].dropna()[1])) + list(run3_timing['Cumulative_Start_Time'][3] + eval(run3_timing['Stressor_Onset_Times'].dropna()[3])) + list(run3_timing['Cumulative_Start_Time'][5] + eval(run3_timing['Stressor_Onset_Times'].dropna()[5]))

        run3_P, run3_U, run3_P_regress, run3_U_regress = [[], [], [], []]
        if run3_timing['Threat_Predictability'][1] == 'U':
            for x in range(len(run3_stress_onsets)):
                run3_U.append(run3[int(round(run3_stress_onsets[x],0)):int(round(run3_stress_onsets[x],0) + window)])
            
            run3_U = pd.concat([run3_U[0], run3_U[1], run3_U[2], run3_U[3]], axis=0, ignore_index=True)
            run3_U_regress = run3[~run3.Timing_Index.isin(run3_U.Timing_Index)]
            run3_P, run3_P_regress = [pd.DataFrame(), pd.DataFrame()]
        else:
            for x in range(len(run3_stress_onsets)):
                run3_P.append(run3[int(round(run3_stress_onsets[x],0)):int(round(run3_stress_onsets[x],0) + window)])
                run3_P_regress.append(run3[int(round(run3_stress_onsets[x]-pre,0)):int(round(run3_stress_onsets[x],0) + window)])

            run3_P = pd.concat([run3_P[0], run3_P[1], run3_P[2], run3_P[3]], axis=0, ignore_index=True)    
            run3_P_regress = pd.concat([run3_P_regress[0], run3_P_regress[1], run3_P_regress[2], run3_P_regress[3]], axis=0, ignore_index=True)
            run3_P_regress = run3[~run3.Timing_Index.isin(run3_P.Timing_Index)]            
            run3_U, run3_U_regress = [pd.DataFrame(), pd.DataFrame()]
        
    else:
        print "Subject %s is missing SCR data for run 3" %i[:-4]
        run3_P, run3_U, run3_P_regress, run3_U_regress = [pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()]
        
    if 5 in codes:
        run4 = data.ix[int(data.ix[data["Event"] == 5][-1:].iloc[0][0]) + 1:int(data.ix[data["Event"] == 15].iloc[0][0]) - 1]
        run4 = run4.iloc[::rate,:].reset_index(drop=True)
        run4 = pd.concat([run4, pd.DataFrame(range(len(run4)))], axis=1)
        run4.columns = ['SCR_Index','GSR','Event', 'Timing_Index']
        run4_timing = pd.read_csv(os.path.join(timing_dir + i[:-4] + '/' + i[:-4]+'_4.csv'))
        
        run4_stress_onsets = list(run4_timing['Cumulative_Start_Time'][1] + eval(run4_timing['Stressor_Onset_Times'].dropna()[1])) + list(run4_timing['Cumulative_Start_Time'][3] + eval(run4_timing['Stressor_Onset_Times'].dropna()[3])) + list(run4_timing['Cumulative_Start_Time'][5] + eval(run4_timing['Stressor_Onset_Times'].dropna()[5]))

        run4_P, run4_U, run4_P_regress, run4_U_regress = [[], [], [], []]
        if run4_timing['Threat_Predictability'][1] == 'U':
            for x in range(len(run4_stress_onsets)):
                run4_U.append(run4[int(round(run4_stress_onsets[x],0)):int(round(run4_stress_onsets[x],0) + window)])
            
            run4_U = pd.concat([run4_U[0], run4_U[1], run4_U[2], run4_U[3], run4_U[4]], axis=0, ignore_index=True)
            run4_U_regress = run4[~run4.Timing_Index.isin(run4_U.Timing_Index)]
            run4_P, run4_P_regress = [pd.DataFrame(), pd.DataFrame()]
        else:
            for x in range(len(run4_stress_onsets)):
                run4_P.append(run4[int(round(run4_stress_onsets[x],0)):int(round(run4_stress_onsets[x],0) + window)])
                run4_P_regress.append(run4[int(round(run4_stress_onsets[x]-pre,0)):int(round(run4_stress_onsets[x],0) + window)])
                
            run4_P = pd.concat([run4_P[0], run4_P[1], run4_P[2], run4_P[3], run4_P[4]], axis=0, ignore_index=True)
            run4_P_regress = pd.concat([run4_P_regress[0], run4_P_regress[1], run4_P_regress[2], run4_P_regress[3], run4_P_regress[4]], axis=0, ignore_index=True)
            run4_P_regress = run4[~run4.Timing_Index.isin(run4_P.Timing_Index)]            
            run4_U, run4_U_regress = [pd.DataFrame(), pd.DataFrame()]
        
    else:
        print "Subject %s is missing SCR data for run 4" %i[:-4] 
        run4_P, run4_U, run4_P_regress, run4_U_regress = [pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()]

    
    subj_P = pd.concat([run1_P, run2_P, run3_P, run4_P], axis=0, ignore_index=True)
    subj_U = pd.concat([run1_U, run2_U, run3_U, run4_U], axis=0, ignore_index=True)
    subj_P_regress = pd.concat([run1_P_regress, run2_P_regress, run3_P_regress, run4_P_regress], axis=0, ignore_index=True)
    subj_U_regress = pd.concat([run1_U_regress, run2_U_regress, run3_U_regress, run4_U_regress], axis=0, ignore_index=True)
    
    new_col_P = pd.Series(i[:-4], index=range(len(subj_P))).to_frame()
    new_col_U = pd.Series(i[:-4], index=range(len(subj_U))).to_frame()
    new_col_P_regress = pd.Series(i[:-4], index=range(len(subj_P_regress))).to_frame()
    new_col_U_regress = pd.Series(i[:-4], index=range(len(subj_U_regress))).to_frame()
    
    subj_P = pd.concat([subj_P, new_col_P], axis=1)
    subj_U = pd.concat([subj_U, new_col_U], axis=1)
    subj_P_regress = pd.concat([subj_P_regress, new_col_P_regress], axis=1)
    subj_U_regress = pd.concat([subj_U_regress, new_col_U_regress], axis=1)
    
    all_P = pd.concat([all_P, subj_P], axis=0, ignore_index=True)
    all_U = pd.concat([all_U, subj_U], axis=0, ignore_index=True)
    all_P_regress = pd.concat([all_P_regress, subj_P_regress], axis=0, ignore_index=True)
    all_U_regress = pd.concat([all_U_regress, subj_U_regress], axis=0, ignore_index=True)   
   
    if str(os.listdir(os.path.join(cwd + '/Data/Control/'))[-1]) == i[:-4]:
        final_P_list, final_U_list = [[], []]   
        for j in range(window):
            if j == 0:
                final_P_list.append(all_P.iloc[::window,:]['GSR'].mean())
                final_U_list.append(all_U.iloc[::window,:]['GSR'].mean())
            else:
                final_P_list.append(all_P[j:].iloc[::window,:]['GSR'].mean())
                final_U_list.append(all_U[j:].iloc[::window,:]['GSR'].mean())
               
    
        plt.plot(range(window), final_P_list)
        plt.axis([0,window, -1, 7])
        plt.show()            
         
        plt.plot(range(window), final_U_list)
        plt.axis([0,window, -1, 4])
        plt.legend(['Predictable','Unpredictable'])
        plt.xlabel('Time Window Point (sec)')
        plt.ylabel('Signal')
        plt.title('Avg Controllable Group SCR Signal')
        plt.show()
    
    if str(os.listdir(os.path.join(cwd + '/Data/Uncontrol/'))[-1]) == i[:-4]:
        final_P_list, final_U_list = [[], []]   
        for j in range(window):
            if j == 0:
                final_P_list.append(all_P.iloc[::window,:]['GSR'].mean())
                final_U_list.append(all_U.iloc[::window,:]['GSR'].mean())
            else:
                final_P_list.append(all_P[j:].iloc[::window,:]['GSR'].mean())
                final_U_list.append(all_U[j:].iloc[::window,:]['GSR'].mean())
               
    
        plt.plot(range(window), final_P_list)
        plt.axis([0,window, -1, 7])
        plt.show()            
         
        plt.plot(range(window), final_U_list)
        plt.axis([0,window, -1, 4])
        plt.legend(['Predictable','Unpredictable'])
        plt.xlabel('Time Window Point (sec)')
        plt.ylabel('Signal')
        plt.title('Avg Uncontrollable Group SCR Signal')
        plt.show()  


















          
            
            
            
            
            
            
            
            
            
            
            
            
            
    
    