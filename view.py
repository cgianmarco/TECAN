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
    def __init__(self, shape, listener):
        self.time = shape['time']
        self.depth = shape['depth']
        self.width_value = shape['width']
        self.height_value = shape['height']

        self.datagrid, grid_layout = widgets.Grid(self.width_value, self.height_value)
        self.selected, selection_layout = widgets.selectionGrid(shape, self, listener)
        self.add_control_bars([('time', self.time), ('depth', self.depth)], listener)

        layouts = [selection_layout, self.control_layout['depth'], self.control_layout['time'], grid_layout]
        self.stack_widget = QWidget()
        layout = QVBoxLayout()
        for childLayout in layouts:
            if childLayout is not None:
                layout.addLayout(childLayout)
        layout.addStretch(1)
        self.stack_widget.setLayout(layout)

    def add_control_bars(self, dims, listener):
        self.control_value = {}
        self.control_layout = {}
        for dim in dims:
            name = dim[0]
            value = dim[1]
            if value > 1:
                control_bar = widgets.ControlBar(name)
                control_bar.connect(listener)
                self.control_value[name] = control_bar.value
                self.control_layout[name] = control_bar.layout
            else:
                self.control_value[name] = None
                self.control_layout[name] = None

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

    def update_control_value(self, dim, value):
        if self.control_value[dim] is not None:
            self.control_value[dim].setText(str(value))

    def get_control_value(self, dim):
        return int(self.control_value[dim].text())

    def clear_datagrid_color(self):
        for elem in self.datagrid.values():
            elem.setStyleSheet("color: rgb(76,76,76);")

    def is_in_range(self, dim, start, end):
        if self.control_value[dim] is not None:
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
                    self.datagrid[(i,j)].setStyleSheet("color: rgb(255, 0, 255);")


def DEFAULT_ACTION(*args, **kwargs):
    raise NotImplementedError("Action not yet implemented")


       


class View(QMainWindow):
    
    def __init__(self, listener, parent=None):
        super(View, self).__init__(parent)
        self.listener = listener
        # self.init_listeners()
        self.init_menu_bar()
        self.init_ui()

    # def init_listeners(self):
    #     self.tensor_load_action = DEFAULT_ACTION
    #     self.mean_action = DEFAULT_ACTION
    #     self.std_action = DEFAULT_ACTION

    #     # Listeners
    #     self.subtract_action = DEFAULT_ACTION
    #     self.move_back_action = DEFAULT_ACTION
    #     self.move_forward_action = DEFAULT_ACTION
    #     self.text_changed_action = DEFAULT_ACTION
    #     self.changed_selection_action = DEFAULT_ACTION
    #     self.changed_stack_action = DEFAULT_ACTION



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
        

        self.list_widget, self.values_widget, self.stack_layout = widgets.stackLayout()
        self.list_widget.currentRowChanged.connect(self.listener.on_changed_stack)    
        self.listValue = widgets.listWidget()



        # Add Child Layouts
        vlayout.addLayout(self.stack_layout)
    	vlayout.addWidget(self.listValue)


    	mainWidget = QWidget()
    	mainWidget.setLayout(vlayout)
    	self.setCentralWidget(mainWidget)        
        self.move(300, 150)
        self.setWindowTitle('TECAN Reader')
        self.show()

    def add_new_stack(self, shape):
        self.last_index += 1
        new_key = "Matrix" + str(self.last_index)
        self.stacks[new_key] = Stack(shape, self.listener)
        self.values_widget.addWidget(self.stacks[new_key].stack_widget)
        self.list_widget.addItem(new_key)
        self.current_stack = new_key

    def remove_stack(self, key):
        del self.stacks[key]
        self.values_widget.removeWidget(self.values_widget.widget(0))
        self.list_widget.takeItem(0)

    def set_stack_index(self, i):
        self.values_widget.setCurrentIndex(i)
        self.current_stack = "Matrix" + str(i)

    def update_values_list(self, values):
        self.listValue.clear()
        for value in values:
            self.listValue.addItem(value)

    @property
    def stack(self):
        return self.stacks[self.current_stack]

    # View should not have access to these
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
        self.changed_stack_action = action
        self.list_widget.currentRowChanged.connect(action)

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



