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


def selectionGrid(parent):
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
        optionsRow = [str(x) for x in range(parent.widthValue)]
        optionsColumn = [str(x) for x in range(parent.heightValue)]

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
        leFromRow.activated.connect(parent.changedSelectionAction)
        leToRow.activated.connect(parent.changedSelectionAction)

        leFromColumn.activated.connect(parent.changedSelectionAction)
        leToColumn.activated.connect(parent.changedSelectionAction)

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

def Grid(parent):
        dataGrid = {}
        grid = QGridLayout()
        grid.setSpacing(0)

        for i in range(parent.widthValue):
            newButton = QLabel(str(i))
            newButton.setAlignment(Qt.AlignHCenter)
            newButton.setFixedWidth(60)
            grid.addWidget(newButton, 0, i+1)

        for j in range(parent.heightValue):
            newButton = QLabel(str(j))
            newButton.setFixedWidth(20)
            grid.addWidget(newButton, j+1, 0)

        for i in range(parent.widthValue):
            for j in range(parent.heightValue):
                newLineEdit = QLineEdit()
                newLineEdit.setFixedWidth(60)

                dataGrid[(i,j)] = newLineEdit
                grid.addWidget(newLineEdit, i+1, j+1)
        return dataGrid, grid






def controlsBar(parent):
        # Controls
        controlGrid = QGridLayout()

        bBack = QPushButton('back')
        bForward = QPushButton('forward')
        bBack.clicked.connect(parent.moveBackAction)
        bForward.clicked.connect(parent.moveForwardAction)
        leValue = QLineEdit()
        leValue.textChanged.connect(parent.textChangedAction)
        leValue.setFixedWidth(50)
        controlValue = leValue

        controlGrid.addWidget(bBack, 0,1)
        controlGrid.addWidget(leValue, 0,2)
        controlGrid.addWidget(bForward, 0,3)
        return controlValue, controlGrid