#!/usr/bin/python
# -*- coding: utf-8 -*-

from pyforms.utils.settings_manager import conf

from AnyQt           import QtCore, _api
from AnyQt.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSpinBox
from AnyQt.QtGui     import QFont, QColor, QCursor, QPainter

from pyforms.gui.controls.ControlBase import ControlBase


class GaugeWidgetVertical(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)

        self.setMouseTracking(True)
        self.setMinimumHeight(30)
        self.setMinimumWidth(30)
        self.setMaximumWidth(50)

        self._step = 0
        self._lower = 0
        self._higher = 100
        self._minVal = 0
        self._maxVal = 75
        self._lastMouseY = None
        self._moving = False
        self._resizingBottom = False
        self._resizingTop = False
        self._scale = 1.0
        self._use_float = False

    def changed_event(self):
        pass

    def paintEvent(self, e):
        # call the base implementation to paint normal interface
        super(GaugeWidgetVertical, self).paintEvent(e)
        draw = QPainter()
        draw.begin(self)

        window_with = self.width() - 1
        diff = (self._higher - self._lower) * self.scale
        try:
            self._step = float(self.height()) / float(diff)
        except ZeroDivisionError:
            self._step = 0
        y_start = self.height() - (self._minVal - self._lower) * self._step * self.scale
        y_end = self.height() - (self._maxVal - self._lower) * self._step * self.scale

        draw.setOpacity(1.0)
        draw.setBrush(QtCore.Qt.NoBrush)
        draw.setPen(QColor(200, 200, 255))

        b = int(self.height() / 5)
        e = int(self.height() - (self.height() / 5) + 1)
        s = int(self.height() / 5)

        for i in range( b, e, s ):
            draw.drawLine(0, i, window_with, i)

        draw.setBrush(QColor(33, 133, 208))
        draw.setPen(QColor(33, 133, 208))
        draw.setOpacity(0.7)
        draw.drawRect(0, y_start, window_with, y_end - y_start)

        draw.setFont(QFont('Decorative', 8))
        draw.setPen(QColor(30, 30, 30))
        draw.drawText(3, self.height() - 3, str(self._lower) if self._use_float else str(int(round(self._lower))))
        draw.drawText(3, 10, str(self._higher) if self._use_float else str(int(round(self._higher))))

        draw.drawText(3, y_start + 11, str(self._minVal) if self._use_float else str(int(round(self._minVal))))
        draw.drawText(3, y_end - 4, str(self._maxVal) if self._use_float else str(int(round(self._maxVal))))

        draw.end()

    def mousePressEvent(self, event):
        self._moving = False
        self._resizingBottom = False
        self._resizingTop = False

        y_start = self.height() - (self._minVal - self._lower) * self._step * self.scale
        y_end = self.height() - (self._maxVal - self._lower) * self._step * self.scale

        if event.buttons() == QtCore.Qt.LeftButton:
            if y_start > event.y() > y_end:
                self._moving = True
            elif event.y() < y_end:
                self._resizingTop = True
            elif y_start < event.y():
                self._resizingBottom = True

    def mouseReleaseEvent(self, event):
        self._moving = False
        self._resizingBottom = False
        self._resizingTop = False

    def mouseMoveEvent(self, event):
        super(GaugeWidgetVertical, self).mouseMoveEvent(event)

        y_start = self.height() - (self._minVal - self._lower) * self._step * self.scale
        y_end = self.height() - (self._maxVal - self._lower) * self._step * self.scale

        if y_start < event.y() or event.y() < y_end:
            self.setCursor(QCursor(QtCore.Qt.SizeVerCursor))
        else:
            self.setCursor(QCursor(QtCore.Qt.ArrowCursor))

        if event.buttons() == QtCore.Qt.LeftButton:
            if self._lastMouseY != None:
                diff = self._lastMouseY - event.y()
                if diff != 0:
                    if self._moving:
                        new_min = self._minVal * self.scale + diff * 1 / self._step
                        new_max = self._maxVal * self.scale + diff * 1 / self._step
                        if new_min < new_max:
                            self._minVal = new_min / self.scale
                            self._maxVal = new_max / self.scale
                    elif self._resizingTop:
                        new_max = self._maxVal * self.scale + diff * 1 / self._step
                        if self._minVal < (new_max / self.scale): self._maxVal = new_max / self.scale
                    elif self._resizingBottom:
                        new_min = self._minVal * self.scale + diff * 1 / self._step
                        if (new_min / self.scale) < self._maxVal: self._minVal = new_min / self.scale

                    self.repaint()

                    self.changed_event()

            self._lastMouseY = event.y()

    def mouseReleaseEvent(self, event):
        self._lastMouseY = None

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value):
        self._scale = value


