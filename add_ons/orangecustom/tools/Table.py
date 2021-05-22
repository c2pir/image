# -*- coding: utf-8 -*-
from Orange.widgets.widget import OWComponent,OWWidget
from AnyQt import QtWidgets, QtCore, QtGui
from Orange.widgets import gui, settings

class STable(QtWidgets.QWidget,OWComponent):
    def __init__(self, parent: OWWidget = None,
                 title = None,
                 column_count = 2,
                 column_headers = ["x","y"]):
        QtWidgets.QWidget.__init__(self,parent)
        OWComponent.__init__(self,parent)

        # GUI
        self.table = gui.table(self,0,column_count)
        # selection multiline and row
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.MultiSelection)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        # set headers labels
        self.table.setHorizontalHeaderLabels(column_headers)
        # columns shapes
        self.table.horizontalHeader().setResizeMode(QtWidgets.QHeaderView.Stretch)

        vbox = QtWidgets.QVBoxLayout()
        if title is not None:
            vbox.addWidget(gui.label(self,parent,title))
        vbox.addWidget(self.table)
        self.setLayout(vbox)

    def init_with_list(self,table):
        """ """
        pass

    def add_row(self):
        """ """
        self.table.setRowCount(self.table.rowCount()+1)

    def remove_selection(self):
        """ """
        selection = self.table.selectionModel().selectedRows()
        for sel in selection:
            self.table.removeRow(sel.row())

    def contextMenuEvent(self, event):
        """ """
        selection = self.table.selectionModel().selectedRows()
        #self.try_parse()

        contextMenu = QtWidgets.QMenu(self)
        addAct = contextMenu.addAction("Add a row")
        addAct.triggered.connect(self.add_row)
        if len(selection)>0:
            removeAct = contextMenu.addAction("Remove selection")
            removeAct.triggered.connect(self.remove_selection)

        action = contextMenu.exec_(self.mapToGlobal(event.pos()))

    def try_parse(self,columns_types = [int,int]):
        """ """
        table = []
        for i in range(self.table.rowCount()):
            l = []
            for j in range(self.table.columnCount()):
                try:
                    val = self.table.item(i,j)
                    l.append(columns_types[j](val.text()))
                except:
                    print("Not able to parse element at ({},{})".format(i,j))
            table.append(l)

        return table