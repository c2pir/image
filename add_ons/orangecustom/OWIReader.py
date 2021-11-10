# -*- coding: utf-8 -*-
"""

"""

import numpy as np

import Orange.data
from Orange.widgets.widget import OWWidget, Input, Output
from Orange.widgets import gui,settings

import os
from AnyQt import QtWidgets, QtCore, QtGui

from Orange.widgets.data import owfile
from skimage import io

from orangecustom.tools.OWWDisplay3D import OWWDisplay3D

class OWIReader(OWWDisplay3D):
    name = "Reader"
    description = "Ouvre les images présentes dans un dossier"
    icon = "icons/image_reader.png"
    priority = 10

    class Outputs:
        gray = Output("Grayscale", list)
        red = Output("Rouges", list)
        green = Output("Verts", list)
        blue = Output("Bleus", list)

    #want_main_area = False

    def __init__(self):
        super().__init__()

        self.folderpath = ""
        self.red = None
        self.green = None
        self.blue = None
        self.gray = None
        self.result = None

        # GUI
        layout = QtWidgets.QGridLayout()
        layout.setSpacing(4)
        gui.widgetBox(self.controlArea, orientation=layout, box='Folder')

        box = gui.hBox(None, addToLayout=False, margin=0)
        box.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        box.layout().addWidget(gui.widgetLabel(box, 'Select a folder:'))

        file_button = gui.button(
            None, self, '...', callback=self.browse_folder, autoDefault=False)
        file_button.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_DirOpenIcon))
        file_button.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        box.layout().addWidget(file_button)

        reload_button = gui.button(
            None, self, "Reload", callback=self.load_data, autoDefault=False)
        reload_button.setIcon(self.style().standardIcon(
            QtWidgets.QStyle.SP_BrowserReload))
        reload_button.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        #layout.addWidget(reload_button, 0, 2)
        box.layout().addWidget(reload_button)
        layout.addWidget(box, 0, 0)

        self.infoa = gui.widgetLabel(self, 'No path selected.')
        layout.addWidget(self.infoa , 1, 0)

        self.infob = gui.widgetLabel(self, '...')
        layout.addWidget(self.infob, 2, 0)
        
        layout.addItem(QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))


# GUI methods
    def browse_folder(self):
        """Open folder explorer then load images."""
        self.folderpath = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Folder')
        self.infoa.setText(self.folderpath)
        self.load_data()


    def load_data(self):
        """Load images in folder path."""
        if self.folderpath != "":
            self.red = []
            self.green = []
            self.blue = []
            self.gray = []
            self.result = []
            list_files = ""
            cpt = 0
            for file_name in os.listdir(self.folderpath):
                if file_name.endswith(".jpg") or file_name.endswith(".png"):

                    path = os.path.join(self.folderpath, file_name)
                    img = io.imread(path)

                    if len(img.shape)>=3:
                        img_gray = io.imread(path,as_gray=True)
                        self.result.append(img)
                        self.gray.append(img_gray)
                        self.red.append(img[:, :, 0]/255.0)
                        self.green.append(img[:, :, 1]/255.0)
                        self.blue.append(img[:, :, 2]/255.0)

                        list_files += "{}: {}\n".format(cpt, file_name)
                        cpt += 1

            self.infob.setText(list_files)
            self.update_display()
            self.commit()

# Orange methods
    def commit(self):
        """Send the outputs"""
        self.Outputs.gray.send(self.gray)
        self.Outputs.red.send(self.red)
        self.Outputs.green.send(self.green)
        self.Outputs.blue.send(self.blue)

if __name__ == "__main__":
    # https://orange3.readthedocs.io/projects/orange-development/en/latest/testing.html#running-widgets-as-scripts
    from Orange.widgets.utils.widgetpreview import WidgetPreview
    WidgetPreview(OWIReader).run()