class GaugeWidgetHorizontal(GaugeWidgetVertical):
    def __init__(self, *args, **kwargs):
        super(GaugeWidgetHorizontal, self).__init__(*args, **kwargs)

        self.setMaximumWidth(1000000)
        self.setMinimumHeight(20)
        self.setMaximumHeight(20)

    def paintEvent(self, e):
        # call the base implementation to paint normal interface
        QWidget.paintEvent(self, e);
        draw = QPainter();
        draw.begin(self)

        h = self.height() - 1
        diff = (self._higher - self._lower) * self.scale

        try:
            self._step = float(self.width()) / float(diff)
        except ZeroDivisionError:
            self._step = 0
        x_start = (self._minVal - self._lower) * self._step * self.scale
        x_end = (self._maxVal - self._lower) * self._step * self.scale

        draw.setOpacity(1.0)
        draw.setBrush(QtCore.Qt.NoBrush)
        draw.setPen(QColor(200, 200, 255))

        for i in range( int(self.width()/5), int(self.width()-self.width()/5) + 1, int(self.width()/5) ): 
            draw.drawLine(i, 0, i, h)

        draw.setBrush(QColor(238, 238, 238))
        draw.setPen(QColor(238, 238, 238))
        draw.drawRoundedRect(0, 2, self.width(), h - 4, 3, 3)

        draw.setBrush(QColor(33, 133, 208))
        draw.setPen(QColor(33, 133, 208))
        draw.drawRoundedRect(int(round(x_start)), 2, int(round(x_end - x_start)), h - 4, 3, 3)
        # draw.setOpacity(1.0)
        draw.setFont(QFont('Decorative', 8))
        draw.setPen(QColor(80, 80, 80))

        str(self._maxVal) if self._use_float else str(int(round(self._maxVal)))

        boundtext = draw.boundingRect(QtCore.QRectF(),
                                      str(self._higher) if self._use_float else str(int(round(self._higher))))
        draw.drawText(self.width() - boundtext.width(), 14,
                      str(self._higher) if self._use_float else str(int(round(self._higher))))
        draw.drawText(0, 14, str(self._lower) if self._use_float else str(int(round(self._lower))))

        draw.setPen(QColor(255, 255, 255))
        boundtext = draw.boundingRect(QtCore.QRectF(),
                                      str(self._minVal) if self._use_float else str(int(round(self._minVal))))
        draw.drawText(x_start + 2, 14, str(self._minVal) if self._use_float else str(int(round(self._minVal))))
        boundtext = draw.boundingRect(QtCore.QRectF(),
                                      str(self._maxVal) if self._use_float else str(int(round(self._maxVal))))
        draw.drawText(x_end - boundtext.width(), 14,
                      str(self._maxVal) if self._use_float else str(int(round(self._maxVal))))

        draw.end()

    def mousePressEvent(self, event):
        self._moving = False
        self._resizingLeft = False
        self._resizingRight = False

        x_start = (self._minVal - self._lower) * self._step * self.scale
        x_end = (self._maxVal - self._lower) * self._step * self.scale

        if event.buttons() == QtCore.Qt.LeftButton:
            if x_start < event.x() < x_end:
                self._moving = True
            elif event.x() > x_end:
                self._resizingLeft = True
            elif x_start > event.x():
                self._resizingRight = True

    def mouseMoveEvent(self, event):
        super(GaugeWidgetVertical, self).mouseMoveEvent(event)

        x_start = (self._minVal - self._lower) * self._step * self.scale
        x_end = (self._maxVal - self._lower) * self._step * self.scale

        # set the cursors
        if x_start >= event.x() or event.x() >= x_end:
            self.setCursor(QCursor(QtCore.Qt.SizeHorCursor))
        else:
            self.setCursor(QCursor(QtCore.Qt.ArrowCursor))

        if event.buttons() == QtCore.Qt.LeftButton:
            if self._lastMouseY != None:
                diff = self._lastMouseY - event.x()
                if diff != 0:
                    if self._moving:
                        new_min = self._minVal * self.scale - diff * 1 / self._step
                        new_max = self._maxVal * self.scale - diff * 1 / self._step
                        if new_min < new_max:
                            self._minVal = new_min / self.scale
                            self._maxVal = new_max / self.scale
                    elif self._resizingLeft:
                        new_max = self._maxVal * self.scale - diff * 1 / self._step
                        if self._minVal < (new_max / self.scale): self._maxVal = new_max / self.scale
                    elif self._resizingRight:
                        new_min = self._minVal * self.scale - diff * 1 / self._step
                        if (new_min / self.scale) < self._maxVal: self._minVal = new_min / self.scale

                    self.repaint()
                    self.changed_event()

            self._lastMouseY = event.x()


