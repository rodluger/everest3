#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Version
__version__ = "3.0.0"
__author__ = "Rodrigo Luger (rodluger@uw.edu)"
__copyright__ = "Copyright 2017 Rodrigo Luger"

# Was everest3 imported from setup.py?
try:
  __EVEREST3_SETUP__
except NameError:
  __EVEREST3_SETUP__ = False

if not __EVEREST3_SETUP__:
    
    # Main modules
    from . import constants
    from . import containers
    from . import pld
    from . import utils
    
    # Mission modules
    from . import k2