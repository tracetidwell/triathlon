import numpy as np
import pandas as pd
import math
import time
from lxml import objectify

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

def bike_data(bike_course):
    
    gpx = GPXParser(bike_course)
    lat = gpx.lat_values()
    lon = gpx.lon_values()
    ele = gpx.ele_values()
    data = np.append(lat.T, lon.T, axis=1)
    data = np.append(data, ele.T, axis=1)
    columns = ['lat', 'lon', 'ele']
    df = pd.DataFrame(data, columns = columns)
    #sometimes the file starts recording while in place
    #we remove duplicates
    df.drop_duplicates(inplace=True)

    #we then reset the index to start at 0 and run until the end
    df.reset_index(drop=True, inplace=True)
    #unique, indices = np.unique(data, return_index=True)
    
    return df.values

def calc_distance(lat, lon):

    sum_phi = (lat[1:] + lat[:-1]) * math.pi / 180
    del_lam = (lon[1:] - lon[:-1]) * math.pi / 180
    x = del_lam * np.cos(sum_phi/2)
    y = (lat[1:] - lat[:-1]) * math.pi / 180
    return 6371000 * np.sqrt(np.power(x, 2) + np.power(y, 2))

def calc_delta_y(ele):
    return np.array(ele[1:] - ele[:1])

def calc_theta(distance, ele):
	grade = np.array(ele[1:] - ele[:-1]) / distance
	return np.arctan(grade)

def calc_power(bike_ftp, grade, intensities):
	power = []

	for _, grd in grade:
	    if grd <= -0.06:
	       return bike_ftp * intensities[0]
	    elif grd <= -0.02:
	        return bike_ftp * intensities[1]
	    elif grd <= 0.02:
	        return bike_ftp * intensities[2]
	    elif grd <= 0.06:
	        return bike_ftp * intensities[3]
	    elif grd <= 0.1:
	        return bike_ftp * intensities[4]
	    else:
	        return bike_ftp * intensities[5]

def cube_root(value):

    if value > 0:
        return value ** (1./3)
    else:
        return -((-value) ** (1./3))

def calc_v(a, c, d):
        
    A = - (d/(2*a))
    B = (c/(3*a)) 
    C = np.sqrt(A**2 + B**3)
    D = A + C
    E = A - C
    D_cube_root = []
    E_cube_root =[]

    for val1 in D:
        D_cube_root.append(cube_root(val1))

    for val2 in E:
        E_cube_root.append(cube_root(val2))

    return (np.array(D_cube_root) + np.array(E_cube_root)) * 3.6 * 0.621371
    
def bike_time(course_data, bike_ftp, intensities, total_mass, 
        cda=0.3215, crr=0.002475, rho=1.29):

    g = 9.81 #acceleration due to gravity, m/s^2

    distance = calc_distance(course_data[:, 0], course_data[:, 1])

    pos = [distance[0]]
    for i in range(1, len(distance)):
        pos.append(distance[i] + pos[i-1])
    pos = np.array(pos)

    grade = np.array(course_data[1:, 2] - course_data[:-1, 2]) / distance

    course_data = course_data[1:, :]

    power = []
    for gra in grade:
        power.append(calc_power(bike_ftp, gra, intensities))
    power = np.array(power)
    
    a = 0.5 * rho * cda
    c = total_mass * g * (crr + np.sin(np.arctan(grade)))
    d = -power
    velocity = np.array(calc_v(a, c, d)) 
    
    times = (distance / 5280) / velocity

    course_data = np.append(course_data, np.reshape(distance, (-1, 1)), axis=1)
    course_data = np.append(course_data, np.reshape(grade, (-1, 1)), axis=1)
    course_data = np.append(course_data, np.reshape(power, (-1, 1)), axis=1)
    course_data = np.append(course_data, np.reshape(velocity, (-1, 1)), axis=1)
    course_data = np.append(course_data, np.reshape(times, (-1, 1)), axis=1)
    course_data = np.append(course_data, np.reshape(pos, (-1, 1)), axis=1)
    
    cols = ['lat', 'lon', 'ele', 'distance', 'grade', 'power', 'velocity', 'time', 'pos']
    df = pd.DataFrame(course_data, columns=cols)

    #return the total time, the distance covered, and the average speed
    return df#['time'].sum()

def normalized_power(power):
    norm = np.zeros(len(power)-30)
    for i, _ in enumerate(norm):
        norm[i] = sum(power[i:i+30]) / 30
    return int(round(np.power(sum(np.power(norm, 4)) / len(norm), 0.25)))