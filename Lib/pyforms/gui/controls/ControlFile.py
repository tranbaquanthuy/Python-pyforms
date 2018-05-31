#!/usr/bin/python
# -*- coding: utf-8 -*-

from pyforms.utils.settings_manager 					  import conf
from pyforms.gui.controls.ControlText import ControlText

import pyforms.utils.tools as tools


from AnyQt 			 import uic, _api
from AnyQt.QtWidgets import QFileDialog


class ControlFile(ControlText):

	def __init__(self, *args, **kwargs):

		super(ControlFile, self).__init__(*args, **kwargs)
		self.use_save_dialog = kwargs.get('use_save_dialog', False)

	def init_form(self):
		control_path = tools.getFileInSameDirectory(__file__, "fileInput.ui")
		self._form = uic.loadUi(control_path)
		self._form.label.setText(self._label)
		self._form.pushButton.clicked.connect(self.click)
		self.form.lineEdit.editingFinished.connect(self.finishEditing)
		self._form.pushButton.setIcon(conf.PYFORMS_ICON_FILE_OPEN)

	def finishEditing(self):
		"""Function called when the lineEdit widget is edited"""
		self.changed_event()

	def click(self):

		if self.use_save_dialog:
			value, _ = QFileDialog.getSaveFileName(self.parent, self._label, self.value)
		else:
			value = QFileDialog.getOpenFileName(self.parent, self._label, self.value)

		
		if _api.USED_API == _api.QT_API_PYQT5:
			value = value[0]
		elif _api.USED_API == _api.QT_API_PYQT4:
			value = str(value)

		if value and len(value)>0: self.value = value

