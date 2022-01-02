#
# Copyright 2015-2017 Eric Thivierge
#
import sys

from PySide2.QtCore import Qt, QByteArray, QDataStream, QIODevice, QMimeData
# from PySide2.Qt import QString
from PySide2.QtGui import QKeySequence

from PySide2.QtWidgets import QMainWindow, QApplication, QLineEdit, QTableWidget, QTableWidgetItem, QAbstractItemView, \
    QMenu
from qtpy import QtGui, QtWidgets, QtCore

# Add the pyflowgraph module to the current environment if it does not already exist


"""
try:
    imp.find_module('pyflowgraph')
    found = True
except ImportError:
    import os, sys

    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "..")))
"""
from pyflowgraph.graph_view import GraphView
from pyflowgraph.graph_view_widget import GraphViewWidget
from pyflowgraph.node import Node
from pyflowgraph.port import InputPort, OutputPort, IOPort
import os, sys


class H3TableHandler:

    def __init__(self, parent=None):
        self.parent = parent

    def right_click(self):
        # bar = self.parent.menuBar()
        top_menu = QMenu(self.parent)

        menu = top_menu.addMenu("Menu")
        config = menu.addMenu("Configuration ...")

        _load = config.addAction("&Load ...")
        _save = config.addAction("&Save ...")

        config.addSeparator()

        config1 = config.addAction("Config1")
        config2 = config.addAction("Config2")
        config3 = config.addAction("Config3")

        action = menu.exec_(QtGui.QCursor.pos())

        if action == _load:
            # do this
            pass
        elif action == _save:
            # do this
            pass
        elif action == config1:
            # do this
            pass
        elif action == config2:
            # do this
            pass
        elif action == config3:
            # do this
            pass


import pyperclip

class TableWidgetCustom(QTableWidget, QTableWidgetItem):
    def __init__(self, parent=None):
        super(TableWidgetCustom, self).__init__(parent)
        self.clipboard = QApplication.clipboard()
        self.mime_data = self.clipboard.mimeData()
        self.pc = pyperclip
        self.text_clip = ""

    def keyPressEvent(self, event):
        if event.matches(QKeySequence.Save):
            self.save()
        if event.matches(QKeySequence.Open):
            self.restore()
        if event.matches(QKeySequence.Delete):
            self.delete()
        if event.matches(QKeySequence.Copy):
            self.copy()
        if event.matches(QKeySequence.Paste):
            self.paste()
        QTableWidget.keyPressEvent(self, event)

    def delete(self):
        for row in range(self.rowCount()):
            for col in range(self.columnCount()):
                item = self.item(row, col)
                if item.isSelected():
                    item = QTableWidgetItem()
                    item.setText(str(""))
                    self.setItem(row, col, item)


    def copy(self):
        #self.clipboard.clear(mode=self.clipboard.Clipboard)
        clip = ""
        i=0
        print(self.rowCount(), self.columnCount())
        for row in range(self.rowCount()):
            for col in range(self.columnCount()):
                item = self.item(row, col)
                if item.isSelected():
                    i = i + 1
                    item = QTableWidgetItem()
                    item = self.item(row, col)
                    clip = clip + str(item.text())+str(",")
            clip = clip + str("\n")
        encoded_clip = clip.encode()
        self.text_clip = clip
        clip_bytearray = bytearray(encoded_clip)
        #self.mime_data.setData("xls", clip_bytearray)
        #self.clipboard.setMimeData(self.mime_data)
        self.pc.init_qt_clipboard()
        self.pc.set_clipboard("qt")
        self.pc.lazy_load_stub_copy(clip)
        print("selected ", i, "\n", clip)

    def paste(self):
        #self.clipboard.clear(mode=self.clipboard.Clipboard)
        clip = ""
        i = 0
        print(self.rowCount(), self.columnCount())
        l = self.text_clip.split(",")
        for row in range(self.rowCount()):
            for col in range(self.columnCount()):
                item = self.item(row, col)
                if item.isSelected():
                    item = QTableWidgetItem()
                    item = self.item(row, col)
                    item.setText(l[i].strip())
                    self.setItem(row, col, item)
                    i = i + 1
                    if i >= len(l)-1:
                        i=0

    def save(self):
        print("saving")
        # using findChildren is for simplicity, it's probably better to create
        # your own list of widgets to cycle through
        f = open(str(self.windowTitle())+"_data", "wt")
        for row in range(self.rowCount()):
            for col in range(self.columnCount()):
                item = self.item(row, col)
                if item:
                    txt = item.text()
                else:
                    txt = 'x'
                f.write(txt)
                f.write(",")
            f.write("\n")
        f.close()

    def restore(self):
        print("restore")
        f = open(str(self.windowTitle())+"_data", "rt")
        i = 0
        for row in range(self.rowCount()):
            l = f.readline()
            d = l.split(",")
            for col in range(self.columnCount()):
                item = QTableWidgetItem()
                if col >= len(d):
                    item.setText("")
                else:
                    item.setText(str(d[col]))
                i = i + 1
                self.setItem(row, col, item)
                item.setTextAlignment(Qt.AlignHCenter)

        f.close()

    """
    def h3_table_right_click(self, position):
        o_h3_table = H3TableHandler(parent=self)
        o_h3_table.right_click()
        """

