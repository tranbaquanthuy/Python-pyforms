#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__      = "Ricardo Ribeiro"
__credits__     = ["Ricardo Ribeiro"]
__license__     = "MIT"
__version__     = "0.0"
__maintainer__  = "Ricardo Ribeiro"
__email__       = "ricardojvr@gmail.com"
__status__      = "Development"


from pyforms.utils.settings_manager import conf

from AnyQt.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout

from pyforms.gui.controls.ControlBase import ControlBase


from AnyQt import _api

if _api.USED_API == _api.QT_API_PYQT5:
	from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
	from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
elif _api.USED_API == _api.QT_API_PYQT4:
	from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
	from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar

from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D



class ControlMatplotlib(ControlBase, QWidget):

	def __init__(self, *args, **kwargs):
		QWidget.__init__(self)
		ControlBase.__init__(self, *args, **kwargs)

	def init_form(self):

		self._fig   = Figure((5.0, 4.0), dpi=100)
		self.canvas = FigureCanvas(self._fig)
		self.canvas.setParent(self)
		self.mpl_toolbar = NavigationToolbar(self.canvas, self)
	 
		vbox = QVBoxLayout()
		vbox.addWidget(self.canvas)
		vbox.addWidget(self.mpl_toolbar)
		self.setLayout(vbox)

	@property
	def value(self): return None

	@value.setter
	def value(self, value): 
		self.on_draw = value
		self.draw()

	def draw(self): 
		self.on_draw(self._fig)
		self.canvas.draw()

	def on_draw(self, figure):
		""" Redraws the figure
		"""
		x = range(len(self.value))

		#self._axes = self._fig.add_subplot(111)
		
		#self._axes.bar(left=x, height=self.data)
		#self.canvas.draw()

		axes = figure.add_subplot(111, projection='3d')
		axes.clear(); 
		pts = axes.scatter(x, x, x, c=x)
		figure.colorbar(pts)


	############################################################################
	############ Properties ####################################################
	############################################################################

	@property
	def fig(self): return self._fig
	@fig.setter
	def fig(self, value): self._fig = value


	@property
	def form(self): return self