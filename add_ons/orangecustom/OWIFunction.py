# -*- coding: utf-8 -*-
"""
"""

import numpy as np
import Orange.data
from Orange.widgets.widget import OWWidget, Input, Output
from Orange.widgets import gui, settings
from AnyQt import QtWidgets, QtCore, QtGui
from skimage import morphology as sm #import dilation, erosion

from orangecustom.tools.OWWDisplay3D import OWWDisplay3D
from orangecustom.tools.DataFormatVerifications import isListOfArray


def rescale_range(x):
    """First line is not shown
Rescale maximum and minimum values of an array to 1 and 0

Parameters
-----
    x: numpy array

Returns
-----
    A ndarray with for each values (x-np.min(x))/(np.max(x)-np.min(x))"""
    return (x-np.min(x))/(np.max(x)-np.min(x))


def negatif(x):
    """First line is not shown
Compute negatif of a grayscale image

Parameters
-----
    x: input image

Returns
-----
    The negatif of the input with automatic rescaling of the min max
    between 0 and 1."""
    return 1.0-rescale_range(x)

function_dict = {
    "absolute": np.abs,
    "logarithm": np.log,
    "exponential": np.exp,
    "sinus": np.sin,
    "cosinus": np.cos,
    "tangent": np.tan,
    "hyperbolic tangent": np.tanh,
    "rescale range": rescale_range,
    "negatif": negatif
}


class OWIFunction(OWWDisplay3D):
    name = "Functions"
    description = "Applique une fonction A*f(a*x+b)+B pour chaque image de la liste en entrée"
    icon = "icons/function.png"
    priority = 10

    class Inputs:
        imgs = Input("Images list", list)

    class Outputs:
        result = Output("Results", list)

    A = settings.Setting(1.0)
    B = settings.Setting(0.0)
    a = settings.Setting(1.0)
    b = settings.Setting(0.0)
    selected_function = settings.Setting(0)
    automatic_propagation = settings.Setting(False)

    def __init__(self):
        super().__init__()
        self.imgs = None

        # GUI
        self.infoa = gui.widgetLabel(self.box_info, 'No data yet, waiting to get something.')

        box2 = gui.widgetBox(self.controlArea, "A*f(a*x+b)+B")
        gui.doubleSpin(box2, self, 'A', minv=-1000, maxv=1000, step=0.5, label='A:', labelWidth=30)
        gui.doubleSpin(box2, self, 'B', minv=-1000, maxv=1000, step=0.5, label='B:', labelWidth=30)
        gui.doubleSpin(box2, self, 'a', minv=-1000, maxv=1000, step=0.5, label='a:', labelWidth=30)
        gui.doubleSpin(box2, self, 'b', minv=-1000, maxv=1000, step=0.5, label='b:', labelWidth=30)
        hb1 = gui.hBox(box2)
        gui.label(hb1,self,'f:')
        self.cb_selectes_filter = gui.comboBox(hb1,self,'selected_function',
                                items=tuple([key for key in function_dict]),
                                callback=self.selection_changed,
                                searchable=True)
        self.infob = gui.widgetLabel(box2, "")#function_dict["absolute"].__doc__)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.controlArea.layout().addItem(spacerItem)

        gui.checkBox(self.buttonsArea,self,
                     'automatic_propagation',
                     'Automatic propagation',
                     callback=self.commit)

# GUI methods
    def compute(self,filter_name):
        """ Apply selected function on inputs images """
        self.result = []
        for img in self.imgs:
            r = self.A*function_dict[filter_name](self.a*img+self.b)+self.B
            self.result.append(r)

    def selection_changed(self):
        """Update function selected and update if propagation is on """
        filter_name = self.cb_selectes_filter.currentText()

        # show function description
        self.infob.setText("\n".join(function_dict[filter_name].__doc__.split("\n")[1:]))

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
    WidgetPreview(OWIFunction).run(inp)