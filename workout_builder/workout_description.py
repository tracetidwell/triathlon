# -*- coding: utf-8 -*-
"""
Created on Thu Jul  6 21:54:34 2017

@author: Trace
"""



dist = 'olympic'
ph = 'build1'
disc = 'bike'
sess = 'all'

sess = sess + '.txt'

filename = '\\'.join(['distance', dist, ph, disc, sess])
session = open(filename, 'r')
print(session.read())
