# -*- coding: utf-8 -*-
"""

"""

import numpy as np

import Orange.data
from Orange.widgets.widget import OWWidget, Input, Output
from Orange.widgets import gui,settings

import os
from AnyQt import QtWidgets, QtCore, QtGui
from Orange.widgets.data import owfile
from skimage import io

from orangecustom.tools.OWWDisplay3D import OWWDisplay3D

class OWIRandom(OWWDisplay3D):
    name = "Random"
    description = "Crée une image random"
    icon = "icons/random.png"
    priority = 10

    class Outputs:
        gray = Output("Grayscale", list)

    #want_main_area = False
    width = settings.Setting(100)
    heigth = settings.Setting(100)
    nb_imgs = settings.Setting(1) 

    def __init__(self):
        super().__init__()

        self.result = None

        # GUI
        layout = QtWidgets.QGridLayout()
        layout.setSpacing(4)
        gui.widgetBox(self.controlArea, orientation=layout, box='Configuration')

        
        box0 = gui.hBox(None, addToLayout=False, margin=0)
        box0.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        box0.layout().addWidget(gui.widgetLabel(box0, 'Number of images:'))
        
        self.s_width = gui.spin(box0,self,"nb_imgs",1,20)
        
        box1 = gui.hBox(None, addToLayout=False, margin=0)
        box1.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        box1.layout().addWidget(gui.widgetLabel(box1, 'Choose dimentions:'))
        
        self.s_width = gui.spin(box1,self,"width",50,1024)
        self.s_height = gui.spin(box1,self,"heigth",50,1024)
        gui.toolButton(box1,self,'create',callback=self.commit)
        
        #box.layout().addWidget(self.s_width)
        layout.addWidget(box0, 0, 0)

        self.infoa = gui.widgetLabel(self, 'Output not generated.')
        layout.addWidget(box1 , 1, 0)
        layout.addItem(QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))


# Orange methods
    def commit(self):
        """Send the outputs"""
        self.result = []
        for i in range(self.nb_imgs):
            self.result.append(np.random.random((self.heigth,self.width)))
        self.Outputs.gray.send(self.result)
        self.update_display()
        self.infoa.setText('Random grayscale images created.')


if __name__ == "__main__":
    # https://orange3.readthedocs.io/projects/orange-development/en/latest/testing.html#running-widgets-as-scripts
    from Orange.widgets.utils.widgetpreview import WidgetPreview
    WidgetPreview(OWIRandom).run()