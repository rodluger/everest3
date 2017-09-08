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
import numpy as np
import kplr
from kplr.config import KPLR_ROOT
client = kplr.API()
try:
    import pyfits
except ImportError:
    try:
        import astropy.io.fits as pyfits
    except ImportError:
        raise Exception('Please install the `pyfits` package.')
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
    
    @property
    def season(self):
        '''
        The K2 campaign number for this target.
        
        '''
        
        if self._season is None:
            raise NotImplementedError('TODO: Automatically figure out the campaign number here.')
        else:
            return self._season
    
    @season.setter
    def season(self, value):
        self._season = value
    
    def download(self, clobber = False):
        '''
        Downloads the raw data for this target.
    
        '''
        
        # Get the raw target pixel file path
        tpf = os.path.join(KPLR_ROOT, 'data', 'k2', 'target_pixel_files', 
                           str(self.ID), 'ktwo%09d-c%02d_lpd-targ.fits.gz'
                           % (self.ID, self.season))
        
        # Download the file if necessary
        if (clobber) or (not os.path.exists(tpf)):
        
            # HACK: Temporarily disable logging to
            # suppress `kplr` warning messages and
            # download the target pixel files
            
            logging.disable(logging.CRITICAL)
            star = client.k2_star(self.ID)
            tpfs = star.get_target_pixel_files(fetch = True)
            logging.disable(logging.NOTSET)
        
        # Read the TPF
        with pyfits.open(tpf) as f:
            tpf_data = f[1].data
        
        # Store the data in the light curve
        time = np.array(tpf_data.field('TIME'), dtype='float64')
        flux = np.array(tpf_data.field('FLUX'), dtype='float64')
        error = np.array(tpf_data.field('FLUX_ERR'), dtype='float64')
        self.lightcurve = containers.TimeSeries(time, flux, error)
        
    def scatter(self):
        '''
        Computes the scatter metric for the light curve.
    
        '''
    
        raise NotImplementedError('Not yet implemented.')