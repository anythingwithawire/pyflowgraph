
#
# Copyright 2015-2017 Eric Thivierge
#
import sys
from qtpy import QtGui, QtWidgets, QtCore

# Add the pyflowgraph module to the current environment if it does not already exist
import imp
try:
    imp.find_module('pyflowgraph')
    found = True
except ImportError:
    import os, sys
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "..")))

from pyflowgraph.graph_view import GraphView
from pyflowgraph.graph_view_widget import GraphViewWidget
from pyflowgraph.node import Node
from pyflowgraph.port import InputPort, OutputPort, IOPort
from pyflowgraph.cable import Cable

app = QtWidgets.QApplication(sys.argv)

widget = GraphViewWidget()
graph = GraphView(parent=widget)

cables = []


#from .node import Node
#from .port import InputPort, OutputPort, IOPort
#from .cable import Cable

termMap = []
for c in range(1,13):
    termMap.append(c)

t = termMap[6]
termMap[6]=termMap[9]
termMap[9] = t


node1 = Node(graph, 'Terminals001')
for c in range(0,11):
    pname = str(c).zfill(2)

    if c == 3:
        pname = str(7).zfill(2)
    if c == 7:
        pname = str(3).zfill(2)

    node1.addPort(OutputPort(node1, graph, pname, QtGui.QColor(128, 170, 170, 255), 'xxx'))
node1.setGraphPos(QtCore.QPointF( 500, 0 ))
graph.addNode(node1)

node2 = Node(graph, 'Terminals002')
for c in range(0,11):
    pname = str(c).zfill(2)
    node2.addPort(InputPort(node2, graph, pname, QtGui.QColor(128, 170, 170, 255), 'zzz'))
node2.setGraphPos(QtCore.QPointF(-500, 0 ))
graph.addNode(node2)


cables.append(Cable(graph, "NewCable001", node1, node1.getPorts(), termMap, node2, node2.getPorts(), termMap))




widget.setGraphView(graph)
widget.show()

sys.exit(app.exec_())
