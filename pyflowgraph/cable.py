
#
# Copyright 2015-2017 Eric Thivierge
#

from qtpy import QtGui, QtWidgets, QtCore

import pyflowgraph.connection
from .port import InputPort, OutputPort, PortCircle
from .connection import Connection

class Cable(QtWidgets.QGraphicsPathItem):
    __defaultPen = QtGui.QPen(QtGui.QColor(168, 134, 3), 1.5)

    def __init__(self, graph, name, srcNode, srcPortCircle, srcTermNum, dstNode, dstPortCircle, dstTermNum):
        super(Cable, self).__init__()


        __cableType = ("1W", "1B", "2W", "2B", "3W", "3B", "4W", "4B", "5W", "5B", "6W", "6B", "7W", "7B", "8W", "8B")
        self.__name = name
        self.__coreSeq = []
        self.__coreNum = []
        self.__coreName = []
        self.__coreFrom = []
        self.__coreTo = []
        self.__wireMarkerFrom = []
        self.__wireMarkerTo = []
        self.__srcTerm = []
        self.__dstTerm = []
        self.__PortCircle = PortCircle

        self.__srcNodePos = srcNode.getGraphPos()

        self.__graph = graph

        self.__cableColor = QtGui.QColor(0, 0, 0)
        """
        self.__cableColor.setRgbF(*self.__srcPortCircle.getColor().getRgbF())
        self.__cableColor.setAlpha(125)
        if self.isSelected():
            self.__cableColor.setAlpha(255)

        self.__defaultPen = QtGui.QPen(self.__cableColor, 1.5, style=penStyle)
        self.__defaultPen.setDashPattern([1, 2, 2, 1])

        self.__cableHoverColor = QtGui.QColor(0, 0, 0)
        self.__cableHoverColor.setRgbF(*self.__srcPortCircle.getColor().getRgbF())
        self.__cableHoverColor.setAlpha(255)

        self.__hoverPen = QtGui.QPen(self.__cableHoverColor, 1.5, style=penStyle)
        self.__hoverPen.setDashPattern([1, 2, 2, 1])
        """
        self.setPen(self.__defaultPen)
        self.setZValue(-1)


        for c in range(0, len(srcPortCircle)-1):
            self.__coreSeq.append(c)
            self.__coreNum.append(c)
            self.__coreName.append(__cableType[c])
            self.__wireMarkerFrom.append(str(srcTermNum[c]).zfill(4) + str(c).zfill(4))
            self.__srcTerm.append(srcPortCircle[c])

        for c in range(0,len(dstPortCircle)-1):
            self.__coreSeq.append(c)
            self.__coreNum.append(c)
            self.__coreName.append(__cableType[c])
            self.__wireMarkerTo.append(str(dstTermNum[c]).zfill(4) + str(c).zfill(4))
            self.__dstTerm.append(dstPortCircle[c])

        for c in range(0,len(dstPortCircle)):
            s = srcPortCircle[c]
            d = dstPortCircle[c]
            ps = srcPortCircle[0].pos()
            pd = dstPortCircle[0].pos()
            self.__graph.connectPorts(srcNode, str(c).zfill(2), dstNode, str(c).zfill(2), ps, pd)
            self.setAcceptHoverEvents(True)



    def setPenStyle(self, penStyle):
        self.__defaultPen.setStyle(penStyle)
        self.__hoverPen.setStyle(penStyle)
        self.setPen(self.__defaultPen) # Force a redraw


    def setPenWidth(self, width):
        self.__defaultPen.setWidthF(width)
        self.__hoverPen.setWidthF(width)
        self.setPen(self.__defaultPen) # Force a redraw


    def getSrcPortCircle(self):
        return self.__srcPortCircle


    def getDstPortCircle(self):
        return self.__dstPortCircle


    def getSrcPort(self):
        return self.__srcPortCircle.getPort()


    def getDstPort(self):
        return self.__dstPortCircle.getPort()


    def boundingRect(self):
        srcPoint = self.mapFromScene(self.__srcPortCircle.centerInSceneCoords()[0])
        dstPoint = self.mapFromScene(self.__dstPortCircle.centerInSceneCoords()[0])
        penWidth = self.__defaultPen.width()

        return QtCore.QRectF(
            min(srcPoint.x(), dstPoint.x()),
            min(srcPoint.y(), dstPoint.y()),
            abs(dstPoint.x() - srcPoint.x()),
            abs(dstPoint.y() - srcPoint.y()),
            ).adjusted(-penWidth/2, -penWidth/2, +penWidth/2, +penWidth/2)


    def paint(self, painter, option, widget):

        for s in self.__coreSeq:

            srcBase = self.mapFromScene(self.__srcTerm[0].centerInSceneCoords())
            srcPoint = self.mapFromScene(self.__srcTerm[s-1].centerInSceneCoords())
            dstPoint = self.mapFromScene(self.__dstTerm[s-1].centerInSceneCoords())

            dist_between = dstPoint - srcPoint

            self.__path = QtGui.QPainterPath()
            srcBase.setY(0)
            self.__path.moveTo(srcBase)
            self.__path.cubicTo(srcPoint + QtCore.QPointF(dist_between.x() * 0.4, 0), dstPoint - QtCore.QPointF(dist_between.x() * 0.4, 0), dstPoint )

            self.setSelected(True)
            self.setPath(self.__path)
            super(Cable, self).paint(painter, option, widget)


    def hoverEnterEvent(self, event):
        self.setPen(self.__hoverPen)

        super(Cable, self).hoverEnterEvent(event)


    def hoverLeaveEvent(self, event):
        self.setPen(self.__defaultPen)
        super(Cable, self).hoverLeaveEvent(event)


    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.__dragging = True
            self._lastDragPoint = self.mapToScene(event.pos())
            self.setSelected(True)
            print("selected")
            event.accept()
        else:
            super(Cable, self).mousePressEvent(event)


    def mouseMoveEvent(self, event):
        if self.__dragging:
            pos = self.mapToScene(event.pos())
            delta = pos - self._lastDragPoint
            if delta.x() != 0:

                self.__graph.removeCable(self)

                from . import mouse_grabber
                if delta.x() < 0:
                    mouse_grabber.MouseGrabber(self.__graph, pos, self.__srcPortCircle, 'In')
                else:
                    mouse_grabber.MouseGrabber(self.__graph, pos, self.__dstPortCircle, 'Out')

        else:
            super(Cable, self).mouseMoveEvent(event)


    def disconnect(self):
        self.__srcPortCircle.removeCable(self)
        self.__dstPortCircle.removeCable(self)


    def connect(self, src, dst):
        from .connection import Connection
        InputPort.connect(src)
        OutputPort.connect(dst)

