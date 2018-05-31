# !/usr/bin/python
# -*- coding: utf-8 -*-

from pyforms.utils.settings_manager import conf

from AnyQt.QtWidgets import QDialog, QInputDialog, QColorDialog
from AnyQt.QtGui import QColor, QPixmap, QFont, QPainter
from AnyQt import uic
from AnyQt import QtCore


import pyforms.utils.tools as tools


class TimelinePopupWindow(QDialog):
	"""
	Opens a dialog where the user can specify the behavior annotated
	in the selected line, as well as some related options.

	The parent timeline widget must be given, as well as the track
	identifier to edit.
	"""

	def __init__(self, parent, track_id):
		"""
		
		:param parent: 
		:param track_id: 
		"""
		super(TimelinePopupWindow, self).__init__(parent=parent)
		self._parent = parent
		control_path = tools.getFileInSameDirectory(
			__file__, "TimelinePopupWindow.ui")
		self._ui = uic.loadUi(control_path)
		self._ui.setWindowTitle("Track {:d} properties".format(track_id + 1))

		# Dialog variables
		self.behaviors = []
		self.behavior = None
		self.color = self._parent.color
		self.current_track = track_id

		self._default_comboBox_text = "Add a new label"
		self.__get_existing_tracklabels()

		# Set default color display
		self.__preview_color()

		# SIGNALS
		self._ui.comboBox.currentIndexChanged.connect(
			self.__on_comboBox_change)
		self._ui.pushButton_add.clicked.connect(self.__add_behavior)
		self._ui.pushButton_remove.clicked.connect(self.__remove_behavior)
		self._ui.pushButton_color.clicked.connect(self.__pick_color)

	def __on_comboBox_change(self):
		"""
		Handles comboBox index change.
		"""
		cb = self._ui.comboBox
		self.behavior = cb.itemText(cb.currentIndex())

	def __add_behavior(self):
		"""
		Add a behavior to the already existing ones.
		"""
		cb = self._ui.comboBox
		text, ok = QInputDialog.getText(
			self, 'Add behavior', 'Description:', text='')
		if ok:
			self.behavior = str(text)
			self.behaviors.append(self.behavior)
			self._ui.comboBox.addItem(self.behavior)
			cb.setCurrentIndex(cb.findText(self.behavior))

		# If adding the first item, we need to enable the comboBox and
		# remove the placeholder text
		if not cb.isEnabled():
			cb.removeItem(cb.findText(self._default_comboBox_text))
			cb.setEnabled(True)

	def __remove_behavior(self):
		"""Remove a behavior from the already existing ones."""
		cb = self._ui.comboBox
		i = cb.currentIndex()
		self.behaviors.remove(str(cb.itemText(i)))
		cb.removeItem(i)

		# If there are no behaviors assigned, just fill the comboBox
		# with a placeholder
		if cb.count() < 1:
			cb.addItem(self._default_comboBox_text)
			cb.setEnabled(False)

	def __pick_color(self):
		"""Dialog to choose a color."""
		self.color = QColorDialog.getColor(self.color)
		self.__preview_color()

	def __preview_color(self):
		"""
		Shows selected colors in two QLabel widgets.

		The first shows true color, while the second presents the color
		with an opacity as seen in the timeline and with some dummy text
		to preview readability.
		"""
		pixmap = QPixmap(50, 25)
		color = QColor(*self.color.getRgb())

		# Preview color
		color.setAlpha(int(255 * 1.0))
		pixmap.fill(color)
		self._ui.label_color.setPixmap(pixmap)

		# Preview color with transparency and some text
		color.setAlpha(int(255 * 0.5))
		pixmap.fill(color)
		painter = QPainter(pixmap)
		painter.setFont(QFont('Decorative', 8))
		painter.drawText(pixmap.rect(), QtCore.Qt.AlignCenter, "Text")
		painter.end()
		self._ui.label_color_alpha.setPixmap(pixmap)

	def __get_existing_tracklabels(self):
		"""
		Gets existing track labels already assigned.

		Scans the timeline track labels and sets the comboBox value
		accordingly.
		"""
		cb = self._ui.comboBox

		# Loop across timeline labels
		for index, track in enumerate(self._parent._tracks):
			# If there is already an assigned label, append it to the
			# behaviors list and to the comboBox (if not a duplicate)
			if track.title != '':
				self.behavior = track.title
				if self.behavior not in self.behaviors:
					cb.addItem(self.behavior)
					self.behaviors.append(self.behavior)

				# Set comboBox value to the one of the selected track
				if index == self.current_track:
					cb.setCurrentIndex(cb.findText(self.behavior))

		# If there are no behaviors assigned yet, just fill the comboBox
		# with a placeholder
		if cb.count() < 1:
			cb.addItem(self._default_comboBox_text)
			cb.setEnabled(False)

########################################################################
###
# MAYBE IN THE FUTURE IMPLEMENT THIS USING THE BaseWidget

# class TimelinePopupWindow(BaseWidget):
#     """
#     Opens a dialog where the user can specify the behavior annotaded
#     in the selected line, as well as some related options.
#     """

#     def __init__(self, parent=None):
#         super(TimelinePopupWindow, self).__init__('Adjust line options')

#         if parent is not None:
#             self.parent = parent

#         self._behaviors = None
#         self._behaviorname  = None
#         self._linecolor = None

#         # Combobox
#         self._combobox = ControlCombo()

#         # Buttons
#         self._btn_add = ControlButton()
#         self._btn_remove = ControlButton()
#         self._btn_import = ControlButton()
#         self._btn_export = ControlButton()
#         self._btn_color = ControlButton()
#         self._btn_ok = ControlButton()
#         self._btn_cancel = ControlButton()

#         self._formset = ['_combobox',
#                          ('_btn_add', '_btn_remove', '_btn_import', '_btn_export'),
#                          ('_btn_ok', '_btn_cancel')]

#         def __choose_color(self):
#             pass
#             QColorDialog.getColor()
