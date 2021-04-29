# -*- coding: utf-8 -*-
"""
"""

import numpy as np
import Orange.data
from Orange.widgets.widget import OWWidget, Input, Output
from Orange.widgets import gui, settings
from AnyQt import QtWidgets, QtCore, QtGui


class OWIMean(OWWidget):
    name = "Mean"
    description = "Calculs les moyennes pour chaque image de la liste en entrée"
    icon = "icons/mean.png"
    priority = 10

    class Inputs:
        imgs = Input("Liste d'images", list)

    class Outputs:
        result = Output("Table des moyennes", Orange.data.Table)

    want_main_area = False

    def __init__(self):
        super().__init__()
        self.result = None
        self.imgs = None

        # GUI
        box = gui.widgetBox(self.controlArea, "Info")
        self.infoa = gui.widgetLabel(box, 'No data yet, waiting to get something.')

        self.tw_results = QtWidgets.QTableWidget(self)
        self.tw_results.setColumnCount(1)
        box.layout().addWidget(self.tw_results)

# Orange methods
    @Inputs.imgs
    def set_imgs(self, dataset):
        self.imgs = dataset
        if (dataset is not None):
            self.infoa.setText('%d instances in input dataset' % len(dataset))
            self.tw_results.setRowCount(len(dataset))
            self.commit()

    def commit(self):
        """Send the outputs"""
        r = []
        i = 0
        for img in self.imgs:
            mean = np.mean(img)
            r.append(mean)
            self.tw_results.setCellWidget(i,0,QtWidgets.QLabel("{}".format(mean)))
            i += 1
        r = np.array([r]).T

        self.result = Orange.data.table.Table.from_numpy(None,r)
        self.Outputs.result.send(self.result)

if __name__ == "__main__":
    # https://orange3.readthedocs.io/projects/orange-development/en/latest/testing.html#running-widgets-as-scripts
    from Orange.widgets.utils.widgetpreview import WidgetPreview
    WidgetPreview(OWIMean).run()