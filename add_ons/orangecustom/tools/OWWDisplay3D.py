from Orange.widgets.widget import OWWidget, Input, Output
from Orange.widgets import gui, settings
from AnyQt import QtWidgets, QtCore, QtGui
from skimage.feature import match_template

from orangecustom.tools.Graph import SFigure

class OWWDisplay3D(OWWidget):
    want_main_area = True

    def __init__(self):
        super().__init__()
        self.result = None
        self.index_current_img = 0

        # GUI
        self.box_info = gui.widgetBox(self.controlArea, "Info")
        # next and previous button to navigate in the image list
        hb0 = gui.hBox(self.box_info)
        gui.label(hb0, self, 'Displayed image : ')
        gui.toolButton(hb0, self, '<', callback=self.previous_img)
        self.l_img_index = gui.label(hb0, self, '.../...')
        self.l_img_index.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignVCenter)
        gui.toolButton(hb0, self, '>', callback=self.next_img)

        box = gui.widgetBox(self.mainArea, "Display")
        self.display = SFigure(self)
        box.layout().addWidget(self.display)

# GUI methods
    def on_img_change(self):
        """For children"""
        pass

    def previous_img(self):
        """ TODO """
        if self.result is not None:
            if self.index_current_img > 0:
                self.index_current_img += -1
                self.update_display()

    def next_img(self):
        """ TODO """
        if self.result is not None:
            if self.index_current_img < len(self.result):
                self.index_current_img += 1
                self.update_display()


    def update_display(self):
        """ TODO """
        if len(self.result) > self.index_current_img:
            self.l_img_index.setText("{}/{}".format(self.index_current_img + 1, len(self.result)))
            self.display.clear()
            self.display.draw3D(self.result[self.index_current_img])
            self.on_img_change()

