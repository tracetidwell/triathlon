# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 18:09:06 2017

@author: Trace
"""

"Simple parser for Garmin TCX files."

import numpy as np
import time
from lxml import objectify

namespace = 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2'
namespace3 = 'http://www.garmin.com/xmlschemas/ActivityExtension/v2'

class TCXParser:

    def __init__(self, tcx_file):
        tree = objectify.parse(tcx_file)
        self.root = tree.getroot()
        self.activity = self.root.Activities.Activity
        
    def get_data(self):
        distance = []
        hr = []
        power = []
        speed = []
        cadence = []
        alt = []
        
        for lap in self.activity.Lap:
            for trackpoint in lap.Track.getchildren():
                
                #Distance
                try: 
                    if trackpoint.DistanceMeters >= 0:
                        distance.append(float(trackpoint.DistanceMeters.text))
                except AttributeError:
                    distance.append(0)
                    
                #Heart Rate
                try:
                    if trackpoint.HeartRateBpm.Value:
                        hr.append(int(trackpoint.HeartRateBpm.Value))
                except AttributeError:
                    hr.append(0)
                    
                #Power and Speed
                try:
                    if trackpoint.Extensions:
                        if len(trackpoint.Extensions.getchildren()) == 0:
                            power.append(-1)
                            speed.append(-1)
                        else:
                                    # If so, check to see if Watts child exists under TPX
                            if len(trackpoint.Extensions.getchildren()[0].getchildren()) == 2:
                                power.append(int(trackpoint.Extensions.getchildren()[0].getchildren()[0]))
                                speed.append(int(trackpoint.Extensions.getchildren()[0].getchildren()[1]))
                            elif len(trackpoint.Extensions.getchildren()[0].getchildren()) == 1:
                                if trackpoint.Extensions.getchildren()[0].getchildren()[0].tag == '{http://www.garmin.com/xmlschemas/ActivityExtension/v2}Watts':
                                    power.append(int(trackpoint.Extensions.getchildren()[0].getchildren()[0]))
                                    speed.append(-1)
                                else:
                                    power.append(-1)
                                    speed.append(int(trackpoint.Extensions.getchildren()[0].getchildren()[0]))
                    else:
                        power.append(-1)
                        speed.append(-1)
                            
                except AttributeError:
                    power.append(-1)
                    speed.append(-1)
                    
                #Cadence
                try: 
                    if trackpoint.Cadence >= 0:
                        cadence.append(float(trackpoint.Cadence.text))
                except AttributeError:
                    cadence.append(-1)
                    
                #Altitude
                try: 
                    if trackpoint.Altitude >= 0:
                        alt.append(float(trackpoint.Altitude.text))
                except AttributeError:
                    alt.append(-1)
                    
        self.dist = distance
        self.hr = hr
        self.power = power
        self.speed = speed
        self.cadence = cadence
        self.alt = alt
        
        def process_num(metric, num, *args):
            temp = metric
                        
            if sum(temp) > 0:
                if temp[-1] == num:
                    i = -2
                    while temp[i] == num:
                        i -= 1
                    temp[i+1:] = [temp[i] for x in range(-i-1)]
                    
                if temp[0] == num and args[0] == 'hr':
                    i = 1
                    while temp[i] == num:
                        i += 1
                    temp[0:i+1] = [temp[i+1] for x in range(i+1)]
                        
                if num == 0:
                    for j, val in enumerate(temp):
                        if val == 0 and j != 0:
                            k = 1
                            while temp[j+k] == 0:
                                k += 1
                            temp[j:j+k] = [temp[j-1] + ((temp[j+k]-temp[j-1])/(k+1)) * x for x in range(1, k+1)]
                else:
                    for j, val in enumerate(temp):
                        if val == -1:
                            k = 1
                            while temp[j+k] == -1:
                                k += 1
                            temp[j:j+k] = [temp[j-1] + ((temp[j+k]-temp[j-1])/(k+1)) * x for x in range(1, k+1)]
                        
            return temp
    
        self.dist = process_num(self.dist, 0, 'dist')
        self.hr = process_num(self.hr, 0, 'hr')
        if np.mean(power) == -1:
            self.power = np.zeros(len(self.power))
        else:
            self.power = process_num(self.power, -1)
        self.speed = process_num(self.speed, -1, 'speed')
        self.cadence = process_num(self.cadence, -1, 'cadence')
        self.alt = process_num(self.alt, -1, 'alt')

    def altitude_points(self):
        return [float(x.text) for x in self.root.xpath('//ns:AltitudeMeters', namespaces={'ns': namespace})]
    
    def time_values(self):
        return [x.text for x in self.root.xpath('//ns:Time', namespaces={'ns': namespace})]
    
    @property
    def activity_id(self):
        return self.activity.Id.text
    
    @property
    def normalized_power(self):
        power_data = self.power
        norm = np.zeros(len(power_data)-30)
        for i, _ in enumerate(norm):
            norm[i] = sum(power_data[i:i+30]) / 30
        return int(round(np.power(sum(np.power(norm, 4)) / len(norm), 0.25)))
            
    @property
    def latitude(self):
        if hasattr(self.activity.Lap.Track.Trackpoint, 'Position'):
            return self.activity.Lap.Track.Trackpoint.Position.LatitudeDegrees.pyval

    @property
    def longitude(self):
        if hasattr(self.activity.Lap.Track.Trackpoint, 'Position'):
            return self.activity.Lap.Track.Trackpoint.Position.LongitudeDegrees.pyval

    @property
    def activity_type(self):
        return self.activity.attrib['Sport'].lower()

    @property
    def completed_at(self):
        return self.activity.Lap[-1].Track.Trackpoint[-1].Time.pyval

    @property
    def distance(self):
        if sum(self.dist) > 0:
            return self.dist[-1]
        else: 
            return sum(self.root.findall('.//ns:DistanceMeters', namespaces={'ns': namespace}))

    @property
    def distance_units(self):
        return 'meters'

    @property
    def duration(self):
        """Returns duration of workout in seconds."""
        return sum(lap.TotalTimeSeconds for lap in self.activity.Lap)

        
    @property
    def avg_speed(self):
        return round((self.distance / self.duration) * 2.23694, 2)

    @property
    def calories(self):
        return sum(lap.Calories for lap in self.activity.Lap)
    
    @property
    def power_avg(self):
        """Average heart rate of the workout"""
        power_data = self.power
        return int(sum(power_data)/len(power_data))

    @property
    def power_max(self):
        """Maximum heart rate of the workout"""
        return int(max(self.power))
    
    @property
    def cadence_avg(self):
        """Average heart rate of the workout"""
        cadence_data = self.cadence
        return int(sum(cadence_data)/len(cadence_data))

    @property
    def cadence_max(self):
        """Maximum heart rate of the workout"""
        return int(max(self.cadence))

    @property
    def hr_avg(self):
        """Average heart rate of the workout"""
        hr_data = self.hr
        return int(sum(hr_data)/len(hr_data))

    @property
    def hr_max(self):
        """Maximum heart rate of the workout"""
        return int(max(self.hr))

    @property
    def hr_min(self):
        """Minimum heart rate of the workout"""
        return int(min(self.hr))

    @property
    def pace(self):
        """Average pace (mm:ss/km for the workout"""
        secs_per_km = self.duration/(self.distance/1000)
        return time.strftime('%H:%M:%S', time.gmtime(secs_per_km*1.60934))

    @property
    def altitude_avg(self):
        """Average altitude for the workout"""
        altitude_data = self.altitude_points()
        return sum(altitude_data)/len(altitude_data)

    @property
    def altitude_max(self):
        """Max altitude for the workout"""
        altitude_data = self.altitude_points()
        return max(altitude_data)

    @property
    def altitude_min(self):
        """Min altitude for the workout"""
        altitude_data = self.altitude_points()
        return min(altitude_data)

    @property
    def ascent(self):
        """Returns ascent of workout in meters"""
        total_ascent = 0.0
        altitude_data = self.altitude_points()
        for i in range(len(altitude_data) - 1):
            diff = altitude_data[i+1] - altitude_data[i]
            if diff > 0.0:
                total_ascent += diff
        return total_ascent

    @property
    def descent(self):
        """Returns descent of workout in meters"""
        total_descent = 0.0
        altitude_data = self.altitude_points()
        for i in range(len(altitude_data) - 1):
            diff = altitude_data[i+1] - altitude_data[i]
            if diff < 0.0:
                total_descent += abs(diff)
        return total_descent