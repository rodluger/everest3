#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
test_k2.py
----------

'''

from __future__ import division, print_function, absolute_import, unicode_literals
import everest3

def test_k2():
    '''
    Test K2 light curve downloading and de-trending
    
    '''
    
    star = everest3.k2.Target(205071984)
    star.detrend()
    star.plot_dvs()