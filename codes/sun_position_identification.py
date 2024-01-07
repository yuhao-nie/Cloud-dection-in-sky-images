# -*- coding: utf-8 -*-
"""
Created on Aug 6 16:41:00 2019
Revised version on Feb 12 17:26:00 2020
@author: ynie
"""

import numpy as np
from math import *
import calendar

def doy_tod_conv(date_and_time,longitude,time_zone_center_longitude):
    """
    Takes a single datetime.datetime as input. 
    Returns two values: 1st being day of year
    and 2nd being time of day solely in seconds-24 hr clock.
    """
    # Time correction. The center of PST is -120 W, while the logitude of location of interest is about 2 degree west of PST center
    pst_center_longitude = time_zone_center_longitude # minus sign indicate west longitude
    loc_longitude = longitude # minus sign indicate west longitude
    correction = np.abs(60/15*(loc_longitude - pst_center_longitude))
    min_correction = int(correction) # local time delay in minutes from the PST
    sec_correction = int((correction - min_correction)*60)  # Local time delay in seconds from the PST
    if date_and_time.minute<=min_correction:
        date_and_time= date_and_time.replace(hour = date_and_time.hour-1, minute=60+date_and_time.minute-min_correction-1, second=60-sec_correction)
    else:
        date_and_time = date_and_time.replace(minute=date_and_time.minute-min_correction-1, second=60-sec_correction)
    
    time_of_day=date_and_time.hour * 3600 + date_and_time.minute * 60 + date_and_time.second
    
    # Following piece of code calculates day of year
    months=[31,28,31,30,31,30,31,31,30,31,30,31] # days in each month
    if (date_and_time.year % 4 == 0) and (date_and_time.year % 100 != 0 or date_and_time.year % 400 ==0 ) == True:
        months[1]=29 # Modification for leap year
    day_of_year=sum(months[:date_and_time.month-1])+date_and_time.day
    
    # Fix for daylight savings (NOTE: This doesn't work for 1st hour of each day in DST period.
    # which day of year is the 2nd Sunday of March in that year
    dst_start_day = sum(months[:2]) + calendar.monthcalendar(date_and_time.year,date_and_time.month)[1][6] 
    # which day of year is the 1st Sunday of Nov in that year 
    dst_end_day = sum(months[:10]) + calendar.monthcalendar(date_and_time.year,date_and_time.month)[0][6]
    if day_of_year >= dst_start_day and day_of_year < dst_end_day:
        time_of_day=time_of_day-3600
    
    return day_of_year, time_of_day

def solar_angle(times, latitude=37.424107, longitude=-122.174199, time_zone_center_longitude=-120):
    
    """
    Calculate the solar angles (Azimuth, Zenith) for a specific location
    Input: time stamp in datetime.datetime format,
    latitude and longitude of the location of interest in degree
    time_zone_center_longitude (for local time correction): the longitude in degree for the time zone center (e.g., for pst time zone, it is -120)
    """

    day_of_year, time_of_day=doy_tod_conv(times,longitude,time_zone_center_longitude)
    latitude=radians(latitude) # Latitudinal co-ordinate of Stanford

    # Calculating parameters dependent on time, day and location, refer to the textbook by DaRosa
    alpha=2*pi*(time_of_day-43200)/86400 # Hour angle in radians
    delta=radians(23.44*sin(radians((360/365.25)*(day_of_year-80)))); # Solar declination angle
    chi=acos(sin(delta)*sin(latitude)+cos(delta)*cos(latitude)*cos(alpha))# Zenith angle of sun
    tan_xi=sin(alpha)/(sin(latitude)*cos(alpha)-cos(latitude)*tan(delta)) # tan(Azimuth angle of sun,xi)
    if alpha>0 and tan_xi>0:
        xi=pi+atan(tan_xi)
    elif alpha>0 and tan_xi<0:
        xi=2*pi+atan(tan_xi)
    elif alpha<0 and tan_xi>0:
        xi=atan(tan_xi)
    else:
        xi=pi+atan(tan_xi)
    
    return degrees(xi), degrees(chi)

def sun_position(time):
    """
    Take the time stamp of the sky image
    return the position of the sun (x, y), in Cartesian coordinates, and a binary sun mask
    For explanation of the method, refer to Figure 7 of our paper https://doi.org/10.1063/5.0014016
    or Figure 4 in README of this repository
    """
    
    # default parameters
    delta = 14.036  # the difference between geological north and sky image north
    r = 29 # radius of sky image (the circle) 
    origin_x = 29 # Cartesian coordinates of the sky image center x=29
    origin_y = 30 # Cartesian coordinates of the sky image center y=30

    # calculate
    azimuth, zenith = solar_angle(time)
    rho = zenith/90*r # polar coordinate length dimension
    theta = azimuth-delta+90 # polar coordinate degree dimension
    sun_center_x = round(origin_x-rho*sin(radians(theta)))
    sun_center_y = round(origin_y+rho*cos(radians(theta)))
    
    sun_mask = np.zeros((64,64,3),dtype=np.uint8)
    for i in range(64):
        for j in range(64):
            if (i-sun_center_x)**2+(j-sun_center_y)**2<=2**2:
                sun_mask[:,:,0][i,j]=255

    return sun_center_x, sun_center_y, sun_mask