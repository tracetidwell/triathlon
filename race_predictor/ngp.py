# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 15:54:59 2017

@author: Trace
"""

import numpy as np
import pandas as pd
from sklearn import linear_model
from sklearn.metrics import mean_squared_error

data = pd.read_csv('uphill.csv', sep=',', header=0)

X = data.values[:, :-1]
y = data.values[:, -1:]

model= linear_model.LinearRegression()

model.fit(X, y)

pred = model.predict([[1, 10+34/60, 2.3]])
ans = 9+32/60

print(pred[0][0])
print(ans)
print((ans-pred[0][0])/ans)
print(model.coef_)