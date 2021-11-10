# -*- coding: utf-8 -*-
"""
"""

import numpy as np
import Orange.data
from Orange.widgets.widget import OWWidget, Input, Output
from Orange.widgets import gui, settings
from AnyQt import QtWidgets, QtCore, QtGui

from orangecustom.tools.Graph import SFigure
from orangecustom.tools.DataFormatVerifications import isListOfArray


class OWISelection(OWWidget):
    name = "Select"
    description = "Permet de sélectionner une parties des images en entrées"
    icon = "icons/selection.png"
    priority = 10

    class Inputs:
        imgs = Input("Images", list, multiple=True)

    class Outputs:
        result = Output("Images selectionnées", list)
        selection = Output("Dernière selection", Orange.data.Table)

    automatic_propagation = settings.Setting(False)
    controlAreaVisible = False

    def __init__(self):
        super().__init__()
        self.imgs = {}
        self.selection = None
        self.result = None

        # GUI
        box = gui.widgetBox(self.controlArea, "Info",margin=3)
        self.infoa = gui.widgetLabel(box, 'No data yet, waiting to get something.')

        self.controlArea.layout().addItem(QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))
        gui.checkBox(self.buttonsArea,self,
                     'automatic_propagation',
                     'Automatic propagation',
                     callback=self.commit)

        box2 = gui.widgetBox(self.mainArea, "Display")
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
        #print(item.text())
        self.result = []

        # construct image list
        l_imgs = []
        for key in self.imgs:
            l_imgs += self.imgs[key]

        # get selected images
        for itm in self.lv_images.selectedItems():
            index = self.lv_images.row(itm)
            self.result.append(l_imgs[index])

        index = self.lv_images.row(item)
        s = l_imgs[index]

        self.display.clear()
        self.display.draw3D(s)

        self.selection = Orange.data.table.Table.from_numpy(None, s)
        self.commit()

    def update_listview(self):
        """Update content of self.lv_images from self.imgs list."""
        cpt = 0
        self.lv_images.clear()
        for key in self.imgs:
            imgs = self.imgs[key]
            for img in imgs:
                self.lv_images.addItem("img{} shape: {}".format(cpt, img.shape))
                cpt += 1

# Orange methods
    @Inputs.imgs
    def set_imgs(self, dataset, id):
        if (dataset is not None):
            if isListOfArray(dataset):
                self.imgs[id[0]] = dataset
                self.infoa.setText('%d instances in img dataset' % len(self.imgs))
            else:
                self.warning("Input must be a list of numpy array")
        else:
            # remove corresponding input
            if id[0] in self.imgs:
                del self.imgs[id[0]]

        self.update_listview()

    def commit(self):
        """Send the outputs"""
        if self.automatic_propagation:
            self.Outputs.result.send(self.result)
            self.Outputs.selection.send(self.selection)

if __name__ == "__main__":
    # https://orange3.readthedocs.io/projects/orange-development/en/latest/testing.html#running-widgets-as-scripts
    from Orange.widgets.utils.widgetpreview import WidgetPreview
    from skimage import io
    inp = None# ([io.imread("icons/find.png",as_gray=True)/255.0,
    #       io.imread("icons/selection.png",as_gray=True)/255.0,
    #       io.imread("icons/image_reader.png",as_gray=True)/255.0],(0,"",None))
    WidgetPreview(OWISelection).run(inp)