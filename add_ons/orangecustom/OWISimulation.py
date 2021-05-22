# -*- coding: utf-8 -*-
"""
"""

import numpy as np
import Orange.data
from Orange.widgets.widget import OWWidget, Input, Output
from Orange.widgets import gui, settings
from AnyQt import QtWidgets, QtCore, QtGui
from AnyQt.QtWidgets import QStyle, QSizePolicy
from skimage.transform import resize

from orangecustom.tools.Graph import SFigure
from orangecustom.tools.Table import STable
from orangecustom.tools.DataFormatVerifications import isListOfArray
from orangecustom.specific.NodeEqualizer import create_nodes_equalizer_from

class OWISimulation(OWWidget):
    name = "Simulation"
    description = "Crée une simulation temporelle où chaque pixel a un comportement paramétrable."
    icon = "icons/simulate.png"
    priority = 10

    class Inputs:
        img = Input("Image", Orange.data.Table)
        enable = Input("Enable", Orange.data.Table)


    def __init__(self):
        super().__init__()
        self.img = None
        self.enable = None

        self.nodes = None

        #GUI
        box0 = gui.widgetBox(self.controlArea, "Shifts")
        self.in_shift_table = STable(self, title="Inputs indexes table:")
        self.out_shift_table = STable(self, title="Outputs indexes table:")
        box0.layout().addWidget(self.in_shift_table)
        box0.layout().addWidget(self.out_shift_table)

        file_button = gui.button(self.controlArea,self,"Open script", autoDefault=False)
        file_button.setIcon(self.style().standardIcon(QStyle.SP_DirOpenIcon))
        file_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        box = gui.widgetBox(self.mainArea, "Display")
        self.display = SFigure(self)
        box.layout().addWidget(self.display)



# GUI methods
    def run_simu(self):
        """Launch corresponding thread."""
        # TODO
        pass

# Orange methods
    @Inputs.img
    def set_img(self, dataset):
        self.img = dataset

    @Inputs.enable
    def set_enable(self, dataset):
        self.enable = dataset

if __name__ == "__main__":
    # https://orange3.readthedocs.io/projects/orange-development/en/latest/testing.html#running-widgets-as-scripts
    from Orange.widgets.utils.widgetpreview import WidgetPreview
    from skimage import io
    inp = io.imread("icons/simulate.png",as_gray=True)/255.0
    WidgetPreview(OWISimulation).run()