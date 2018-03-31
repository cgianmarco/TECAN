#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import widgets

# TODO
# def generate_layouts(self.shape, self.actions)
# width_value to width

class Stack():
    # This should be __init__(self, shape, axis_values, listener)
    def __init__(self, shape, listener):
        self.time = shape['time']
        self.depth = shape['depth']
        self.width_value = shape['width']
        self.height_value = shape['height']

        self.grid = widgets.Grid(self.width_value, self.height_value)

        self.selection_grid = widgets.SelectionGrid(shape)
        # self.selection_grid = widgets.SelectionGrid(shape, axis_values)
        self.selection_grid.connect(listener)

        self.control_bar = {}

        if self.depth > 1:
            self.control_bar['depth'] = widgets.ControlBar('depth')
            self.control_bar['depth'].connect(listener)

        if self.time > 1:
            self.control_bar['time'] = widgets.ControlBar('time')
            self.control_bar['time'].connect(listener)

        self.widget = QWidget()
        self.layout = QVBoxLayout()

        for child_layout in self.child_layouts:
            self.layout.addLayout(child_layout)

        self.layout.addStretch(1)
        self.widget.setLayout(self.layout)

    @property
    def child_layouts(self):
        yield self.selection_grid.layout
        if 'depth' in self.control_bar:
            yield self.control_bar['depth'].layout
        if 'time' in self.control_bar:
            yield self.control_bar['time'].layout
        yield self.grid.layout

    def update_grid(self, matrix):
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                value = matrix[i][j]
                self.grid.datagrid[(i,j)].setText(str(value))

    def get_selected(self):
        return self.selection_grid.get_selected()

    def update_control_value(self, dim, value):
        if dim in self.control_bar:
            self.control_bar[dim].value.setText(str(value))

    def get_control_value(self, dim):
        return int(self.control_bar[dim].value.text())

    def clear_datagrid_color(self):
        for elem in self.grid.datagrid.values():
            elem.setStyleSheet("color: rgb(76,76,76);")

    def is_in_range(self, dim, start, end):
        if dim in self.control_bar:
            current = self.get_control_value(dim)
            return start <= current and current <= end
        else: 
            return True

    def update_datagrid_color(self, selected):
        start_row = selected['start_width']
        end_row = selected['end_width']
        start_column = selected['start_height']
        end_column = selected['end_height']
        start_depth = selected['start_depth']
        end_depth = selected['end_depth']
        start_time = selected['start_time']
        end_time = selected['end_time']

        if start_row <= end_row and start_column <= end_column and self.is_in_range('depth', start_depth, end_depth) and self.is_in_range('time', start_time, end_time):
            for i in range(start_row, end_row+1):
                for j in range(start_column, end_column+1):
                    self.grid.datagrid[(i,j)].setStyleSheet("color: rgb(255, 0, 255);")


def DEFAULT_ACTION(*args, **kwargs):
    raise NotImplementedError("Action not yet implemented")


       


class View(QMainWindow):
    
    def __init__(self, listener, parent=None):
        super(View, self).__init__(parent)
        self.listener = listener
        # self.init_listeners()
        self.init_menu_bar()
        self.init_ui()


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

        self.stacks = {}
        self.current_stack = ""
        self.last_index = -1
        

        self.stack_container = widgets.StackContainer()
        self.stack_container.list_widget.currentRowChanged.connect(self.listener.on_changed_stack)    
        self.listValue = widgets.listWidget()



        # Add Child Layouts
        vlayout.addLayout(self.stack_container.layout)
    	vlayout.addWidget(self.listValue)


    	mainWidget = QWidget()
    	mainWidget.setLayout(vlayout)
    	self.setCentralWidget(mainWidget)        
        self.move(300, 150)
        self.setWindowTitle('TECAN Reader')
        self.show()

    # This should be add_new_stack(self, shape, axis_values)
    def add_new_stack(self, shape):
        self.last_index += 1
        new_key = "Matrix" + str(self.last_index)
        self.stacks[new_key] = Stack(shape, self.listener)
        # self.stacks[new_key] = Stack(shape, axis_values, self.listener)
        self.stack_container.add_stack(new_key, self.stacks[new_key].widget)
        self.current_stack = new_key

    def remove_stack(self, key):
        del self.stacks[key]
        self.stack_container.stacks_widget.removeWidget(self.values_widget.widget(0))
        self.stack_container.list_widget.takeItem(0)

    def set_stack_index(self, i):
        self.stack_container.stacks_widget.setCurrentIndex(i)
        self.current_stack = "Matrix" + str(i)

    def update_values_list(self, values):
        self.listValue.clear()
        for value in values:
            self.listValue.addItem(value)

    @property
    def stack(self):
        return self.stacks[self.current_stack]

    def get_file_name(self):
        return QFileDialog.getOpenFileName(self, 'Open file', "Excel files (*.xlsx)")

    def process_trigger(self, q):
        if q.text() == 'Load Matrix':
            self.listener.on_tensor_load(self.get_file_name())
        elif q.text() == 'Mean':
            self.listener.on_mean_action(self.get_selected())
        elif q.text() == 'Value from Selected':
            self.listener.on_subtract_action(self.get_selected(), self.get_list_selected())
        elif q.text() == 'Standard deviation':
            self.listener.on_std_action(self.get_selected())

    def update_grid(self, matrix):
        self.stack.update_grid(matrix)
    
    def get_selected(self):
        return self.stack.get_selected()
    
    def update_control_value(self, dim, value):
        self.stack.update_control_value(dim, value)
    
    def get_list_selected(self):
        return float(str(self.listValue.currentItem().text()).split(" ")[1])

    def get_control_value(self, dim):
        return self.stack.get_control_value(dim)

    def clear_datagrid_color(self):
        self.stack.clear_datagrid_color()

    def update_datagrid_color(self, selected):
        self.stack.update_datagrid_color(selected)



