# -*- coding: utf-8 -*-
"""
"""

import numpy as np
import Orange.data
from Orange.widgets.widget import OWWidget, Input, Output
from Orange.widgets import gui, settings
from AnyQt import QtWidgets, QtCore, QtGui

from orangecustom.tools.OWWDisplay3D import OWWDisplay3D
from orangecustom.tools.DataFormatVerifications import isListOfArray

class OWIResize(OWWDisplay3D):
    name = "Resize"
    description = "Applique des redimensions à une liste d'image"
    icon = "icons/resize.png"
    priority = 10

    class Inputs:
        imgs = Input("Images", list)

    class Outputs:
        result = Output("Resized images", list)

    selected_resize_type = settings.Setting(0)

    def __init__(self):
        super().__init__()
        self.imgs = None
        self.result = None
        self.saved_config = []

        # GUI
        self.infoa = gui.widgetLabel(self.box_info, 'No data yet, waiting to get something.')

        # TODO checkbox auto

        box2 = gui.widgetBox(self.controlArea, "Custom")
        self.info_shape = gui.widgetLabel(box2, 'Original shape: ')
        hl0 = gui.hBox(box2)
        gui.label(hl0, self, "Desired shape:")
        self.sp_w = QtWidgets.QSpinBox(self) # gui.spin(hl0, self, 'desired_width', minv=1, maxv=5000, step=1)
        self.sp_h = QtWidgets.QSpinBox(self) #self.sp_h = gui.spin(hl0, self, 'desired_height', minv=1, maxv=5000, step=1)
        self.sp_w.setMinimum(1)
        self.sp_h.setMinimum(1)
        #self.sp_w.valueChanged.connect(self.on_value_change)
        #self.sp_h.valueChanged.connect(self.on_value_change)
        hl0.layout().addWidget(self.sp_w)
        hl0.layout().addWidget(self.sp_h)

        gui.radioButtons(box2,self,'selected_resize_type',["Crop top left","Crop center","Resize"])

        gui.toolButton(box2,self,"Apply and save current settings",callback=self.do_save_conf)

# GUI methods
    def init_default_config(self):
        self.saved_config = []
        for img in self.imgs:
            d = {"selected_resize_type":0,
                 "desired_width":img.shape[1],
                 "desired_height":img.shape[0]}
            self.saved_config.append(d)

    def do_save_conf(self):
        conf = self.saved_config[self.index_current_img]
        conf["desired_width"] = self.sp_w.value()
        conf["desired_height"] = self.sp_h.value()
        conf["selected_resize_type"] = self.selected_resize_type

    def on_img_change(self):
        img = self.imgs[self.index_current_img]
        conf = self.saved_config[self.index_current_img]
        self.info_shape.setText("Original shape: {}".format(img.shape))
        self.sp_w.setMaximum(img.shape[1])
        self.sp_w.setValue(conf["desired_width"])
        self.sp_h.setMaximum(img.shape[0])
        self.sp_h.setValue(conf["desired_height"])
        self.selected_resize_type = conf["selected_resize_type"]


# Orange methods
    @Inputs.imgs
    def set_imgs(self, dataset):
        if isListOfArray(dataset):
            self.imgs = dataset
            self.init_default_config()
            self.commit()
        else:
            self.warning("Wrong input, it must be a list of numpy arrays")

    def commit(self):
        """Send the outputs"""
        self.result = self.imgs
        self.Outputs.result.send(self.result)
        self.update_display()

if __name__ == "__main__":
    # https://orange3.readthedocs.io/projects/orange-development/en/latest/testing.html#running-widgets-as-scripts
    from Orange.widgets.utils.widgetpreview import WidgetPreview
    from skimage import io
    inp = [io.imread("icons/find.png",as_gray=True)/255.0,
           io.imread("icons/selection.png",as_gray=True)/255.0]
    WidgetPreview(OWIResize).run(inp)