# -*- coding: utf-8 -*-
"""
"""

import numpy as np
import Orange.data
from Orange.widgets.widget import OWWidget, Input, Output
from Orange.widgets import gui, settings
from AnyQt import QtWidgets, QtCore, QtGui
from skimage.transform import resize

from orangecustom.tools.OWWInteract3D import OWWInteract3D
from orangecustom.tools.DataFormatVerifications import isListOfArray

class OWICut(OWWInteract3D):
    name = "Cut"
    description = "Applique des redimensions à une liste d'image"
    icon = "icons/cut.png"
    priority = 10

    class Inputs:
        imgs = Input("Images", list)

    class Outputs:
        result = Output("Resized images", list)

    def __init__(self):
        super().__init__()

        # GUI TODO

# Orange methods
    @Inputs.imgs
    def set_imgs(self, dataset):
        if isListOfArray(dataset):
            pass

    def commit(self):
        """Send the outputs"""
        pass

if __name__ == "__main__":
    # https://orange3.readthedocs.io/projects/orange-development/en/latest/testing.html#running-widgets-as-scripts
    from Orange.widgets.utils.widgetpreview import WidgetPreview
    from skimage import io
    inp = [io.imread("icons/find.png",as_gray=True)/255.0,
           io.imread("icons/selection.png",as_gray=True)/255.0]
    WidgetPreview(OWICut).run(inp)