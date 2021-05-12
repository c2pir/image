# -*- coding: utf-8 -*-
"""
"""

import numpy as np
import Orange.data
from Orange.widgets.widget import OWWidget, Input, Output
from Orange.widgets import gui, settings
from AnyQt import QtWidgets, QtCore, QtGui

from orangecustom.tools.OWWDisplay3D import OWWDisplay3D

class OWIHadamard(OWWDisplay3D):
    name = "Alpha"
    description = "Applique une couche alpha à une liste d'image"
    icon = "icons/alpha.png"
    priority = 10

    class Inputs:
        weight = Input("Tableau de pondération", Orange.data.Table)
        imgs = Input("Images", list)

    class Outputs:
        result = Output("Produit de Hadamard", list)


    def __init__(self):
        super().__init__()
        self.weight = None
        self.imgs = None
        self.result = None

        # GUI
        # checkbox auto
        # checkbox normalisé

    @Inputs.weight
    def set_weight(self, dataset):
        self.weight = dataset
        if self.imgs is not None:
            self.commit()

    @Inputs.imgs
    def set_imgs(self, dataset):
        self.imgs = dataset
        if self.weight is not None:
            self.commit()

    def commit(self):
        """Send the outputs"""
        alpha = self.weight.X
        self.result = []
        for img in self.imgs:
            if img.shape==alpha.shape:
                self.result.append(alpha * img)
        self.Outputs.result.send(self.result)