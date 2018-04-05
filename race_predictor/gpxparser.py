# -*- coding: utf-8 -*-
"""
Created on Sun Jul  9 14:10:55 2017

@author: Trace
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 18:09:06 2017

@author: Trace
"""

"Simple parser for Garmin TCX files."

import numpy as np
import time
from lxml import objectify

#namespace = 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2'
#namespace3 = 'http://www.garmin.com/xmlschemas/ActivityExtension/v2'

class GPXParser:

    def __init__(self, gpx_file):
        tree = objectify.parse(gpx_file)
        self.root = tree.getroot()
        self.trkseg = self.root.trk.trkseg
        
    def lat_values(self):
        return np.array([[float(x.attrib['lat']) for x in self.trkseg.trkpt]])
    
    def lon_values(self):
        return np.array([[float(x.attrib['lon']) for x in self.trkseg.trkpt]])
    
    def ele_values(self):
        return np.array([[float(x.ele) for x in self.trkseg.trkpt]])
        
#    def power_values(self):
#        return [int(x.text) for x in self.root.xpath('//ns3:Watts', namespaces={'ns3': namespace3})]
#    
#    def hr_values(self):
#        hr = []
#        for lap in self.activity.Lap:
#            for trackpoint in lap.Track.Trackpoint:
#                try:
#                    if trackpoint.HeartRateBpm.Value:
#                        hr.append(trackpoint.HeartRateBpm.Value)
#                except AttributeError:
#                    hr.append(0)
#                    
#        for i, val in enumerate(hr):
#            if val == 0:
#                j = 1
#                while hr[i+j] == 0:
#                    j += 1
#                hr[i] = (hr[i-1] + hr[i+j]) // 2
#        return hr
#        #return [int(x.text) for x in self.root.xpath('//ns:HeartRateBpm/ns:Value', namespaces={'ns': namespace})]
#
#    def altitude_points(self):
#        return [float(x.text) for x in self.root.xpath('//ns:AltitudeMeters', namespaces={'ns': namespace})]
#    
#    def time_values(self):
#        return [x.text for x in self.root.xpath('//ns:Time', namespaces={'ns': namespace})]
#    
#    @property
#    def normalized_power(self):
#        power_data = self.power_values()
#        norm = np.zeros(len(power_data)-30)
#        for i, _ in enumerate(norm):
#            norm[i] = sum(power_data[i:i+30]) / 30
#        return int(round(np.power(sum(np.power(norm, 4)) / len(norm), 0.25)))
#            
#    @property
#    def latitude(self):
#        if hasattr(self.activity.Lap.Track.Trackpoint, 'Position'):
#            return self.activity.Lap.Track.Trackpoint.Position.LatitudeDegrees.pyval
#
#    @property
#    def longitude(self):
#        if hasattr(self.activity.Lap.Track.Trackpoint, 'Position'):
#            return self.activity.Lap.Track.Trackpoint.Position.LongitudeDegrees.pyval
#
#    @property
#    def activity_type(self):
#        return self.activity.attrib['Sport'].lower()
#
#    @property
#    def completed_at(self):
#        return self.activity.Lap[-1].Track.Trackpoint[-1].Time.pyval
#
#    @property
#    def distance(self):
#        distance_values = self.root.findall('.//ns:DistanceMeters', namespaces={'ns': namespace})
#        if distance_values:
#            return distance_values[-1]
#        return 0
#
#    @property
#    def distance_units(self):
#        return 'meters'
#
#    @property
#    def duration(self):
#        """Returns duration of workout in seconds."""
#        return sum(lap.TotalTimeSeconds for lap in self.activity.Lap)
#
#    @property
#    def calories(self):
#        return sum(lap.Calories for lap in self.activity.Lap)
#
#    @property
#    def hr_avg(self):
#        """Average heart rate of the workout"""
#        hr_data = self.hr_values()
#        return sum(hr_data)/len(hr_data)
#
#    @property
#    def hr_max(self):
#        """Maximum heart rate of the workout"""
#        return max(self.hr_values())
#
#    @property
#    def hr_min(self):
#        """Minimum heart rate of the workout"""
#        return min(self.hr_values())
#
#    @property
#    def pace(self):
#        """Average pace (mm:ss/km for the workout"""
#        secs_per_km = self.duration/(self.distance/1000)
#        return time.strftime('%M:%S', time.gmtime(secs_per_km))
#
#    @property
#    def altitude_avg(self):
#        """Average altitude for the workout"""
#        altitude_data = self.altitude_points()
#        return sum(altitude_data)/len(altitude_data)
#
#    @property
#    def altitude_max(self):
#        """Max altitude for the workout"""
#        altitude_data = self.altitude_points()
#        return max(altitude_data)
#
#    @property
#    def altitude_min(self):
#        """Min altitude for the workout"""
#        altitude_data = self.altitude_points()
#        return min(altitude_data)
#
#    @property
#    def ascent(self):
#        """Returns ascent of workout in meters"""
#        total_ascent = 0.0
#        altitude_data = self.altitude_points()
#        for i in range(len(altitude_data) - 1):
#            diff = altitude_data[i+1] - altitude_data[i]
#            if diff > 0.0:
#                total_ascent += diff
#        return total_ascent
#
#    @property
#    def descent(self):
#        """Returns descent of workout in meters"""
#        total_descent = 0.0
#        altitude_data = self.altitude_points()
#        for i in range(len(altitude_data) - 1):
#            diff = altitude_data[i+1] - altitude_data[i]
#            if diff < 0.0:
#                total_descent += abs(diff)
#        return total_descent