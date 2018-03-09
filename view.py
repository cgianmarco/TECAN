#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import widgets

class View(QMainWindow):
    
    def __init__(self, parent=None):
        super(View, self).__init__(parent)
        self.widthValue = 8
        self.heightValue = 8
        self.initListeners()
        self.initMenuBar()
        self.initUI()

    def initListeners(self):
        self.matrixLoadAction = lambda x : None
        self.meanAction = lambda x : None
        self.stdAction = lambda x : None
        self.subtractAction = lambda x : None
        self.moveBackAction = lambda x : None
        self.moveForwardAction = lambda x : None
        self.textChangedAction = lambda x : None
        self.changedSelectionAction = lambda x : None



    def initMenuBar(self):
    	# menubar
        bar = self.menuBar()
        file = bar.addMenu("File")
        file.triggered[QAction].connect(self.processtrigger)

        # actions
        file.addAction("Load Matrix")
        file.addAction("Mean")
        file.addAction("Standard deviation")
    
        subtract = file.addMenu("Subtract")
        subtract.addAction("Value from Selected")

      
    def initUI(self):
        # main layout
        vlayout = QVBoxLayout()

        self.dataGrid, gridlayout = widgets.Grid(self)
        self.selected, selectionLayout = widgets.selectionGrid(self)
        self.controlValue, controlLayout = widgets.controlsBar(self)
        self.listValue, listWidget = widgets.listWidget()

        # Add Child Layouts
        vlayout.addLayout(selectionLayout)
        vlayout.addLayout(controlLayout)
    	vlayout.addLayout(gridlayout)
    	vlayout.addWidget(listWidget)


    	mainWidget = QWidget()
    	mainWidget.setLayout(vlayout)
    	self.setCentralWidget(mainWidget)        
        self.move(300, 150)
        self.setWindowTitle('TECAN Reader')
        self.show()

    def setDimensions(self, width, height):
        self.widthValue = width
        self.heightValue = height

    def getFileName(self):
        return QFileDialog.getOpenFileName(self, 'Open file', "Excel files (*.xlsx)")

    def addMatrixLoadAction(self, action):
        self.matrixLoadAction = action

    def addMeanAction(self, action):
        self.meanAction = action

    def addStdAction(self, action):
        self.stdAction = action

    def addSubtractAction(self, action):
        self.subtractAction = action

    def addMoveBackAction(self, action):
        self.moveBackAction = action

    def addMoveForwardAction(self, action):
        self.moveForwardAction = action

    def addTextChangedAction(self, action):
        self.textChangedAction = action

    def addChangedSelectionAction(self, action):
        self.changedSelectionAction = action

    def processtrigger(self, q):
        if q.text() == 'Load Matrix':
            self.matrixLoadAction()
        elif q.text() == 'Mean':
            self.meanAction()
        elif q.text() == 'Value from Selected':
            self.subtractAction()
        elif q.text() == 'Standard deviation':
            self.stdAction()

    def updateGrid(self, matrix):
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                value = matrix[i][j]
                self.dataGrid[(i,j)].setText(str(value))

    def getSelected(self):
        return [ int(elem.currentText()) for elem in self.selected ]

    def updateControlValue(self, value):
        # controlValue.setText(str(processing.wl_start + processing.currentDepth))
        self.controlValue.setText(str(value))

    def getListSelected(self):
        return float(str(self.listValue.currentItem().text()).split(" ")[1])



