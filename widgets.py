#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

def listWidget():
        listWidget = QListWidget()
        listWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        listValue = listWidget
        listWidget.resize(300,120)

        return listValue, listWidget


def selectionGrid(width, height, changedSelectionAction):
        # selector
        selectionGrid = QGridLayout()
        lFrom = QLabel('Da')
        lTo = QLabel('A')

        lFrom.setFixedWidth(20)
        lTo.setFixedWidth(20)

        lRow = QLabel('Riga')
        lColumn = QLabel('Colonna')
        lDepth = QLabel('Profondità')

        # optionsDepth = [str(x) for x in range(len(data))]
        optionsRow = [str(x) for x in range(width)]
        optionsColumn = [str(x) for x in range(height)]

        leFromRow = QComboBox()
        leFromRow.addItems(optionsRow)
        
        leToRow = QComboBox()
        leToRow.addItems(optionsRow)

        leFromColumn = QComboBox()
        leFromColumn.addItems(optionsColumn)

        leToColumn = QComboBox()
        leToColumn.addItems(optionsColumn)
        selected = [leFromRow, leToRow, leFromColumn, leToColumn]

        # leFromDepth = QComboBox()
        # leFromDepth.addItems(optionsDepth)

        # leToDepth = QComboBox()
        # leToDepth.addItems(optionsDepth)

        # Events
        leFromRow.activated.connect(changedSelectionAction)
        leToRow.activated.connect(changedSelectionAction)

        leFromColumn.activated.connect(changedSelectionAction)
        leToColumn.activated.connect(changedSelectionAction)

        selectionGrid.addWidget(lFrom, 1,0)
        selectionGrid.addWidget(lTo, 2,0)

        selectionGrid.addWidget(lRow, 0,1)
        selectionGrid.addWidget(lColumn, 0,2)
        # selectionGrid.addWidget(lDepth, 0,3)

        selectionGrid.addWidget(leFromRow, 1,1)
        selectionGrid.addWidget(leFromColumn, 1,2)
        # selectionGrid.addWidget(leFromDepth, 1,3)

        selectionGrid.addWidget(leToRow, 2,1)
        selectionGrid.addWidget(leToColumn, 2,2)
        # selectionGrid.addWidget(leToDepth, 2,3)
        return selected, selectionGrid

def Grid(width, height):
        dataGrid = {}
        grid = QGridLayout()
        grid.setSpacing(0)

        for i in range(width):
            newButton = QLabel(str(i))
            newButton.setAlignment(Qt.AlignHCenter)
            newButton.setFixedWidth(60)
            grid.addWidget(newButton, 0, i+1)

        for j in range(height):
            newButton = QLabel(str(j))
            newButton.setFixedWidth(20)
            grid.addWidget(newButton, j+1, 0)

        for i in range(width):
            for j in range(height):
                newLineEdit = QLineEdit()
                newLineEdit.setFixedWidth(60)

                dataGrid[(i,j)] = newLineEdit
                grid.addWidget(newLineEdit, i+1, j+1)

        stretch = QHBoxLayout()
        stretch.addStretch(1)
        grid.addLayout(stretch, 0, height + 2)

        return dataGrid, grid






def controlsBar(moveBackAction, moveForwardAction, textChangedAction):
        # Controls
        controlGrid = QGridLayout()

        bBack = QPushButton('back')
        bForward = QPushButton('forward')
        bBack.clicked.connect(moveBackAction)
        bForward.clicked.connect(moveForwardAction)
        leValue = QLineEdit()
        leValue.textChanged.connect(textChangedAction)
        leValue.setFixedWidth(50)
        controlValue = leValue

        controlGrid.addWidget(bBack, 0,1)
        controlGrid.addWidget(leValue, 0,2)
        controlGrid.addWidget(bForward, 0,3)
        return controlValue, controlGrid

def newStack(layouts):
        # self.dataGrid, gridLayout = widgets.Grid(self)
        # self.selected, selectionLayout = widgets.selectionGrid(self)
        # self.controlValue, controlLayout = widgets.controlsBar(self)

        # layouts = [selectionLayout, controlLayout, gridLayout]


        stack = QWidget()
        layout = QVBoxLayout()
        for childLayout in layouts:
            layout.addLayout(childLayout)
        stack.setLayout(layout)
        return stack
        # self.stacks.addWidget(stack)
        # self.stacklist.insertItem (0, 'Matrix0' )

def changedStack(x):
    print(x)

def stackLayout():
    stacklist = QListWidget ()
    # stacklist.insertItem (1, 'Matrix0' )
    #stacklist.insertItem (2, 'Educational')

    # stack1 = QWidget()
    # stack2 = QWidget()
    # stack3 = QWidget()
        
    # stack1UI(stack1, parent)
    # stack2UI(stack2)
    # stack3UI(stack3)
        
    stack = QStackedWidget()
    # Stack.addWidget(stack1)
    # Stack.addWidget(stack2)
    # Stack.addWidget(stack3)

    # stacklist.currentRowChanged.connect(changedStackAction)
    #stacklist.currentRowChanged.connect(prova)

    hbox = QHBoxLayout()
    hbox.addWidget(stacklist)
    hbox.addWidget(stack)

    return stacklist, stack, hbox