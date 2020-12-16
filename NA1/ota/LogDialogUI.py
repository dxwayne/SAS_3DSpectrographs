# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'LogDialogUI.ui',
# licensing of 'LogDialogUI.ui' applies.
#
# Created: Wed Dec 16 07:57:44 2020
#      by: pyside2-uic  running on PySide2 5.9.0~a1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_LogDialogUI(object):
    def setupUi(self, LogDialogUI):
        LogDialogUI.setObjectName("LogDialogUI")
        LogDialogUI.resize(640, 579)
        self.buttonBox = QtWidgets.QDialogButtonBox(LogDialogUI)
        self.buttonBox.setGeometry(QtCore.QRect(270, 545, 91, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.logGroupBox = QtWidgets.QGroupBox(LogDialogUI)
        self.logGroupBox.setGeometry(QtCore.QRect(15, 10, 606, 536))
        self.logGroupBox.setObjectName("logGroupBox")
        self.logText = QtWidgets.QPlainTextEdit(self.logGroupBox)
        self.logText.setGeometry(QtCore.QRect(5, 25, 596, 501))
        self.logText.setObjectName("logText")

        self.retranslateUi(LogDialogUI)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), LogDialogUI.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), LogDialogUI.reject)
        QtCore.QMetaObject.connectSlotsByName(LogDialogUI)

    def retranslateUi(self, LogDialogUI):
        LogDialogUI.setWindowTitle(QtWidgets.QApplication.translate("LogDialogUI", "Log", None, -1))
        self.logGroupBox.setToolTip(QtWidgets.QApplication.translate("LogDialogUI", "Log entries for one or more entities.", None, -1))
        self.logGroupBox.setTitle(QtWidgets.QApplication.translate("LogDialogUI", "Log", None, -1))

