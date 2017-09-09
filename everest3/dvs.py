#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
dvs.py
------

The :py:mod:`everest3` data validation summary (DVS)-related functions.

'''

from __future__ import division, print_function, absolute_import
import matplotlib.pyplot as pl
import numpy as np
import logging
log = logging.getLogger(__name__)

#: The default DVS page layout
default_layout = (  "  0  0  0  0  0  0  0  0  0  0  0  0"
                    "  1  1  1  1  1  1  1  1  2  2  2  2"
                    "  1  1  1  1  1  1  1  1  2  2  2  2"
                    "  1  1  1  1  1  1  1  1  2  2  2  2"
                    "  1  1  1  1  1  1  1  1  2  2  2  2"
                    "  3  3  3  3  3  3  3  3  2  2  2  2"
                    "  3  3  3  3  3  3  3  3  2  2  2  2"
                    "  3  3  3  3  3  3  3  3  2  2  2  2"
                    "  3  3  3  3  3  3  3  3  2  2  2  2"
                    "  4  4  4  4  4  4  4  4  5  5  5  5"
                    "  4  4  4  4  4  4  4  4  5  5  5  5"
                    "  4  4  4  4  4  4  4  4  5  5  5  5"
                    "  4  4  4  4  4  4  4  4  5  5  5  5"
                    "  6  6  6  6  6  6  6  6  7  7  7  7"
                    "  6  6  6  6  6  6  6  6  7  7  7  7"
                    "  6  6  6  6  6  6  6  6  7  7  7  7"
                    "  6  6  6  6  6  6  6  6  7  7  7  7"
                    "  8  8  8  8  8  8  8  8  9  9  9  9"
                    "  8  8  8  8  8  8  8  8  9  9  9  9"
                    "  8  8  8  8  8  8  8  8  9  9  9  9"
                    "  8  8  8  8  8  8  8  8  9  9  9  9"
                    " 10 10 10 10 10 10 10 10 10 10 10 10"  )

class _Cell(object):
    '''
    A simple cell object containing an axis instance. Called from
    :py:class:`DVS` to create the page layout. Not user-facing.
    
    '''
    
    def __init__(self, n, x = 0, y = 0, dx = 10, dy = 10, labels = False):
        '''
        
        '''
        
        self.n = n
        self.ax = pl.subplot2grid((22, 12), (y, x), colspan = dx, rowspan = dy)
        if labels:
            self.ax.annotate('Cell #%02d' % self.n, xy = (0.5, 0.5), ha = 'center', 
                             va = 'center', fontsize = 14, alpha = 0.5,
                             fontweight = 'bold')
            self.ax.set_xticks([])
            self.ax.set_yticks([])
            for sp in ['left', 'right', 'top', 'bottom']:
                self.ax.spines[sp].set_linestyle('--')
                self.ax.spines[sp].set_alpha(0.5)
        else:
            for tick in self.ax.get_xticklabels() + self.ax.get_yticklabels():
                tick.set_fontsize(5)
class DVS(object):
    '''
    A data validation summary object. This contains a list of cells (axis
    instances) arranged according to a specified layout.

    :param str layout: A string representation of the page layout, with \
           integers corresponding to each of the cells. Default is to use \
           the string :py:obj:`default_layout` defined in this module. Note \
           that :py:obj:`layout` **must** have shape `(22, 12)` when converted\
           into a matrix. When specifying a new layout, please use the default\
           one as a template.
    :param float margins: Margin sizes in inches.
    :param bool labels: If :py:obj:`True`, adds labels to the cells in the \
           DVS for visualization. Default :py:obj:`False`.
    :param float hspace: Passed directly to :py:func:`fig.subplots_adjust()`. \
           Default :py:obj:`None`.
    :param float wspace: Passed directly to :py:func:`fig.subplots_adjust()`. \
           Default :py:obj:`None`.

    .. plot::
         :align: center
     
         from everest3.dvs import DVS
         import matplotlib.pyplot as pl
         DVS(labels = True)
         pl.show()
    
    '''
    
    def __init__(self, layout = None, margins = 0.5, labels = False,
                 hspace = 0.75, wspace = 0.75):
        '''
                
        '''

        # Letter-sized DVS
        self._fig = pl.figure(figsize = (8.5, 11))
        
        # Set the margins
        self._fig.subplots_adjust(left = margins / 8.5, 
                                  top = 1 - margins / 11., 
                                  bottom = margins / 11., 
                                  right = 1 - margins / 8.5)
        
        # Set the spacing
        self._fig.subplots_adjust(hspace = hspace, wspace = wspace)
        
        # Get the layout
        if layout is None:
            layout = default_layout
            
        # Convert to a 2D array
        layout = np.array(np.matrix(layout)).reshape(-22,12)
        
        # Create the cells
        self._cell = []
        for n in range(99):
            
            # Get the indices of this cell
            y, x = np.where(layout == n)
            if len(y) == 0:
                break
            
            # The extent of the cell
            dx = np.max(x) - np.min(x) + 1
            dy = np.max(y) - np.min(y) + 1
            
            # The upper left position of the cell
            x = np.min(x)
            y = np.min(y)
            
            # Create the cell
            self._cell.append(_Cell(n, x, y, dx, dy, labels).ax)
    
    @property
    def fig(self):
        '''
        The DVS figure instance.
        
        '''
        
        return self._fig
    
    @property
    def cell(self):
        '''
        A list of axis instances corresponding to each of the cells
        in the DVS report.
        
        '''
        
        return self._cell