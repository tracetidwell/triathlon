
import numpy as np
import pandas as pd
import math

def bike_data(bike_course):

    #Function to calculate time to complete bike course based on average power

    #read the text file
    data = pd.read_csv(bike_course, header=None)
    data = data[:][0]

    #create a dataframe to store calculated values
    columns = ['lat', 'lon', 'ele']
    df = pd.DataFrame(columns = columns)

    #loop through the bike course file and store the latitude,
    #longitude, and elevation values in the dataframe
    for idx, row in data.iteritems():
        if '<trkpt' in row:
            for item in (row.strip()).split(' '):
                if 'lat' in item:
                    lat = float(item[5:len(item)-1])
                elif 'lon' in item:
                    lon = float(item[5:len(item)-2])
            if '<ele>' in data[idx+1]:
                ele = float(data[idx+1].strip()[5:len(data[idx+1].strip())-6])
            df = df.append({'lat':lat, 'lon':lon, 'ele':ele}, ignore_index=True)

    #sometimes the file starts recording while in place
    #we remove duplicates
    df.drop_duplicates(inplace=True)

    #we then reset the index to start at 0 and run until the end
    df.reset_index(drop=True, inplace=True)

    #return the dataframe for further processing
    return df

def bike_time(df, bike_avg_power, total_mass, 
        cda=0.32, crr=0.002475, rho=1.29):

    g = 9.81 #acceleration due to gravity, m/s^2
    f_roll = total_mass * g * crr #force needed to overcome rolling friction
    c1 = 0.5 * rho * cda #coeffienct needed to calculate velocity from power and force
    q = -bike_avg_power / c1 ##coeffienct needed to calculate velocity from power and force

    def calc_distance(lat, lon):
        sum_phi = (lat[1:] + lat[:-1]) * math.pi / 180
        del_lam = (lon[1:] - lon[:-1]) * math.pi / 180
        x = del_lam * np.cos(sum_phi/2)
        y = (lat[1:] - lat[:-1]) * math.pi / 180
        return 3959.0 * np.sqrt(np.power(x, 2) + np.power(y, 2)) * 5280.0

    d = calc_distance(np.array(df['lat'].values), np.array(df['lon'].values))

    grade = np.array(df['ele'][1:].values - df['ele'][:-1].values) / d

    #now we remove the top row of the dataframe, so we can insert the delta variables
    df = df.iloc[1:]
    df.reset_index(drop=True, inplace=True)
    df.insert(loc=df.shape[1], column='d', value=d)
    df.insert(loc=df.shape[1], column='grade', value=grade)

    def cube_root(value):
        if value > 0:
            return value ** (1./3)
        else:
            return -((-value) ** (1./3))

    def calc_v_ms(grade):
        c2 = (np.sin(np.arctan(grade)) + crr) * total_mass * g
        p = c2 / c1
        u3 = np.sqrt((q**2)/4 + (p**3)/27) + (-q/2)
        v3 = -np.sqrt((q**2)/4 + (p**3)/27) + (-q/2)
        
        u3_cube_root = []
        for i in u3:
            u3_cube_root.append(cube_root(i))
        
        v3_cube_root = []
        for j in v3:
            v3_cube_root.append(cube_root(j))

        return np.array(u3_cube_root) + np.array(v3_cube_root)

    v_ms = calc_v_ms(grade)

    df.insert(loc=df.shape[1], column='v_ms', value=v_ms)

    df.insert(loc=df.shape[1], column='v_mph', value=v_ms*3.6*0.621371)

    #df['v_mph'] = v_ms * 3.6 * 0.621371

    df['f_climb'] = np.sin(np.arctan(grade)) * total_mass * g

    df['f_air'] = 0.5 * rho * df['v_ms']**2 * cda

    df['f_total'] = f_roll + df['f_climb'] + df['f_air']

    df['t'] = (df['d'] / 5280) / df['v_mph']

    #return the total time, the distance covered, and the average speed
    return df['t'].sum() #, df['d'].sum() / 5280, df['v_mph'].mean()