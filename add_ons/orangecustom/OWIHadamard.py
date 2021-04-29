# -*- coding: utf-8 -*-
"""
TODO obsolete
"""

import numpy as np
import Orange.data
from Orange.widgets.widget import OWWidget, Input, Output
from Orange.widgets import gui, settings
from AnyQt import QtWidgets, QtCore, QtGui


class OWIHadamard(OWWidget):
    name = "Hadamard product"
    description = "Multiplie 2 tableaux de même dimension terme à terme"
    icon = "icons/multiply.png"
    priority = 10

    class Inputs:
        weight = Input("Tableau de pondération", Orange.data.Table)
        in_table = Input("Tableau d'entrée", Orange.data.Table)

    class Outputs:
        result = Output("Produit de Hadamard", Orange.data.Table)


    def __init__(self):
        super().__init__()
        self.weight = None
        self.in_table = None
        self.result = None

        # GUI
        # checkbox auto
        # checkbox normalisé

    @Inputs.weight
    def set_weight(self, dataset):
        self.weight = dataset
        if self.in_table is not None:
            self.commit()

    @Inputs.in_table
    def set_in_table(self, dataset):
        self.in_table = dataset
        if self.weight is not None:
            self.commit()

    def commit(self):
        """Send the outputs"""
        r = self.weight.X * self.in_table.X
        self.result = Orange.data.table.Table.from_numpy(None,r)
        self.Outputs.result.send(self.result)