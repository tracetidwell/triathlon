# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 19:34:41 2017

@author: Trace
"""

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

cols = ['DateTime', 'Lat', 'Lon', 'Alt', 'Dist', 'HR', 'Speed']
data = pd.DataFrame(columns=cols)
    
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
            elif '<ns3:Speed' in file[i+j]:
                temp[6] = file[i+j]
            j += 1
        data = data.append(pd.Series(temp, index=cols), ignore_index=True)

def clean_datetime(row):
    if row != 0:
        return row[6: 6 + (len(row)-18)]

def clean_lat(row):
    if row != 0:
        return row[17: 17 + (len(row)-35)]

def clean_lon(row):
    if row != 0:
        return row[18: 18 + (len(row)-37)]

def clean_alt(row):
    if row != 0:
        return row[16: 16 + (len(row)-33)]

def clean_dist(row):
    if row != 0:
        return row[16: 16 + (len(row)-33)]

def clean_hr(row):
    if row != 0:
        return row[7: 7 + (len(row)-15)]

def clean_speed(row):
    if row != 0:
        return row[11: 11 + (len(row)-23)]
    
def set_time(row):
    if row != 0:
        return row.split('T')[1]
    
data['DateTime'] = data['DateTime'].apply(clean_datetime)
data['Lat'] = data['Lat'].apply(clean_lat)
data['Lon'] = data['Lon'].apply(clean_lon)
data['Alt'] = data['Alt'].apply(clean_alt)
data['Dist'] = data['Dist'].apply(clean_dist)
data['HR'] = data['HR'].apply(clean_hr)
data['Speed'] = data['Speed'].apply(clean_speed)
data['Time'] = data['DateTime'].apply(set_time)

        
