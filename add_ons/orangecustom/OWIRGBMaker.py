# -*- coding: utf-8 -*-
"""
"""

import numpy as np
import Orange.data
from Orange.widgets.widget import OWWidget, Input, Output
from Orange.widgets import gui, settings
from AnyQt import QtWidgets, QtCore, QtGui

from orangecustom.tools.Graph import SFigure


class OWIRGBMaker(OWWidget):
    name = "RGB builder"
    description = "Construit une image à partir des nuances de rouge, bleu et vert."
    icon = "icons/rgb.png"
    priority = 10

    class Inputs:
        red = Input("Rouges", Orange.data.Table)
        green = Input("Verts", Orange.data.Table)
        blue = Input("Bleus", Orange.data.Table)


    def __init__(self):
        super().__init__()
        self.red = None
        self.green = None
        self.blue = None
        self.rgb = None

        # GUI
        box = gui.widgetBox(self.controlArea, "Info")
        self.infor = gui.widgetLabel(box, 'No red data yet, waiting to get something.')
        self.infog = gui.widgetLabel(box, 'No green data yet, waiting to get something.')
        self.infob = gui.widgetLabel(box, 'No blue data yet, waiting to get something.')
        gui.toolButton(box,self,'Compose RGB image',callback=self.compose)

        box2 = gui.widgetBox(self.mainArea, "Display")
        self.display = SFigure(self)
        box2.layout().addWidget(self.display)

    def compose(self):
        """TODO"""
        if (self.red is not None) and \
            (self.green is not None) and \
            (self.blue is not None):
            # check dimensions
            if (self.red.X.shape == self.green.X.shape) and (self.red.X.shape == self.blue.X.shape):
                n,m = self.red.X.shape
                r = np.zeros((n,m,3))
                r[:, :, 0] = self.red.X
                r[:, :, 1] = self.green.X
                r[:, :, 2] = self.blue.X
                self.rgb = r
                self.display.draw3D(self.rgb)
                self.clear_messages()
            else:
                self.warning("Red, green and blue images havn't the same shape: {} {} {}".format(self.red.X.shape,
                                                                                                self.green.X.shape,
                                                                                                self.blue.X.shape))

# Orange methods
    @Inputs.red
    def set_red(self, dataset):
        self.red = dataset
        if dataset is not None:
            self.infor.setText("red shape: {}".format(dataset.X.shape))

    @Inputs.green
    def set_green(self, dataset):
        self.green = dataset
        if dataset is not None:
            self.infog.setText("green shape: {}".format(dataset.X.shape))

    @Inputs.blue
    def set_blue(self, dataset):
        self.blue = dataset
        if dataset is not None:
            self.infob.setText("blue shape: {}".format(dataset.X.shape))

if __name__ == "__main__":
    # https://orange3.readthedocs.io/projects/orange-development/en/latest/testing.html#running-widgets-as-scripts
    from Orange.widgets.utils.widgetpreview import WidgetPreview
    WidgetPreview(OWIRGBMaker).run()