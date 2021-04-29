# -*- coding: utf-8 -*-
"""
TODO obsolete
"""

import numpy as np
import Orange.data
from Orange.widgets.widget import OWWidget, Input, Output
from Orange.widgets import gui, settings
from AnyQt import QtWidgets, QtCore, QtGui
from orangecustom.tools.Graph import SFigure

class OWISobel(OWWidget):
    name = "Sobel"
    description = "Calculs l'opérateur de Sobel pour chaque image de la liste en entrée"
    icon = "icons/sobel.png"
    priority = 10

    class Inputs:
        imgs = Input("Liste d'images", list)

    class Outputs:
        result = Output("Liste d'images traitées", list)

    #want_main_area = False

    def __init__(self):
        super().__init__()
        self.imgs = None
        self.sobel = None

        # GUI
        box = gui.widgetBox(self.controlArea, "Info")
        self.infoa = gui.widgetLabel(box, 'No data on msk yet, waiting to get something.')
        self.infob = gui.widgetLabel(box, '...')

        box2 = gui.widgetBox(self.mainArea,"Display")
        self.display = SFigure(self)
        box2.layout().addWidget(self.display)

    @Inputs.imgs
    def set_imgs(self, dataset):
        self.imgs = dataset
        if (dataset is not None):
            self.infoa.setText('%d instances in img dataset' % len(dataset))
            self.commit()

    def commit(self):
        """Send the outputs"""

        self.sobel = []
        for img in self.imgs:
            sob = (np.roll(img.copy(), 1, axis=0) + np.roll(img.copy(), -1, 0) - 2 * img.copy()) ** 2
            sob += (np.roll(img.copy(), 1, axis=1) + np.roll(img.copy(), -1, 1) - 2 * img.copy()) ** 2
            sob = sob**0.5
            self.sobel.append(sob)

        if len(self.sobel)>0:
            self.display.clear()
            self.display.draw3D(self.sobel[0])

        self.Outputs.result.send(list(self.sobel))

if __name__ == "__main__":
    # https://orange3.readthedocs.io/projects/orange-development/en/latest/testing.html#running-widgets-as-scripts
    from Orange.widgets.utils.widgetpreview import WidgetPreview
    from skimage import io
    inp = [io.imread("icons/find.png",as_gray=True)/255.0]
    WidgetPreview(OWISobel).run(inp)