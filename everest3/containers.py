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

__all__ = ['DetrendedTimeSeries',
           'RawTimeSeries',
           'Lightcurve',
           'Target' ]

class DetrendedTimeSeries(object):
    '''
    A data container for a detrended timeseries of fluxes and flux errors.
    
    :param raw: A raw time series container.
    :type raw: :py:class:`RawTimeSeries`
    :param array_like model: The array corresponding to the linear model.
    :param array_like errors: The array of errors on the model, which will \
           be added in quadrature to the raw errors.
    
    '''
    
    def __init__(self, raw, model = None, errors = None):
        '''
        
        '''
        
        # Store the arrays
        if model is not None:
            self._model = model
        else:
            self._model = np.zeros_like(self._raw.time)
        if errors is not None:
            self._model_errors = errors
        else:
            self._model_errors = np.zeros_like(self._raw.errors)
    
    @property
    def time(self):
        '''
        The time array.
        
        '''
        
        return self._raw.time

    @property
    def model(self):
        '''
        The linear de-trending model.
        
        '''
        
        return self._model
 
    @property
    def flux(self):
        '''
        The de-trended flux array.
        
        '''
        
        return self._raw.flux - self._model   
    
    @property
    def errors(self):
        '''
        The de-trended flux errors array.
        
        '''
        
        return np.sqrt(self._raw.errors ** 2 + self._model_errors ** 2)
        
class RawTimeSeries(object):
    '''
    A **static** data container for a raw timeseries of fluxes and flux errors 
    defined on a two-dimensional postage stamp.
    
    :param array_like time: The array of times for each of the \
           observations.
    :param array_like flux3D: The raw 3D pixel postage stamps across \
           the timeseries. This is an array with dimensions \
           `(ncols, nrows, ncads)`.
    :param array_like errors3D: The raw 3D pixel postage stamp errors \
           across the timeseries. This is an array with dimensions \
           `(ncols, nrows, ncads)`.
    :param array_like aperture: A 2D binary array of shape 
           `(ncols, nrows)` with 1's corresponding  to pixels included \
           in the aperture and 0's to pixels outside the aperture.
    
    '''
    
    def __init__(self, time, aperture, flux3D, errors3D = None):
        '''
        
        '''
        
        # Store the arrays
        self._time = time
        self._aperture = aperture
        self._flux3D = flux3D
        if errors3D is not None:
            self._errors3D = errors3D
        else:
            self._errors3D = np.zeros_like(self._flux3D)
        
        # Compute simple properties
        self._npix = np.count_nonzero(self._aperture)
        self._ncols = self._flux3D.shape[0]
        self._nrows = self._flux3D.shape[1]
        self._ncads = self._flux3D.shape[2]
        
        # Indices within aperture
        ap = np.where(self._aperture & 1)
        
        # Compute the collapsed fluxes and errors
        self._flux2D = np.array([p[ap] for p in self._flux3D]) 
        self._flux = np.sum(self._flux2D, axis = 0)  
        self._errors2D = np.array([p[ap] for p in self._errors3D]) 
        self._errors = np.sqrt(np.sum(self._errors2D ** 2, axis = 0)) 
        
    @property
    def time(self):
        '''
        The time array.
        
        '''
        
        return self._time
    
    @property
    def aperture(self):
        '''
        A 2D binary array of shape `(ncols, nrows)` with 1's corresponding 
        to pixels included in the aperture and 0's to pixels outside the
        aperture.
        
        '''
        
        return self._aperture
    
    @property
    def flux3D(self):
        '''
        The raw 3D pixel postage stamps across the timeseries.
        This is an array with dimensions `(ncols, nrows, ncads)`.
        
        '''
        
        return self._flux3D

    @property
    def flux2D(self):
        '''
        The flattened pixel timeseries *within the aperture*. This
        is a 2D array with dimensions `(npix, ncads)`.
        
        '''
        
        return self._flux2D
    
    @property
    def flux(self):
        '''
        The SAP flux array, obtained by summing the fluxes in each of the
        pixels in the aperture at each cadence.
        
        '''
        
        return self._flux

    @property
    def errors3D(self):
        '''
        The raw 3D pixel postage stamp errors across the timeseries.
        This is an array with dimensions `(ncols, nrows, ncads)`.
        
        '''
        
        return self._errors3D

    @property
    def errors2D(self):
        '''
        The flattened pixel errors timeseries *within the aperture*. This
        is a 2D array with dimensions `(npix, ncads)`.
        
        '''
        
        return self._errors2D
    
    @property
    def errors(self):
        '''
        The SAP flux array, obtained by summing the errors in quadrature
        for each of the pixels in the aperture at each cadence.
        
        '''
        
        return self._errors
        
    @property
    def ncads(self):
        '''
        The number of cadences in the timeseries.
        
        '''
        
        return self._ncads

    @property
    def npix(self):
        '''
        The number of pixels within the aperture.
        
        '''
        
        return self._npix
    
    @property
    def nrows(self):
        '''
        The number of rows in the postage stamp.
        
        '''
        
        return self._nrows

    @property
    def ncols(self):
        '''
        The number of columns in the postage stamp.
        
        '''
        
        return self._ncols
        
class Lightcurve(object):
    '''
    A container for a generic light curve dataset.
    
    :param raw: A raw time series container.
    :type raw: :py:obj:`RawTimeSeries`
    :param detrended: A de-trended time series container.
    :type detrended: :py:obj:`DetrendedTimeSeries`
    
    '''
    
    def __init__(self, raw, detrended = None):
        '''
        
        '''
        
        self._raw = raw
        if detrended is not None:
            self._detrended = detrended
        else:
            self._detrended = DetrendedTimeSeries(self._raw)
    
    @property
    def raw(self):
        '''
        The raw light curve container.
        
        '''
        
        return self._raw
    
    @raw.setter
    def raw(self, val):
        self._raw = val
        self._detrended._raw = val
    
    @property
    def detrended(self):
        '''
        The de-trended light curve container.
        
        '''
        
        return self._detrended
    
class Target(object):
    '''
    A class that stores all the information, data, attributes, etc. for a star
    de-trended with :py:obj:`everest3`.
    
    '''
    
    def __init__(self, ID, season = None, mag = None, 
                 cadence = KEPLER_LONG_CADENCE):
        '''
        
        '''
        
        self.ID = ID
        self.season = season
        self.mag = mag
        self.cadence = cadence
        self.lc = Lightcurve()
    
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
        A :py:class:`Lightcurve` object containing the dataset for this target.
        
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
    