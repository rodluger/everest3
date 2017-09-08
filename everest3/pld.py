#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
pld.py
------

The :py:mod:`everest3` core PLD de-trending functions.

'''

from __future__ import division, print_function, absolute_import, \
                       unicode_literals
import numpy as np
import logging
log = logging.getLogger(__name__)

def detrend(target, **kwargs):
    '''
    De-trend a light curve with PLD.
    
    :param target: The target to de-trend
    :type target: :py:class:`everest3.containers.Target`
    
    '''
    
    # Do the de-trending here here.
    
    # Assign the model
    target.model = np.zeros_like(target.time)