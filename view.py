#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import widgets

def default_action(*args, **kwargs):
    raise NotImplementedError("Action not yet implemented")

class Stack(object):
    def __init__(self, width, height, changed_selection_action=default_action, move_back_action=default_action, move_forward_action=default_action, text_changed_action=default_action):
        self.width_value = width
        self.height_value = height
        self.datagrid, grid_layout = widgets.Grid(width, height)
        self.selected, selection_layout = widgets.selectionGrid(width, height, changed_selection_action)
        self.control_value, control_layout = widgets.controlsBar(move_back_action, move_forward_action, text_changed_action)

        layouts = [selection_layout, control_layout, grid_layout]
        self.widget = QWidget()
        layout = QVBoxLayout()
        for childLayout in layouts:
            layout.addLayout(childLayout)
        layout.addStretch(1)
        self.widget.setLayout(layout)

    def update_grid(self, matrix):
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                value = matrix[i][j]
                self.datagrid[(i,j)].setText(str(value))

class StackList():
    def __init__(self):
        self.stacks = {}
        self.list_widget, self.values_widget, self.stack_container_layout = widgets.stackLayout()
        self.current_stack = ""
        self.last_index = 0
        self.initialized = False

    def add_stack(self, width, height, changed_selection_action=default_action, move_back_action=default_action, move_forward_action=default_action, text_changed_action=default_action):
        if self.initialized == True:
            self.last_index += 1
        else:
            self.initialized = True
            # self.values_widget.removeWidget(self.stacked_widget.widget(0))
        new_key = "Matrix" + str(self.last_index)
        self.stacks[new_key] = Stack(width, height, changed_selection_action, move_back_action, move_forward_action, text_changed_action)
        self.list_widget.addItem(new_key)
        self.values_widget.addWidget(self.stacks[new_key].widget)
        self.last_index = self.get_next_last_index()
        if self.current_stack == "":
                self.current_stack = self.stacks.keys()[0]

    def remove_stack(self, key):
        index = int(key.replace("Matrix", ""))
        del self.stacks[key]
        self.values_widget.removeWidget(self.values_widget.widget(index))
        self.list_widget.takeItem(index)

    def get_next_last_index(self):
        indeces = [ int(key.replace("Matrix", "")) for key in self.stacks.keys() ]
        free_indeces = [ i for i in range(max(indeces)) if i not in indeces ]
        if len(free_indeces) > 0:
            return free_indeces[0]
        else:
            return max(indeces) + 1





class View(QMainWindow):
    
    def __init__(self, parent=None):
        super(View, self).__init__(parent)
        self.init_listeners()
        self.init_menu_bar()
        self.init_ui()

    def init_listeners(self):
        self.tensor_load_action = lambda x : None
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

        
        self.stack_list = StackList()
        self.listValue, listWidget = widgets.listWidget()

        # Add Child Layouts
        vlayout.addLayout(self.stack_list.stack_container_layout)
    	vlayout.addWidget(listWidget)


    	mainWidget = QWidget()
    	mainWidget.setLayout(vlayout)
    	self.setCentralWidget(mainWidget)        
        self.move(300, 150)
        self.setWindowTitle('TECAN Reader')
        self.show()

    def add_new_stack(self, width, height, changed_selection_action=default_action, move_back_action=default_action, move_forward_action=default_action, text_changed_action=default_action):
        self.stack_list.add_stack(width, height, changed_selection_action, move_back_action, move_forward_action, text_changed_action)

    def remove_stack(self, key):
        self.stack_list.remove_stack(key)

    @property
    def stacked_widget(self):
        return self.stack_list.values_widget

    @property
    def stackList(self):
        return self.stack_list.list_widget

    @property
    def stack(self):
        return self.stack_list.stacks[self.stack_list.current_stack]

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

    def add_tensor_load_action(self, action):
        self.tensor_load_action = action

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
        self.stack_list.list_widget.currentRowChanged.connect(action)

    def process_trigger(self, q):
        if q.text() == 'Load Matrix':
            self.tensor_load_action()
        elif q.text() == 'Mean':
            self.mean_action()
        elif q.text() == 'Value from Selected':
            self.subtract_action()
        elif q.text() == 'Standard deviation':
            self.std_action()

    def update_grid(self, matrix):
        self.stack.update_grid(matrix)

    def get_selected(self):
        return [ int(elem.currentText()) for elem in self.selected ]

    def update_control_value(self, value):
        self.control_value.setText(str(value))

    def get_list_selected(self):
        return float(str(self.listValue.currentItem().text()).split(" ")[1])



