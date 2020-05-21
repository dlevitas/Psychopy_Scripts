# -*- coding: utf-8 -*-
"""
Created on Mon Aug 29 10:42:44 2016

@author: Daniel
PNR Behavioral Analysis
"""
from __future__ import division
import pandas as pd
import os

cwd = os.path.dirname(__file__)
header1 = ["Subject","NN Intensity Rate","PP Intensity Rate","UU Intensity Rate",
           "NP-PN Intensity Rate","NP Intensity Rate", "PN Intensity Rate",
           "NU-UN Intensity Rate", "NU Intensity Rate","UN Intensity Rate","PU-UP Intensity Rate",
           "PU Intensity Rate","UP Intensity Rate"]

header2 = ["Subject","NN Pleasantness Rate","PP Pleasantness Rate","UU Pleasantess Rate",
           "NP-PN Pleasantess Rate","NP Pleasantness Rate","PN Pleasantness Rate",
           "NU-UN Pleasantness Rate","NU Pleasantness Rate","UN Pleasantness Rate",
           "PU-UP Pleasantness Rate","PU Pleasantness Rate","UP Pleasantness Rate"]

header3 = ["Subject","NN Intensity RT","PP Intensity RT","UU Intensity RT","NP-PN Intensity RT",
           "NP Intensity RT", "PN Intensity RT","NU-UN Intensity RT", "NU Intensity RT",
           "UN Intensity RT","PU-UP Intensity RT","PU Intensity RT","UP Intensity Rate"]

header4 = ["Subject","NN Pleasantess RT","PP Pleasantness RT","UU Pleasantess RT",
           "NP-PN Pleasantess RT","NP Pleasantness RT","PN Pleasantness RT",
           "NU-UN Pleasantness RT", "NU Pleasantness RT","UN Pleasantness RT",
           "PU-UP Pleasantness RT","PU Pleasantness RT","UP Pleasantness RT"]

run_param_list1 = []
run_param_list2 = []
run_param_list3 = []
run_param_list4 = []

def Int_Rate_RT(condition, prime_pic, total):
    if condition in [1,2,3]:
        avg_rate = round(data.query('Condition == %s' %condition)["Intensity Rating"].mean(),2) 
        avg_rt = round(data.query('Condition == %s' %condition)["Intensity RT"].mean(),2) 
    elif condition in [4,5,6] and total == 'yes':
        avg_rate = round(data.query('Condition == %s' %condition)["Intensity Rating"].mean(),2) 
        avg_rt = round(data.query('Condition == %s' %condition)["Intensity RT"].mean(),2)
    elif condition in [4,5,6] and total == 'no':
        avg_rate = round(data[(data["Prime Picture"].str.contains(str(prime_pic))) 
            & (data["Condition"] == condition)]["Intensity Rating"].mean(),2)
        avg_rt = round(data[(data["Prime Picture"].str.contains(str(prime_pic))) 
            & (data["Condition"] == condition)]["Intensity RT"].mean(),2)
    else:
        raise ValueError("Parameters inproperly set. Please review")
    
    return avg_rate, avg_rt
    
def Pleasant_Rate_RT(condition, prime_pic, total):
    if condition in [1,2,3]:
        avg_rate = round(data.query('Condition == %s' %condition)["Valence Rating"].mean(),2) 
        avg_rt = round(data.query('Condition == %s' %condition)["Valence RT"].mean(),2) 
    elif condition in [4,5,6] and total == 'yes':
        avg_rate = round(data.query('Condition == %s' %condition)["Valence Rating"].mean(),2) 
        avg_rt = round(data.query('Condition == %s' %condition)["Valence RT"].mean(),2)
    elif condition in [4,5,6] and total == 'no':
        avg_rate = round(data[(data["Prime Picture"].str.contains(str(prime_pic))) 
            & (data["Condition"] == condition)]["Valence Rating"].mean(),2)
        avg_rt = round(data[(data["Prime Picture"].str.contains(str(prime_pic))) 
            & (data["Condition"] == condition)]["Valence RT"].mean(),2)
    else:
        raise ValueError("Parameters inproperly set. Please review")
    
    return avg_rate, avg_rt

expected_data = ['Run1.csv','Run2.csv','Run3.csv','Run4.csv','Run5.csv','Run6.csv']
    
