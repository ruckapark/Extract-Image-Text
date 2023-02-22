# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 11:24:45 2023

Function to change datetime to string for ffmpeg crop

@author: George
"""

import datetime

def strfdelta(tdelta, fmt = "{hours}:{minutes}:{seconds}"):
    d = {}
    days = tdelta.days
    d["hours"], rem = divmod(tdelta.seconds, 3600)
    d["hours"] = d["hours"] + 24*days
    d["minutes"], d["seconds"] = divmod(rem, 60)
    
    #2 sf
    for key in [*d]:
        d[key] = str(d[key])
        if len(d[key]) < 2:
            d[key] = '0{}'.format(d[key])
            
    return fmt.format(**d)

if __name__ == '__main__':
    
    #test examples
    print(strfdelta(datetime.timedelta(days = 0,hours = 0,minutes = 0,seconds = 0)))
    print(strfdelta(datetime.timedelta(days = 0,hours = 1,minutes = 0,seconds = 0)))
    print(strfdelta(datetime.timedelta(days = 0,hours = 1,minutes = 1,seconds = 1)))
    print(strfdelta(datetime.timedelta(days = 1,hours = 0,minutes = 0,seconds = 0)))
    print(strfdelta(datetime.timedelta(days = 2,hours = 0,minutes = 0,seconds = 0)))
    print(strfdelta(datetime.timedelta(days = 0,hours = 20,minutes = 0,seconds = 0)))
    print(strfdelta(datetime.timedelta(days = 0,hours = 20,minutes = 0,seconds = 45)))
    print(strfdelta(datetime.timedelta(days = 0,hours = 20,minutes = 500,seconds = 0)))
    print(strfdelta(datetime.timedelta(days = 3,hours = 21,minutes = 50,seconds = 0)))
    print(strfdelta(datetime.timedelta(days = 3,hours = 21,minutes = 5,seconds = 40)))
    print(strfdelta(datetime.timedelta(days = 3,hours = 0,minutes = 0,seconds = 40)))
    print(strfdelta(datetime.timedelta(days = 3,hours = 0,minutes = 0,seconds = 400)))