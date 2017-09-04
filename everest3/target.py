#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
target.py
---------

Defines the :py:class:`Target` class for all :py:obj:`everest` light curves.

'''

from __future__ import division, print_function, absolute_import, \
                       unicode_literals
from . import pld
from .constants import *
import logging
log = logging.getLogger(__name__)

class Target(object):
    '''
    A class that stores all the information, data, attributes, etc. for a star
    de-trended with :py:obj:`everest`.
    
    '''
    
    def __init__(self, ID, season = None, mag = None, 
                 cadence = KEPLER_LONG_CADENCE):
        '''
        
        '''
        
        self.ID = ID
        self.season = season
        self.mag = mag
        self.cadence = cadence
    
    @property
    def mission(self):
        '''
        The mission name.
        
        '''
        raise NotImplementedError('Must be defined via subclasses.')
    
    @property
    def ID(self):
        '''
        A :py:obj:`str` or :py:obj:`int` identifier for this target.
        
        '''
        
        return self._ID
    
    @ID.setter
    def ID(self, value):
        self._ID = value

    @property
    def season(self):
        '''
        An :py:obj:`int` or :py:obj:`float` season/quarter/campaign identifier for this target.
        
        '''
        
        return self._season
    
    @season.setter
    def season(self, value):
        self._season = value
    
    @property
    def mag(self):
        '''
        A :py:obj:`float` corresponding to the magnitude of this target in the mission band.
        
        '''
        
        return self._mag
    
    @mag.setter
    def mag(self, value):
        self._mag = value

    @property
    def cadence(self):
        '''
        A :py:obj:`float` corresponding to the observation cadence in seconds.
        
        '''
        
        return self._cadence
    
    @cadence.setter
    def cadence(self, value):
        self._cadence = value
    
    def detrend(self, *args, **kwargs):
        '''
        De-trend the light curve via :py:func:`everest.pld.detrend()`.
        
        '''
        
        pld.detrend(self, *args, **kwargs)
    