#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import widgets

class Stack():
    def __init__(self, width, height, changed_selection_action, move_back_action, move_forward_action, text_changed_action):
        self.width_value = width
        self.height_value = height
        self.datagrid, grid_layout = widgets.Grid(width, height)
        self.selected, selection_layout = widgets.selectionGrid(width, height, changed_selection_action)
        self.control_value, control_layout = widgets.controlsBar(move_back_action, move_forward_action, text_changed_action)

        layouts = [selection_layout, control_layout, grid_layout]
        self.stack_widget = QWidget()
        layout = QVBoxLayout()
        for childLayout in layouts:
            layout.addLayout(childLayout)
        layout.addStretch(1)
        self.stack_widget.setLayout(layout)



class View(QMainWindow):
    
    def __init__(self, parent=None):
        super(View, self).__init__(parent)
        self.init_listeners()
        self.init_menu_bar()
        self.init_ui()

    def init_listeners(self):
        self.matrix_load_action = lambda x : None
        self.mean_action = lambda x : None
        self.std_action = lambda x : None
        self.subtract_action = lambda x : None
        self.move_back_action = lambda x : None
        self.move_forward_action = lambda x : None
        self.text_changed_action = lambda x : None
        self.changed_selection_action = lambda x : None
        self.changed_stack_action = lambda x : None



    def init_menu_bar(self):
    	# menubar
        bar = self.menuBar()
        file = bar.addMenu("File")
        file.triggered[QAction].connect(self.process_trigger)

        # actions
        file.addAction("Load Matrix")
        file.addAction("Mean")
        file.addAction("Standard deviation")
    
        subtract = file.addMenu("Subtract")
        subtract.addAction("Value from Selected")

      
    def init_ui(self):
        # main layout
        vlayout = QVBoxLayout()

        self.stacks = {"Matrix0" : Stack(6, 6, self.changed_selection_action, self.move_back_action, self.move_forward_action, self.text_changed_action)}
        self.current_stack = "Matrix0"
        self.last_index = 0
        self.stackList, self.stacked_widget, stackLayout = widgets.stackLayout()
        self.listValue, listWidget = widgets.listWidget()
        self.initialized = False

        # Add Child Layouts
        self.stacked_widget.addWidget(self.stack.stack_widget)
        vlayout.addLayout(stackLayout)
    	vlayout.addWidget(listWidget)


    	mainWidget = QWidget()
    	mainWidget.setLayout(vlayout)
    	self.setCentralWidget(mainWidget)        
        self.move(300, 150)
        self.setWindowTitle('TECAN Reader')
        self.show()

    def add_new_stack(self, width, height):
        if self.initialized == True:
            self.last_index += 1
        else:
            self.initialized = True
            self.stacked_widget.removeWidget(self.stacked_widget.widget(0))
        new_key = "Matrix" + str(self.last_index)
        self.stacks[new_key] = Stack(width, height, self.changed_selection_action, self.move_back_action, self.move_forward_action, self.text_changed_action)
        self.stacked_widget.addWidget(self.stacks[new_key].stack_widget)
        self.stackList.addItem(new_key)
        self.current_stack = new_key

    def remove_stack(self, key):
        del self.stacks[key]
        self.stacked_widget.removeWidget(self.stacked_widget.widget(0))
        self.stackList.takeItem(0)

    @property
    def stack(self):
        return self.stacks[self.current_stack]

    @property
    def datagrid(self):
        return self.stack.datagrid

    @property
    def control_value(self):
        return self.stack.control_value

    @property
    def selected(self):
        return self.stack.selected

    @property
    def width_value(self):
        return self.stack.width_value

    @property
    def height_value(self):
        return self.stack.height_value

    @width_value.setter
    def width_value(self, value):
        self.stack.width_value = value

    @height_value.setter
    def height_value(self, value):
        self.stack.height_value = value


    def set_dimensions(self, width, height):
        self.width_value = width
        self.height_value = height

    def get_file_name(self):
        return QFileDialog.getOpenFileName(self, 'Open file', "Excel files (*.xlsx)")

    def add_matrix_load_action(self, action):
        self.matrix_load_action = action

    def add_mean_action(self, action):
        self.mean_action = action

    def add_std_action(self, action):
        self.std_action = action

    def add_subtract_action(self, action):
        self.subtract_action = action

    def add_move_back_action(self, action):
        self.move_back_action = action

    def add_move_forward_action(self, action):
        self.move_forward_action = action

    def add_text_changed_action(self, action):
        self.text_changed_action = action

    def add_changed_selection_action(self, action):
        self.changed_selection_action = action

    def add_changed_stack_action(self, action):
        self.stackList.currentRowChanged.connect(action)

    def process_trigger(self, q):
        if q.text() == 'Load Matrix':
            self.matrix_load_action()
        elif q.text() == 'Mean':
            self.mean_action()
        elif q.text() == 'Value from Selected':
            self.subtract_action()
        elif q.text() == 'Standard deviation':
            self.std_action()

    def update_grid(self, matrix):
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                value = matrix[i][j]
                self.datagrid[(i,j)].setText(str(value))

    def get_selected(self):
        return [ int(elem.currentText()) for elem in self.selected ]

    def update_control_value(self, value):
        self.control_value.setText(str(value))

    def get_list_selected(self):
        return float(str(self.listValue.currentItem().text()).split(" ")[1])



