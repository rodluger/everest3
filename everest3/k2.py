#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
k2.py
-----

Routines for de-trending `K2` light curves with :py:obj:`everest3`.

'''

from __future__ import division, print_function, absolute_import, \
                       unicode_literals
from . import containers
from .constants import *
import os
import logging
log = logging.getLogger(__name__)

__all__ = ['path', 'name', 'Target']

#: The mission data directory
path = os.path.join(EVEREST_DATA_DIR, 'k2')
if not os.path.exists(path):
    os.mkdir(path)

#: The mission name
name = 'K2'

#: The time unit for the mission
time_unit = 'BJD - 2454833'

#: The magnitude string for the mission
mag_str = 'Kp'

class Target(containers.Target):
    '''
    A class that stores all the information, data, attributes, etc. for a `K2`
    target de-trended with :py:obj:`everest3`.
    
    '''
    
    def __init__(self, *args, **kwargs):
        '''
        
        '''
        
        super(Target, self).__init__(*args, **kwargs)
    
    @property
    def mission(self):
        '''
        The mission name.
        
        '''
        
        return 'K2'
    
    def download(self):
        '''
        Downloads the raw data for this target.
    
        '''
    
        raise NotImplementedError('Not yet implemented.')
        
    def scatter(self):
        '''
        Computes the scatter metric for the light curve.
    
        '''
    
        raise NotImplementedError('Not yet implemented.')