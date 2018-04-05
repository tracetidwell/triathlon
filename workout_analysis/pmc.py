# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 20:47:23 2017

@author: Trace
"""

import numpy as np
import math
import pyodbc
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

cnxn = pyodbc.connect("Driver={ODBC Driver 13 for SQL Server};" + 
                      "Server=LAPTOP-90DSR0LF\SQLEXPRESS; Database=training;" +
                      "trusted_connection=yes; UID=trace; PWD=trace")

cursor = cnxn.cursor()
activities = ['running']
result = cursor.execute("SELECT activity_id, tss, activity_type FROM dbo.summaries WHERE " +
                        "activity_type IN ('" + "', '".join(activities) + "') " + 
                        "AND activity_id >= '2017-10-24' AND activity_id <= '2017-11-15'")

tss_u = []
activity_id = []

for row in result:
    activity_id_, tss_, activity_ = row
    tss_u.append(tss_)
    activity_id.append(activity_id_)
    
tss_u = np.array(tss_u)

start = activity_id[0] - datetime.timedelta(1, 0)
days = (activity_id[-1] - start).days + 1

tss = np.zeros(days)
for i, day in enumerate(activity_id):
    pos = (day - start).days
    tss[pos] = tss_u[i]
    
ctl = np.zeros(len(tss))
atl = np.zeros(len(tss))
tsb = np.zeros(len(tss))

ctl[0] = 2
atl[0] = 1
tsb[0] = 2

nF = 42
lambdaF = math.exp(-1/nF)

nA = 7
lambdaA = math.exp(-1/nA)

for i in range(1, len(ctl)):
    ctl[i] = (tss[i] * (1 - lambdaF)) + (ctl[i-1] * lambdaF)
    atl[i] = (tss[i] * (1 - lambdaA)) + (atl[i-1] * lambdaA)
    
tsb[1:] = ctl[:-1] - atl[:-1]

dates = [start + datetime.timedelta(i, 0) for i in range(days)]

fig, ax = plt.subplots(figsize=(20,10))
par1 = ax.twinx()
par2 = ax.twinx()

ax.set_ylim(0, int(np.ceil(max(max(ctl), max(atl))/10)*10)+5)
par1.set_ylim(0, int(np.ceil(max(tss)/10)*10)+10)
par2.set_ylim(-30, 30)

ax.set_xlabel('Date')
ax.set_ylabel('CTL/ATL')
par1.set_ylabel('TSS/d')
par2.set_ylabel('TSB')

ax.set_yticks(range(0, int(np.ceil(max(max(ctl), max(atl))/10)*10+5)), 5)
par1.set_yticks(range(0, int(np.ceil(max(tss)/10)*10)+20, 10))
par2.set_yticks(range(-30, 40, 10))

ax.plot(dates, ctl, 'b')
ax.plot(dates, atl, 'pink')
par1.scatter(dates, tss, c='red', s=10)
par2.plot(dates, tsb, 'y')

par1.spines['right'].set_position(('outward', 60))

ax.set_title('PMC - {} \n {} - {}'.format(activity_, start, activity_id[-1]))

fig.savefig('test')