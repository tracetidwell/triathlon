# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 09:25:42 2018

@author: Trace
"""

import login
import signup
import workout_analysis.athlete

option = input('Would you like to login or signup? ')

if option == 'login':
    user = login.login()
    
else:
    user = signup.signup()
    
athlete = workout_analysis.athlete.Athlete(user)
    
print('What would you like to do?')
print('Please select an option from below.')
print('1 - Edit athlete data.')
selection = input()

while int(selection) not in list(range(1, 2)):
    selection = input('Please select a valid entry. ')
    
if selection == '1':
    athlete_data.athlete_data(athlete)
