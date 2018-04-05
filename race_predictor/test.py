# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 14:27:36 2017

@author: Trace
"""

import numpy as np
import pandas as pd
import math
import bike_calcs2
import time
import matplotlib.pyplot as plt
import bike

race_type = 'half'
bike_ftp = 240 #W
bike_if = 0.81
bike_mass = 10 #mass of bike, kg
rider_mass = 65.9 #mass of rider, kg
total_mass = bike_mass + rider_mass
bike_course = 'GPX-Route_6863_340.gpx'
intensities = [0.7, 0.8, 0.9, 1, 1.1, 2]

rpm = 90
v_crank = rpm * 2 * math.pi / 60 * 0.165
g = 9.81
crr = 0.002475
rho = 1.29
cda = 0.3215
k = 0.5 * rho * cda

bike = bike.Bike(bike_course, bike_ftp, total_mass, intensities)
bike.predict()
v = bike.avg_velocity
print(v)