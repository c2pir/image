# -*- coding: utf-8 -*-
"""
Created on Mon Dec 03 09:15:10 2018

    cmapP=matplotlib.cm.jet

@author: 46053149
"""

import matplotlib
try:
    from PyQt5 import QtCore, QtGui, QtWidgets
    matplotlib.use('Qt5Agg')
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
except:
    from PyQt4 import QtCore, QtGui
    QtWidgets=QtGui
    matplotlib.use('Qt4Agg')
    from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.backends.backend_qt4 import NavigationToolbar2QT as NavigationToolbar

from matplotlib.figure import Figure

#from matplotlib.patches import Polygon
#from matplotlib.collections import PatchCollection

import numpy as np

from Orange.widgets.widget import OWComponent,OWWidget


class CustomNavigationToolbar( NavigationToolbar ):
    picked=QtCore.pyqtSignal(int,name='picked')

    def __init__(self, canvas, parent):
        NavigationToolbar.__init__(self,canvas,parent)
        self.clearButtons=[]
        # Search through existing buttons
        nextB=None
        
        not_in = ('Subplots','Customize')
        
        for c in self.findChildren(QtWidgets.QToolButton):
            if nextB is None:
                nextB=c
            # Don't want to see subplots and customize
            if str(c.text()) in not_in:
                c.defaultAction().setVisible(False)
                continue
            # Need to keep track of pan and zoom buttons
            # Also grab toggled event to clear checked status of picker button
            if str(c.text()) in ('Pan','Zoom'):
                self.clearButtons.append(c)
                nextB=None

    def pickerToggled(self, checked):
        if checked:            
            if self._active == "PAN":
                self.pan()
            elif self._active == "ZOOM":
                self.zoom()
            self.set_message('Reject/use observation')

class SFigure(QtWidgets.QWidget,OWComponent):
    def __init__(self, parent: OWWidget = None):
        QtWidgets.QWidget.__init__(self,parent)
        OWComponent.__init__(self,parent)

        self.parent = parent
        
        # Create the mpl Figure and FigCanvas objects. 5x4 inches, 100 dots-per-inch
        self.dpi = 100
        self.fig = Figure((5.0, 4.0), dpi=self.dpi)
        self.fig.subplots_adjust(left=0.12, bottom=0.07, right=0.98, top=0.98)
        
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self)
        self.canvas.mpl_connect('button_release_event',self.onRelease)
        self.canvas.mpl_connect('motion_notify_event',self.onMouseMove)
        self.canvas.mpl_connect('button_press_event',self.onPress)
        
        self.axes = self.fig.add_subplot(111)
        
        # Create the navigation toolbar, tied to the canvas
        self.mpl_toolbar = CustomNavigationToolbar(self.canvas, self) #♥NavigationToolbar
        
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.mpl_toolbar)
        vbox.addWidget(self.canvas)
        self.setLayout(vbox)   
        self.layout().setContentsMargins(0, 0, 0, 0)
    
    
    def draw3D(self,data):
        self.axes.clear()
        self.axes.imshow(data) #pcolormesh(X,Y,img)
        #self.axes.update_datalim([[0,0],[len(img),len(img[0])]])
        self.canvas.draw()

    def clear(self):
        self.axes.clear()

    def draw2D(self,*data,**kwargs):
        self.axes.plot(*data,**kwargs) #,label = self.label)
        self.axes.legend()
        self.canvas.draw()
        
    
    def onPress(self,event):
        pass
    
    def onMouseMove(self,event):
        pass
    
    def onRelease(self,event):
        pass