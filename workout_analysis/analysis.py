# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 18:10:54 2017

@author: Trace
"""

import db_tables
from sqlalchemy import create_engine
import pyodbc
import os
from athlete import Athlete

trace = Athlete(70, 2, 180, '08:30', 150, 162, 174)

os.chdir('sessions')
files = [file for file in os.listdir() if os.path.isfile(file)]

for file in files:

    session, summary = db_tables.db_tables(file, trace)
    print(summary)
    
    #os.rename(file, 'added/' + file)

    conn = pyodbc.connect(r'DSN=mydsn;UID=trace;PWD=trace')
    engine = create_engine('mssql+pyodbc://trace:trace@mydsn')
    
    #session.to_sql(name='sessions', con=engine, if_exists='append', index=False)
    summary.to_sql(name='summaries', con=engine, if_exists='append', index=False)