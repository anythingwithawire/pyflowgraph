
#
# Copyright 2015-2017 Eric Thivierge
#

import sys
from qtpy import QtGui, QtWidgets, QtCore

from .graph_view import GraphView

class GraphViewWidget(QtWidgets.QWidget):

    rigNameChanged = QtCore.Signal()

    def __init__(self, parent=None):

        # constructors of base classes
        super(GraphViewWidget, self).__init__(parent)
        self.openedFile = None
        self.setObjectName('graphViewWidget')
        self.setAttribute(QtCore.Qt.WA_WindowPropagation, True)


    def setGraphView(self, graphView):

        self.graphView = graphView

        # Setup Layout
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.graphView)
        self.setLayout(layout)

        #########################
        ## Setup hotkeys for the following actions.
        deleteShortcut = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Delete), self)
        deleteShortcut.activated.connect(self.graphView.deleteSelectedNodes)

        frameShortcut = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_F), self)
        frameShortcut.activated.connect(self.graphView.frameSelectedNodes)

        frameShortcut = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_A), self)
        frameShortcut.activated.connect(self.graphView.frameAllNodes)


    def getGraphView(self):
        return self.graphView



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    widget = GraphViewWidget()
    graph = GraphView(parent=widget)
    cables = []


    from .node import Node
    from .port import InputPort, OutputPort, IOPort
    from .cable import Cable

    termMap = []
    for c in range(1,13):
        termMap.append(c)



    node1 = Node(graph, 'Terminals001')
    for c in range(1,12):
        pname = str(c).zfill(2)
        node1.addPort(OutputPort(node1, graph, pname, QtGui.QColor(128, 170, 170, 255), 'MyDataX'))
    node1.setGraphPos(QtCore.QPointF( -200, 0 ))
    graph.addNode(node1)

    node2 = Node(graph, 'Terminals002')
    for c in range(1,12):
        pname = str(c).zfill(2)
        node1.addPort(InputPort(node1, graph, pname, QtGui.QColor(128, 170, 170, 255), 'MyDataX'))
    node1.setGraphPos(QtCore.QPointF( 200, 0 ))
    graph.addNode(node1)

    cables.append(Cable(graph, "NewCable001", node1.getPorts(), termMap, node2.getPorts(), termMap))




    widget.setGraphView(graph)
    widget.show()

    sys.exit(app.exec_())
