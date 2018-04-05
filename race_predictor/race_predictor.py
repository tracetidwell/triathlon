# -*- coding: utf-8 -*-
"""
Created on Sun Jul  9 13:59:16 2017

@author: Trace
"""
import numpy as np
import bike_calcs2
import time
import matplotlib.pyplot as plt
from scipy import optimize

bike_course = 'GPX-Route_6863_340.gpx'
bike_ftp = 240
total_mass = 75.9
intensities = [0.6, 0.7, 0.76, 0.8, 0.9, 1.0]

course_data = bike_calcs2.bike_data(bike_course)
df = bike_calcs2.bike_time(course_data, bike_ftp, intensities, total_mass)
args = (course_data, bike_ftp, total_mass)

#res = optimize.minimize(bike_calcs2.bike_time, intensities, args=args)
bike_time = df['time'].sum()
norm_p = bike_calcs2.normalized_power(df['power'] * 1.02)
ap = df['power'].sum() / len(df['power'])
vi = norm_p / ap
bike_tss = (norm_p / bike_ftp) ** 2 * 100 * bike_time
intensity_factor = norm_p / bike_ftp
print("Time:", time.strftime("%H:%M:%S", time.gmtime(bike_time*60*60)))
print("NP:", norm_p)
print("AP:", ap)
print("TSS:", bike_tss)
print("IF:", intensity_factor)
