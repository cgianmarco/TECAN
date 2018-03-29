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


def selectionGrid(shape, parent, listener):
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
                leFromDim.activated.connect(lambda : listener.on_changed_selection(parent.get_selected()))
                leToDim.activated.connect(lambda : listener.on_changed_selection(parent.get_selected()))
            else:
                selection[dim] = None


        for i in range(len(lDims)):
            selectionGrid.addWidget(lDims[i], 0, i+1)

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

class SelectionGrid():
    def __init__(self, shape):
        # selector
        self.layout = QGridLayout()
        lFrom = QLabel('Da')
        lTo = QLabel('A')

        lFrom.setFixedWidth(20)
        lTo.setFixedWidth(20)

        self.selected = []
        lDims = []
        self.selection = {}
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

                self.selected.extend([leFromDim, leToDim])
                self.selection[dim] = (leFromDim, leToDim)
            else:
                self.selection[dim] = None


        for i in range(len(lDims)):
            self.layout.addWidget(lDims[i], 0, i+1)

        for j in range((len(self.selected)/2)):
            self.layout.addWidget(self.selected[2*j], 1, j+1)
            self.layout.addWidget(self.selected[2*j+1], 2, j+1)

        self.layout.addWidget(lFrom, 1,0)
        self.layout.addWidget(lTo, 2,0)


    def get_selected(self):
        selected = {}
        for dim in self.selection.keys():
            if self.selection[dim] != None:
                selected['start_' + dim] = int(self.selection[dim][0].currentText())
                selected['end_' + dim] = int(self.selection[dim][1].currentText())
            else:
                selected['start_' + dim] = 0
                selected['end_' + dim] = 0
        return selected

    def connect(self, listener):
        for combobox in self.selected:
            combobox.activated.connect(lambda : listener.on_changed_selection(self.get_selected()))




class ControlBar():
    def __init__(self, dim):
        self.dim = dim
        self.layout = QGridLayout()
        self.bBack = QPushButton('back')
        self.bForward = QPushButton('forward')
        self.leValue = QLineEdit()

        self.leValue.setFixedWidth(50)

        self.layout.addWidget(self.bBack, 0,1)
        self.layout.addWidget(self.leValue, 0,2)
        self.layout.addWidget(self.bForward, 0,3)

    def connect(self, listener):
        self.bBack.clicked.connect(lambda : listener.on_move_back(self.dim))
        self.bForward.clicked.connect(lambda : listener.on_move_forward(self.dim))
        self.leValue.textChanged.connect(lambda : listener.on_text_changed(self.dim))

    @property
    def value(self):
        return self.leValue



def newStack(layouts):
        stack = QWidget()
        layout = QVBoxLayout()
        for childLayout in layouts:
            layout.addLayout(childLayout)
        stack.setLayout(layout)
        return stack

def stackLayout():
    stacklist = QListWidget ()        
    stack = QStackedWidget()
    hbox = QHBoxLayout()
    hbox.addWidget(stacklist)
    hbox.addWidget(stack)

    return stacklist, stack, hbox