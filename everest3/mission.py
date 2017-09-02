#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
mission.py
----------

Mission or telescope-specific routines. Each mission should be a subclass
of the :py:class:`Mission` object defined below.

'''

from __future__ import division, print_function, absolute_import, unicode_literals

class Mission(object):
    '''
    A generic mission object.
    
    '''
    
    def __init__(self):
        '''
        
        '''
        
        pass
    
    @property
    def name(self):
        '''
        The mission name.
        
        '''
        
        raise NotImplementedError('This property must be implemented via subclasses.') 
    
    @property
    def path(self):
        '''
        The full path to the top-level mission data directory.
        
        '''
        
        raise NotImplementedError('This property must be implemented via subclasses.') 
        
    def download(self, target):
        '''
        Downloads the raw data for a specific target.
        
        :param target: The target identifier
        :type target: :py:obj:`float`, :py:obj:`int`, or :py:obj:`str`
        
        '''
        
        raise NotImplementedError('This method must be implemented via subclasses.')
        
    def scatter(self, time, flux):
        '''
        Computes the scatter metric for a light curve.
        
        :param array_like time: The time array
        :param array_like flux: The flux array
        :return scatter: The scatter metric for the light curve, in ppm
        :type scatter: :py:obj:`float`
        
        '''
        
        raise NotImplementedError('This method must be implemented via subclasses.')
        
        