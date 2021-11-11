# -*- coding: utf-8 -*-
"""
"""

import numpy as np
import Orange.data
from Orange.widgets.widget import OWWidget, Input, Output
from Orange.widgets import gui, settings
from AnyQt import QtWidgets, QtCore, QtGui
from skimage.feature import match_template

from orangecustom.tools.OWWDisplay3D import OWWDisplay3D


class OWIFindPattern(OWWDisplay3D):
    name = "Find pattern"
    description = "Cherche un pattern dans une image"
    icon = "icons/find.png"
    priority = 10

    class Inputs:
        imgs = Input("Images", list)
        pattern = Input("Pattern", Orange.data.Table)

    class Outputs:
        result = Output("Coefficients de correlation", list)

    def __init__(self):
        super().__init__()
        self.imgs = None
        self.pattern = None
        self.index_current_img = 0

        # GUI
        self.infoa = gui.widgetLabel(self.box_info, 'No pattern yet, waiting to get something.')
        self.infob = gui.widgetLabel(self.box_info, 'No data on img yet, waiting to get something.')
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.controlArea.layout().addItem(spacerItem)

# Orange methods
    @Inputs.pattern
    def set_pattern(self, dataset):
        self.pattern = dataset
        if (dataset is not None):
            self.infoa.setText('pattern shape: {}'.format(self.pattern.X.shape))
        if self.imgs is not None:
            self.commit()

    @Inputs.imgs
    def set_imgs(self, dataset):
        self.imgs = dataset
        if (dataset is not None):
            self.infob.setText('%d instances in img dataset' % len(dataset))
        if self.pattern is not None:
            self.commit()

    def commit(self):
        """Send the outputs"""
        self.result = []
        for img in self.imgs:
            r = match_template(img, self.pattern.X, pad_input=True)
            self.result.append(r)
        self.update_display()

        self.Outputs.result.send(self.result)

if __name__ == "__main__":
    # https://orange3.readthedocs.io/projects/orange-development/en/latest/testing.html#running-widgets-as-scripts
    from Orange.widgets.utils.widgetpreview import WidgetPreview
    WidgetPreview(OWIFindPattern).run()