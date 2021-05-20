# -*- coding: utf-8 -*-
"""
"""

import numpy as np
import Orange.data
from Orange.widgets.widget import OWWidget, Input, Output
from Orange.widgets import gui, settings
from AnyQt import QtWidgets, QtCore, QtGui
from skimage.transform import resize

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
    allow_propagation = settings.Setting(True)
    auto_resize = settings.Setting(False)

    def __init__(self):
        super().__init__()
        self.imgs = None
        self.result = None
        self.saved_config = []

        # GUI
        self.infoa = gui.widgetLabel(self.box_info, 'No data yet, waiting to get something.')

        gui.checkBox(self.controlArea, self,
                     'auto_resize',
                     'Apply automatic settings',
                     callback=self.do_auto_conf)

        self.box_custom = gui.widgetBox(self.controlArea, "Custom")
        self.info_shape = gui.widgetLabel(self.box_custom, 'Original shape: ')
        hl0 = gui.hBox(self.box_custom)
        gui.label(hl0, self, "Desired shape:")
        self.sp_w = QtWidgets.QSpinBox(self) # gui.spin(hl0, self, 'desired_width', minv=1, maxv=5000, step=1)
        self.sp_h = QtWidgets.QSpinBox(self) #self.sp_h = gui.spin(hl0, self, 'desired_height', minv=1, maxv=5000, step=1)
        self.sp_w.setMinimum(1)
        self.sp_h.setMinimum(1)
        #self.sp_w.valueChanged.connect(self.on_value_change)
        #self.sp_h.valueChanged.connect(self.on_value_change)
        hl0.layout().addWidget(self.sp_h)
        hl0.layout().addWidget(self.sp_w)

        gui.radioButtons(self.box_custom,self,'selected_resize_type',["Crop top left","Crop center","Resize"])

        gui.toolButton(self.box_custom,self,"Apply and save current settings",callback=self.do_save_conf)

        gui.checkBox(self.buttonsArea, self,
                     'allow_propagation',
                     'Allow propagation',
                     callback=self.commit)

# GUI methods
    def init_default_config(self):
        """Initialize default UI configurations"""
        self.saved_config = []
        for img in self.imgs:
            d = {"selected_resize_type":0,
                 "desired_width":img.shape[1],
                 "desired_height":img.shape[0]}
            self.saved_config.append(d)

    def do_auto_conf(self):
        """TODO"""
        if self.auto_resize:
            # GUI
            self.box_custom.setEnabled(False)

            if self.imgs is not None:
                # find mean heigth and width
                hm,wm = 0,0
                n = len(self.imgs)
                for img in self.imgs:
                    h,w = img.shape
                    hm += h/float(n)
                    wm += w/float(n)
                print(hm,wm)

                # TODO apply resize on too small images
                for img in self.imgs:
                    h,w = img.shape
                    do_it = False
                    if (h<hm) and (h<=w):
                        new_shape = (hm,int((hm/h)*w))
                        do_it = True
                    if (w<wm) and (w<=h):
                        new_shape = (int((wm/w)*h),wm)
                        do_it = True
                    if do_it:
                        img2 = resize(img,new_shape)

                # TODO apply crop on too big images
        else:
            self.box_custom.setEnabled(True)


    def do_save_conf(self):
        """Apply crop or resize on current displayed image."""
        conf = self.saved_config[self.index_current_img]
        conf["desired_width"] = self.sp_w.value()
        conf["desired_height"] = self.sp_h.value()
        conf["selected_resize_type"] = self.selected_resize_type
        self.compute()
        self.update_display()
        self.commit()

    def on_img_change(self):
        """On current displayed image change method."""
        img = self.imgs[self.index_current_img]
        conf = self.saved_config[self.index_current_img]
        self.info_shape.setText("Original shape: {}".format(img.shape))
        self.sp_w.setMaximum(img.shape[1])
        self.sp_w.setValue(conf["desired_width"])
        self.sp_h.setMaximum(img.shape[0])
        self.sp_h.setValue(conf["desired_height"])
        self.selected_resize_type = conf["selected_resize_type"]

    def compute(self):
        """Apply choosen transformation on selected image."""
        img = self.imgs[self.index_current_img]
        conf = self.saved_config[self.index_current_img]
        w,h = conf["desired_width"],conf["desired_height"]

        if conf["selected_resize_type"] == 0:
            self.result[self.index_current_img] = img[:h,:w]

        elif conf["selected_resize_type"] == 1:
            H,W = img.shape
            self.result[self.index_current_img] = img[int(H/2-h/2):int(H/2+h/2),
                                                      int(W/2-w/2):int(W/2+w/2)]
        elif conf["selected_resize_type"] == 2:
            self.result[self.index_current_img] = resize(img.copy(),(h,w))

# Orange methods
    @Inputs.imgs
    def set_imgs(self, dataset):
        if isListOfArray(dataset):
            self.imgs = dataset
            self.result = [img.copy() for img in self.imgs]
            self.init_default_config()
            self.commit()
        else:
            self.warning("Wrong input, it must be a list of numpy arrays")

    def commit(self):
        """Send the outputs"""
        if self.allow_propagation:
            self.Outputs.result.send(self.result)
            self.update_display()

if __name__ == "__main__":
    # https://orange3.readthedocs.io/projects/orange-development/en/latest/testing.html#running-widgets-as-scripts
    from Orange.widgets.utils.widgetpreview import WidgetPreview
    from skimage import io
    inp = [io.imread("icons/find.png",as_gray=True)/255.0,
           io.imread("icons/selection.png",as_gray=True)/255.0]
    WidgetPreview(OWIResize).run(inp)