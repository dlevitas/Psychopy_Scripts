# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 13:08:25 2016

@author: Daniel

Getting ToM stimuli from matlab files. This is the worse because the .mat files
are arrays within arrays so getting everything together is a drag.
"""
import scipy.io as sio
import os
import numpy as np
import pandas as pd

cwd = os.path.dirname(__file__)

num_audio_files = len(sio.loadmat('Stimuli.mat').values()[0])
stim_list = []
headers = ['Audio_file','Choice1','Choice2','Correct','Degree Difficulty']

for i in range(num_audio_files):
    audio = str(sio.loadmat('Stimuli.mat').values()[0][i][0][0][0][0])
    num_question_files = len(sio.loadmat('Stimuli.mat').values()[0][i][0][1][0])
    for k in range(num_question_files):
        choice1 = str(sio.loadmat('Stimuli.mat').values()[0][i][0][1][0][k][0][0][2][0])
        choice2 = str(sio.loadmat('Stimuli.mat').values()[0][i][0][1][0][k][0][0][3][0])
        diff = int(sio.loadmat('Stimuli.mat').values()[0][i][0][1][0][k][0][0][1][0][0])

        stim_list.append([audio, choice1, choice2, choice1, diff])
        
fid = pd.DataFrame(stim_list, columns = headers)
fid.to_csv('ToM_Stim_List.csv', header = True)

"""
data = pd.read_csv('ToM_Stim_List.csv')
del data['Unnamed: 0']
for i in range(len(data)):
    choice1 = np.random.permutation(data.ix[i][2:4])[0]
    choice2 = np.random.permutation(data.ix[i][2:4])[1]
    
    if choice1 == data['Correct Statement'][i]:
        print "Same"
    else:
        print "Changed"
"""





















