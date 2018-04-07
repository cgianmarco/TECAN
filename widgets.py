#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *


labels = { 'width' : 'Columns',
            'height' : 'Rows',
            'depth' : 'Wavelengths',
            'time': 'Time intervals'}

def listWidget():
        listWidget = QListWidget()
        listWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        listWidget.resize(300,120)

        return listWidget


class Grid:
    def __init__(self, width, height):
        self.datagrid = {}
        self.layout = QGridLayout()
        self.layout.setSpacing(0)

        for i in range(width):
            newButton = QLabel(str(i))
            newButton.setAlignment(Qt.AlignHCenter)
            newButton.setFixedWidth(60)
            self.layout.addWidget(newButton, 0, i+1)

        for j in range(height):
            newButton = QLabel(str(j))
            newButton.setFixedWidth(20)
            self.layout.addWidget(newButton, j+1, 0)

        for i in range(width):
            for j in range(height):
                newLineEdit = QLineEdit()
                newLineEdit.setFixedWidth(60)

                self.datagrid[(i, j)] = newLineEdit
                self.layout.addWidget(newLineEdit, j+1, i+1)

        stretch = QHBoxLayout()
        stretch.addStretch(1)
        self.layout.addLayout(stretch, 0, height + 2)


class SelectionGrid():
    # This should be __init__(self, shape, axis_values)
    def __init__(self, shape, axis_values):
        self.axis_values = axis_values

        # selector
        Hlayout = QGridLayout()
        lFrom = QLabel('From')
        lTo = QLabel('To')

        lFrom.setFixedWidth(40)
        lTo.setFixedWidth(40)

        selected = []
        lDims = []
        self.selection = {}
        for dim in shape.keys():
            if shape[dim] > 1:
                lDim = QLabel(labels[dim])
                lDims.append(lDim)
                # optionsDim = axis_values[dim]
                if dim != 'depth':
                    optionsDim = [str(x) for x in range(shape[dim])]
                else:
                    optionsDim = [str(x + 550) for x in range(shape[dim])]

                leFromDim = QComboBox()
                leFromDim.setFixedWidth(90)
                leFromDim.addItems(optionsDim)

                leToDim = QComboBox()
                leToDim.setFixedWidth(90)
                leToDim.addItems(optionsDim)

                selected.extend([leFromDim, leToDim])
                self.selection[dim] = (leFromDim, leToDim)
            else:
                self.selection[dim] = None


        for i in range(len(lDims)):
            Hlayout.addWidget(lDims[i], 0, i+1)

        for j in range((len(selected)/2)):
            Hlayout.addWidget(selected[2*j], 1, j+1)
            Hlayout.addWidget(selected[2*j+1], 2, j+1)

        Hlayout.addWidget(lFrom, 1,0)
        Hlayout.addWidget(lTo, 2,0)
        self.layout = QHBoxLayout()
        self.layout.addLayout(Hlayout)
        self.layout.addStretch(1)


    def get_selected(self):
        selected = {}
        for dim in self.selection.keys():
            if self.selection[dim] != None:
                selected['start_' + dim] = int(self.selection[dim][0].currentIndex())
                selected['end_' + dim] = int(self.selection[dim][1].currentIndex())
            else:
                selected['start_' + dim] = 0
                selected['end_' + dim] = 0
        return selected

    def connect(self, listener):
        for combobox in reduce(lambda x,y: x+y if y is not None else x, self.selection.values()):
            combobox.activated.connect(lambda : listener.on_changed_selection(self.get_selected()))




class ControlBar():
    def __init__(self, dim, axis_values):
        self.dim = dim
        self.axis_values = axis_values
        grid_layout = QGridLayout()

        self.bBack = QPushButton('<')
        self.bForward = QPushButton('>')
        self.leValue = QLineEdit()

        self.leValue.setFixedWidth(50)
        self.bBack.setFixedWidth(50)
        self.bForward.setFixedWidth(50)

        grid_layout.addWidget(QLabel(labels[dim]), 0,0, 1,0)
        grid_layout.addWidget(self.bBack, 1,0)
        grid_layout.addWidget(self.leValue, 1,1)
        grid_layout.addWidget(self.bForward, 1,2)        
        self.layout = grid_layout

    def connect(self, listener):
        self.bBack.clicked.connect(lambda : listener.on_move_back(self.dim))
        self.bForward.clicked.connect(lambda : listener.on_move_forward(self.dim))
        self.leValue.textChanged.connect(lambda text : listener.on_text_changed(text, self.dim, self.axis_values))

    @property
    def value(self):
        return self.leValue



class StackContainer():
    def __init__(self):
        self.list_widget = QListWidget ()        
        self.stacks_widget = QStackedWidget()
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.list_widget)
        self.layout.addWidget(self.stacks_widget)

    def add_stack(self, key, stack_widget):
        self.stacks_widget.addWidget(stack_widget)
        self.list_widget.addItem(key)