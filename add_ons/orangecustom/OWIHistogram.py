# -*- coding: utf-8 -*-
"""
"""

import numpy as np
import Orange.data
from Orange.widgets.widget import OWWidget, Input, Output
from Orange.widgets import gui, settings
from AnyQt import QtWidgets, QtCore, QtGui

from orangecustom.tools.Graph import SFigure

class OWIHistogram(OWWidget):
    name = "Histogram"
    description = "Calculs les histogrammes pour chaque image de la liste en entrée"
    icon = "icons/histogram.png"
    priority = 10

    class Inputs:
        imgs = Input("Liste d'images", list)

    class Outputs:
        hist = Output("Liste des histogrammes", list)

    #want_main_area = False

    def __init__(self):
        super().__init__()
        self.imgs = None

        # GUI
        box = gui.widgetBox(self.controlArea, "Info")
        self.infoa = gui.widgetLabel(box, 'No data yet, waiting to get something.')
        self.infob = gui.widgetLabel(box, '...')

        box2 = gui.widgetBox(self.mainArea,"Display")
        self.display = SFigure(self)
        box2.layout().addWidget(self.display)

# Orange methods
    @Inputs.imgs
    def set_imgs(self, dataset):
        self.imgs = dataset
        if (dataset is not None):
            self.infoa.setText('%d instances in input dataset' % len(dataset))
            self.commit()

    def commit(self):
        """Send the outputs"""
        r = []
        cpt = 0
        self.display.clear()
        for img in self.imgs:
            data = img.ravel()
            N = int(len(data)**0.5)+1
            N = min(N,250)
            histo,edges = np.histogram(data,bins = N)
            histo = (1.0*histo)/np.sum(histo)
            r.append((histo,edges))
            self.display.draw2D(edges[:-1],histo,label="*{}".format(cpt))
            cpt += 1

        self.Outputs.hist.send(r)

if __name__ == "__main__":
    # https://orange3.readthedocs.io/projects/orange-development/en/latest/testing.html#running-widgets-as-scripts
    from Orange.widgets.utils.widgetpreview import WidgetPreview
    from skimage import io
    inp = [io.imread("icons/find.png",as_gray=True)/255.0]
    WidgetPreview(OWIHistogram).run(inp)