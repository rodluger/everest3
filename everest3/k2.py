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
import sys
import numpy as np
import kplr
client = kplr.API()
from kplr.config import KPLR_ROOT
try:
    import pyfits
except ImportError:
    try:
        import astropy.io.fits as pyfits
    except ImportError:
        raise Exception('Please install the `pyfits` package.')
import logging
log = logging.getLogger(__name__)

__all__ = ['path', 'name', 'time_unit', 'mag_str', 'Target']

@property
def _url(self):
    '''
    This is a :py:obj:`kplr` hack. The current version of the package (0.2.2) 
    doesn't support campaigns above 0 because of this function, so let's 
    replace it.

    '''
    
    base_url = "http://archive.stsci.edu/pub/k2/"
    if self.ktc_k2_id < 201000000:
        base_url += "{0}/c%d/200000000/{1:05d}/{2}" % self.sci_campaign
    else:
        base_url += ("{{0}}/c%d/{0}/{{1:05d}}/{{2}}" % self.sci_campaign) \
            .format(int(int(self.ktc_k2_id * 1e-5) * 1e5))
    return base_url.format(self.product,
                           int(int(int(self.kepid[-5:][-5:])*1e-3)*1e3),
                           self._filename)
kplr.api.K2TargetPixelFile.url = _url

#: The mission data directory
path = os.path.join(EVEREST_DATA_DIR, 'k2')
if not os.path.exists(path):
    os.makedirs(path)

#: The mission name
name = 'K2'

#: The time unit for the mission
time_unit = 'BJD - 2454833'

#: The flux unit for the mission
flux_unit = 'e-/s'

#: The magnitude string for the mission
mag_str = 'Kp'

#: The catalog identifier for the mission
ID_str = 'EPIC'

class _NoWarnings():
    '''
    A context manager to temporarily disable all logging
    warnings. Useful for overriding :py:obj:`kplr` warnings.
    
    '''
    
    def __init__(self):
        pass
        
    def __enter__(self):
        logging.disable(logging.CRITICAL)
        
    def __exit__(self, type, value, traceback):
        logging.disable(logging.NOTSET)

class Target(containers.Target):
    '''
    A class that stores all the information, data, attributes, etc. for a `K2`
    target de-trended with :py:obj:`everest3`.
    
    :param bool clobber_raw: Overwrite existing raw light curve? \
           Default :py:obj:`False`.
    
    '''
    
    def __init__(self, *args, **kwargs):
        '''
        
        '''
        
        # User options
        self.clobber_raw = kwargs.get('clobber_raw', False)
        
        # Initialize parent class
        super(Target, self).__init__(*args, **kwargs)

    @property
    def mission(self):
        '''
        The mission module (this module, :py:mod:`k2`).
        
        '''
        
        return sys.modules[__name__]
    
    @property
    def season(self):
        '''
        The K2 campaign number for this target.
        
        '''
        
        # Do we need to figure out the campaign number for this target?
        if self._season is None:
            with _NoWarnings():
                star = client.k2_star(self.ID)
                tpfs = star.get_target_pixel_files(fetch = False)
                self._season = tpfs[0].sci_campaign
       
        return self._season
    
    @season.setter
    def season(self, value):
        self._season = value
    
    @property
    def path(self):
        '''
        The full path to the directory where data is stored for this target.
        
        '''
        
        target_path = os.path.join(path, 'c%02d' % self.season, 
                                  ('%09d' % self.ID)[:4] + '00000', 
                                  ('%09d' % self.ID)[4:])
        
        if not os.path.exists(target_path):
            os.makedirs(target_path)
        
        return target_path
        
    def get_raw_data(self):
        '''
        Downloads the raw data for this target.
    
        '''
        
        # Get the raw target pixel file path
        tpf = os.path.join(KPLR_ROOT, 'data', 'k2', 'target_pixel_files', 
                           str(self.ID), 'ktwo%09d-c%02d_lpd-targ.fits.gz'
                           % (self.ID, self.season))
        
        # Download the file if necessary
        if (self.clobber_raw) or (not os.path.exists(tpf)):
            log.info('Downloading raw data...')
            with _NoWarnings():
                star = client.k2_star(self.ID)
                tpfs = star.get_target_pixel_files(fetch = True)
        
        # Read the TPF
        with pyfits.open(tpf) as f:
            tpf_data = f[1].data
        
        # Set the magnitude (TODO)
        self.mag = np.nan
        
        # Store the data in the raw light curve container
        time = np.array(tpf_data.field('TIME'), dtype='float64')
        flux = np.array(tpf_data.field('FLUX'), dtype='float64')
        error = np.array(tpf_data.field('FLUX_ERR'), dtype='float64')
        self.raw = containers.TimeSeries(time, flux, error)
        
    def get_aperture(self):
        '''
        Computes the optimal aperture for this target.
    
        '''
        
        log.info('Computing the optimal aperture...')
        self.aperture = np.ones((self.raw.ncols, self.raw.nrows), 
                                dtype = 'int32')