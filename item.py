#copyright 2017 Łukasz Kostrzewa

import sys, os, PyPDF2
from PyQt4 import QtGui, QtCore, uic

class fileItem(QtGui.QWidget):
	def __init__(self, file, PdfFilesList, window, parent=None):
		super(fileItem, self).__init__(parent)


		self.styleData = ''		
		with open('blue_style.stylesheet', 'r') as styleFile:
			self.styleData = styleFile.read()

		self.setStyleSheet(self.styleData)
	  
		itemLayout = QtGui.QGridLayout(self)

		self.fileInfo = file



		self.checkBox = QtGui.QCheckBox(file['FileName'] + ".pdf")
		self.checkBox.setObjectName("checkBox")


		if file["isChecked"] == False:
			self.checkBox.setCheckState(QtCore.Qt.Unchecked)
		if file["isChecked"] == True:
			self.checkBox.setCheckState(QtCore.Qt.Checked)

		self.checkBox.stateChanged.connect(lambda: self.changeCheckedState(PdfFilesList))


		self.directoryLabel = QtGui.QLabel(file["Directory"])
		self.directoryLabel.setObjectName("directoryLabel")
		self.directoryLabel.setWordWrap(True)


		self.fileSizeLabel = QtGui.QLabel(file["FileSize"])
		self.fileSizeLabel.setObjectName("fileSizeLabel")

		self.upButton = QtGui.QPushButton()
		self.upButton.setObjectName("upButton")
		if self.fileInfo['ordinal'] == 0:
			self.upButton.setEnabled(False)

		self.upButton.clicked.connect(lambda: self.changeOrderUp(PdfFilesList, window))

		self.downButton = QtGui.QPushButton()
		self.downButton.setObjectName("downButton")
		if self.fileInfo['ordinal'] == len(PdfFilesList)-1:
			self.downButton.setEnabled(False)

		self.downButton.clicked.connect(lambda: self.changeOrderDown(PdfFilesList, window))


		self.deleteButton = QtGui.QPushButton()
		self.deleteButton.setObjectName("deleteButton")
		self.deleteButton.clicked.connect(lambda: self.deleteItem(PdfFilesList, window))


		itemLayout.addWidget(self.checkBox, 0, 0, 0, 4)
		itemLayout.addWidget(self.directoryLabel, 0, 5, 0, 5)
		itemLayout.addWidget(self.fileSizeLabel, 0, 11, 0, 2)
		itemLayout.addWidget(self.upButton, 0, 14)
		itemLayout.addWidget(self.downButton, 0, 15)
		itemLayout.addWidget(self.deleteButton, 0, 16)


	def changeCheckedState(self, PdfFilesList):

		for file in PdfFilesList:
			if self.fileInfo["id"] == file["id"]:

				if file["isChecked"] == False:
					file["isChecked"] = True
				else:
					file["isChecked"] = False


	def changeOrderUp(self, PdfFilesList, window):

		for i in range(len(PdfFilesList)):

			if self.fileInfo["id"] == PdfFilesList[i]["id"]:

				PdfFilesList[i]['ordinal'] -= 1
				PdfFilesList[i-1]['ordinal'] += 1
				break

		window.appendListWidget()

	
	def changeOrderDown(self, PdfFilesList, window):

		for i in range(len(PdfFilesList)):

			if self.fileInfo["id"] == PdfFilesList[i]["id"]:

				PdfFilesList[i]['ordinal'] += 1
				PdfFilesList[i+1]['ordinal'] -= 1
				break

		window.appendListWidget()


	def deleteItem(self, PdfFilesList, window):
		index=0
		for file in PdfFilesList:
			if self.fileInfo["id"] == file["id"]:
				for i in range(len(PdfFilesList)-1,index,-1):
					print(i)
					PdfFilesList[i]["ordinal"] = PdfFilesList[i-1]["ordinal"]

				PdfFilesList.pop(index)
				break
			index+=1

		window.appendListWidget()
