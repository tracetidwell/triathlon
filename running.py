# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 18:05:04 2017

@author: Trace
"""
import numpy as np
import pandas as pd

file = []

with open('activity.tcx') as inputfile:
    for line in inputfile:
        file.append(line.strip())

cols = ['Time', 'Lat', 'Lon', 'Alt', 'Dist', 'HR', 'Speed']
data = pd.DataFrame(cols)
    
for i, row in enumerate(file):
    if '<Trackp' in file[i]:
        j = 1
        temp = [0, 0, 0, 0, 0, 0, 0]
        while '</Trackp' not in file[i+j]:
            if '<Time' in file[i+j]:
                temp[0] = file[i+j]
            elif '<Lat' in file[i+j]:
                temp[1] = file[i+j]
            elif '<Lon' in file[i+j]:
                temp[2] = file[i+j]
            elif '<Alt' in file[i+j]:
                temp[3] = file[i+j]
            elif '<Dist' in file[i+j]:
                temp[4] = file[i+j]
            elif '<Value' in file[i+j]:
                temp[5] = file[i+j]
            elif '<Speed' in file[i+j]:
                temp[6] = file[i+j]
            data = data.append(pd.Series(temp, index=cols), ignore_index=True)
            j += 1
