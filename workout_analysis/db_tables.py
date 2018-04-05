# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 19:44:09 2017

@author: Trace
"""
import numpy as np
import pandas as pd
import tcxparser
import time

def session_table(tcx):
    
    length = len(tcx.time_values())
    print(len([tcx.activity_id] * length))
    print(len([tcx.activity_type] * length))
    print(len(tcx.time_values()))
    print(len(tcx.dist))
    print(len(tcx.hr))
    print(len(tcx.cadence))
    print(len(tcx.power))
    print(len(tcx.speed))
    df_dict = {'activity_id': [tcx.activity_id] * length,
               'activity_type': [tcx.activity_type] * length,
               'time': np.array(tcx.time_values()),
               'distance': np.array(tcx.dist),
               'heart_rate': np.array(tcx.hr),
               'cadence': np.array(tcx.cadence),
               'power': np.array(tcx.power),
               'speed': np.array(tcx.speed)
                }
    
    cols = ['activity_id', 'activity_type', 'time', 'distance', 'heart_rate', 'cadence', 'power', 'speed']
    df = pd.DataFrame(df_dict, columns=cols)
    df.drop_duplicates(inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df
    
def summary_table(tcx, athlete):
    ftp = athlete.get_ftp(tcx.activity_type)
    if tcx.activity_type == 'biking':
        intensity_factor = round(tcx.normalized_power/ftp, 2)
    else:
        intensity_factor = round(tcx.avg_speed/(60/(ftp/60)), 2)
        
    df_dict = {'activity_id': tcx.activity_id,
               'activity_type': tcx.activity_type,
               'duration': time.strftime('%H:%M:%S', time.gmtime(tcx.duration)),# / 3600,
               'distance': round(tcx.distance / 1609.34, 2),
               'avg_speed': tcx.avg_speed,
               'avg_pace': tcx.pace,
               'calories': tcx.calories,
               'ascent': round(tcx.ascent, 2),
               'tss': round(intensity_factor**2 * tcx.duration/3600 * 100, 0),
               'if': intensity_factor,
               'work': tcx.power_avg * 3.6,
               'normalized_power': tcx.normalized_power,
               'hr_min': tcx.hr_min,
               'hr_avg': tcx.hr_avg,
               'hr_max': tcx.hr_max,
               'power_avg': tcx.power_avg,
               'power_max': tcx.power_max,
               'cadence_avg': tcx.cadence_avg,
               'cadence_max': tcx.cadence_max}
               
    cols = ['activity_id', 'activity_type', 'duration', 'distance', 'avg_speed', 'avg_pace', 
            'calories', 'ascent', 'tss', 'if', 'work', 'normalized_power', 'hr_min', 
            'hr_avg', 'hr_max', 'power_avg', 'power_max', 'cadence_avg', 'cadence_max']
    return pd.DataFrame(df_dict, columns=cols, index=[0])

def db_tables(file, athlete):
    tcx = tcxparser.TCXParser(file)
    tcx.get_data()
    
    session = session_table(tcx)
    
    summary = summary_table(tcx, athlete)
    
    return session, summary
    
        