#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import widgets

class Stack():
    def __init__(self, width, height, changedSelectionAction, moveBackAction, moveForwardAction, textChangedAction):
        self.widthValue = width
        self.heightValue = height
        self.dataGrid, gridLayout = widgets.Grid(width, height)
        self.selected, selectionLayout = widgets.selectionGrid(width, height, changedSelectionAction)
        self.controlValue, controlLayout = widgets.controlsBar(moveBackAction, moveForwardAction, textChangedAction)

        layouts = [selectionLayout, controlLayout, gridLayout]
        self.stackWidget = QWidget()
        layout = QVBoxLayout()
        for childLayout in layouts:
            layout.addLayout(childLayout)
        layout.addStretch(1)
        self.stackWidget.setLayout(layout)



class View(QMainWindow):
    
    def __init__(self, parent=None):
        super(View, self).__init__(parent)
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
        self.changedStackAction = lambda x : None



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

        self.stacks = {"Matrix0" : Stack(6, 6, self.changedSelectionAction, self.moveBackAction, self.moveForwardAction, self.textChangedAction)}
        self.currentStack = "Matrix0"
        self.lastIndex = 0
        self.stackList, self.stackedWidget, stackLayout = widgets.stackLayout()
        self.listValue, listWidget = widgets.listWidget()
        self.initialized = False

        # Add Child Layouts
        self.stackedWidget.addWidget(self.stack.stackWidget)
        vlayout.addLayout(stackLayout)
    	vlayout.addWidget(listWidget)


    	mainWidget = QWidget()
    	mainWidget.setLayout(vlayout)
    	self.setCentralWidget(mainWidget)        
        self.move(300, 150)
        self.setWindowTitle('TECAN Reader')
        self.show()

    def addNewStack(self, width, height):
        if self.initialized == True:
            self.lastIndex += 1
        else:
            self.initialized = True
            self.stackedWidget.removeWidget(self.stackedWidget.widget(0))
        newKey = "Matrix" + str(self.lastIndex)
        self.stacks[newKey] = Stack(width, height, self.changedSelectionAction, self.moveBackAction, self.moveForwardAction, self.textChangedAction)
        self.stackedWidget.addWidget(self.stacks[newKey].stackWidget)
        self.stackList.addItem(newKey)
        self.currentStack = newKey

    def removeStack(self, key):
        del self.stacks[key]
        self.stackedWidget.removeWidget(self.stackedWidget.widget(0))
        self.stackList.takeItem(0)

    @property
    def stack(self):
        return self.stacks[self.currentStack]

    @property
    def dataGrid(self):
        return self.stack.dataGrid

    @property
    def controlValue(self):
        return self.stack.controlValue

    @property
    def selected(self):
        return self.stack.selected

    @property
    def widthValue(self):
        return self.stack.widthValue

    @property
    def heightValue(self):
        return self.stack.heightValue

    @widthValue.setter
    def widthValue(self, value):
        self.stack.widthValue = value

    @heightValue.setter
    def heightValue(self, value):
        self.stack.heightValue = value


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

    def addChangedStackAction(self, action):
        self.stackList.currentRowChanged.connect(action)

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