class MainWindow(QMainWindow, TableWidgetCustom):
    def __init__(self, e=None):
        super().__init__()
        self.setWindowTitle("FlowGraph Main")
        self.setGeometry(2000, 0, 200, 200)
        pb1 = QtWidgets.QPushButton('Set Node IP\nFrom Cable', self)
        pb1.resize(90,32)
        pb1.move(50,50)
        pb1.clicked.connect(self.pb1_clicked)

        pb2 = QtWidgets.QPushButton('Set Node OP\nFrom Cable', self)
        pb2.resize(90,32)
        pb2.move(150,50)
        pb2.clicked.connect(self.pb2_clicked)

        pb3 = QtWidgets.QPushButton('Zoom In', self)
        pb3.resize(90,32)
        pb3.move(50,150)
        pb3.clicked.connect(self.pb3_clicked)

        pb4 = QtWidgets.QPushButton('Zoom Out', self)
        pb4.resize(90,32)
        pb4.move(150,150)
        pb4.clicked.connect(self.pb4_clicked)




        self.pc = pyperclip

        self.cableInfoWidget = TableWidgetCustom()
        #self.cableInfoWidget.setEditTriggers(QAbstractItemView.AllEditTriggers)
        self.cableInfoWidget.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.cableInfoWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.cableInfoWidget.setColumnCount(6)
        self.cableInfoWidget.setRowCount(20)
        self.cableInfoWidget.setGeometry(1000, 0, 400, 600)
        """
            for row in range(self.cableInfoWidget.rowCount()):
            d = ""
            for col in range(self.cableInfoWidget.columnCount()):
                item = QTableWidgetItem(row, col)
                item.setText(d)
                item.setTextAlignment(Qt.AlignHCenter)
        """
        self.cableInfoWidget.setWindowTitle("Cable Termination Map")
        self.cableInfoWidget.setHorizontalHeaderLabels((("FmTermName;FmCoreNum;Cable;ToCoreNum;ToTermName").split(";")))
        self.cableInfoWidget.horizontalHeaderItem(1).setTextAlignment(Qt.AlignHCenter)

        #self.restore()
        #self.cableInfoWidget.cellClicked.connect(self.save)

        self.cableInfoWidget.show()

        self.widget = GraphViewWidget()
        self.graph = GraphView(parent=self.widget)
        self.graph.setWindowTitle("FlowGraph")

        self.node1 = Node(self.graph, 'Short')
        self.node1.addPort(InputPort(self.node1, self.graph, 'InPort1', QtGui.QColor(128, 170, 170, 255), 'MyDataX'))
        self.node1.addPort(InputPort(self.node1, self.graph, 'InPort2', QtGui.QColor(128, 170, 170, 255), 'MyDataX'))
        self.node1.addPort(OutputPort(self.node1, self.graph, 'OutPort', QtGui.QColor(32, 255, 32, 255), 'MyDataY'))
        self.node1.addPort(IOPort(self.node1, self.graph, 'IOPort1', QtGui.QColor(32, 255, 32, 255), 'MyDataY'))
        self.node1.addPort(IOPort(self.node1, self.graph, 'IOPort2', QtGui.QColor(32, 255, 32, 255), 'MyDataY'))
        self.node1.setGraphPos(QtCore.QPointF(-100, 0))

        self.graph.addNode(self.node1)

        self.node2 = Node(self.graph, 'ReallyLongLabel')
        self.node2.addPort(InputPort(self.node2, self.graph, 'InPort1', QtGui.QColor(128, 170, 170, 255), 'MyDataY'))
        self.node2.addPort(InputPort(self.node2, self.graph, 'InPort2', QtGui.QColor(128, 170, 170, 255), 'MyDataX'))
        self.node2.addPort(OutputPort(self.node2, self.graph, 'OutPort', QtGui.QColor(32, 255, 32, 255), 'MyDataY'))
        self.node2.addPort(IOPort(self.node2, self.graph, 'IOPort1', QtGui.QColor(32, 255, 32, 255), 'MyDataY'))
        self.node2.addPort(IOPort(self.node2, self.graph, 'IOPort2', QtGui.QColor(32, 255, 32, 255), 'MyDataY'))
        self.node2.setGraphPos(QtCore.QPointF(100, 0))

        self.graph.addNode(self.node2)
        self.graph.connectPorts(self.node1, 'OutPort', self.node2, 'InPort1')

        self.widget.setGraphView(self.graph)
        self.widget.setGeometry(1500, 500, 1000, 1000)
        self.widget.show()

    def pb1_clicked(self):
        if not self.graph.getSelectedNodes():
            nodex = Node(self.graph, 'nnnn')
            for i in range(self.cableInfoWidget.rowCount()):
                termName = self.cableInfoWidget.item(i, 1).text()
                nodex.addPort(InputPort(nodex, self.graph, termName, QtGui.QColor(128, 170, 170, 255), 'MyDataX'))
            self.graph.addNode(nodex)
            nodex.setGraphPos(QtCore.QPointF(-100, 500))
        else:
            nodes = self.graph.getSelectedNodes()
            for nodex in nodes:
                for i in range(self.cableInfoWidget.rowCount()):
                    termName = self.cableInfoWidget.item(i, 1).text()
                    nodex.addPort(InputPort(nodex, self.graph, termName, QtGui.QColor(128, 170, 170, 255), 'MyDataX'))
            self.graph.update()

    def pb2_clicked(self):
        if not self.graph.getSelectedNodes():
            nodex = Node(self.graph, 'nnnn')
            for i in range(self.cableInfoWidget.rowCount()):
                termName = self.cableInfoWidget.item(i, 1).text()
                nodex.addPort(OutputPort(nodex, self.graph, termName, QtGui.QColor(128, 170, 170, 255), 'MyDataX'))
            self.graph.addNode(nodex)
            nodex.setGraphPos(QtCore.QPointF(-100, 500))

    def pb3_clicked(self):
        self.graph.scale(1.5, 1.5)

    def pb4_clicked(self):
        self.graph.scale(0.5, 0.5)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.resize(500, 500)
    w.setWindowTitle("FlowGraph")
    w.show()
    sys.exit(app.exec_())
