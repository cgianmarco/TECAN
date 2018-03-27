#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

def listWidget():
        listWidget = QListWidget()
        listWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        listWidget.resize(300,120)

        return listWidget


def selectionGrid(shape, changed_selection_action):
        # selector
        selectionGrid = QGridLayout()
        lFrom = QLabel('Da')
        lTo = QLabel('A')

        lFrom.setFixedWidth(20)
        lTo.setFixedWidth(20)

        selected = []
        lDims = []
        selection = {}
        for dim in shape.keys():
            if shape[dim] > 1:
                lDim = QLabel(dim.capitalize())
                lDims.append(lDim)
                if dim != 'depth':
                    optionsDim = [str(x) for x in range(shape[dim])]
                else:
                    optionsDim = [str(x + 550) for x in range(shape[dim])]

                leFromDim = QComboBox()
                leFromDim.addItems(optionsDim)

                leToDim = QComboBox()
                leToDim.addItems(optionsDim)

                selected.extend([leFromDim, leToDim])
                selection[dim] = (leFromDim, leToDim)
                leFromDim.activated.connect(changed_selection_action)
                leToDim.activated.connect(changed_selection_action)
            else:
                selection[dim] = None

        print(selected)

        for i in range(len(lDims)):
            selectionGrid.addWidget(lDims[i], 0, i+1)

        print(len(selected))
        for j in range((len(selected)/2)):
            selectionGrid.addWidget(selected[2*j], 1, j+1)
            selectionGrid.addWidget(selected[2*j+1], 2, j+1)

        selectionGrid.addWidget(lFrom, 1,0)
        selectionGrid.addWidget(lTo, 2,0)

        return selection, selectionGrid

def Grid(width, height):
        datagrid = {}
        grid = QGridLayout()
        grid.setSpacing(0)

        for i in range(width):
            newButton = QLabel(str(i))
            newButton.setAlignment(Qt.AlignHCenter)
            newButton.setFixedWidth(60)
            grid.addWidget(newButton, i+1, 0)

        for j in range(height):
            newButton = QLabel(str(j))
            newButton.setFixedWidth(20)
            grid.addWidget(newButton, 0, j+1)

        for i in range(width):
            for j in range(height):
                newLineEdit = QLineEdit()
                newLineEdit.setFixedWidth(60)

                datagrid[(i,j)] = newLineEdit
                grid.addWidget(newLineEdit, i+1, j+1)

        stretch = QHBoxLayout()
        stretch.addStretch(1)
        grid.addLayout(stretch, 0, height + 2)

        return datagrid, grid






def controlsBar(depth, move_back_action, move_forward_action, text_changed_action):
    if depth > 1:
        # Controls
        controlGrid = QGridLayout()

        bBack = QPushButton('back')
        bForward = QPushButton('forward')
        bBack.clicked.connect(move_back_action)
        bForward.clicked.connect(move_forward_action)
        leValue = QLineEdit()
        leValue.textChanged.connect(text_changed_action)
        leValue.setFixedWidth(50)
        control_value = leValue

        controlGrid.addWidget(bBack, 0,1)
        controlGrid.addWidget(leValue, 0,2)
        controlGrid.addWidget(bForward, 0,3)
        return control_value, controlGrid
    else:
        return None, None

def newStack(layouts):
        stack = QWidget()
        layout = QVBoxLayout()
        for childLayout in layouts:
            layout.addLayout(childLayout)
        stack.setLayout(layout)
        return stack

def changedStack(x):
    print(x)

def stackLayout():
    stacklist = QListWidget ()        
    stack = QStackedWidget()
    hbox = QHBoxLayout()
    hbox.addWidget(stacklist)
    hbox.addWidget(stack)

    return stacklist, stack, hbox