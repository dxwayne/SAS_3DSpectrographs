# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'NASpectrographyUI.ui',
# licensing of 'NASpectrographyUI.ui' applies.
#
# Created: Wed Dec 16 07:57:44 2020
#      by: pyside2-uic  running on PySide2 5.9.0~a1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_NASpectrography(object):
    def setupUi(self, NASpectrography):
        NASpectrography.setObjectName("NASpectrography")
        NASpectrography.resize(640, 480)
        NASpectrography.setStyleSheet("QMainWindow {background: yellow}")
        self.centralwidget = QtWidgets.QWidget(NASpectrography)
        self.centralwidget.setStyleSheet("QWidget#centralwidget {background: darkred}")
        self.centralwidget.setObjectName("centralwidget")
        self.OTADialog = QtWidgets.QPushButton(self.centralwidget)
        self.OTADialog.setGeometry(QtCore.QRect(30, 20, 91, 23))
        self.OTADialog.setStyleSheet("QPushButton {background-color: darkred; color: white}")
        self.OTADialog.setObjectName("OTADialog")
        self.SpectrographDialog = QtWidgets.QPushButton(self.centralwidget)
        self.SpectrographDialog.setGeometry(QtCore.QRect(30, 50, 91, 23))
        self.SpectrographDialog.setStyleSheet("QPushButton {background-color: darkred; color: white}")
        self.SpectrographDialog.setObjectName("SpectrographDialog")
        self.PhotometryDialog = QtWidgets.QPushButton(self.centralwidget)
        self.PhotometryDialog.setGeometry(QtCore.QRect(30, 80, 91, 23))
        self.PhotometryDialog.setStyleSheet("QPushButton {background-color: darkred; color: white}")
        self.PhotometryDialog.setObjectName("PhotometryDialog")
        self.WeatherDialog = QtWidgets.QPushButton(self.centralwidget)
        self.WeatherDialog.setGeometry(QtCore.QRect(30, 110, 91, 23))
        self.WeatherDialog.setStyleSheet("QPushButton {background-color: darkred; color: white}")
        self.WeatherDialog.setObjectName("WeatherDialog")
        NASpectrography.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(NASpectrography)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 20))
        self.menubar.setStyleSheet("QMenuBar#menubar { background-color: black; color: white}")
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        NASpectrography.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(NASpectrography)
        self.statusbar.setStyleSheet("QStatusBar#statusbar {background-color: black}")
        self.statusbar.setObjectName("statusbar")
        NASpectrography.setStatusBar(self.statusbar)
        self.menufileOpen = QtWidgets.QAction(NASpectrography)
        self.menufileOpen.setObjectName("menufileOpen")
        self.menuDilogs = QtWidgets.QAction(NASpectrography)
        self.menuDilogs.setObjectName("menuDilogs")
        self.actionSpectrograph_Dialog = QtWidgets.QAction(NASpectrography)
        self.actionSpectrograph_Dialog.setObjectName("actionSpectrograph_Dialog")
        self.actionPhotometry_Dialog = QtWidgets.QAction(NASpectrography)
        self.actionPhotometry_Dialog.setObjectName("actionPhotometry_Dialog")
        self.actionWeather_Dialog = QtWidgets.QAction(NASpectrography)
        self.actionWeather_Dialog.setObjectName("actionWeather_Dialog")
        self.menuFile.addAction(self.menufileOpen)
        self.menuHelp.addAction(self.menuDilogs)
        self.menuHelp.addAction(self.actionSpectrograph_Dialog)
        self.menuHelp.addAction(self.actionPhotometry_Dialog)
        self.menuHelp.addAction(self.actionWeather_Dialog)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(NASpectrography)
        QtCore.QMetaObject.connectSlotsByName(NASpectrography)

    def retranslateUi(self, NASpectrography):
        NASpectrography.setWindowTitle(QtWidgets.QApplication.translate("NASpectrography", "MainWindow", None, -1))
        self.OTADialog.setText(QtWidgets.QApplication.translate("NASpectrography", "OTA", None, -1))
        self.SpectrographDialog.setText(QtWidgets.QApplication.translate("NASpectrography", "Spectrograph", None, -1))
        self.PhotometryDialog.setText(QtWidgets.QApplication.translate("NASpectrography", "Photometry", None, -1))
        self.WeatherDialog.setText(QtWidgets.QApplication.translate("NASpectrography", "Weather", None, -1))
        self.menuFile.setTitle(QtWidgets.QApplication.translate("NASpectrography", "File", None, -1))
        self.menuHelp.setTitle(QtWidgets.QApplication.translate("NASpectrography", "Dialogs", None, -1))
        self.menufileOpen.setText(QtWidgets.QApplication.translate("NASpectrography", "Open", None, -1))
        self.menuDilogs.setText(QtWidgets.QApplication.translate("NASpectrography", "OTA Dialog", None, -1))
        self.actionSpectrograph_Dialog.setText(QtWidgets.QApplication.translate("NASpectrography", "Spectrograph Dialog", None, -1))
        self.actionPhotometry_Dialog.setText(QtWidgets.QApplication.translate("NASpectrography", "Photometry Dialog", None, -1))
        self.actionWeather_Dialog.setText(QtWidgets.QApplication.translate("NASpectrography", "Weather Dialog", None, -1))

