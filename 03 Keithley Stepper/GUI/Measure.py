# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Measure.ui'
#
# Created: Wed Jan 13 16:45:38 2016
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(879, 672)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout_2 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.scrollArea = QtGui.QScrollArea(self.centralwidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 857, 650))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.upButton = QtGui.QPushButton(self.scrollAreaWidgetContents)
        self.upButton.setGeometry(QtCore.QRect(210, 100, 41, 23))
        self.upButton.setObjectName(_fromUtf8("upButton"))
        self.downButton = QtGui.QPushButton(self.scrollAreaWidgetContents)
        self.downButton.setGeometry(QtCore.QRect(260, 100, 41, 23))
        self.downButton.setObjectName(_fromUtf8("downButton"))
        self.zeroButton = QtGui.QPushButton(self.scrollAreaWidgetContents)
        self.zeroButton.setGeometry(QtCore.QRect(310, 170, 91, 23))
        self.zeroButton.setObjectName(_fromUtf8("zeroButton"))
        self.input = QtGui.QLineEdit(self.scrollAreaWidgetContents)
        self.input.setGeometry(QtCore.QRect(70, 170, 131, 20))
        self.input.setObjectName(_fromUtf8("input"))
        self.inputLable = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.inputLable.setGeometry(QtCore.QRect(10, 170, 61, 21))
        self.inputLable.setObjectName(_fromUtf8("inputLable"))
        self.selectVisa = QtGui.QComboBox(self.scrollAreaWidgetContents)
        self.selectVisa.setGeometry(QtCore.QRect(10, 20, 391, 22))
        self.selectVisa.setObjectName(_fromUtf8("selectVisa"))
        self.selectVisaButton = QtGui.QPushButton(self.scrollAreaWidgetContents)
        self.selectVisaButton.setGeometry(QtCore.QRect(10, 60, 91, 23))
        self.selectVisaButton.setObjectName(_fromUtf8("selectVisaButton"))
        self.updateVisaButton = QtGui.QPushButton(self.scrollAreaWidgetContents)
        self.updateVisaButton.setGeometry(QtCore.QRect(110, 60, 91, 23))
        self.updateVisaButton.setObjectName(_fromUtf8("updateVisaButton"))
        self.error = QtGui.QTextEdit(self.scrollAreaWidgetContents)
        self.error.setGeometry(QtCore.QRect(210, 210, 191, 61))
        self.error.setObjectName(_fromUtf8("error"))
        self.sendButton = QtGui.QPushButton(self.scrollAreaWidgetContents)
        self.sendButton.setGeometry(QtCore.QRect(210, 170, 91, 23))
        self.sendButton.setObjectName(_fromUtf8("sendButton"))
        self.quitButton = QtGui.QPushButton(self.scrollAreaWidgetContents)
        self.quitButton.setGeometry(QtCore.QRect(780, 620, 71, 23))
        self.quitButton.setObjectName(_fromUtf8("quitButton"))
        self.stepValue = QtGui.QLineEdit(self.scrollAreaWidgetContents)
        self.stepValue.setGeometry(QtCore.QRect(70, 210, 71, 20))
        self.stepValue.setObjectName(_fromUtf8("stepValue"))
        self.outputLable = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.outputLable.setGeometry(QtCore.QRect(10, 480, 41, 21))
        self.outputLable.setObjectName(_fromUtf8("outputLable"))
        self.setpValueLable = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.setpValueLable.setGeometry(QtCore.QRect(10, 210, 61, 21))
        self.setpValueLable.setObjectName(_fromUtf8("setpValueLable"))
        self.errorLable = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.errorLable.setGeometry(QtCore.QRect(170, 210, 31, 21))
        self.errorLable.setObjectName(_fromUtf8("errorLable"))
        self.selectVisaLable = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.selectVisaLable.setGeometry(QtCore.QRect(10, 0, 71, 21))
        self.selectVisaLable.setObjectName(_fromUtf8("selectVisaLable"))
        self.closeVisaButton = QtGui.QPushButton(self.scrollAreaWidgetContents)
        self.closeVisaButton.setGeometry(QtCore.QRect(310, 60, 91, 23))
        self.closeVisaButton.setObjectName(_fromUtf8("closeVisaButton"))
        self.plotWidget = QtGui.QWidget(self.scrollAreaWidgetContents)
        self.plotWidget.setGeometry(QtCore.QRect(400, 10, 461, 611))
        self.plotWidget.setObjectName(_fromUtf8("plotWidget"))
        self.plot = MatplotlibWidget(self.plotWidget)
        self.plot.setGeometry(QtCore.QRect(210, 290, 51, 41))
        self.plot.setObjectName(_fromUtf8("plot"))
        self.visaLable = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.visaLable.setGeometry(QtCore.QRect(10, 40, 71, 21))
        self.visaLable.setObjectName(_fromUtf8("visaLable"))
        self.visa = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.visa.setGeometry(QtCore.QRect(70, 40, 331, 21))
        self.visa.setText(_fromUtf8(""))
        self.visa.setObjectName(_fromUtf8("visa"))
        self.voltage = QtGui.QLineEdit(self.scrollAreaWidgetContents)
        self.voltage.setGeometry(QtCore.QRect(70, 100, 131, 20))
        self.voltage.setObjectName(_fromUtf8("voltage"))
        self.voltageLable = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.voltageLable.setGeometry(QtCore.QRect(10, 100, 61, 21))
        self.voltageLable.setObjectName(_fromUtf8("voltageLable"))
        self.timeStepValueLable = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.timeStepValueLable.setGeometry(QtCore.QRect(10, 250, 61, 21))
        self.timeStepValueLable.setObjectName(_fromUtf8("timeStepValueLable"))
        self.timeStepValue = QtGui.QLineEdit(self.scrollAreaWidgetContents)
        self.timeStepValue.setGeometry(QtCore.QRect(70, 250, 71, 20))
        self.timeStepValue.setObjectName(_fromUtf8("timeStepValue"))
        self.currentLable = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.currentLable.setGeometry(QtCore.QRect(10, 130, 61, 21))
        self.currentLable.setObjectName(_fromUtf8("currentLable"))
        self.current = QtGui.QLineEdit(self.scrollAreaWidgetContents)
        self.current.setGeometry(QtCore.QRect(70, 130, 131, 20))
        self.current.setObjectName(_fromUtf8("current"))
        self.output = QtGui.QTextEdit(self.scrollAreaWidgetContents)
        self.output.setGeometry(QtCore.QRect(10, 500, 391, 111))
        self.output.setObjectName(_fromUtf8("output"))
        self.saveBox = QtGui.QGroupBox(self.scrollAreaWidgetContents)
        self.saveBox.setGeometry(QtCore.QRect(10, 280, 191, 181))
        self.saveBox.setObjectName(_fromUtf8("saveBox"))
        self.browseButton = QtGui.QPushButton(self.saveBox)
        self.browseButton.setGeometry(QtCore.QRect(10, 20, 81, 23))
        self.browseButton.setObjectName(_fromUtf8("browseButton"))
        self.fileTypeLable = QtGui.QLabel(self.saveBox)
        self.fileTypeLable.setGeometry(QtCore.QRect(10, 50, 51, 21))
        self.fileTypeLable.setObjectName(_fromUtf8("fileTypeLable"))
        self.csvRadio = QtGui.QRadioButton(self.saveBox)
        self.csvRadio.setGeometry(QtCore.QRect(70, 50, 41, 17))
        self.csvRadio.setObjectName(_fromUtf8("csvRadio"))
        self.txtRadio = QtGui.QRadioButton(self.saveBox)
        self.txtRadio.setGeometry(QtCore.QRect(120, 50, 41, 17))
        self.txtRadio.setObjectName(_fromUtf8("txtRadio"))
        self.directoryLable = QtGui.QLabel(self.saveBox)
        self.directoryLable.setGeometry(QtCore.QRect(10, 80, 111, 21))
        self.directoryLable.setObjectName(_fromUtf8("directoryLable"))
        self.directory = QtGui.QLineEdit(self.saveBox)
        self.directory.setGeometry(QtCore.QRect(10, 100, 171, 20))
        self.directory.setObjectName(_fromUtf8("directory"))
        self.fileLable = QtGui.QLabel(self.saveBox)
        self.fileLable.setGeometry(QtCore.QRect(200, 130, 51, 21))
        self.fileLable.setObjectName(_fromUtf8("fileLable"))
        self.saveButton = QtGui.QPushButton(self.saveBox)
        self.saveButton.setGeometry(QtCore.QRect(100, 20, 81, 23))
        self.saveButton.setObjectName(_fromUtf8("saveButton"))
        self.folderName = QtGui.QComboBox(self.saveBox)
        self.folderName.setGeometry(QtCore.QRect(10, 150, 171, 21))
        self.folderName.setObjectName(_fromUtf8("folderName"))
        self.folderNameLable = QtGui.QLabel(self.saveBox)
        self.folderNameLable.setGeometry(QtCore.QRect(10, 130, 71, 21))
        self.folderNameLable.setObjectName(_fromUtf8("folderNameLable"))
        self.fileBox = QtGui.QGroupBox(self.scrollAreaWidgetContents)
        self.fileBox.setGeometry(QtCore.QRect(210, 280, 191, 71))
        self.fileBox.setObjectName(_fromUtf8("fileBox"))
        self.defaultFile = QtGui.QRadioButton(self.fileBox)
        self.defaultFile.setGeometry(QtCore.QRect(10, 20, 91, 17))
        self.defaultFile.setObjectName(_fromUtf8("defaultFile"))
        self.customFile = QtGui.QRadioButton(self.fileBox)
        self.customFile.setGeometry(QtCore.QRect(10, 40, 61, 17))
        self.customFile.setObjectName(_fromUtf8("customFile"))
        self.file = QtGui.QLineEdit(self.fileBox)
        self.file.setGeometry(QtCore.QRect(70, 40, 111, 20))
        self.file.setObjectName(_fromUtf8("file"))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.upButton.setText(_translate("MainWindow", "Up", None))
        self.downButton.setText(_translate("MainWindow", "Down", None))
        self.zeroButton.setText(_translate("MainWindow", "Zero", None))
        self.inputLable.setText(_translate("MainWindow", "Target Vol:", None))
        self.selectVisaButton.setText(_translate("MainWindow", "Select", None))
        self.updateVisaButton.setText(_translate("MainWindow", "Update", None))
        self.sendButton.setText(_translate("MainWindow", "Send", None))
        self.quitButton.setText(_translate("MainWindow", "Quit", None))
        self.outputLable.setText(_translate("MainWindow", "Output:", None))
        self.setpValueLable.setText(_translate("MainWindow", "Step Value:", None))
        self.errorLable.setText(_translate("MainWindow", "Error:", None))
        self.selectVisaLable.setText(_translate("MainWindow", "Select Visa:", None))
        self.closeVisaButton.setText(_translate("MainWindow", "Close Visa", None))
        self.visaLable.setText(_translate("MainWindow", "Curent Visa:", None))
        self.voltageLable.setText(_translate("MainWindow", "Curent Vol:", None))
        self.timeStepValueLable.setText(_translate("MainWindow", "Time Step:", None))
        self.currentLable.setText(_translate("MainWindow", "Curent I:", None))
        self.saveBox.setTitle(_translate("MainWindow", "Save", None))
        self.browseButton.setText(_translate("MainWindow", "Browse", None))
        self.fileTypeLable.setText(_translate("MainWindow", "File Type:", None))
        self.csvRadio.setText(_translate("MainWindow", "csv", None))
        self.txtRadio.setText(_translate("MainWindow", "txt", None))
        self.directoryLable.setText(_translate("MainWindow", "Directory:", None))
        self.fileLable.setText(_translate("MainWindow", "File Name:", None))
        self.saveButton.setText(_translate("MainWindow", "Save", None))
        self.folderNameLable.setText(_translate("MainWindow", "Folder Name:", None))
        self.fileBox.setTitle(_translate("MainWindow", "File Name", None))
        self.defaultFile.setText(_translate("MainWindow", "Date and Time", None))
        self.customFile.setText(_translate("MainWindow", "Custum", None))

from matplotlibwidget import MatplotlibWidget