for j in ['Ver1','Ver2','Ver3','Ver4','Ver5','Ver6','Ver7','Ver8']:
    subjIDs = os.listdir(os.path.join(cwd + "/" + j + "/Data/"))
    for i in subjIDs:
        i = str(i)        
        os.chdir(os.path.join(cwd + "/" + j + "/Data/" + i + "/"))
        runs = os.listdir(os.path.join(cwd + "/" + j + "/Data/" + i + "/"))
        runs = [str(x) for x in runs]
        missing = [x for x in expected_data if x not in runs]
        
        if len(missing):
            print "Missing %s for participant %s" %(','.join(missing), i)
        else:
            print "No missing data for participant %s" %i
            
        if "Run1.csv" in runs:
            run1 = pd.read_csv("Run1.csv")
        else:
            run1 = pd.DataFrame()
        if "Run2.csv" in runs:
            run2 = pd.read_csv("Run2.csv")
        else:
            run2 = pd.DataFrame()
        if "Run3.csv" in runs:
            run3 = pd.read_csv("Run3.csv")
        else:
            run3 = pd.DataFrame()            
        if "Run4.csv" in runs:
            run4 = pd.read_csv("Run4.csv")
        else:
            run4 = pd.DataFrame()        
        if "Run5.csv" in runs:
            run5 = pd.read_csv("Run5.csv")
        else:
            run5 = pd.DataFrame()        
        if "Run6.csv" in runs:
            run6 = pd.read_csv("Run6.csv")
        else:
            run6 = pd.DataFrame()     
            
        data = pd.concat([run1, run2, run3, run4, run5, run6], axis=0, ignore_index=True)
        del data["Unnamed: 0"]
            
        #Intensity Ratings and Reaction Times:
        NN_intensity_rate, NN_intensity_rt = Int_Rate_RT(1, "", "")
        PP_intensity_rate, PP_intensity_rt = Int_Rate_RT(2, "", "")
        UU_intensity_rate, UU_intensity_rt = Int_Rate_RT(3, "", "")
        
        NP_PN_intensity_rate, NP_PN_intensity_rt = Int_Rate_RT(4, "", "yes")
        NP_intensity_rate, NP_intensity_rt = Int_Rate_RT(4, "neu","no")
        PN_intensity_rate, PN_intensity_rt = Int_Rate_RT(4, "ero","no")
        
        NU_UN_intensity_rate, NU_UN_intensity_rt = Int_Rate_RT(5, "", "yes")
        NU_intensity_rate, NU_intensity_rt = Int_Rate_RT(5, "neu","no")
        UN_intensity_rate, UN_intensity_rt = Int_Rate_RT(5, "mut","no") 
        
        PU_UP_intensity_rate, PU_UP_intensity_rt = Int_Rate_RT(6, "", "yes")
        PU_intensity_rate, PU_intensity_rt = Int_Rate_RT(6, "ero","no")
        UP_intensity_rate, UP_intensity_rt = Int_Rate_RT(6, "mut","no")    
        
        #Pleasantness Ratings and Reaction Times:
        NN_pleasant_rate, NN_pleasant_rt = Pleasant_Rate_RT(1, "", "")
        PP_pleasant_rate, PP_pleasant_rt = Pleasant_Rate_RT(2, "", "")
        UU_pleasant_rate, UU_pleasant_rt = Pleasant_Rate_RT(3, "", "")
        
        NP_PN_pleasant_rate, NP_PN_pleasant_rt = Pleasant_Rate_RT(4, "", "yes")
        NP_pleasant_rate, NP_pleasant_rt = Pleasant_Rate_RT(4, "neu", "no")
        PN_pleasant_rate, PN_pleasant_rt = Pleasant_Rate_RT(4, "ero", "no")        

        NU_UN_pleasant_rate, NU_UN_pleasant_rt = Pleasant_Rate_RT(5, "", "yes")
        NU_pleasant_rate, NU_pleasant_rt = Pleasant_Rate_RT(5, "neu", "no")
        UN_pleasant_rate, UN_pleasant_rt = Pleasant_Rate_RT(5, "mut", "no")
        
        PU_UP_pleasant_rate, PU_UP_pleasant_rt = Pleasant_Rate_RT(6, "", "yes")
        PU_pleasant_rate, PU_pleasant_rt = Pleasant_Rate_RT(6, "ero", "no")
        UP_pleasant_rate, UP_pleasant_rt = Pleasant_Rate_RT(6, "mut", "no")         
                        
        #Append Lists and make CSV files:         
        run_param_list1.append([i, NN_intensity_rate, PP_intensity_rate,
            UU_intensity_rate, NP_PN_intensity_rate, NP_intensity_rate, PN_intensity_rate,
            NU_UN_intensity_rate, NU_intensity_rate, UN_intensity_rate, PU_UP_intensity_rate,
            PU_intensity_rate, UP_intensity_rate])
            
        run_param_list2.append([i, NN_pleasant_rate, PP_pleasant_rate, UU_pleasant_rate, 
            NP_PN_pleasant_rate, NP_pleasant_rate, PN_pleasant_rate, NU_UN_pleasant_rate,
            NU_pleasant_rate, UN_pleasant_rate, PU_UP_pleasant_rate, PU_pleasant_rate, 
            UP_pleasant_rate])
        
        run_param_list3.append([i, NN_intensity_rt, PP_intensity_rt, UU_intensity_rt, 
            NP_PN_intensity_rt, NP_intensity_rt, PN_intensity_rt, NU_UN_intensity_rt,
            NU_intensity_rt, UN_intensity_rt, PU_UP_intensity_rt, PU_intensity_rt,
            UP_intensity_rt]) 
        
        run_param_list4.append([i, NN_pleasant_rt, PP_pleasant_rt, UU_pleasant_rt, 
            NP_PN_pleasant_rt, NP_pleasant_rt, PN_pleasant_rt, NU_UN_pleasant_rt, 
            NU_pleasant_rt, UN_pleasant_rt, PU_UP_pleasant_rt, PU_pleasant_rt,
            UP_pleasant_rt])
        
        os.chdir(cwd)
        fid1 = pd.DataFrame(run_param_list1, columns=header1)
        fid2 = pd.DataFrame(run_param_list2, columns=header2)
        fid3 = pd.DataFrame(run_param_list3, columns=header3)
        fid4 = pd.DataFrame(run_param_list4, columns=header4)
        
        gender = pd.read_csv("Gender.csv")
        
        fid1 = fid1.merge(gender, on="Subject")
        fid2 = fid2.merge(gender, on="Subject")
        fid3 = fid3.merge(gender, on="Subject")
        fid4 = fid4.merge(gender, on="Subject")
        
        fid1.to_csv("Behavioral Data Analysis Intensity Rating.csv", header=True)
        fid2.to_csv("Behavioral Data Analysis Pleasantness Rating.csv", header=True)
        fid3.to_csv("Behavioral Data Analysis Intensity RT.csv", header=True)
        fid4.to_csv("Behavioral Data Analysis pleasantness RT.csv", header=True)
          
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
        
        
        