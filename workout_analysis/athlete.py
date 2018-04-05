# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 21:06:58 2017

@author: Trace
"""
import numpy as np
import pandas as pd
import time
from sqlalchemy import create_engine
import pyodbc

class Athlete:
    
    def __init__(self, username):
        
        cnxn = pyodbc.connect("Driver={ODBC Driver 13 for SQL Server};" + 
                              "Server=LAPTOP-90DSR0LF\SQLEXPRESS; Database=training;" +
                              "trusted_connection=yes; UID=trace; PWD=trace")
    
        cursor = cnxn.cursor()
        
        result = cursor.execute("SELECT * FROM dbo.athlete_data WHERE " +
                                "username = '" + username + "'")
        
        data = result.fetchone()
        
        self.sftp = data[1]
        self.bftp = int(data[2])
        self.rftp = data[3]
        #stru_time = time.strptime(rftp, '%M:%S')
        #self.rftps = stru_time[4] * 60 + stru_time[5] 
        self.slthr = data[4]
        self.blthr = int(data[5])
        self.rlthr = int(data[6])
        self.mass = int(data[7])
        
        def calc_zones(self):
        
            def calc_power_zones(self):
                power_zones = self.bftp * np.array([[0.00, 0.55],
                                                    [0.56, 0.75],
                                                    [0.76, 0.90],
                                                    [0.91, 1.05],
                                                    [1.06, 1.20],
                                                    [1.21, 2000]])
                power_zones[-1][-1] = 2000
                self.power_zones = pd.DataFrame(power_zones, columns=['min', 'max'], index=range(1,7))
            
            def calc_pace_zones(self):
                pace_zones = self.rftps * np.array([[30, 1.29],
                                                    [1.28, 1.14],
                                                    [1.13, 1.06],
                                                    [1.05, 1.01],
                                                    [1.00, 0.97],
                                                    [0.96, 0.90],
                                                    [0.89, 0.01]])
                pace_zones_df = pd.DataFrame(columns=['min', 'max'], index=range(1,8))
                for i, row in enumerate(pace_zones):
                    for j, val in enumerate(row):
                        pace_zones_df.iloc[i][j] = time.strftime('%M:%S', time.gmtime(val))
                pace_zones_df.iloc[-1][-1] = '00:01'
                self.pace_zones = pace_zones_df
                
            def calc_bhr_zones(self):
                bhr_zones = self.blthr * np.array([[0.00, 0.80],
                                                   [0.81, 0.89],
                                                   [0.90, 0.93],
                                                   [0.94, 0.99],
                                                   [1.00, 1.02],
                                                   [1.03, 1.06],
                                                   [1.06, 3.00]])
                
                bhr_zones[-1][-1] = 255
                self.bhr_zones = pd.DataFrame(bhr_zones.astype(int), columns=['min', 'max'], index=range(1,8))
                
            def calc_rhr_zones(self):
                rhr_zones = self.rlthr * np.array([[0.00, 0.84],
                                                   [0.85, 0.89],
                                                   [0.90, 0.94],
                                                   [0.95, 0.99],
                                                   [1.00, 1.02],
                                                   [1.03, 1.06],
                                                   [1.06, 3.00]])
                
                rhr_zones[-1][-1] = 255
                self.rhr_zones = pd.DataFrame(rhr_zones.astype(int), columns=['min', 'max'], index=range(1,8))
                
            calc_power_zones(self)
            calc_pace_zones(self)
            calc_bhr_zones(self)
            calc_rhr_zones(self)
        
        calc_zones(self)
        
    def get_ftp(self, activity):
        if activity == 'swimming':
            return self.sftp
        elif activity == 'biking':
            return self.bftp
        elif activity == 'running':
            return self.rftps
        
    def get_lthr(self, activity):
        if activity == 'swimming':
            return self.slthr
        elif activity == 'biking':
            return self.blthr
        elif activity == 'running':
            return self.rlthr
        
    def set_ftp(self, activity, ftp):
        if activity == 'swimming':
            self.sftp = ftp
        elif activity == 'biking':
            self.bftp = ftp
        elif activity == 'running':
            self.rftp = ftp
            
    def set_lthr(self, activity, lthr):
        if activity == 'swimming':
            self.slthr = lthr
        elif activity == 'biking':
            self.blthr = lthr
        elif activity == 'running':
            self.rlthr = lthr
            
    