# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'navbar.ui'
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

class Ui_NavBar(object):
    def setupUi(self, NavBar):
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.bBack = QtGui.QPushButton()
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bBack.sizePolicy().hasHeightForWidth())
        self.bBack.setSizePolicy(sizePolicy)
        self.bBack.setMinimumSize(QtCore.QSize(31, 31))
        self.bBack.setMaximumSize(QtCore.QSize(31, 31))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.bBack.setFont(font)
        self.bBack.setStyleSheet(_fromUtf8(""))
        self.bBack.setObjectName(_fromUtf8("bBack"))
        self.horizontalLayout.addWidget(self.bBack)
        self.leValue = QtGui.QLineEdit()
        self.leValue.setMinimumSize(QtCore.QSize(0, 31))
        self.leValue.setMaximumSize(QtCore.QSize(100, 31))
        self.leValue.setObjectName(_fromUtf8("leValue"))
        self.horizontalLayout.addWidget(self.leValue)
        self.bForward = QtGui.QPushButton()
        self.bForward.setMinimumSize(QtCore.QSize(31, 31))
        self.bForward.setMaximumSize(QtCore.QSize(31, 31))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.bForward.setFont(font)
        self.bForward.setStyleSheet(_fromUtf8(""))
        self.bForward.setObjectName(_fromUtf8("bForward"))
        self.horizontalLayout.addWidget(self.bForward)

        self.retranslateUi()

    def retranslateUi(self):
        self.bBack.setText(_translate("NavBar", "<", None))
        self.bForward.setText(_translate("NavBar", ">", None))



if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    NavBar = QtGui.QWidget()
    ui = Ui_NavBar()
    ui.setupUi(NavBar)
    NavBar.show()
    sys.exit(app.exec_())