class ControlBoundingSlider(ControlBase):
    def __init__(self, *args, **kwargs):
        self._horizontal     = kwargs.get('horizontal', True)
        self._show_spinboxes = kwargs.get('show_spinboxes', True)
        ControlBase.__init__(self,  *args, **kwargs)

        self.min = kwargs.get('min', kwargs.get('minimum', 0))
        self.max = kwargs.get('max', kwargs.get('maximum', 100))
        self.value = kwargs.get('default', [10,20])
        self.__update()

    def init_form(self):
        self._boundingbox = GaugeWidgetHorizontal() if self._horizontal else GaugeWidgetVertical()
        self._boundingbox.changed_event = self.__update

        if self._show_spinboxes:
            self._form = hwidget = QWidget()
            if self._horizontal:
                hlayout = QHBoxLayout()
            else:
                hlayout = QVBoxLayout()
            

            if _api.USED_API == _api.QT_API_PYQT5:
                hlayout.setContentsMargins(0,0,0,0)
            elif _api.USED_API == _api.QT_API_PYQT4:
                hlayout.setMargin(0)


            hwidget.setLayout(hlayout)
            self._min_spinbox = QSpinBox()
            self._min_spinbox.valueChanged.connect(self.__min_spinbox_changed)
            self._min_spinbox.setMaximumWidth(95)

            self._max_spinbox = QSpinBox()
            self._max_spinbox.valueChanged.connect(self.__max_spinbox_changed)
            self._max_spinbox.setMaximumWidth(95)

            if self._horizontal:
                hlayout.addWidget(self._min_spinbox)
            else:
                hlayout.addWidget(self._max_spinbox)
            hlayout.addWidget(self._boundingbox)
            if self._horizontal:
                hlayout.addWidget(self._max_spinbox)
            else:
                hlayout.addWidget(self._min_spinbox)

        else:
            self._form = self._boundingbox

        super(ControlBoundingSlider, self).init_form()

    def __max_spinbox_changed(self, value):
        if value < self._boundingbox._minVal: return
        if hasattr(self, '_is_updating_spinboxes'): return
        self.scale = self.__find_scale_factor(value)
        self._boundingbox._maxVal = value
        self._boundingbox.repaint()
        self.changed_event()

    def __min_spinbox_changed(self, value):
        if value > self._boundingbox._maxVal: return
        if hasattr(self, '_is_updating_spinboxes'): return
        self.scale = self.__find_scale_factor(value)
        self._boundingbox._minVal = value
        self._boundingbox.repaint()
        self.changed_event()

    def __update(self):
        l, h = self._boundingbox._minVal, self._boundingbox._maxVal
        self._is_updating_spinboxes = True
        self._min_spinbox.setValue(l)
        self._max_spinbox.setValue(h)
        del self._is_updating_spinboxes
        self.changed_event()

    def changed_event(self):
        pass

    def __find_scale_factor(self, value):
        scale = 1.0
        new_value = value
        while abs(new_value) < 0.0:
            scale *= 10.0
            new_value = value * scale
        return scale

    def load_form(self, data, path=None):
        """
        Load a value from the dict variable
        @param data: dictionary with the value of the Control
        """

        self.convert_2_int = data.get('convert-int', self.convert_2_int)
        self.scale = data.get('scale', self.scale)
        self.max = data.get('max', self.max)
        self.min = data.get('min', self.min)
        self.value = data.get('value', self.value)
        

    def save_form(self, data, path=None):
        """
        Save a value to dict variable
        @param data: dictionary with to where the value of the Control will be added
        """
        data['value']       = self.value
        data['max']         = self.max
        data['min']         = self.min
        data['scale']       = self.scale
        data['convert-int'] = self.convert_2_int
        return data

    ##########################################################################
    ############ Properties ##################################################
    ##########################################################################

    @property
    def value(self):
        return self._boundingbox._minVal, self._boundingbox._maxVal

    @value.setter
    def value(self, value):
        self.scale = self.__find_scale_factor(value[0])
        self._boundingbox._minVal, self._boundingbox._maxVal = value[0], value[1]
        if hasattr(self, '_min_spinbox'): self._min_spinbox.setValue(value[0])
        if hasattr(self, '_max_spinbox'): self._max_spinbox.setValue(value[1])
        ControlBase.value.fset(self, value)
        self._boundingbox.repaint()

    @property
    def min(self):
        return self._boundingbox._lower

    @min.setter
    def min(self, value):
        self._boundingbox._lower = value
        self._boundingbox.repaint()
        if hasattr(self, '_min_spinbox'): self._min_spinbox.setMinimum(value)
        if hasattr(self, '_max_spinbox'): self._max_spinbox.setMinimum(value)

    @property
    def max(self):
        return self._boundingbox._higher

    @max.setter
    def max(self, value):
        self._boundingbox._higher = value
        self._boundingbox.repaint()
        if hasattr(self, '_min_spinbox'): self._min_spinbox.setMaximum(value)
        if hasattr(self, '_max_spinbox'): self._max_spinbox.setMaximum(value)

    @property
    def scale(self):
        return self._boundingbox.scale

    @scale.setter
    def scale(self, value):
        self._boundingbox.scale = value

    @property
    def convert_2_int(self):
        return not self._boundingbox._use_float

    @convert_2_int.setter
    def convert_2_int(self, value):
        self._boundingbox._use_float = not value
