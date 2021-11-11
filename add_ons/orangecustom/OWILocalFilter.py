# -*- coding: utf-8 -*-
"""
"""

import numpy as np
import Orange.data
from Orange.widgets.widget import OWWidget, Input, Output
from Orange.widgets import gui, settings
from AnyQt import QtWidgets, QtCore, QtGui

from orangecustom.tools.OWWDisplay3D import OWWDisplay3D


class OWILocalFilter(OWWDisplay3D):
    name = "Convolution"
    description = "Fait le produit de convolution entre une image et un masque"
    icon = "icons/convolution.png"
    priority = 10

    class Inputs:
        img = Input("Images", list)
        msk = Input("Masque", Orange.data.Table)

    class Outputs:
        result = Output("Produits de convolution", list)


    center_x = settings.Setting(0)
    center_y = settings.Setting(0)

    def __init__(self):
        super().__init__()
        self.imgs = None
        self.msk = None

        # GUI
        self.infoa = gui.widgetLabel(self.box_info, 'No data yet, waiting to get something.')

        optionsBox = gui.widgetBox(self.controlArea, "Mask center")
        hl0 = gui.hBox(optionsBox)
        gui.label(hl0,self,'shift x')
        gui.spin(hl0, self, 'center_x', minv=0, maxv=1000, step=1)
        hl1 = gui.hBox(optionsBox)
        gui.label(hl1, self, 'shift y')
        gui.spin(hl1, self, 'center_y', minv=0, maxv=1000, step=1)
        gui.toolButton(optionsBox,self,"Refresh",callback=self.commit)
        
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.controlArea.layout().addItem(spacerItem)

# Orange methods
    @Inputs.msk
    def set_msk(self, dataset):
        self.msk = dataset
        if self.imgs is not None:
            self.commit()

    @Inputs.img
    def set_imgs(self, dataset):
        self.imgs = dataset
        if self.msk is not None:
            self.commit()

    def commit(self):
        """Send the outputs"""
        msk = self.msk.X
        self.result = []
        for img in self.imgs:
            r = 0
            for i in range(msk.shape[0]):
                for j in range(msk.shape[1]):
                    si, sj = (i-self.center_y), (j-self.center_x)
                    shifted = np.roll(img.copy(), si, 0)
                    shifted = np.roll(shifted, sj, 1)
                    r += msk[i,j]*shifted.copy()
            self.result.append(r)

        self.update_display()

        self.Outputs.result.send(self.result)

if __name__ == "__main__":
    # https://orange3.readthedocs.io/projects/orange-development/en/latest/testing.html#running-widgets-as-scripts
    from Orange.widgets.utils.widgetpreview import WidgetPreview
    WidgetPreview(OWILocalFilter).run()