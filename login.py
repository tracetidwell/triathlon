# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 09:32:42 2018

@author: Trace
"""

from sqlalchemy import create_engine
import pyodbc

def login():

    cnxn = pyodbc.connect("Driver={ODBC Driver 13 for SQL Server};" + 
                          "Server=LAPTOP-90DSR0LF\SQLEXPRESS; Database=training;" +
                          "trusted_connection=yes; UID=trace; PWD=trace")
    
    cursor = cnxn.cursor()
    
    
    username = input('What is your username? ')
    result = cursor.execute("SELECT username FROM dbo.users WHERE " +
                            "username = '" + username + "'")
    
    while result.rowcount == 0:
       print('Username not found.')
       username = input('Please re-enter your username. ')
       
       result = cursor.execute("SELECT username FROM dbo.users WHERE " +
                               "username = '" + username + "'")
       
    password = input('What is your password? ')
    result = cursor.execute("SELECT password FROM dbo.users WHERE " +
                            "username = '" + username + "'")
    #db_password = result.fetchone
    
    while result.fetchone()[0].split()[0] != password:
        print('Password incorrect.')
        password = input('What is your password? ')
       
        result = cursor.execute("SELECT password FROM dbo.users WHERE " +
                               "username = '" + username + "'")
        
    print('Login successful!')
    
    return username