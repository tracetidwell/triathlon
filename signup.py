# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 09:32:42 2018

@author: Trace
"""

import pandas as pd
from sqlalchemy import create_engine
import pyodbc

def signup():
    
    cnxn = pyodbc.connect("Driver={ODBC Driver 13 for SQL Server};" + 
                          "Server=LAPTOP-90DSR0LF\SQLEXPRESS; Database=training;" +
                          "trusted_connection=yes; UID=trace; PWD=trace")

    cursor = cnxn.cursor()
    
    engine = create_engine('mssql+pyodbc://trace:trace@mydsn')
    
    username = input('Please select a username. ')
    
    result = cursor.execute("SELECT username FROM dbo.users WHERE " +
                            "username = '" + username + "'")
    
    while result.rowcount != 0:
       print('Username is unavailable.')
       username = input('Please select a username. ')
       
       result = cursor.execute("SELECT username FROM dbo.users WHERE " +
                               "username = '" + username + "'")
       
    password = input('Please select a password. ')
    
    pd.DataFrame({'username': username, 'password': password}, 
                 columns=['username', 'password'], 
                 index=[0]).to_sql(name='users', con=engine, if_exists='append', index=False)
    
    print('Signup Succesful!')
    print('You are now logged in.')
    setup = input('Since this is your first time, would you like to setup your athlete profile (y/n)? ')
    
    if setup == 'y':
        print('If you are unsure of some values or simply do not wish to add them, just press enter.')
        mass = input('Please enter your mass in pounds or kilograms. ')
        sftp = input('Please enter your swim FTP in minutes per 100 y or m. ')
        bftp = input('Please enter your bike FTP in W. ')
        rftp = input('Please enter your run FTP in minutes per mile or km. ')
        slthr = input('Please enter your swim LTHR in bpm. ')
        blthr = input('Please enter your bike LTHR in bpm. ')
        rlthr = input('Please enter your run LTHR in bpm. ')
        
        vals = [username, sftp, bftp, rftp, slthr, blthr, rlthr, mass]
        
    else:
        vals = [username, '', '', '', '', '', '', '']
        
    df = pd.DataFrame([vals], columns=['username', 'swim_ftp', 'bike_ftp', 'run_ftp', 'swim_lthr', 'bike_lthr', 'run_lthr', 'mass'])
    df.to_sql(name='athlete_data', con=engine, if_exists='replace', index=False)
        
    return username