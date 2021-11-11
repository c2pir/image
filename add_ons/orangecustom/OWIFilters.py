# -*- coding: utf-8 -*-
"""
"""

import numpy as np
import Orange.data
from Orange.widgets.widget import OWWidget, Input, Output
from Orange.widgets import gui, settings
from AnyQt import QtWidgets, QtCore, QtGui
from skimage import filters as sf
from skimage.feature import canny
from skimage import morphology as sm #import dilation, erosion

from orangecustom.tools.OWWDisplay3D import OWWDisplay3D
from orangecustom.tools.DataFormatVerifications import isListOfArray

filters_dict = {
    "Flou - gaussian": sf.gaussian,
    "Flou - median": sf.median,
    "Laplace": sf.laplace,
    "Contours - roberts": sf.roberts,
    "Contours - sobel": sf.sobel,
    "Contours - scharr": sf.scharr,
    "Contours - canny": canny,
    "Seuil - threshold yen" : sf.threshold_yen,
    "Seuil - threshold mean" : sf.threshold_mean,
    "dilation": sm.dilation,
    "erosion": sm.erosion,
    "local minima" : sm.local_minima,
    "local maxima" : sm.local_maxima
}


class OWIFilters(OWWDisplay3D):
    name = "Filters"
    description = "Applique des filtes standarts pour chaque image de la liste en entrée"
    icon = "icons/filter.png"
    priority = 10

    class Inputs:
        imgs = Input("Liste d'images", list)

    class Outputs:
        result = Output("Liste des resultats", list)

    selected_filter = settings.Setting(0)
    automatic_propagation = settings.Setting(False)

    def __init__(self):
        super().__init__()
        self.imgs = None

        # GUI
        self.infoa = gui.widgetLabel(self.box_info, 'No data yet, waiting to get something.')

        box2 = gui.widgetBox(self.controlArea, "Filter")
        hb1 = gui.hBox(box2)
        gui.label(hb1,self,'Selection :')
        self.cb_selectes_filter = gui.comboBox(hb1,self,'selected_filter',
                                items=tuple([key for key in filters_dict]),
                                callback=self.selection_changed,
                                searchable=True)
        gui.toolButton(hb1,self,'+',tooltip="Configuration")
        self.infob = gui.widgetLabel(box2, filters_dict["Flou - gaussian"].__doc__)

        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.controlArea.layout().addItem(spacerItem)
        
        gui.checkBox(self.buttonsArea,self,
                     'automatic_propagation',
                     'Automatic propagation',
                     callback=self.commit)

# GUI methods
    def compute(self,filter_name):
        """ Apply selected filter on inputs images """
        self.result = []
        for img in self.imgs:
            r = filters_dict[filter_name](img)
            if "threshold" in filter_name:
                r = img>r
            r = 1.0*r.copy()
            self.result.append(r)

    def selection_changed(self):
        """Update filter selected and update if propagation is on """
        filter_name = self.cb_selectes_filter.currentText()

        # show filter description
        self.infob.setText(filters_dict[filter_name].__doc__)
        #print(self.selected_filter)

        self.compute(filter_name)
        # afficher
        self.update_display()

        self.commit()

# Orange methods
    @Inputs.imgs
    def set_imgs(self, dataset):
        if isListOfArray(dataset):
            self.imgs = dataset
            if (dataset is not None):
                self.infoa.setText('%d instances in input dataset' % len(dataset))
                self.selection_changed()
            self.clear_messages()
        else:
            self.warning("Wrong input, it must be a list of numpy arrays")

    def commit(self):
        """Send the outputs"""
        if self.automatic_propagation:
            #print("propagate")
            self.Outputs.result.send(self.result)


if __name__ == "__main__":
    # https://orange3.readthedocs.io/projects/orange-development/en/latest/testing.html#running-widgets-as-scripts
    from Orange.widgets.utils.widgetpreview import WidgetPreview
    from skimage import io
    inp = [io.imread("icons/find.png",as_gray=True)/255.0,
           io.imread("icons/selection.png",as_gray=True)/255.0]
    WidgetPreview(OWIFilters).run(inp)