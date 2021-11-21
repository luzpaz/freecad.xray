#***************************************************************************
#*                                                                         *
#*   Copyright (c) 2011, 2016 Jose Luis Cercos Pita <jlcercos@gmail.com>   *
#*                                                                         *
#*   This program is free software; you can redistribute it and/or modify  *
#*   it under the terms of the GNU Lesser General Public License (LGPL)    *
#*   as published by the Free Software Foundation; either version 2 of     *
#*   the License, or (at your option) any later version.                   *
#*   for detail see the LICENCE text file.                                 *
#*                                                                         *
#*   This program is distributed in the hope that it will be useful,       *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
#*   GNU Library General Public License for more details.                  *
#*                                                                         *
#*   You should have received a copy of the GNU Library General Public     *
#*   License along with this program; if not, write to the Free Software   *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
#*   USA                                                                   *
#*                                                                         *
#***************************************************************************

import FreeCAD
import numpy as np


AIRPORT_COLORS = {'red':   ((0.0, 1.0, 1.0),
                            (0.5, 0.0, 0.0),
                            (1.0, 1.0, 1.0)),
                  'green': ((0.0, 1.0, 1.0),
                            (0.5, 0.0, 0.0),
                            (1.0, 0.5, 0.5)),
                  'blue':  ((0.0, 1.0, 1.0),
                            (0.5, 0.5, 0.5),
                            (1.0, 0.0, 0.0))}
try:
    from matplotlib.colors import LinearSegmentedColormap
    airport_cmap = LinearSegmentedColormap(
        'airport', segmentdata=AIRPORT_COLORS, N=256)
except ImportError:
    airport_cmap = 'PuRd'
CMAPS = ['gray', 'binary', airport_cmap]


class Plot(object):
    def __init__(self, xray):
        self.plt = None
        try:
            from FreeCAD.Plot import Plot
        except ImportError:
            try:
                from freecad.plot import Plot
            except ImportError:
                FreeCAD.Console.PrintWarning(
                    'Plot module is disabled, so I cannot perform the plot\n')
                return

        self.xray = xray
        self.aspect = (xray.ChamberHeight / xray.ChamberRadius).Value
        self.plt = Plot.figure("Radiography")
        self.plt.update()
        self.cbar = None

    def update(self, img, cmap_index=0, vmin=0.0, vmax=1.0):
        if not self.plt:
            return
        self.plt.axes.clear()
        if self.cbar is not None:
            self.cbar.remove()
        cmin, cmax = np.min(img), np.max(img)
        vmin = cmin + vmin * (cmax - cmin)
        vmax = cmin + vmax * (cmax - cmin)
        plt_img = self.plt.axes.imshow(
            img, cmap=CMAPS[cmap_index], vmin=vmin, vmax=vmax,
            aspect=self.aspect, origin='lower')
        self.cbar = self.plt.fig.colorbar(plt_img)
        self.plt.update()
