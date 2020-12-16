# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AttitudeUI.ui',
# licensing of 'AttitudeUI.ui' applies.
#
# Created: Wed Dec 16 07:57:44 2020
#      by: pyside2-uic  running on PySide2 5.9.0~a1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Attitude(object):
    def setupUi(self, Attitude):
        Attitude.setObjectName("Attitude")
        Attitude.resize(402, 157)
        self.closeButton = QtWidgets.QDialogButtonBox(Attitude)
        self.closeButton.setGeometry(QtCore.QRect(165, 115, 86, 32))
        self.closeButton.setOrientation(QtCore.Qt.Horizontal)
        self.closeButton.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.closeButton.setObjectName("closeButton")
        self.radecLabel = QtWidgets.QLabel(Attitude)
        self.radecLabel.setGeometry(QtCore.QRect(10, 45, 59, 15))
        self.radecLabel.setObjectName("radecLabel")
        self.attitudeLabel = QtWidgets.QLabel(Attitude)
        self.attitudeLabel.setGeometry(QtCore.QRect(10, 80, 59, 15))
        self.attitudeLabel.setObjectName("attitudeLabel")
        self.label_3 = QtWidgets.QLabel(Attitude)
        self.label_3.setGeometry(QtCore.QRect(105, 65, 21, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Attitude)
        self.label_4.setGeometry(QtCore.QRect(185, 65, 21, 16))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Attitude)
        self.label_5.setGeometry(QtCore.QRect(255, 65, 21, 16))
        self.label_5.setObjectName("label_5")
        self.coordinatesText = QtWidgets.QLineEdit(Attitude)
        self.coordinatesText.setGeometry(QtCore.QRect(85, 40, 301, 23))
        self.coordinatesText.setToolTip("")
        self.coordinatesText.setAccessibleDescription("")
        self.coordinatesText.setText("")
        self.coordinatesText.setObjectName("coordinatesText")
        self.attitude_xText = QtWidgets.QLineEdit(Attitude)
        self.attitude_xText.setGeometry(QtCore.QRect(85, 80, 61, 23))
        self.attitude_xText.setObjectName("attitude_xText")
        self.attitude_yText = QtWidgets.QLineEdit(Attitude)
        self.attitude_yText.setGeometry(QtCore.QRect(155, 80, 61, 23))
        self.attitude_yText.setObjectName("attitude_yText")
        self.attitude_zText = QtWidgets.QLineEdit(Attitude)
        self.attitude_zText.setGeometry(QtCore.QRect(225, 80, 61, 23))
        self.attitude_zText.setObjectName("attitude_zText")
        self.attitude_update = QtWidgets.QPushButton(Attitude)
        self.attitude_update.setGeometry(QtCore.QRect(305, 80, 80, 23))
        self.attitude_update.setObjectName("attitude_update")
        self.dateobsLabel = QtWidgets.QLabel(Attitude)
        self.dateobsLabel.setGeometry(QtCore.QRect(10, 10, 71, 16))
        self.dateobsLabel.setObjectName("dateobsLabel")
        self.dateobsText = QtWidgets.QLineEdit(Attitude)
        self.dateobsText.setGeometry(QtCore.QRect(85, 5, 151, 23))
        self.dateobsText.setText("")
        self.dateobsText.setObjectName("dateobsText")
        self.siderealLabel = QtWidgets.QLabel(Attitude)
        self.siderealLabel.setGeometry(QtCore.QRect(245, 10, 59, 15))
        self.siderealLabel.setObjectName("siderealLabel")
        self.siderealText = QtWidgets.QLineEdit(Attitude)
        self.siderealText.setGeometry(QtCore.QRect(305, 5, 76, 23))
        self.siderealText.setText("")
        self.siderealText.setObjectName("siderealText")
        self.pushButton = QtWidgets.QPushButton(Attitude)
        self.pushButton.setGeometry(QtCore.QRect(10, 115, 51, 23))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Attitude)
        QtCore.QObject.connect(self.closeButton, QtCore.SIGNAL("rejected()"), Attitude.reject)
        QtCore.QObject.connect(self.closeButton, QtCore.SIGNAL("accepted()"), Attitude.accept)
        QtCore.QMetaObject.connectSlotsByName(Attitude)

    def retranslateUi(self, Attitude):
        Attitude.setWindowTitle(QtWidgets.QApplication.translate("Attitude", "Attitude", None, -1))
        self.radecLabel.setText(QtWidgets.QApplication.translate("Attitude", "RA/Dec", None, -1))
        self.attitudeLabel.setText(QtWidgets.QApplication.translate("Attitude", "Attitude", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("Attitude", "X", None, -1))
        self.label_4.setText(QtWidgets.QApplication.translate("Attitude", "Y", None, -1))
        self.label_5.setText(QtWidgets.QApplication.translate("Attitude", "Z", None, -1))
        self.coordinatesText.setPlaceholderText(QtWidgets.QApplication.translate("Attitude", "15 59 30.1619486506 +25 55 12.607985109", None, -1))
        self.attitude_update.setText(QtWidgets.QApplication.translate("Attitude", "Refresh", None, -1))
        self.dateobsLabel.setText(QtWidgets.QApplication.translate("Attitude", "DATE-OBS", None, -1))
        self.dateobsText.setPlaceholderText(QtWidgets.QApplication.translate("Attitude", "2020-07-04T00:00:00", None, -1))
        self.siderealLabel.setText(QtWidgets.QApplication.translate("Attitude", "Sidereal", None, -1))
        self.siderealText.setPlaceholderText(QtWidgets.QApplication.translate("Attitude", "12:00:00", None, -1))
        self.pushButton.setText(QtWidgets.QApplication.translate("Attitude", "Now", None, -1))

