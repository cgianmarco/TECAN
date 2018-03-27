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



        # lRow = QLabel('Riga')
        # lColumn = QLabel('Colonna')
        # lDepth = QLabel('Profondità')

        # # optionsDepth = [str(x) for x in range(len(data))]
        # optionsRow = [str(x) for x in range(width)]
        # optionsColumn = [str(x) for x in range(height)]

        # leFromRow = QComboBox()
        # leFromRow.addItems(optionsRow)
        
        # leToRow = QComboBox()
        # leToRow.addItems(optionsRow)

        # leFromColumn = QComboBox()
        # leFromColumn.addItems(optionsColumn)

        # leToColumn = QComboBox()
        # leToColumn.addItems(optionsColumn)
        # selected = [leFromRow, leToRow, leFromColumn, leToColumn]

        # leFromDepth = QComboBox()
        # leFromDepth.addItems(optionsDepth)

        # leToDepth = QComboBox()
        # leToDepth.addItems(optionsDepth)

        # Events
        # leFromRow.activated.connect(changed_selection_action)
        # leToRow.activated.connect(changed_selection_action)

        # leFromColumn.activated.connect(changed_selection_action)
        # leToColumn.activated.connect(changed_selection_action)

        selectionGrid.addWidget(lFrom, 1,0)
        selectionGrid.addWidget(lTo, 2,0)

        # selectionGrid.addWidget(lRow, 0,1)
        # selectionGrid.addWidget(lColumn, 0,2)
        # selectionGrid.addWidget(lDepth, 0,3)

        # selectionGrid.addWidget(leFromRow, 1,1)
        # selectionGrid.addWidget(leToRow, 2,1)

        # selectionGrid.addWidget(leFromColumn, 1,2)
        # selectionGrid.addWidget(leToColumn, 2,2)

        # # selectionGrid.addWidget(leFromDepth, 1,3)
        # selectionGrid.addWidget(leToDepth, 2,3)

        
        
        
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

    def connect(self, move_back_action, move_forward_action, text_changed_action):
        self.bBack.clicked.connect(lambda : move_back_action(self.dim))
        self.bForward.clicked.connect(lambda : move_forward_action(self.dim))
        self.leValue.textChanged.connect(lambda : text_changed_action(self.dim))

    @property
    def value(self):
        return self.leValue



def controlsBar(depth, move_back_action, move_forward_action, text_changed_action):
    if depth > 1:
        # Controls
        control_bar = ControlBar('depth')
        control_bar.connect(move_back_action, move_forward_action, text_changed_action)
        return control_bar.value, control_bar.layout
    else:
        return None, None

def newStack(layouts):
        # self.datagrid, grid_layout = widgets.Grid(self)
        # self.selected, selection_layout = widgets.selectionGrid(self)
        # self.control_value, control_layout = widgets.controlsBar(self)

        # layouts = [selection_layout, control_layout, grid_layout]


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

    # stacklist.currentRowChanged.connect(changed_stack_action)
    #stacklist.currentRowChanged.connect(prova)

    hbox = QHBoxLayout()
    hbox.addWidget(stacklist)
    hbox.addWidget(stack)

    return stacklist, stack, hbox