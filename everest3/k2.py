#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
k2.py
-----

Routines for de-trending `K2` light curves with :py:obj:`everest`.

'''

from __future__ import division, print_function, absolute_import, \
                       unicode_literals
from . import target
from .constants import *
import os
import logging
log = logging.getLogger(__name__)

__all__ = ['path', 'name', 'download', 'scatter', 'Target']

#: The mission data directory
path = os.path.join(EVEREST_DATA_DIR, 'k2')
if not os.path.exists(path):
    os.mkdir(path)

#: The mission name
name = 'K2'

class Target(target.Target):
    '''
    A class that stores all the information, data, attributes, etc. for a `K2`
    target de-trended with :py:obj:`everest`.
    
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