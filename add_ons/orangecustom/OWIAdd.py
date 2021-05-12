# -*- coding: utf-8 -*-
"""
"""

import numpy as np
import Orange.data
from Orange.widgets.widget import OWWidget, Input, Output
from Orange.widgets import gui, settings
from AnyQt import QtWidgets, QtCore, QtGui

from orangecustom.tools.DataFormatVerifications import isListSameShape
from orangecustom.tools.Graph import SFigure

class OWIAdd(OWWidget):
    name = "Add"
    description = "Additionne des mages de même dimensions terme à terme"
    icon = "icons/add.png"
    priority = 10

    class Inputs:
        imgs = Input("Liste d'mages", list)

    class Outputs:
        result = Output("Somme", Orange.data.Table)

    want_main_area = False

    def __init__(self):
        super().__init__()
        self.imgs = None
        self.result = None

        #GUI
        box2 = gui.widgetBox(self.controlArea, "Display")
        hb = gui.hBox(box2)
        self.display = SFigure(self)
        hb.layout().addWidget(self.display)
        self.lv_images = QtWidgets.QListWidget(self)
        self.lv_images.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.lv_images.itemClicked.connect(self.on_selection)
        hb.layout().addWidget(self.lv_images)

# GUI methods
    def on_selection(self, item):
        """Image list selection callback."""
        self.commit()


    def update_listview(self):
        """Update content of self.lv_images from self.imgs list."""
        cpt = 0
        self.lv_images.clear()
        for img in self.imgs:
            self.lv_images.addItem("img{} shape: {}".format(cpt, img.shape))
            cpt += 1

# Orange methods
    @Inputs.imgs
    def set_imgs(self, dataset):
        self.imgs = dataset
        self.update_listview()
        if isListSameShape(dataset): # verification same shape
            self.clear_messages()
            self.commit()
        else:
            self.warning("Images in inputs have not all the same size")

    def commit(self):
        """Send the outputs"""
        r = 0
        for itm in self.lv_images.selectedItems():
            s = self.imgs[self.lv_images.row(itm)]
            r += s

        # TODO add normalisation option

        self.display.clear()
        if len(self.lv_images.selectedItems()) != 0:
            self.display.draw3D(r)
            self.result = Orange.data.table.Table.from_numpy(None, r)
            self.Outputs.result.send(self.result)