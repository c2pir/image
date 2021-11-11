# -*- coding: utf-8 -*-
"""
"""

import numpy as np
import Orange.data
from Orange.widgets.widget import OWWidget, Input, Output
from Orange.widgets import gui, settings
from AnyQt import QtWidgets, QtCore, QtGui
from orangecustom.tools.Graph import SFigure


class OWIGenerator(OWWidget):
    name = "Image generator"
    description = "Crée une image à partir d'une équation."
    icon = "icons/math.png"
    priority = 10

    class Outputs:
        result = Output("Result", Orange.data.Table)

    expr = settings.Setting("x+y")
    width = settings.Setting(100)
    heigth = settings.Setting(100)

    def __init__(self):
        super().__init__()
        self.result = None

        #GUI
        box = gui.widgetBox(self.mainArea, "Display")
        self.display = SFigure(self)
        box.layout().addWidget(self.display)
        
        box_param = gui.widgetBox(self.controlArea, "Parameters")
        gui.label(box_param, self, 'Note: x is between 0 and 1, \nand y domain is given by the ratio height/width. \nGray level is given by the expression f.')
        gui.spin(box_param, self, 'width', minv=3, maxv=2000, step=10, label='width:', labelWidth=50)
        gui.spin(box_param, self, 'heigth', minv=3, maxv=2000, step=10, label='heigth:', labelWidth=50)
        gui.lineEdit(box_param, self, 'expr', label="f(x,y) =", labelWidth=50)

        gui.toolButton(self.controlArea,self,"Create grayscale image",callback=self.commit)

        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.controlArea.layout().addItem(spacerItem)



# GUI methods
    def compute(self):
        """ """
        f = eval("lambda x, y: "+str(self.expr))
        ym = float(self.heigth)/float(self.width)
        x,y = np.meshgrid(np.linspace(0,1,self.width), np.linspace(0,ym,self.heigth))
        
        z = f(x,y)
        
        self.display.clear()
        self.display.draw3D(z)
        
        self.result = Orange.data.table.Table.from_numpy(None, z)


# Orange methods
    def commit(self):
        """Send the outputs"""
        self.compute()
        self.Outputs.result.send(self.result)

if __name__ == "__main__":
    # https://orange3.readthedocs.io/projects/orange-development/en/latest/testing.html#running-widgets-as-scripts
    from Orange.widgets.utils.widgetpreview import WidgetPreview
    WidgetPreview(OWIGenerator).run()