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
    def __init__(self, shape, changed_selection_action, move_back_action, move_forward_action, text_changed_action):
        self.time = shape['time']
        self.depth = shape['depth']
        self.width_value = shape['width']
        self.height_value = shape['height']

        self.datagrid, grid_layout = widgets.Grid(self.width_value, self.height_value)
        self.selected, selection_layout = widgets.selectionGrid(shape, changed_selection_action)
        self.control_value, control_layout = widgets.controlsBar(self.depth, move_back_action, move_forward_action, text_changed_action)

        layouts = [selection_layout, control_layout, grid_layout]
        self.stack_widget = QWidget()
        layout = QVBoxLayout()
        for childLayout in layouts:
            if childLayout is not None:
                layout.addLayout(childLayout)
        layout.addStretch(1)
        self.stack_widget.setLayout(layout)

    def get_control_value(self):
        return int(self.control_value.text())

    def clear_datagrid_color(self):
        for elem in self.datagrid.values():
            elem.setStyleSheet("color: rgb(76,76,76);")

    def is_in_range(self, control_value, start, end):
        if control_value is not None:
            current = int(control_value.text())
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
        if start_row <= end_row and start_column <= end_column and self.is_in_range(self.control_value, start_depth, end_depth):
            for i in range(start_row, end_row+1):
                for j in range(start_column, end_column+1):
                    self.datagrid[(i,j)].setStyleSheet("color: rgb(255, 0, 255);")


def DEFAULT_ACTION(*args, **kwargs):
    raise NotImplementedError("Action not yet implemented")


class StackList():
    def __init__(self):
        self.stacks = {}
        self.current_stack = ""
        self.last_index = -1

        # Listeners
        self.subtract_action = DEFAULT_ACTION
        self.move_back_action = DEFAULT_ACTION
        self.move_forward_action = DEFAULT_ACTION
        self.text_changed_action = DEFAULT_ACTION
        self.changed_selection_action = DEFAULT_ACTION
        self.changed_stack_action = DEFAULT_ACTION

        self.list_widget, self.values_widget, self.stack_layout = widgets.stackLayout()

    def add_new_stack(self, shape):
        self.last_index += 1
        new_key = "Matrix" + str(self.last_index)
        self.stacks[new_key] = Stack(shape, self.changed_selection_action, self.move_back_action, self.move_forward_action, self.text_changed_action)
        self.values_widget.addWidget(self.stacks[new_key].stack_widget)
        self.list_widget.addItem(new_key)
        self.current_stack = new_key

    def remove_stack(self, key):
        del self.stacks[key]
        self.values_widget.removeWidget(self.values_widget.widget(0))
        self.list_widget.takeItem(0)

    def set_index(self, i):
        self.values_widget.setCurrentIndex(i)
        self.current_stack = "Matrix" + str(i)
       


class View(QMainWindow):
    
    def __init__(self, parent=None):
        super(View, self).__init__(parent)
        self.init_listeners()
        self.init_menu_bar()
        self.init_ui()

    def init_listeners(self):
        self.tensor_load_action = DEFAULT_ACTION
        self.mean_action = DEFAULT_ACTION
        self.std_action = DEFAULT_ACTION



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
        self.listValue = widgets.listWidget()

        # Add Child Layouts
        vlayout.addLayout(self.stack_list.stack_layout)
    	vlayout.addWidget(self.listValue)


    	mainWidget = QWidget()
    	mainWidget.setLayout(vlayout)
    	self.setCentralWidget(mainWidget)        
        self.move(300, 150)
        self.setWindowTitle('TECAN Reader')
        self.show()

    def add_new_stack(self, shape):
        self.stack_list.add_new_stack(shape)

    def remove_stack(self, key):
        self.stack_list.remove_stack(key)

    def set_stack_index(self, i):
        self.stack_list.set_index(i)

    def update_values_list(self, values):
        self.listValue.clear()
        for value in values:
            self.listValue.addItem(value)

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
        self.stack_list.move_back_action = action

    def add_move_forward_action(self, action):
        self.stack_list.move_forward_action = action

    def add_text_changed_action(self, action):
        self.stack_list.text_changed_action = action

    def add_changed_selection_action(self, action):
        self.stack_list.changed_selection_action = action

    def add_changed_stack_action(self, action):
        self.stack_list.changed_stack_action = action
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
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                value = matrix[i][j]
                self.datagrid[(i,j)].setText(str(value))

    def get_selected(self):
        selected = {}
        for dim in self.selected.keys():
            if self.selected[dim] != None:
                selected['start_' + dim] = int(self.selected[dim][0].currentText())
                selected['end_' + dim] = int(self.selected[dim][1].currentText())
            else:
                selected['start_' + dim] = 0
                selected['end_' + dim] = 0
        return selected

    def update_control_value(self, value):
        if self.control_value is not None:
            self.control_value.setText(str(value))

    def get_list_selected(self):
        return float(str(self.listValue.currentItem().text()).split(" ")[1])

    def get_control_value(self):
        return self.stack.get_control_value()

    def clear_datagrid_color(self):
        self.stack.clear_datagrid_color()

    def update_datagrid_color(self, selected):
        self.stack.update_datagrid_color(selected)



