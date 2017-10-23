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
                    "  1  1  1  1  1  1  1  1  6  6  7  7"
                    "  1  1  1  1  1  1  1  1  6  6  7  7"
                    "  1  1  1  1  1  1  1  1  6  6  7  7"
                    "  1  1  1  1  1  1  1  1  6  6  7  7"
                    "  2  2  2  2  2  2  2  2  8  8  9  9"
                    "  2  2  2  2  2  2  2  2  8  8  9  9"
                    "  2  2  2  2  2  2  2  2  8  8  9  9"
                    "  2  2  2  2  2  2  2  2  8  8  9  9"
                    "  3  3  3  3  3  3  3  3 10 10 10 10"
                    "  3  3  3  3  3  3  3  3 10 10 10 10"
                    "  3  3  3  3  3  3  3  3 11 11 11 11"
                    "  3  3  3  3  3  3  3  3 11 11 11 11"
                    "  4  4  4  4  4  4  4  4 12 12 12 12"
                    "  4  4  4  4  4  4  4  4 12 12 12 12"
                    "  4  4  4  4  4  4  4  4 13 13 13 13"
                    "  4  4  4  4  4  4  4  4 13 13 13 13"
                    "  5  5  5  5  5  5  5  5 14 14 14 14"
                    "  5  5  5  5  5  5  5  5 14 14 14 14"
                    "  5  5  5  5  5  5  5  5 15 15 15 15"
                    "  5  5  5  5  5  5  5  5 15 15 15 15"
                    " 16 16 16 16 16 16 16 16 16 16 16 16"  )

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
            self.ax.tick_params(direction = 'in')
            
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
    :param float margin_left: Left margin sizes in inches.
    :param float margin_right: Right margin sizes in inches.
    :param float margin_top: Top margin sizes in inches.
    :param float margin_bottom: bottom margin sizes in inches.
    :param bool labels: If :py:obj:`True`, adds labels to the cells in the \
           DVS for visualization. Default :py:obj:`False`.
    :param float hspace: Passed directly to :py:func:`fig.subplots_adjust()`. \
           Default :py:obj:`None`.
    :param float wspace: Passed directly to :py:func:`fig.subplots_adjust()`. \
           Default :py:obj:`None`.
    :param int header: The cell index corresponding the header. Default `0`.
    :param int footer: The cell index corresponding the footer. Default `-1`.
    :param int detrended: The cell index corresponding the detrended light \
           curve. Default `1`.
    :param int raw: The cell index corresponding the raw light curve. \
           Default `2`.
           
    .. plot::
         :align: center
     
         from everest3.dvs import DVS
         import matplotlib.pyplot as pl
         DVS(labels = True)
         pl.show()
    
    '''
    
    def __init__(self, layout = None, margin_left = 0.5, margin_right = 0.5,
                 margin_top = 0.25, margin_bottom = 0.1, labels = False,
                 hspace = 1.25, wspace = 1.25, header = 0, footer = -1,
                 detrended = 1, raw = 2):
        '''
                
        '''

        # Letter-sized DVS
        self._fig = pl.figure(figsize = (8.5, 11))
        
        # Set the margins
        self._fig.subplots_adjust(left = margin_left / 8.5, 
                                  top = 1 - margin_top / 11., 
                                  bottom = margin_bottom / 11., 
                                  right = 1 - margin_right / 8.5)
        
        # Set the spacing
        self._fig.subplots_adjust(hspace = hspace, wspace = wspace)
        
        # Get the layout
        if layout is None:
            layout = default_layout
            
        # Convert to a 2D array
        layout = np.array(np.matrix(str(layout))).reshape(-22,12)
                
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
        
        # Special cell indices
        self._header = header
        self._footer = footer
        self._raw = raw
        self._detrended = detrended
        self.header.axis('off')
        self.footer.axis('off')
        
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
    
    @property
    def header(self):
        '''
        The header cell.
        
        '''
        
        return self._cell[self._header]
    
    @property
    def footer(self):
        '''
        The footer cell.
        
        '''
        
        return self._cell[self._footer]

    @property
    def raw(self):
        '''
        The raw light curve cell.
        
        '''
        
        return self._cell[self._raw]

    @property
    def detrended(self):
        '''
        The de-trended light curve cell.
        
        '''
        
        return self._cell[self._detrended]