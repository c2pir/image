# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 08:55:03 2021

@author: 46053149
"""

import numpy as np

from skimage import io
from skimage.color import rgb2gray,rgb2hsv,rgb2luv
import matplotlib.pyplot as plt

class Image(object):
    def __init__(self, file_name=None, shape=None, do_grey=False):
        self.rgb = None
        self.gray = None
        self.hsv = None
        self.cmyk = None
        
        if shape is not None:
            self.rgb = np.zeros(shape)
        
        if file_name is not None:
            self.ouvrir(file_name)
        
        if do_grey:
            self.rgb2gray()
    
    def ouvrir(self,file_name):
        """ouvre une image"""
        self.rgb = io.imread(file_name)/255.0
    
    def rgb2cmyk(self):
        """ """
        if self.rgb is not None:
            k = self.rgb.min(2) # min entre r,g et b
            
            c = 1.0-self.rgb[:,:,0]
            m = 1.0-self.rgb[:,:,1]
            y = 1.0-self.rgb[:,:,2] #(1.0-self.rgb[:,:,2]-k)/(1-k)
            self.cmyk = np.array([c,m,y,k])
            
    def rgb2gray(self):
        """ """
        if self.rgb is not None:
            self.gray = rgb2gray(self.rgb)
    
    def rgb2hsv(self):
        """ """
        if self.rgb is not None:
            self.hsv = rgb2hsv(self.rgb)

    def apply_mask(self,msk):
        """ """
        return 0

    def save(self,file_name):
        """ """
        if self.rgb is not None:
            io.imsave(file_name,self.rgb)
        
    def show(self):
        """ """
        if self.rgb is not None:
            plt.imshow(self.rgb)

