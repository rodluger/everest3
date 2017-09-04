#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
constants.py
------------

General constants used throughout the code.

'''

from __future__ import division, print_function, absolute_import, \
                       unicode_literals
from . import __version__
import os
import six
from six.moves import urllib
import logging
log = logging.getLogger(__name__)

#: Alias for the :py:obj:`everest` version number
EVEREST_VERSION = __version__

#: The major.minor version number
EVEREST_MAJOR_MINOR = ".".join(EVEREST_VERSION.split(".")[:-1])

#: The top-level :py:obj:`everest` data directory
EVEREST_DATA_DIR = os.path.expanduser(os.environ.get("EVEREST3_DATA_DIR", os.path.join("~", ".everest3")))                               
if not os.path.exists(EVEREST_DATA_DIR):
    os.mkdir(EVEREST_DATA_DIR)

#: The :py:mod:`everest3` source code directory
EVEREST_SRC_DIR = os.path.dirname(os.path.abspath(__file__))

#: Kepler/K2 long cadence in seconds
KEPLER_LONG_CADENCE =  (1800./86400.)

#: Kepler/K2 short cadence in seconds
KEPLER_SHORT_CADENCE = (60./86400.)