# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'banner.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
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

class Ui_Banner(object):
    def setupUi(self, Banner):
        Banner.setObjectName(_fromUtf8("Banner"))
        Banner.resize(500, 500)
        self.centralwidget = QtGui.QWidget(Banner)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 240, 461, 51))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setStyleSheet(_fromUtf8(""))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(160, 160, 171, 111))
        font = QtGui.QFont()
        font.setPointSize(48)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(390, 440, 98, 27))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        Banner.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(Banner)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        Banner.setStatusBar(self.statusbar)

        self.retranslateUi(Banner)
        QtCore.QMetaObject.connectSlotsByName(Banner)

    def retranslateUi(self, Banner):
        Banner.setWindowTitle(_translate("Banner", "AVAS", None))
        self.label.setText(_translate("Banner", "Array visualization and analysis software", None))
        self.label_2.setText(_translate("Banner", "AVAS", None))
        self.pushButton.setText(_translate("Banner", "Load File", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Banner = QtGui.QMainWindow()
    ui = Ui_Banner()
    ui.setupUi(Banner)
    Banner.show()
    sys.exit(app.exec_())

