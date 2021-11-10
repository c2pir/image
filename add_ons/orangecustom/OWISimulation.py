# -*- coding: utf-8 -*-
"""
"""

import numpy as np
import Orange.data
from Orange.widgets.widget import OWWidget, Input, Output
from Orange.widgets import gui, settings
from AnyQt import QtWidgets, QtCore, QtGui
from AnyQt.QtWidgets import QStyle, QSizePolicy
import imageio

#from orangecustom.tools.Graph import SFigure
#from orangecustom.tools.Table import STable
from orangecustom.tools.OWWDisplay3D import OWWDisplay3D
from orangecustom.tools.DataFormatVerifications import isListOfArray
from orangecustom.specific.NodeEqualizer import create_nodes_equalizer_from

class OWISimulation(OWWDisplay3D):
    name = "Simulation ED"
    description = "Crée une simulation spatio-temporelle paramétrable."
    icon = "icons/simulate.png"
    priority = 10

    class Inputs:
        img = Input("Initial image", Orange.data.Table)
        coeff = Input("ED coefficient", Orange.data.Table)
        dirichet = Input("Dirichlet conditions", Orange.data.Table)

    dirichlet_mode = settings.Setting(0)
    dt = settings.Setting(0.1)
    dl = settings.Setting(0.5)
    nb_iterations = settings.Setting(10)

    def __init__(self):
        super().__init__()
        self.img = None
        self.coeff = None
        self.dirichet = None
        self.in_dirichet = None

        #GUI
        box_cond = gui.widgetBox(self.controlArea, "Dirichlet conditions")
        gui.radioButtons(box_cond, self, 'dirichlet_mode',
                         ["from input","framework", "center"],
                         callback = self.get_dirichlet)

        box_param = gui.widgetBox(self.controlArea, "Parameters")
        gui.doubleSpin(box_param, self, 'dt', minv=0.000001, maxv=2.0, step=0.01, decimals=5, label='dt:', labelWidth=30)
        gui.doubleSpin(box_param, self, 'dl', minv=0.000001, maxv=2.0, step=0.01, label='dl:', labelWidth=30)
        gui.spin(box_param, self, 'nb_iterations', minv=1, maxv=1000, step=5, label='nb. iterations:', labelWidth=80)

        gui.toolButton(self.controlArea,self,"Run",callback=self.commit)
        gui.toolButton(self.controlArea,self,"Save as gif",callback=self.save_as_gif)

        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.controlArea.layout().addItem(spacerItem)



# GUI methods
    def run_simu(self):
        """ """
        coeffs = self.coeff.X
        self.result = [self.img.X]
        img = self.img.X.copy()
        for i in range(self.nb_iterations):
            r = 0
            for coeff in coeffs:
                shifted = np.roll(img, coeff[0], 0)
                shifted = np.roll(shifted, int(coeff[1]), 1)
                r += coeff[3]*(self.dl**coeff[2])*shifted
            tmp = img.copy() + self.dt*r.copy()
            
            # TODO dirichet conditions
            img = tmp*(1-self.dirichet)+img.copy()*self.dirichet
            
            self.result.append(img.copy())
            
        self.index_current_img = len(self.result)-1
        pass


    def get_dirichlet(self):
        if self.dirichlet_mode==0:
            self.dirichet = self.in_dirichet

        if self.dirichlet_mode==1:
            self.dirichet = np.zeros_like(self.img.X)
            self.dirichet[0,:]=1
            self.dirichet[-1,:]=1
            self.dirichet[:,0]=1
            self.dirichet[:,-1]=1
        
        if self.dirichlet_mode==2:
            # TODO
            pass


    def save_as_gif(self):
        # TODO open folder
        filename = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', '', "Animation (*.gif)")
        if filename!="":
            imageio.mimsave(filename, self.result)

# Orange methods
    @Inputs.img
    def set_img(self, dataset):
        self.img = dataset

    @Inputs.coeff
    def set_coeff(self, dataset):
        self.coeff = dataset

    @Inputs.dirichet
    def set_dirichet(self, dataset):
        if self.dirichlet_mode==0:
            self.in_dirichet = dataset.X

    def commit(self):
        """Send the outputs"""
        self.get_dirichlet()
        
        if (self.coeff is None) or (self.img is None) or (self.dirichet is None):
            return
        
        
        self.run_simu()
        
        self.update_display()
        #self.Outputs.result.send(self.result)

if __name__ == "__main__":
    # https://orange3.readthedocs.io/projects/orange-development/en/latest/testing.html#running-widgets-as-scripts
    from Orange.widgets.utils.widgetpreview import WidgetPreview
    WidgetPreview(OWISimulation).run()