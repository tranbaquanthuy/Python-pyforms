# !/usr/bin/python
# -*- coding: utf-8 -*-

import logging

from pyforms.utils.settings_manager import conf

logger = logging.getLogger(__name__)

from pyforms.gui.controls.ControlBase import ControlBase

from AnyQt.QtWidgets import QSizePolicy

from AnyQt import _api

from OpenGL.GL  import *
from OpenGL.GLU import *
        
from AnyQt import _api
if _api.USED_API == _api.QT_API_PYQT5:
    try:
        from AnyQt.QtOpenGL import QGLWidget
    except:
        logger.debug("No OpenGL library available")

    import platform
    if platform.system() == 'Darwin':
        from pyforms.gui.controls.control_player.VideoQt5GLWidget import VideoQt5GLWidget as VideoGLWidget
    else:
        from pyforms.gui.controls.control_player.VideoGLWidget import VideoGLWidget

elif _api.USED_API == _api.QT_API_PYQT4:
    try:
        from PyQt4.QtOpenGL import QGLWidget
    except:
        logger.debug("No OpenGL library available")

    from pyforms.gui.controls.control_player.VideoGLWidget import VideoGLWidget


class OpenglGLWidget(QGLWidget):
    def __init__(self, parent=None):
        QGLWidget.__init__(self, parent)

        self._zoom = 1.0
        self._scene = None
        self._rotation = [0, 0, 0]

        self._mouseLeftDown = False
        self._mouseRightDown = False

        self._mouseGLPosition = [0, 0, 0]
        self._lastMouseGLPosition = [0, 0, 0]

        self._mousePosition = [0, 0]  # Current mouse position
        self._lastMousePosition = [0, 0]  # Last mouse position

        self._mouseStartDragPoint = None
        self._clear_color = None

        self.setMinimumHeight(100)
        self.setMinimumWidth(100)
        self.setMouseTracking(True)
        self.setAcceptDrops(True)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding);

    def initializeGL(self):
        glClearDepth(1.0)
        if self._clear_color: glClearColor(*self._clear_color)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE)

        glEnable(GL_POINT_SMOOTH);
        glEnable(GL_LINE_SMOOTH);
        glEnable(GL_POLYGON_SMOOTH);
        glHint(GL_POINT_SMOOTH_HINT, GL_NICEST);
        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST);
        glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST);

    def resizeGL(self, width, height):
        """
        
        :param width: 
        :param height: 
        :return: 
        """

        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        if height!=0:
            ratio = float(width) / float(height)
        else:
            ratio = 1
        gluPerspective(65.0, ratio, 0.01, 800.0)

    def paintGL(self):
        """
        
        """
        if self._clear_color:
            glBlendFunc(GL_ONE_MINUS_CONSTANT_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            glClearColor(*self._clear_color)
        else:
            glBlendFunc(GL_SRC_ALPHA, GL_ONE)
            glClearColor(0, 0, 0, 1)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glEnable(GL_BLEND)

        glScalef(1, -1, -1)

        glTranslatef(0, 0, self._zoom)
        glRotatef(self._rotation[0], 1, 0, 0)
        glRotatef(self._rotation[1], 0, 1, 0)
        glRotatef(self._rotation[2], 0, 0, 1)

        if self._scene != None: self._scene.DrawGLScene()

        if self.mouseDown:
            # Get mouse position
            modelview, projection = glGetDoublev(GL_MODELVIEW_MATRIX), glGetDoublev(GL_PROJECTION_MATRIX)
            viewport = glGetIntegerv(GL_VIEWPORT)
            winX, winY = float(self._mousePosition[0]), float(viewport[3] - self._mousePosition[1])
            winZ = glReadPixels(winX, winY, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT)
            self._mouseGLPosition = gluUnProject(winX, winY, winZ[0][0], modelview, projection, viewport)

        glDisable(GL_BLEND)

    def __updateMouse(self, event, pressed=None):
        self._mousePosition[0] = event.x()
        self._mousePosition[1] = event.y()

        if pressed != None:
            if event.button() == 2: self._mouseRightDown = pressed
            if event.button() == 1: self._mouseLeftDown = pressed

    def wheelEvent(self, event):
        """
        
        :param event: 
        """
        if _api.USED_API == _api.QT_API_PYQT5:
            p = event.angleDelta()
            delta = p.y()
        elif _api.USED_API == _api.QT_API_PYQT4:
            delta = event.delta()
        
        
        if delta < 0:
            self._zoom += 1
        else:
            self._zoom -= 1

        self.repaint()

    def mouseReleaseEvent(self, event):
        """
        
        :param event: 
        """
        self.__updateMouse(event)

        if self._mouseRightDown:
            self._lastMouseGLPosition = self._mouseGLPosition
            self._mouseRightDown = False

        if self._mouseLeftDown:
            self.onEndDrag(self._mouseStartDragPoint, self._mouseGLPosition)
            self._mouseLeftDown = False

    def mousePressEvent(self, event):
        """
        
        :param event: 
        """
        QGLWidget.mousePressEvent(self, event)
        self.__updateMouse(event, pressed=True)
        self.repaint()

        if self._mouseLeftDown:  self._mouseStartDragPoint = self._mouseGLPosition
        if self._mouseRightDown: self._lastMouseGLPosition = self._mouseGLPosition

        self.onPress(event.button(), self._mousePosition, self._mouseGLPosition)

    def mouseMoveEvent(self, event):
        """
        
        :param event: 
        """
        QGLWidget.mouseMoveEvent(self, event)
        self.__updateMouse(event)
        self.repaint()

        self.onMove((self._mouseGLPosition[0], self._mouseGLPosition[1]))

        if self.mouseDown:
            if self._mouseLeftDown:
                # p = self._mouseGLPosition[0] - self._x, self._mouseGLPosition[1] + self._y
                # p = self._mouseGLPosition[0], self._mouseGLPosition[1]
                self.onDrag(self._lastMousePosition, self._mousePosition)

        self._lastMousePosition = list(self._mousePosition)

    def onMove(self, point):
        pass

    def onPress(self, button, point, glpoint=None):
        pass

    def onDrag(self, startPoint, endPoint, startGLPoint=None, endGLPoint=None):
        """
        
        :param startPoint: 
        :param endPoint: 
        :param startGLPoint: 
        :param endGLPoint: 
        """
        movX, movY = endPoint[0] - startPoint[0], endPoint[1] - startPoint[1]
        self._rotation[2] -= float(movX) * 0.15
        self._rotation[0] += float(movY) * 0.15

    def onEndDrag(self, startPoint, endPoint, startGLPoint=None, endGLPoint=None):
        pass

    ##############################################################################
    ###### Properties ############################################################
    ##############################################################################

    @property
    def scene(self):
        return self._scene

    @scene.setter
    def scene(self, value):
        self._scene = value

    @property
    def mouseDown(self):
        return self._mouseLeftDown or self._mouseRightDown

    def resetZoomAndRotation(self):
        self._zoom, self._rotation = 0.0, [0, 0, 0]


class ControlOpenGL(ControlBase):
    def init_form(self): self._form = OpenglGLWidget()

    def repaint(self): self._form.repaint()

    def reset_zoom_and_rotation(self): self._form.resetZoomAndRotation()

    @property
    def value(self): return self._form.scene

    @value.setter
    def value(self, value):  self._form.scene = value; self._form.repaint()

    @property
    def clear_color(self): self._form._clear_color

    @clear_color.setter
    def clear_color(self, value):
        self._form._clear_color = value;
        self._form.repaint()

    @property
    def width(self): return self._form.width()

    @property
    def height(self): return self._form.height()
