from Orange.widgets.widget import OWWidget, Input, Output
from Orange.widgets import gui, settings
from AnyQt import QtWidgets, QtCore, QtGui
from skimage.feature import match_template

from orangecustom.tools.OWWDisplay3D import OWWDisplay3D

class OWWInteract3D(OWWDisplay3D):
    want_main_area = True

    selection_mode = settings.Setting(0)

    def __init__(self):
        super().__init__()
        self.saved_selections = []

        self.box_selection = gui.widgetBox(self.controlArea, "Selection Mode")

        gui.radioButtons(self.box_selection, self, 'selection_mode',
                         ["None","Rectangle", "Circle", "Polygone"])


        # https://matplotlib.org/stable/users/event_handling.html
        self.display.canvas.mpl_connect('button_release_event', self.onRelease)
        self.display.canvas.mpl_connect('motion_notify_event', self.onMouseMove)
        self.display.canvas.mpl_connect('button_press_event', self.onPress)

# GUI methods
    def on_img_change(self):
        """TODO"""
        if self.result is not None:
            # draw saved selection
            pass

    def onPress(self, event):
        self.pos_press = [event.xdata, event.ydata]
        print(self.pos_press)

    def onRelease(self, event):
        self.pos_release = [event.xdata, event.ydata]
        print(self.pos_release)

    def onMouseMove(self, event):
        pass