# -*- coding: utf-8 -*-
"""
Created on Sat Aug 10 16:55:00 2019
@author: ynie
"""

import numpy as np
import os
import matplotlib.pyplot as plt
from sun_position_identification import *

def cloud_detection(time, image, csl_time=None):
    
    """
    Take inputs of sky image and its assoicated time
    identify the cloud pixels in the sky image
    return the cloud cover (defined as the fraction of cloud pixels within a sky image)
    and a binary cloud mask
    """
    ### Load clear sky library
    if csl_time == None:
        proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        clear_sky_library_path = os.path.join(proj_path, 'data','clear_sky_library')
        csl_time = np.load(os.path.join(clear_sky_library_path,'csl_times.npy'),allow_pickle=True)
        csl_image = np.load(os.path.join(clear_sky_library_path,'csl_images.npy'),allow_pickle=True)
        csl_sun_center = np.load(os.path.join(clear_sky_library_path,'csl_sun_center.npy'),allow_pickle=True)
        csl_sun_center_x = csl_sun_center[:,0]
        csl_sun_center_y = csl_sun_center[:,1]
    
    ### Sun position in the original image
    sun_center_x, sun_center_y, sun_mask = sun_position(time)
    
    ### Match the image in CSL based on similar sun position
    dist_sun_center = np.sqrt((csl_sun_center_x-sun_center_x)**2+(csl_sun_center_y-sun_center_y)**2)
    match_csl_image = csl_image[np.argmin(dist_sun_center)]
    
    ### Modified threshold method to detect cloud
    NRBR_orig = np.divide((image[:,:,0].astype(int)-image[:,:,2].astype(int)),(image[:,:,0].astype(int)+image[:,:,2].astype(int)))
    NRBR_cs = np.divide((match_csl_image[:,:,0].astype(int)-match_csl_image[:,:,2].astype(int)),(match_csl_image[:,:,0].astype(int)+match_csl_image[:,:,2].astype(int)))
    d_NRBR = np.abs(NRBR_orig-NRBR_cs)
    cloud = np.zeros((64,64),dtype=int)

    for i in range(64):
        for j in range(64):
            if (i-29)**2+(j-30)**2<=29**2:
                if (d_NRBR[i,j] >= 0.175):
                    cloud[i,j] = 1
                    
    unique, counts = np.unique(cloud, return_counts=True)
    try:
        cloud_cover = dict(zip(unique, counts))[1]/int(pi*29**2)
    except:
        cloud_cover = 0
    
    if (cloud_cover>=0.045) and (cloud_cover<0.35):
        cloud = np.zeros((64,64),dtype=int)
        for i in range(64):
            for j in range(64):
                if (i-29)**2+(j-30)**2<=29**2:
                    if (i-sun_center_x)**2+(j-sun_center_y)**2>=7**2:
                        if NRBR_orig[i,j] <= 0.05:
                            cloud[i,j] = 1
    
    if (cloud_cover>=0.35):
        cloud = np.zeros((64,64),dtype=int)
        for i in range(64):
            for j in range(64):
                if (i-29)**2+(j-30)**2<=29**2:
                    if NRBR_orig[i,j] <= 0.05:
                        cloud[i,j] = 1
    
    unique, counts = np.unique(cloud, return_counts=True)
    try:
        cloud_cover = dict(zip(unique, counts))[1]/int(pi*29**2)
    except:
        cloud_cover = 0
    
    ### Cloud mask
    cloud_mask = np.zeros((64,64,3),dtype=np.uint8)
    cloud_mask[:,:,1] = 255 * cloud
        
    return cloud_cover, cloud_mask, sun_mask