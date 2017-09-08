#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
utils.py
--------

General utility functions called from various parts of the code.

'''

from __future__ import division, print_function, absolute_import, \
     unicode_literals
import os
import sys
import traceback
import pdb
import logging
log = logging.getLogger(__name__)

class _NoPILFilter(logging.Filter):
    '''
    The :py:obj:`PIL` image module has a nasty habit of sending all sorts of 
    unintelligible information to the logger. We filter that out here.

    '''

    def filter(self, record):
        return not record.name == 'PIL.PngImagePlugin'

def _ExceptionHook(exctype, value, tb):
    '''
    A custom exception handler that logs errors to file.

    '''

    for line in traceback.format_exception_only(exctype, value):
        log.error(line.replace('\n', ''))
    for line in traceback.format_tb(tb):
        log.error(line.replace('\n', ''))
    sys.__excepthook__(exctype, value, tb)

def _ExceptionHookPDB(exctype, value, tb):
    '''
    A custom exception handler, with :py:obj:`pdb` post-mortem for debugging.

    '''

    for line in traceback.format_exception_only(exctype, value):
        log.error(line.replace('\n', ''))
    for line in traceback.format_tb(tb):
        log.error(line.replace('\n', ''))
    sys.__excepthook__(exctype, value, tb)
    pdb.pm()

def InitializeLogging(file_name = None, quiet = False, pdb = False):
    '''
    A little routine to initialize the logging functionality.

    :param str file_name: The name of the file to log to. \
           Default :py:obj:`None` (set internally by :py:mod:`everest`)

    '''
  
    # Initialize the logging
    root = logging.getLogger()
    root.handlers = []
    
    # Set the logging levels
    root.setLevel(logging.DEBUG)
    log_level = logging.DEBUG
    if quiet:
        screen_level = logging.CRITICAL
    else:
        screen_level = logging.DEBUG
    
    # File handler
    if file_name is not None:
        if not os.path.exists(os.path.dirname(file_name)):
            os.makedirs(os.path.dirname(file_name))
        fh = logging.FileHandler(file_name)
        fh.setLevel(log_level)
        fh_formatter = logging.Formatter("%(asctime)s %(levelname)-5s "
                       + "[%(name)s.%(funcName)s()]: %(message)s", 
                       datefmt="%m/%d/%y %H:%M:%S")
        fh.setFormatter(fh_formatter)
        fh.addFilter(_NoPILFilter())    
        root.addHandler(fh)

    # Screen handler
    sh = logging.StreamHandler(sys.stdout)
    if pdb:
        sh.setLevel(logging.DEBUG)
    else:
        sh.setLevel(screen_level)
        sh_formatter = logging.Formatter("%(levelname)-5s "
                       + "[%(name)s.%(funcName)s()]: %(message)s")
        sh.setFormatter(sh_formatter)
        sh.addFilter(_NoPILFilter()) 
        root.addHandler(sh)

    # Set exception hook
    if pdb:
        sys.excepthook = _ExceptionHookPDB
    else:
        sys.excepthook = _ExceptionHook