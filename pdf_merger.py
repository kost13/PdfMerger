import sys, os, PyPDF2
from PyQt4 import QtGui, QtCore, uic
import operator
from item import *

PdfFilesList = []
idNumber = 0
lastOrdinalNumber = 0;

class MainWindow(QtGui.QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()

		uic.loadUi('merger_gui.ui', self)

		self.styleData = ''
		with open('blue_style.stylesheet', 'r') as styleFile:
			self.styleData = styleFile.read()

		self.setStyleSheet(self.styleData)


		self.main()
		self.show()

	def main(self):

		self.openDirectoryButton.clicked.connect(self.openDirectory)
		self.openFileButton.clicked.connect(self.openFile)
		self.quitButton.clicked.connect(self.closeApp)
		self.mergeButton.clicked.connect(self.mergeFiles)

		self.formLayout = QtGui.QFormLayout()

		self.listWidget = QtGui.QWidget()
		self.listWidget.setLayout(self.formLayout)

		self.scrollArea.setWidget(self.listWidget)

		self.appendListWidget()


	def closeApp(self):
		sys.exit()

	def openDirectory(self):
		newDirectory = ""
		newDirectory = QtGui.QFileDialog.getExistingDirectory(self, "Select Directory")
		if newDirectory != "":
			for file in os.listdir(newDirectory):
				self.appendFilesList(file, newDirectory)

		self.appendListWidget()

	def openFile(self):
		newFiles = []
		newFiles = QtGui.QFileDialog.getOpenFileNames(self, "Select Files")
		if newFiles:
			for fullFile in newFiles:
				fullFile = str(fullFile)
				directory, file = os.path.split(fullFile)
				self.appendFilesList(file, directory)

		self.appendListWidget()


	def appendFilesList(self, file, newDirectory):

		global idNumber
		global lastOrdinalNumber
		fileSize=0
		fileDate=0

		fileName, fileType = os.path.splitext(file)

		if fileType == '.pdf':
			try:
				fileSize = os.path.getsize(newDirectory + '/' + file)
				fileDate = os.path.getctime(newDirectory + '/' + file)
			except OSError:
				pass

			fileDirectory = str(newDirectory) + '/' + str(file)

			if fileSize > 1000000:
				fileSize = str(round(fileSize/1000000.0,2)) + ' MB'
			else:
				fileSize = str(int(fileSize/1000)) + ' KB'

			PdfFilesList.append({'FileName': fileName, 'FileDirectory': fileDirectory, 'Directory': newDirectory, 'FileSize': fileSize, 'FileDate':fileDate,'isChecked':True, 'id':idNumber, 'ordinal': lastOrdinalNumber})
			lastOrdinalNumber+=1
			idNumber+=1


	def appendListWidget(self):

		self.clearLayout(self.formLayout)

		PdfFilesList.sort(key=operator.itemgetter('ordinal'))

		for file in PdfFilesList:

			self.formLayout.addRow(fileItem(file, PdfFilesList, window))


	def mergeFiles(self):

		writer = PyPDF2.PdfFileWriter()
		counter = 0

		for dictionary in PdfFilesList:
			if dictionary['isChecked'] == True:
				counter += 1
				file = dictionary['FileDirectory']
				pdf = open(file, 'rb')
				reader = PyPDF2.PdfFileReader(pdf, strict=False)

				for i in range(reader.numPages):
					page = reader.getPage(i)
					writer.addPage(page)

		if counter < 2:
			msgBox = QtGui.QMessageBox()
			msgBox.setText("Not enough files to merge.")
			msgBox.exec_()

		else:
			file_type = "PDF (*.pdf)"
			FILE_NAME = QtGui.QFileDialog.getSaveFileName(self, 'Save file', "", file_type)

			try:
				outputFile = open(FILE_NAME, 'wb')
			except IOError:
				pass
				
			writer.write(outputFile)
			outputFile.close()

		try:
			pdf.close()
		except UnboundLocalError:
			pass

		self.main()

	def clearLayout(self, layout):
		while layout.count():
			child = layout.takeAt(0)
			if child.widget():
				child.widget().deleteLater()



if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	window = MainWindow()
	window.setWindowTitle("PDFMerger")
	window.show()
	sys.exit(app.exec_())