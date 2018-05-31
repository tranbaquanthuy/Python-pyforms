# !/usr/bin/python
# -*- coding: utf-8 -*-
from pyforms.gui.controls.ControlBase import ControlBase

from AnyQt.QtWidgets import QTreeView, QAbstractItemView
from AnyQt.QtGui 	 import QStandardItem, QStandardItemModel


class ControlTreeView(ControlBase, QTreeView):
	def __init__(self, *args, **kwargs):
		QTreeView.__init__(self)
		ControlBase.__init__(self, *args, **kwargs)

	def init_form(self):
		self.setSelectionBehavior(QAbstractItemView.SelectRows)
		self.header().hide()
		self.setUniformRowHeights(True)
		self.setDragDropMode(QAbstractItemView.InternalMove)
		self.setDragEnabled(True)
		self.setAcceptDrops(True)

		self.setModel(QStandardItemModel())
		self.model().itemChanged.connect(self.__item_changed_event)

		self.selectionChanged = self.selectionChanged

		# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		# populate data
		"""
		for i in range(3):
			parent1 = QtGui.QStandardItem('Family {}. Some long status text for sp'.format(i))
			for j in range(3):
				child1 = QtGui.QStandardItem('Child {}'.format(i*3+j))
				parent1.appendRow(child1)
			model().appendRow(parent1)
			# span container columns
			view.setFirstColumnSpanned(i, view.rootIndex(), True)
		"""

	def __item_changed_event(self, item):
		self.item_changed_event(item)

	def item_changed_event(self, item):
		pass

	def item_selection_changed_event(self):
		pass

	def selectionChanged(self, selected, deselected):
		super(QTreeView, self.form).selectionChanged(selected, deselected)
		self.item_selection_changed_event()

	@property
	def mouseSelectedRowsIndexes(self):
		result = []
		for index in self.form.selectedIndexes():
			result.append(index.row())
		return list(set(result))

	@property
	def selected_row_index(self):
		indexes = self.mouseSelectedRowsIndexes
		if len(indexes) > 0:
			return indexes[0]
		else:
			return None

	@property
	def selectedItem(self):
		for index in self.form.selectedIndexes():
			item = index.model().itemFromIndex(index)
			return item
		else:
			return None

	@property
	def cells(self):
		results = []
		for row in range(self._model().rowCount()):
			r = []
			for col in range(self._model().columnCount()):
				r.append(self._model().item(row, col))
			if len(r) > 0: results.append(r)
		# print r, '---'

		return results

	def __add__(self, other):
		if isinstance(other, TreeItem):
			self._model().invisibleRootItem().appendRow(other)

		elif isinstance(other, list):
			for x in other:
				item = QStandardItem(x)
				self._model().appendRow(item)
		else:
			item = QStandardItem(other)
			self._model().appendRow(item)

		self.form.setFirstColumnSpanned(self._model().rowCount() - 1, self.form.rootIndex(), True)
		return self

	def __sub__(self, other):
		if isinstance(other, int):
			if other < 0:
				indexToRemove = self.selected_row_index
			else:
				indexToRemove = other
			self.model().removeRow(indexToRemove)
		return self

	@property
	def value(self):
		return self.form.model().invisibleRootItem()
		return self.recursivelyReadRoot(root)

	@value.setter
	def value(self, value):
		for row in value: self += row

	def getAllSceneObjects(self):
		return self._model().getChildrens()

	@property
	def form(self):
		return self
