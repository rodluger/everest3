#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
containers.py
-------------

Defines classes to store information about targets and their light curves.

'''

from __future__ import division, print_function, absolute_import, \
                       unicode_literals
from . import pld
from .constants import *
import numpy as np
import logging
log = logging.getLogger(__name__)

__all__ = [ 'TimeSeries',
            'Target' ]

class TimeSeries(object):
    '''
    A data container for a generic photometric timeseries defined on a postage
    stamp.
    
    '''
    
    def __init__(self, time = np.empty((0,), dtype = 'float64'), 
                 flux = np.empty((0,0,0,), dtype = 'float64'), 
                 error = None):
        '''
        
        '''
        
        # Store the arrays
        self.time = time
        self.flux = flux
        if error is not None:
            self.error = error
        else:
            self.error = np.zeros_like(self.flux)
    
    def __repr__(self):
        '''
        
        '''
        
        return "<Timeseries of %d fluxes on a %d x %d pixel postage stamp>" % (self.ncads, self.ncols, self.nrows)
    
    @property
    def time(self):
        '''
        The time array.
        
        '''
        
        return self._time
    
    @time.setter
    def time(self, val):
        self._time = val
    
    @property
    def flux(self):
        '''
        The flux array, shape `(ncads, ncols, nrows)`.
        
        '''
        
        return self._flux  

    @flux.setter
    def flux(self, val):
        assert len(val.shape) == 3, "Parameter `flux` must have shape `(ncads, ncols, nrows)`."
        self._flux = val
    
    @property
    def error(self):
        '''
        The flux errors array shape `(ncads, ncols, nrows)`.
        
        '''
        
        return self._error

    @error.setter
    def error(self, val):
        assert len(val.shape) == 3, "Parameter `error` must have shape `(ncads, ncols, nrows)`."
        self._error = val

    @property
    def ncols(self):
        '''
        The number of columns in the postage stamp.
        
        '''
        
        return self._flux.shape[1]
    
    @property
    def nrows(self):
        '''
        The number of rows in the postage stamp.
        
        '''
        
        return self._flux.shape[2]

    @property
    def ncads(self):
        '''
        The number of columns in the postage stamp.
        
        '''
        
        return self._flux.shape[0]
    
    def pixel_flux(self, aperture = None):
        '''
        The array of pixel fluxes within an aperture.
        
        :param ndarray aperture: A 2D :py:obj:`numpy` array of integers of \
               dimensions `(ncols, nrows)` with 1's corresponding  to pixels \
               included in the aperture and 0's to pixels outside the aperture.
        
        :returns: A 2D pixel flux array of shape `(ncads, npix)`
        
        '''
        
        # If no aperture, assume it's entire postage stamp
        if aperture is None:
            aperture = np.ones((self.ncols, self.nrows), dtype = 'int32')
        
        # Get the indices
        ap = np.where(aperture & 1)
        
        # Collapse the flux array
        return np.array([p[ap] for p in self.flux])

    def pixel_error(self, aperture = None):
        '''
        The array of pixel flux errors within an aperture.
        
        :param ndarray aperture: A 2D :py:obj:`numpy` array of integers of \
               dimensions `(ncols, nrows)` with 1's corresponding  to pixels \
               included in the aperture and 0's to pixels outside the aperture.
        
        :returns: A 2D pixel flux errors array of shape `(ncads, npix)`
        
        '''
        
        # If no aperture, assume it's entire postage stamp
        if aperture is None:
            aperture = np.ones((self.ncols, self.nrows), dtype = 'int32')
        
        # Get the indices
        ap = np.where(aperture & 1)
        
        # Collapse the flux array
        return np.array([p[ap] for p in self.error])
   
    def sap_flux(self, aperture = None):
        '''
        The simple aperture photometry flux.
        
        :param ndarray aperture: A 2D :py:obj:`numpy` array of integers of \
               dimensions `(ncols, nrows)` with 1's corresponding  to pixels \
               included in the aperture and 0's to pixels outside the aperture.
        
        :returns: An 1D SAP flux array of shape `(ncads)`
        
        '''
        
        # Sum the pixels
        return np.nansum(self.pixel_flux(aperture), axis = 0)

    def sap_error(self, aperture = None):
        '''
        The simple aperture photometry flux errors.
        
        :param ndarray aperture: A 2D :py:obj:`numpy` array of integers of \
               dimensions `(ncols, nrows)` with 1's corresponding  to pixels \
               included in the aperture and 0's to pixels outside the aperture.
        
        :returns: An 1D SAP flux errors array of shape `(ncads)`
        
        '''
        
        # Sum the errors in quadrature
        return np.sqrt(np.nansum(self.pixel_error(aperture) ** 2, axis = 0))      

class Target(object):
    '''
    A class that stores all the information, data, attributes, etc. for a star
    de-trended with :py:obj:`everest3`.
    
    '''
    
    def __init__(self, ID, season = None, mag = None, 
                 cadence = KEPLER_LONG_CADENCE, lightcurve = None):
        '''
        
        '''
        
        self.ID = ID
        self.season = season
        self.mag = mag
        self.cadence = cadence
        if lightcurve is not None:
            self.lightcurve = lightcurve
        else:
            self.lightcurve = TimeSeries()
    
    def __repr__(self):
        '''
        
        '''
        
        return "<%s Target: %s>" % (self.mission, self.ID)
    
    # ------------------
    # Generic properties
    # ------------------
    
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
        An :py:obj:`int` or :py:obj:`float` season/quarter/campaign 
        identifier for this target.
        
        '''
        
        return self._season
    
    @season.setter
    def season(self, value):
        self._season = value
    
    @property
    def mag(self):
        '''
        A :py:obj:`float` corresponding to the magnitude of this target 
        in the mission band.
        
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

    # ------------------
    # Light curve stuff
    # ------------------
    
    @property
    def lightcurve(self):
        '''
        A :py:class:`TimeSeries` object containing the dataset for this target.
        
        '''
        
        return self._lightcurve
    
    @lightcurve.setter
    def lightcurve(self, value):
        self._lightcurve = value
    
    # ------------------
    # Main functions
    # ------------------
    
    def detrend(self, *args, **kwargs):
        '''
        De-trend the light curve via :py:func:`everest3.pld.detrend()`.
        
        '''
        
        pld.detrend(self, *args, **kwargs)

    def download(self):
        '''
        Downloads the raw data for this target.
    
        '''
    
        raise NotImplementedError('Must be implemented via subclasses.')
        
    def scatter(self):
        '''
        Computes the scatter metric for the light curve.
    
        '''
    
        raise NotImplementedError('Must be implemented via subclasses.')
    