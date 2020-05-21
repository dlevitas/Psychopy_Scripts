# -*- coding: utf-8 -*-
"""
Created on Fri Mar 03 11:08:28 2017

@author: Daniel
Parameter Generation for the Controllability Study
"""

from __future__ import division
import os, random
import pandas as pd

cwd = os.path.dirname(__file__)

run_param_list = []
header = ['Run','Block','Safe_Block_Time','Threat_Block_Time','Num_Audio_Sounds','Stressor_Onset_Times']

"""Script Parameters"""
safe_range = [30,60]
threat_range = [60,120]
num_threats_range = [0,3]
num_runs, num_blocks, stress_time = [4,6,3]

low_limit, high_limit = [3,7]
ceiling = 12

"""Function 1"""
def generator(num_blocks, safe_range, threat_range, num_threats_range):
    run_order_all, block_order_all, safe_block_times_all, threat_block_times_all, num_threats_all, stressor_onsets_total_all = [[],[],[],[],[],[]]

    for i in range(1, num_runs+1):
        run_order = [i]*num_blocks
        run_order_all.extend(run_order)
        
        block_order = []
        if random.sample(['safe','threat'],1) == ['safe']:
            block_order.extend(['safe','threat']*int(num_blocks/2))
        else:
            block_order.extend(['threat','safe']*int(num_blocks/2))
        block_order_all.extend(block_order)
        """Safe Block Times"""
        safe_block_times = [random.randint(safe_range[0], safe_range[1]) for x in range(int(num_blocks/2))]
        while sum(safe_block_times)/len(safe_block_times) != round(sum(safe_range)/2,0):
            if len([x for x in safe_block_times if safe_block_times.count(x) > 1]):
                safe_block_times.remove([x for x in safe_block_times if safe_block_times.count(x) > 1][0])
                safe_block_times.extend([random.randint(safe_range[0], safe_range[1])])
            else:
                safe_block_times.remove(safe_block_times[0])
                safe_block_times.extend([random.randint(safe_range[0], safe_range[1])])
        safe_block_times_all.extend(safe_block_times)
        """Threat Block Times"""    
        threat_block_times = [random.randint(threat_range[0], threat_range[1]) for x in range(int(num_blocks/2))]
        while sum(threat_block_times)/len(threat_block_times) != round(sum(threat_range)/2,0):
            if len([x for x in threat_block_times if threat_block_times.count(x) > 1]):
                threat_block_times.remove([x for x in threat_block_times if threat_block_times.count(x) > 1][0])
                threat_block_times.extend([random.randint(threat_range[0], threat_range[1])])
            else:
                threat_block_times.remove(threat_block_times[0])
                threat_block_times.extend([random.randint(threat_range[0], threat_range[1])])  
        threat_block_times_all.extend(threat_block_times)
        """The # of threats"""        
        num_threats = [random.randint(num_threats_range[0], num_threats_range[1]) for x in range(int(num_blocks/2))]
        while sum(num_threats)/len(num_threats) != round(sum(num_threats_range)/len(num_threats_range),0):
            if len([x for x in num_threats if num_threats.count(x) > 1]):
                num_threats.remove([x for x in num_threats if num_threats.count(x) > 1][0])
                num_threats.extend([random.randint(num_threats_range[0], num_threats_range[1])])
            else:
                num_threats.remove(num_threats[0])
                num_threats.extend([random.randint(num_threats_range[0], num_threats_range[1])])
        num_threats_all.extend(num_threats)
        """Stressor onset times. 3 lists; one for each threat block"""
        for i in range(len(num_threats)):
            if i == 0:
                stressor_onsets1 = sorted([random.randint(2, threat_block_times[i]-10) for x in range(num_threats[i])])
                for j in range(len(stressor_onsets1)):
                    if j == 0:
                        pass
                    elif stressor_onsets1[j] <= stressor_onsets1[j-1]:
                        stressor_onsets1[j] += (stressor_onsets1[j-1] - stressor_onsets1[j]) + stress_time + 1
                    elif stressor_onsets1[j] < stressor_onsets1[j-1] + stress_time + 1:
                        stressor_onsets1[j] += stress_time + 1
                    else:
                        pass
            elif i == 1:
                stressor_onsets2 = sorted([random.randint(2, threat_block_times[i]-10) for x in range(num_threats[i])])
                for j in range(len(stressor_onsets2)):
                    if j == 0:
                        pass
                    elif stressor_onsets2[j] <= stressor_onsets2[j-1]:
                        stressor_onsets2[j] += (stressor_onsets2[j-1] - stressor_onsets2[j]) + stress_time + 1
                    elif stressor_onsets2[j] < stressor_onsets2[j-1] + stress_time + 1:
                        stressor_onsets2[j] += stress_time + 1
                    else:
                        pass
            else:
                stressor_onsets3 = sorted([random.randint(2, threat_block_times[i]-10) for x in range(num_threats[i])])
                for j in range(len(stressor_onsets3)):
                    if j == 0:
                        pass
                    elif stressor_onsets3[j] <= stressor_onsets3[j-1]:
                        stressor_onsets3[j] += (stressor_onsets3[j-1] - stressor_onsets3[j]) + stress_time + 1
                    elif stressor_onsets3[j] < stressor_onsets3[j-1] + stress_time + 1:
                        stressor_onsets3[j] += stress_time + 1
                    else:
                        pass
            
        stressor_onsets_total = [stressor_onsets1] + [stressor_onsets2] + [stressor_onsets3]
        stressor_onsets_total_all.extend(stressor_onsets_total)
    return block_order_all, safe_block_times_all, threat_block_times_all, num_threats_all, stressor_onsets_total_all, run_order_all
    
    
block_order, safe_block_times, threat_block_times, num_threats, stressor_onsets_total, run_order = generator(num_blocks, safe_range, threat_range, num_threats_range)[0:6]
safe_counter, threat_counter = [0,0]

print sum(safe_block_times[0:3])/3
"""Print output from function 1 to csv file"""
for k in range(len(block_order)):    
    if block_order[k] == 'safe':
        run_param_list.append([run_order[k], block_order[k], safe_block_times[safe_counter], 'N/A', 'N/A', 'N/A'])
        fid = pd.DataFrame(run_param_list, columns=header)
        fid.to_csv('exp_file.csv', header=True, index=False)
        safe_counter +=1
    else:
        run_param_list.append([run_order[k], block_order[k], 'N/A', threat_block_times[threat_counter], num_threats[threat_counter], stressor_onsets_total[threat_counter]])
        fid = pd.DataFrame(run_param_list, columns=header)
        fid.to_csv('exp_file.csv', header=True, index=False)
        threat_counter +=1



"""Function 2"""
def presses_needed(num_threats_range, num_blocks):
    presses_needed = [random.randint(low_limit,high_limit) for x in range(50)]
    presses_needed_list = []
    counter = 1
    while sum(presses_needed) != (round(sum(num_threats_range)/len(num_threats_range),0))*(num_blocks/2)*num_runs:
        if len(presses_needed) == 0:
            presses_needed = [random.randint(low_limit,high_limit) for x in range(50)]
        else:
            presses_needed.remove(presses_needed[0])
            
    for i in presses_needed:
        presses_needed_list.extend([counter]*i)
        counter +=1
        if counter > ceiling:
            counter = ceiling
        
    return presses_needed_list

presses_needed_list = presses_needed(num_threats_range, num_blocks)
print presses_needed_list

        
        
        
        
        
        
    