# -*- coding: utf-8 -*-
"""

"""

import numpy as np

import Orange.data
from Orange.widgets.widget import OWWidget, Input, Output
from Orange.widgets import gui,settings

import os
from AnyQt.QtWidgets import \
    QStyle, QComboBox, QMessageBox, QGridLayout, QLabel, \
    QLineEdit, QSizePolicy as Policy, QCompleter, QFileDialog
from Orange.widgets.data import owfile
from skimage import io



class OWIReader(OWWidget):
    name = "Reader"
    description = "Ouvre les images présentes dans un dossier"
    icon = "icons/image_reader.png"
    priority = 10

    class Outputs:
        gray = Output("Nuance de gris", list)
        red = Output("Rouges", list)
        green = Output("Verts", list)
        blue = Output("Bleus", list)

    want_main_area = False

    def __init__(self):
        super().__init__()

        self.folderpath = ""
        self.red = None
        self.green = None
        self.blue = None
        self.gray = None

        # GUI
        layout = QGridLayout()
        layout.setSpacing(4)
        gui.widgetBox(self.controlArea, orientation=layout, box='Folder')

        box = gui.hBox(None, addToLayout=False, margin=0)
        box.setSizePolicy(Policy.MinimumExpanding, Policy.Fixed)
        self.infoa = gui.widgetLabel(box, 'No path selected.')
        box.layout().addWidget(self.infoa)
        layout.addWidget(box, 0, 1)

        file_button = gui.button(
            None, self, '...', callback=self.browse_folder, autoDefault=False)
        file_button.setIcon(self.style().standardIcon(QStyle.SP_DirOpenIcon))
        file_button.setSizePolicy(Policy.Maximum, Policy.Fixed)
        layout.addWidget(file_button, 0, 2)

        reload_button = gui.button(
            None, self, "Reload", callback=self.load_data, autoDefault=False)
        reload_button.setIcon(self.style().standardIcon(
            QStyle.SP_BrowserReload))
        reload_button.setSizePolicy(Policy.Fixed, Policy.Fixed)
        layout.addWidget(reload_button, 0, 3)

        self.infob = gui.widgetLabel(box, '...')
        layout.addWidget(self.infob, 1, 0)

# GUI methods
    def browse_folder(self):
        """ TODO """
        self.folderpath = QFileDialog.getExistingDirectory(self, 'Select Folder')
        self.infoa.setText(self.folderpath)
        self.load_data()


    def load_data(self):
        """ TODO """
        if self.folderpath != "":
            self.red = []
            self.green = []
            self.blue = []
            self.gray = []
            list_files = ""
            cpt = 0
            for file_name in os.listdir(self.folderpath):
                if file_name.endswith(".jpg") or file_name.endswith(".png"):
                    print(file_name)
                    list_files += "{}: {}\n".format(cpt,file_name)
                    path = os.path.join(self.folderpath, file_name)
                    img = io.imread(path)
                    img_gray = io.imread(path,as_gray=True)
                    self.gray.append(img_gray)
                    self.red.append(img[:, :, 0]/255.0)
                    self.green.append(img[:, :, 1]/255.0)
                    self.blue.append(img[:, :, 2]/255.0)
                    cpt += 1

            self.infob.setText(list_files)
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