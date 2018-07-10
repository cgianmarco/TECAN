#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from navbar import Ui_NavBar


labels = { 'width' : 'Columns',
            'height' : 'Rows',
            'depth' : 'Wavelengths',
            'time': 'Time intervals'}

def listWidget():
        listWidget = QListWidget()
        listWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        listWidget.resize(300,120)

        return listWidget


class Grid(QWidget):
    def __init__(self, width, height, parent=None):
        super(QWidget, self).__init__(parent)
        self.datagrid = {}
        layout = QGridLayout()
        layout.setSpacing(0)

        for i in range(width):
            newButton = QLabel(str(i))
            newButton.setAlignment(Qt.AlignHCenter)
            newButton.setFixedWidth(60)
            newButton.setStyleSheet("font-weight:bold; margin-top:20px; margin-bottom:5px;")
            layout.addWidget(newButton, 0, i+1)

        for j in range(height):
            newButton = QLabel(str(j))
            newButton.setFixedWidth(20)
            newButton.setStyleSheet("font-weight:bold;")
            layout.addWidget(newButton, j+1, 0)

        for i in range(width):
            for j in range(height):
                newLineEdit = QLineEdit()
                newLineEdit.setFixedWidth(60)
                newLineEdit.setFixedHeight(35)
                newLineEdit.setStyleSheet("border-style:solid; border-color:#aaa; border-width: 1px;")

                self.datagrid[(i, j)] = newLineEdit
                layout.addWidget(newLineEdit, j+1, i+1)

        stretch = QHBoxLayout()
        stretch.addStretch(1)
        layout.addLayout(stretch, 0, height + 2)
        self.setLayout(layout)

    def update(self, matrix):
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                value = matrix[i][j]
                self.datagrid[(i,j)].setText(str(value))

    def clear_color(self):
        for elem in self.datagrid.values():
            stylesheet = elem.styleSheet() + "color:#000;"
            elem.setStyleSheet(stylesheet)

    def update_color(self, start_row, end_row, start_col, end_col):
        for i in range(start_row, end_row+1):
                for j in range(start_col, end_col+1):
                    stylesheet = self.datagrid[(i,j)].styleSheet() + "color: rgb(255, 0, 255);"
                    self.datagrid[(i,j)].setStyleSheet(stylesheet)

    def update_background_color(self, start_row, end_row, start_col, end_col):
        color = QColorDialog.getColor()
        for i in range(start_row, end_row+1):
                for j in range(start_col, end_col+1):
                    stylesheet = self.datagrid[(i,j)].styleSheet() + "background-color:" + color.name() + ";"
                    self.datagrid[(i,j)].setStyleSheet(stylesheet)


class SelectionGrid(QWidget):
    # This should be __init__(self, shape, axis_values)
    def __init__(self, shape, axis_values, parent=None):
        super(QWidget, self).__init__(parent)
        self.axis_values = axis_values

        # selector
        Hlayout = QGridLayout()
        lFrom = QLabel('From')
        lTo = QLabel('To')

        lFrom.setFixedWidth(40)
        lTo.setFixedWidth(40)

        lFrom.setStyleSheet("font-weight:bold;")
        lTo.setStyleSheet("font-weight:bold;")

        selected = []
        lDims = []
        self.selection = {}
        for dim in shape.keys():
            if shape[dim] > 1:
                lDim = QLabel(labels[dim])
                lDim.setStyleSheet("font-weight:bold;")
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
        layout = QHBoxLayout()
        layout.addLayout(Hlayout)
        layout.addStretch(1)
        self.setLayout(layout)


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
        print(self.selection)
        comboboxes = ()
        for pair in self.selection.values():
            if pair is not None:
                comboboxes += pair
        for combobox in comboboxes:
            combobox.activated.connect(lambda : listener.on_changed_selection(self.get_selected()))




class ControlBar(QWidget):
    def __init__(self, dim, axis_values, parent=None):
        super(QWidget, self).__init__(parent)

        self.dim = dim
        self.axis_values = axis_values
        layout = QGridLayout()

        self.bBack = QPushButton('<')
        self.bForward = QPushButton('>')
        self.leValue = QLineEdit()

        self.leValue.setFixedWidth(60)
        self.bBack.setFixedWidth(31)
        self.bForward.setFixedWidth(31)

        self.bBack.setFixedHeight(31)
        self.bForward.setFixedHeight(31)


        self.lDim = QLabel(labels[dim])
        self.lDim.setStyleSheet("font-weight:bold; margin-top:20px;")


        layout.addWidget(self.lDim, 0,0, 1,0)
        layout.addWidget(self.bBack, 1,0)
        layout.addWidget(self.leValue, 1,1)
        layout.addWidget(self.bForward, 1,2)        
        self.setLayout(layout)

    def connect(self, listener):
        self.bBack.clicked.connect(lambda : listener.on_move_back(self.dim))
        self.bForward.clicked.connect(lambda : listener.on_move_forward(self.dim))
        self.leValue.textChanged.connect(lambda text : listener.on_text_changed(text, self.dim, self.axis_values))

    @property
    def value(self):
        return self.leValue






class StackContainer(QWidget):
    def __init__(self, parent = None):
        super(QWidget, self).__init__(parent)
        self.list_widget = QListWidget()    
        self.list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list_widget.connect(self.list_widget,SIGNAL("customContextMenuRequested(QPoint)" ), self.open_right_click_menu)    
        self.stacks_widget = QStackedWidget()
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.list_widget)
        self.layout.addWidget(self.stacks_widget)
        self.setLayout(self.layout)

    def add_stack(self, key, stack_widget):
        self.stacks_widget.addWidget(stack_widget)
        self.list_widget.addItem(key)

    def open_right_click_menu(self, QPos): 
        self.listMenu = QMenu()

        # Menu items
        quit_item = self.listMenu.addAction("Remove Item")
        self.connect(quit_item, SIGNAL("triggered()"), self.quit_item_clicked) 

        parentPosition = self.list_widget.mapToGlobal(QPoint(0, 0))        
        self.listMenu.move(parentPosition + QPos)
        self.listMenu.show() 

    def quit_item_clicked(self):
        currentItemName = str(self.list_widget.currentItem().text() )
        print(currentItemName)