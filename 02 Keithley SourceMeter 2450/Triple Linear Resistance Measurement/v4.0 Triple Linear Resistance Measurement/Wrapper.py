"""Written by Bruce Wang.
    Inspired and helped by Johnathon Vannucci.
    Contact wdmzcjwq@gmail.com if you have any questions"""

"""To compile the .ui file into .py file, it is very simple. Do the following stpes:
   1. Open Command Proment (Terminal if you are using mac), using 'cd' to get the directory that contains the .ui file
   2. Type "pyuic4 -x filename.ui -o filename.py"
   3. If nothing strange happens, it means a .py file is successfully created in the same directory contains your original .ui file
   4. Do not change any of the code in the .py file because recomling any new changes in the .ui file will delete your changes"""

# Import os library
import os, inspect

print inspect.getfile(inspect.currentframe()) # script filename (usually with path)
dir_ = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) # script directory
os.chdir(dir_)

import string

# Import system library
import sys

# Import datetime
from datetime import datetime
now = datetime.now()

# Import the visa library
try:
    import visa
    visa_available = True
except:
    visa_available = False

# Import numpy library
import numpy

# Import pylab library 
# It contains some functions necessary to create some of the functions in the used in the plots
from pylab import *

# It makes the text format looks pretty and well-designed
from textwrap import wrap

# Adding navigation toolbar to the figure
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure

# Import the PyQt4 modules for all the commands that control the GUI.
# Importing as from "Module" import * implies that everything from that module is not part of this module.
# You do not need to put the module name before its commands
from PyQt4.QtCore import *
from PyQt4.QtGui import *

# This is very important because it imports the GUI created earlier using Qt Designer
# To import the GUI from another python file, it is very simple. Just following the following steps:
# 1. Create an empyty file called __init__.py in the same directory as the GUI file
# 2. If the GUI file and __init__.py file are in the same directory as this file, just type "from .GUIfilename import classname"
# 3. If the GUI file and __init__.py file are in the sub file of this file, then type "from subfilename.GUIfilename import classname"
# classname is the name of the class in the GUI file, usually it should be 'Ui_MainWindow'
from Sub_Scripts.GUI import Ui_MainWindow

import Sub_Scripts.Sweep as Sweep

# To get the screen dimensions (in pixels) using the standard Python library.
from win32api import GetSystemMetrics
screen_res = [GetSystemMetrics (0), GetSystemMetrics (1)]

import subprocess

continue_check = True
# The class that controls all the operations of the GUI. This is the main class that contains all the functions that control the GUI.
class MyForm(QMainWindow):
    
    # The __init__ function is what is everything the user wants to be initialized when the class is called.
    # Here we shall define the trig functions to corresponding variables.
    # Note that the "self" variable means that the function is part of the class and can be called inside and outside the class.(Although __init__ is special.)
    def __init__(self, parent = None):

        self.collect_data_thread = Collect_data()

        # Standard GUI code
        QWidget.__init__(self, parent)

        # All the GUI data and widgets in the Ui_MainWindow() class is defined to self.ui
        # Thus to do anything on the GUI, the commands must go through this variable
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # When you open the wrapper, the visa gets refreshed
        self.refresh_visa()

        # The canvas replaces the mplwidget to show the plot
        # The tool bar is sticked on canvas and help to edit the plot
        
        # Set up the table 
        self.initalizeTable()
        
        # This is for the allplot canvas.
        self.canvas_allplot = FigureCanvas(self.ui.mplwidget_allplot.figure)
        self.canvas_allplot.setParent(self.ui.widget_allplot)
        # Here is the toolbar widget for the all_plot canvas
        self.mpl_toolbar_allplot = NavigationToolbar(self.canvas_allplot, self.ui.widget_allplot)

        # This is for the time canvas, which is the theoretical Current(Voltage) vs. Time
        self.canvas_time = FigureCanvas(self.ui.mplwidget_time.figure)
        self.canvas_time.setParent(self.ui.widget_time)
        # Here is the toolbar widget for the time canvas
        self.mpl_toolbar_time = NavigationToolbar(self.canvas_time, self.ui.widget_time)
        
        # This is for the left canvas, which is the real Current(Voltage) vs. Time
        self.canvas_real_time = FigureCanvas(self.ui.mplwidget_real_time.figure)
        self.canvas_real_time.setParent(self.ui.widget_real_time)
        # Here is the toolbar widget for the left canvas
        self.mpl_toolbar_real_time = NavigationToolbar(self.canvas_real_time, self.ui.widget_real_time)

        # This is for the first canvas
        # The independent variable of this plot is ascending
        self.canvas_first = FigureCanvas(self.ui.mplwidget_first.figure)
        self.canvas_first.setParent(self.ui.widget_first)
        # Here is the toolbar widget for the middle canvas
        self.mpl_toolbar_first = NavigationToolbar(self.canvas_first, self.ui.widget_first)

        # This is for the second canvas
        # The independent variable of this plot is descending
        self.canvas_second = FigureCanvas(self.ui.mplwidget_second.figure)
        self.canvas_second.setParent(self.ui.widget_second)
        # Here is the toolbar widget for the right canvas
        self.mpl_toolbar_second = NavigationToolbar(self.canvas_second, self.ui.widget_second)
        
        # This is for the third canvas
        # The independent variable of this plot is descending
        self.canvas_third = FigureCanvas(self.ui.mplwidget_third.figure)
        self.canvas_third.setParent(self.ui.widget_third)
        # Here is the toolbar widget for the right canvas
        self.mpl_toolbar_third = NavigationToolbar(self.canvas_third, self.ui.widget_third)


        # Create the QVBoxLayout object and add the widgets into the layout
        # This is for the all_plot canvas
        vbox_allplot = QVBoxLayout()
        # The matplotlib canvas
        vbox_allplot.addWidget(self.canvas_allplot)
        # The matplotlib toolbar
        vbox_allplot.addWidget(self.mpl_toolbar_allplot)
        self.ui.widget_allplot.setLayout(vbox_allplot)
        
        # This is for the time canvas
        vbox_time = QVBoxLayout()
        # The matplotlib canvas
        vbox_time.addWidget(self.canvas_time)
        # The matplotlib toolbar
        vbox_time.addWidget(self.mpl_toolbar_time)
        self.ui.widget_time.setLayout(vbox_time)
        
        # This is for the left canvas
        vbox_real_time = QVBoxLayout()
        # The matplotlib canvas
        vbox_real_time.addWidget(self.canvas_real_time)
        # The matplotlib toolbar
        vbox_real_time.addWidget(self.mpl_toolbar_real_time)
        self.ui.widget_real_time.setLayout(vbox_real_time)

        # This is for the first canvas
        vbox_first = QVBoxLayout()
        # The matplotlib canvas
        vbox_first.addWidget(self.canvas_first)
        # The matplotlib toolbar
        vbox_first.addWidget(self.mpl_toolbar_first)
        self.ui.widget_first.setLayout(vbox_first)

        # This is for the second canvas
        vbox_second = QVBoxLayout()
        # The matplotlib canvas
        vbox_second.addWidget(self.canvas_second)
        # The matplotlib toolbar
        vbox_second.addWidget(self.mpl_toolbar_second)
        self.ui.widget_second.setLayout(vbox_second)
        
        # This is for the third canvas
        vbox_third = QVBoxLayout()
        # The matplotlib canvas
        vbox_third.addWidget(self.canvas_third)
        # The matplotlib toolbar
        vbox_third.addWidget(self.mpl_toolbar_third)
        self.ui.widget_third.setLayout(vbox_third)

        # Connect the mplwidget with canvas
        self.ui.mplwidget_allplot = self.canvas_allplot
        self.ui.mplwidget_time = self.canvas_time
        self.ui.mplwidget_real_time = self.canvas_real_time
        self.ui.mplwidget_first = self.canvas_first
        self.ui.mplwidget_second = self.canvas_second
        self.ui.mplwidget_third = self.canvas_third

        # Set the voltage groupBox to be enabled when the wrapper is opened
        self.ui.groupBox_sweep_voltage.setEnabled(True)
        # At the same time the current groupBox is not enabled
        self.ui.groupBox_sweep_current.setEnabled(False)

        # To following connects the signals sent from an action on the GUI to a function that does something
        # When a button is pressed the corresponding action is run
        # The structure actually is QtCore.QObject.connect (sender_widget, signal_received, action/method)
        # (One does not need the QtCore.QObject necause of how PyQt4 was imported. Here is to show how the actual hierarchy of the command "connect")
        # The action/method must be in the format shown below.
        # For additional signals for widgets refer to the PyQi4 website or the Qt designer website.
        self.connect(self.ui.pushButton_refresh, SIGNAL("clicked()"), self.refresh_visa)
        self.connect(self.ui.pushButton_select, SIGNAL("clicked()"), self.select_visa)
        self.connect(self.ui.pushButton_close, SIGNAL("clicked()"), self.close_visa)
        self.connect(self.ui.pushButton_run, SIGNAL("clicked()"), self.judge_measurement)
        self.connect(self.ui.pushButton_preview, SIGNAL("clicked()"), self.preview)
        #self.connect(self.ui.checkBox_halfbreak, SIGNAL("clicked()"), self.continue_check)
        self.connect(self.ui.pushButton_Stop, SIGNAL("clicked()"), self.Stop)
        self.connect(self.ui.pushButton_Continue, SIGNAL("clicked()"), self.Continue)
        self.connect(self.ui.pushButton_Continue, SIGNAL("clicked()"), self.Continue)
        self.connect(self.ui.pushButton_Select_Directory, SIGNAL('clicked()'), self.select_check)
        self.connect(self.ui.pushButton_Save, SIGNAL('clicked()'), self.save)
        self.connect(self.ui.pushButton_reset, SIGNAL('clicked()'), self.reset)
        self.connect(self.ui.pushButton_browse, SIGNAL('clicked()'), self.Browse)
        self.connect(self.ui.pushButton_check, SIGNAL('clicked()'), self.Check)
        self.connect(self.ui.pushButton_Open, SIGNAL('clicked()'), self.Open)
        
        self.connect(self.ui.radioButton_sweep_voltage, SIGNAL("clicked()"), lambda : self.ui.tabWidget.setCurrentIndex(0))
        self.connect(self.ui.radioButton_sweep_current, SIGNAL("clicked()"), lambda : self.ui.tabWidget.setCurrentIndex(1))
        self.connect(self.ui.radioButton_Custom_Name, SIGNAL('clicked()'), self.enable_custom_name)
        self.connect(self.ui.radioButton_Timename, SIGNAL('clicked()'), self.disable_custom_name)
        self.connect(self.ui.radioButton_sweep_voltage, SIGNAL("clicked()"), self.voltageSweep)
        self.connect(self.ui.radioButton_sweep_current, SIGNAL("clicked()"), self.currentSweep)
        self.connect(self.ui.radioButton_software, SIGNAL('clicked()'), self.software_stepping)

        self.connect(self.collect_data_thread, SIGNAL('plot'), self.plot_dynamic_data)
        self.connect(self.collect_data_thread, SIGNAL('Data'), self.set_data)
        self.connect(self.collect_data_thread, SIGNAL('final_plot'), self.Final_plot)
    
        try:
            print dir_ + '\\' + 'Triple_parameters.txt'
            fp = open(dir_ + '\\' + 'triple_parameters.txt', 'r')
            line1 = fp.readline().replace('\n', '')
            line1 = line1.split(',')
            if line1[1] == 'Sweep Voltage':
                self.ui.radioButton_sweep_voltage.setChecked(True)
            elif line1[1] == 'Sweep Current':
                self.ui.radioButton_sweep_current.setChecked(True)
            line2 = fp.readline().replace('\n', '')
            line2 = line2.split(',')
            if line2[1] == '2-Point Probe':
                self.ui.radioButton_2_point.setChecked(True)
            elif line2[1] == '4-Point Probe':
                self.ui.radioButton_4_point.setChecked(True)
            line3 = fp.readline().replace('\n', '')
            line3 = line3.split(',')
            self.ui.lineEdit_start_voltage.setText(line3[1])
            line4 = fp.readline().replace('\n', '')
            line4 = line4.split(',')
            self.ui.lineEdit_first_voltage.setText(line4[1])
            line5 = fp.readline().replace('\n', '')
            line5 = line5.split(',')
            self.ui.lineEdit_second_voltage.setText(line5[1])
            line6 = fp.readline().replace('\n', '')
            line6 = line6.split(',')
            self.ui.lineEdit_end_voltage.setText(line6[1])
            line7 = fp.readline().replace('\n', '')
            line7 = line7.split(',')
            self.ui.lineEdit_steps_soft.setText(line7[1])
            line8 = fp.readline().replace('\n', '')
            line8 = line8.split(',')
            self.ui.lineEdit_voltage_time_measurements.setText(line8[1])
            line9 = fp.readline().replace('\n', '')
            line9 = line9.split(',')
            line10 = fp.readline().replace('\n', '')
            line10 = line10.split(',')
            self.ui.lineEdit_run_name.setText(line10[1])
        except:
            pass
     
    def Final_plot(self):
        self.ui.mplwidget_allplot.draw()
        self.ui.mplwidget_first.draw()
        self.ui.mplwidget_second.draw()
        self.ui.mplwidget_third.draw()
        self.ui.mplwidget_real_time.draw()
        print "test"
        
    def plot_dynamic_data(self):
        self.ui.mplwidget_allplot.draw()
        self.ui.mplwidget_real_time.draw()
        
    def set_data(self, return_data):
        # 0voltage_values, 1current_values, 2resistance_first, 3resistance_second, 4resistance_third, 5caled_best_fit_first, 6scaled_best_fit_second, 7scaled_best_fit_third, 8voltage_scale, 9current_scale, 10resistance_first_scale, 11resistance_second_scale, 12resistance_third_scale, 13time, 14length_first, 15length_second
        self.data = return_data
        self.voltage_values = return_data[0]
        self.current_values = return_data[1]
        self.resistance_first = return_data[2]
        self.resistance_second = return_data[3]
        self.resistance_third = return_data[4]
        self.voltage_scale = return_data[8]
        self.current_scale = return_data[9]
        self.voltage_values = self.voltage_values / self.voltage_scale[0]
        self.current_values = self.current_values / self.current_scale[0]
        self.resistance_first_scale = return_data[10]
        self.resistance_second_scale = return_data[11]
        self.resistance_third_scale = return_data[12]
        self.time_length = return_data[13]
        self.time_step = self.time_length / len(self.voltage_values)
        self.Time = []
        for i in range(0, len(self.voltage_values)):
            self.Time.append(i * self.time_step)
        self.length_first = return_data[14]
        self.length_second = return_data[15]
        self.first_Time = self.Time[:self.length_first]
        self.first_voltage = self.voltage_values[:self.length_first]
        self.first_current = self.current_values[:self.length_first]
        self.second_Time = self.Time[self.length_first:self.length_first + self.length_second]
        self.second_voltage = self.voltage_values[self.length_first:self.length_first + self.length_second]
        self.second_current = self.current_values[self.length_first:self.length_first + self.length_second]
        self.third_Time = self.Time[self.length_first + self.length_second:]
        self.third_voltage = self.voltage_values[self.length_first + self.length_second:]
        self.third_current = self.current_values[self.length_first + self.length_second:]
        
    def Stop(self):
        self.ui.pushButton_Stop.setEnabled(False)
        self.ui.pushButton_Continue.setEnabled(True)
        self.ui.lineEdit_condition.setText('Stopped. Click "continue" to go on.')
        self.collect_data_thread.stop_continue()

    def Continue(self):
        self.ui.pushButton_Continue.setEnabled(False)
        self.ui.pushButton_Stop.setEnabled(True)
        self.ui.lineEdit_condition.setText('Collecting...')
        self.collect_data_thread.start_continue()

    # If you choose voltage source, then sweep_voltage is enabled and sweep_current isn't        
    def voltageSweep(self):
        self.ui.groupBox_sweep_voltage.setEnabled(True)
        self.ui.groupBox_sweep_current.setEnabled(False)
        
    # If you choose current source, then sweep_current is enabled and sweep_voltage is not.        
    def currentSweep(self):
        self.ui.groupBox_sweep_voltage.setEnabled(False)
        self.ui.groupBox_sweep_current.setEnabled(True)

    # To refresh the visa address connected to the computer
    def refresh_visa(self):
        # Pulls all active visa ports
        # The try.except clause is in case there are no visa port on the computer. Without it, an error is returned.
        self.rm = visa.ResourceManager()
        try:
            # Collects a list of all the visa ports on the computer
            all_visas = self.rm.list_resources()
        except:
            # Return "No visa available. Please check your connections." if there is no visa available
            all_visas = "No visa available. Please check your connections."

        # Remove the previous results in the comboBox
        self.ui.comboBox_visa.clear()
        # Add each visa to the comboBox
        for item in all_visas:
            self.ui.comboBox_visa.addItem(item)

    def select_visa(self):
        # The visa name displayed in the combobox is defined to the variable visa_chosen
        self.visa_address = str(self.ui.comboBox_visa.currentText())
        self.rm = visa.ResourceManager()
        self.rm.list_resources()
        inst = self.rm.open_resource(self.visa_address)
        self.visa_check = self.check_visa(inst)
        if self.visa_check == True:
            self.ui.lineEdit_condition.setText("Visa is selected succefully!")
            self.ui.label_visa_address.setText(self.visa_address)
            self.visa_name = inst.query("*IDN?")
            self.ui.label_visa_name.setText(self.visa_name)
            self.visa_chosen = inst
            
        elif self.visa_check == False:
            self.ui.lineEdit_condition.setText("Invalid visa address.")
            self.ui.label_visa_address.setText("None.")
            self.ui.label_visa_name.setText("None.")
            self.visa_chosen = False
            
        self.ui.tabWidget.setEnabled(True)
        self.ui.groupBox_preview.setEnabled(True)
        self.ui.groupBox_3.setEnabled(True)

    # This one is used to check whether the Keithley is connected correctly using the command "*IDN?"
    # It can be frequently used in the beginning of each function because if the Agilent is not linked no functions can run correctly
    def check_visa(self, inst):
        try:
            inst.ask("*IDN?")
            valid = True
        except:
            valid = False
        return valid

    # To close it just make current visa address and visa name into nothing
    # And also to close the visa_address
    def close_visa(self):
        self.visa_chosen.close()
        self.ui.lineEdit_condition.setText('')
        self.ui.label_visa_address.setText('')
        self.ui.label_visa_name.setText('')

    # To judge using voltage or current
    def judge_measurement(self):
        if self.ui.radioButton_software.isChecked():
            self.ui.groupBox_source.setEnabled(True)
            self.ui.groupBox_stop_continue.setEnabled(True)
        #Reset plots
        self.reset_plot_time()
        self.ui.lineEdit_condition.setText("Collecting data...")
        self.ui.pushButton_Stop.setEnabled(True)
        self.ui.pushButton_run.setEnabled(False)
        if self.ui.radioButton_sweep_voltage.isChecked():
            self.VoltageSweep()
            self.Sweep = 'Voltage'
            
        self.ui.tabWidget_2.setEnabled(True)
        self.ui.pushButton_reset.setEnabled(True)
        
    # If the user wants to stop the measurement during the process, just click the checkbox
    # And this is to judge whether the checkbox is checked
    def software_stepping(self):
        self.ui.groupBox_stop_continue.setEnabled(True)
        self.ui.pushButton_Stop.setEnabled(False)
        self.ui.pushButton_Continue.setEnabled(False)
        self.ui.groupBox_source.setEnabled(True)
        
        
    def VoltageSweep(self):
        # Collect parameters from the interface
        start_voltage = float(self.ui.lineEdit_start_voltage.text())/1000
        first_voltage = float(self.ui.lineEdit_first_voltage.text())/1000
        second_voltage = float(self.ui.lineEdit_second_voltage.text())/1000
        end_voltage = float(self.ui.lineEdit_end_voltage.text())/1000
        if (self.ui.radioButton_software.isChecked() == True):
            num_steps = int(self.ui.lineEdit_steps_soft.text())

        sweep = 'VOLTAGE'
        
        # For the voltage and current limit
        if abs(start_voltage) > abs(first_voltage) and abs(start_voltage) > abs(second_voltage) and abs(start_voltage) > abs(end_voltage):
            voltage_lim = (1.01) * abs(start_voltage)
        elif abs(first_voltage) > abs(start_voltage) and abs(first_voltage) > abs(second_voltage) and abs(start_voltage) > abs(end_voltage):
            voltage_lim = (1.01) * abs(first_voltage)
        elif abs(second_voltage) > abs(start_voltage) and abs(second_voltage) > abs(first_voltage) and abs(second_voltage) > abs(end_voltage):
            voltage_lim = (1.01) * abs(second_voltage)
        else:
            voltage_lim = (1.01) * abs(end_voltage)
        current_lim = 500

        # Other important parameters
        wait_time = float(self.ui.lineEdit_voltage_time_measurements.text())
        if (self.ui.radioButton_software.isChecked() == True):
            voltage_steps = (start_voltage - first_voltage) / num_steps
        #voltage_steps = (2 * first_voltage - start_voltage - end_voltage) / num_steps
        voltage_first = numpy.arange(start_voltage, first_voltage - voltage_steps, - voltage_steps, dtype = 'float')
        voltage_second = numpy.arange(first_voltage, second_voltage + voltage_steps, voltage_steps, dtype = 'float')
        voltage_third = numpy.arange(second_voltage, end_voltage - voltage_steps, - voltage_steps, dtype = 'float')
        Voltage = numpy.append(voltage_first, voltage_second)
        Voltage = numpy.append(Voltage, voltage_third)
        
        if self.ui.radioButton_2_point.isChecked():
            probe = '2'
            self.Probe = '2'
        elif self.ui.radioButton_4_point.isChecked():
            probe = '4'
            self.Probe = '4'
        
        self.collect_data_thread.input(self.visa_chosen, Voltage, voltage_first, voltage_second,
                                       voltage_lim, current_lim, wait_time, self.ui, sweep, probe)

    def CurrentSweep(self):
        # Collect parameters from the interface
        start_current = float(self.ui.lineEdit_start_current.text())/1E6
        first_current = float(self.ui.lineEdit_first_current.text())/1E6
        second_current = float(self.ui.lineEdit_second_current.text())/1E6
        end_current = float(self.ui.lineEdit_end_current.text())/1E6
        if (self.ui.radioButton_software.isChecked() == True):
            num_steps = int(self.ui.lineEdit_steps_soft.text())

        sweep = 'CURRENT'
        
        if abs(start_current) > abs(first_current) and abs(start_current) > abs(second_current) and abs(start_current) > abs(end_current):
            current_lim = (1.01) * abs(start_current)
        elif abs(first_current) > abs(start_current) and abs(first_current) > abs(end_current):
            current_lim = (1.01) * abs(first_current)
        elif abs(second_current) > abs(start_current) and abs(second_current) > abs(first_current) and abs(second_current) > abs(end_current):
            current_lim = (1.01) * abs(second_current)
        else:
            current_lim = (1.01) * abs(end_current)
        voltage_lim = float(self.ui.lineEdit_voltage_limit.text())/1E3

        # Other important parameters
        wait_time = float(self.ui.lineEdit_current_time_measurements.text())
        if (self.ui.radioButton_software.isChecked() == True):
            current_steps = (start_current - first_current) / num_steps
        current_steps = (2 * first_current - start_current - end_current) / num_steps

        current_first = numpy.arange(start_current, first_current - current_steps, - current_steps, dtype = 'float')
        current_second = numpy.arange(first_current, second_current + current_steps, current_steps, dtype = 'float')
        current_third = numpy.arange(second_current, end_current - current_steps, - current_steps, dtype = 'float')
        Current = numpy.append(current_first, current_second)
        Current = numpy.append(Current, current_third)
        
        if self.ui.radioButton_2_point.isChecked():
            probe = '2'
            self.Probe = '2'
        elif self.ui.radioButton_4_point.isChecked():
            probe = '4'
            self.Probe = '4'

        self.collect_data_thread.input(self.visa_chosen, Current, current_first, current_second,
                                       current_lim, voltage_lim, wait_time, self.ui, sweep, probe)

    def reset_plot_time(self):
        self.ui.mplwidget_time.figure.clear()

        # Creates the new plot and is defined to self.axes.
        # All one has to do is to create a plot, which is "self.ui.,plwdget_direction.axes" used equivalently
        # to "self.axes" above and a new subplot does not have to be defined, as done below.)
        #self.axes_real_time = self.ui.mplwidget_real_time.figure.add_subplot(111)
        #self.axes_first = self.ui.mplwidget_first.figure.add_subplot(111)
        self.axes_time = self.ui.mplwidget_time.figure.add_subplot(111)

    def preview(self):
        Time = []
        Values = []
        Voltage = []
        
        if self.ui.radioButton_sweep_voltage.isChecked():
            start_voltage = float(self.ui.lineEdit_start_voltage.text())
            first_voltage = float(self.ui.lineEdit_first_voltage.text())
            second_voltage = float(self.ui.lineEdit_second_voltage.text())
            end_voltage = float(self.ui.lineEdit_end_voltage.text())
            #num_steps = int(self.ui.lineEdit_time_steps_v.text())
            if (self.ui.radioButton_software.isChecked() == True):
                num_steps = int(self.ui.lineEdit_steps_soft.text())
            wait_time = float(self.ui.lineEdit_voltage_time_measurements.text()) * 1E3
            if (self.ui.radioButton_software.isChecked() == True):
                voltage_steps = (start_voltage - first_voltage) / num_steps
            voltage_first = numpy.arange(start_voltage, first_voltage - voltage_steps, - voltage_steps, dtype = 'float')
            voltage_second = numpy.arange(first_voltage, second_voltage + voltage_steps, voltage_steps, dtype = 'float')
            voltage_third = numpy.arange(second_voltage, end_voltage - voltage_steps, - voltage_steps, dtype = 'float')
            Voltage = numpy.append(voltage_first, voltage_second)
            Voltage = numpy.append(Voltage, voltage_third)
            
            # Create Voltage and Time lists
            for i in range(0, len(Voltage)):
                Time.append(wait_time * i)
                Time.append(wait_time * (i +1) - 0.001)
                Values.append(Voltage[i])
                Values.append(Voltage[i])

            # Plot Values vs. Time
            self.reset_plot_time()
            self.axes_time.plot(Time, Values)
            self.axes_time.set_title('\n'.join(wrap('Voltage vs. Theoretical Time')))
            self.axes_time.set_xlabel('Time (ms)')
            self.axes_time.set_ylabel('Voltage (mV)')
            self.ui.mplwidget_time.draw()

        elif self.ui.radioButton_sweep_current.isChecked():
            start_current = float(self.ui.lineEdit_start_current.text())
            first_current = float(self.ui.lineEdit_first_current.text())
            second_current = float(self.ui.lineEdit_second_current.text())
            end_current = float(self.ui.lineEdit_end_current.text())
            if (self.ui.radioButton_software.isChecked() == True):
                num_steps = int(self.ui.lineEdit_steps_soft.text())
            wait_time = float(self.ui.lineEdit_current_time_measurements.text()) * 1E3
            if (self.ui.radioButton_software.isChecked() == True):
                current_steps = (start_current - first_current) / num_steps
            current_first = numpy.arange(start_current, first_current - current_steps, - current_steps, dtype = 'float')
            current_second = numpy.arange(first_current, second_current + current_steps, current_steps, dtype = 'float')
            current_third = numpy.arange(second_current, end_current - current_steps, - current_steps, dtype = 'float')
            Current = numpy.append(current_first, current_second)
            Current = numpy.append(Current, current_third)

            for i in range(0, len(Current)):
                Time.append(wait_time * i)
                Time.append(wait_time * (i + 1) - 0.001)
                Values.append(Current[i])
                Values.append(Current[i])

            self.reset_plot_time()
            self.axes_time.plot(Time, Values)
            self.axes_time.set_title('\n'.join(wrap('Current vs. Theoretical Time')))
            self.axes_time.set_xlabel('Time (ms)')
            self.axes_time.set_ylabel('Current (uA)')
            self.ui.mplwidget_time.draw()
            
    def select_check(self):
        self.ui.pushButton_Save.setEnabled(True)
        self.googledrive_directory = str(self.ui.lineEdit_GoogleDrive.text())
        self.namefolder = str(self.ui.comboBox_Name_Folder.currentText())
        if self.namefolder == 'None':
            self.ui.lineEdit_save_condition.setText('Please choose a name folder to save.')
        else:
            self.date = '%s-%s-%s' % (now.year, now.month, now.day)
            self.ui.lineEdit_save_condition.setText("Save file to Google Drive\\" + self.namefolder + "\Date" + '\\' + self.date)
            self.ui.groupBox_File_Type.setEnabled(True)
            self.ui.groupBox_Filename.setEnabled(True)
            self.ui.label_32.setEnabled(True)
            self.ui.textEdit_comment.setEnabled(True)
    
    def Browse(self):
        prev_dir = 'C:\\'
        self.fileDir = QFileDialog.getExistingDirectory(self, 'Select Google Drive Folder to Open:', prev_dir)
        if self.fileDir != '':
            self.file_list = str(self.fileDir).split('/')
            for i in range(0, len(self.file_list) - 1):
                if i < len(self.file_list) - 1:
                    self.open_dir += self.file_list[i] + '\\'
                elif i == len(self.file_list) - 1:
                    self.open_dir += self.file_list[i]
            self.fileDir.replace('/', '\\')
            self.ui.lineEdit_GoogleDrive.setText(self.fileDir)
            self.ui.lineEdit_save_condition.setText('Open Google Drive User Folder')
        else:
            self.ui.lineEdit_GoogleDrive.setText('None')
            self.ui.lineEdit_save_condition.setText('Failed to Read File')
            
    def Check(self):
        file_list2 = []
        file_list2 = str(self.ui.lineEdit_GoogleDrive.text()).split('\\')
        user_folder = file_list2[len(file_list2) - 1]
        if os.path.exists(self.ui.lineEdit_GoogleDrive.text()) == False:
            self.ui.lineEdit_save_condition.setText('Incorrect Google Drive Directory.')
        else:
            if user_folder.upper() != '03 User Accounts'.upper():
                self.ui.lineEdit_save_condition.setText('Please click browse to the "03 User Accounts" folder')
            else:
                self.ui.label_22.setEnabled(True)
                self.ui.comboBox_Name_Folder.setEnabled(True)
                self.ui.pushButton_Select_Directory.setEnabled(True)
            
    def select_type(self):
        if self.ui.radioButton_csv.isChecked():
            self.type = '.csv'
            self.divide = ','
            self.form = ''
        elif self.ui.radioButton_txt.isChecked():
            self.type = '.txt'
            self.divide = '\t'
            self.form = '                         '
    
    def select_name(self):
        if self.ui.radioButton_Timename.isChecked():
            self.date = '%s-%s-%s' % (now.year, now.month, now.day)
            self.current_time = '%s.%s.%s' % (now.hour, now.minute, now.second)
            self.date_and_time = self.date + ' ' + self.current_time
            self.file_name = str(self.date_and_time)
        elif self.ui.radioButton_Custom_Name.isChecked():
            self.file_name = str(self.ui.lineEdit_Custom_Name.text())
    
    def enable_custom_name(self):
        self.ui.lineEdit_Custom_Name.setEnabled(True)
        
    def disable_custom_name(self):
        self.ui.lineEdit_Custom_Name.setEnabled(False)
        
    def initalizeTable(self):
        variables = ["Select", "Run", "Resistance of the First Period", "Resistance of the Second Period", "Resistance of the Third Period", "Sweep", "Start", "First Peak", "Second Peak", "End", "Num Steps (From Start Voltage to First Peak)", "Limit", "Time Step", "Probe Type"]
        for i in range(len(variables)):
            self.ui.tableWidget_data.insertColumn(0)
        #self.ui.tableWidgetSPreviousBounds.insertRow(0)
        self.ui.tableWidget_data.setHorizontalHeaderLabels(variables)
        #self.PreviousBounds = []
        #self.previousBounds_num = 0
    
    def Open(self):
        opendir = self.path
        open_path = 'explorer "' + opendir + '"'
        subprocess.Popen(open_path)
    
    def reset(self):
        self.reset_plot_time()
        self.ui.pushButton_run.setEnabled(True)
    
    def save(self):
        self.select_type()
        self.select_name()
        if self.file_name == '':
            self.ui.lineEdit_save_condition.setText('Please enter a valid file name')
        else:
            self.path = self.googledrive_directory + '\\' + self.namefolder + '\\' + 'Data' + '\\' + self.date + '\\' + 'Keithley for Resistance'
            # Create a folder at this address
            if not os.path.isdir(self.path):
                os.makedirs(self.path)
            # This the name of the file
            self.name = self.googledrive_directory + '\\' + self.namefolder + '\\' + 'Data' + '\\' + self.date + '\\' + 'Keithley for Resistance' + '\\' + self.file_name + self.type
            
            parameter_txt = self.googledrive_directory + '\\' + self.namefolder + '\\' + 'Data' + '\\' + self.date + '\\' + 'Parameter.txt'
            f = open(parameter_txt, 'w')
            f.write('The parameters of the sweep voltage process are shown blow.' + '\n')
            f.write('Start Voltage' + self.divide + self.ui.lineEdit_start_voltage.text() + self.divide + 'mV' + '\n')
            f.write('First Peak Voltage' + self.divide + self.ui.lineEdit_first_voltage.text() + self.divide + 'mV' + '\n')
            f.write('Second Peak Voltage' + self.divide + self.ui.lineEdit_second_voltage.text() + self.divide + 'mV' + '\n')
            f.write('End Voltage' + self.divide + self.ui.lineEdit_end_voltage.text() + self.divide + 'mV' + '\n')
            f.write('Time Step' + self.divide + self.ui.lineEdit_voltage_time_measurements.text() + self.divide + 's' + '\n')
            f.write('Software Time Step' + self.divide + self.ui.lineEdit_steps_soft.text() + self.divide + '1' + '\n')
            f.close()
            
            f = open(self.name, 'w')
            # The beginning of the file is name and time
            f.write('Name' + self.divide + self.namefolder + '\n')
            f.write('Time' + self.divide + str(now) + '\n')
            f.write('\n')
            
            # First part of the file is labels and parameters
            f.write('Label' + self.divide + 'Parameter' + self.divide + 'Unit' + '\n')
            f.write('Sweep Source' + self.divide + self.Sweep + '\n')
            f.write('Points of Probe' + self.divide + str(self.Probe) + '\n')
            if self.Sweep == 'Voltage':
                f.write('Start Voltage' + self.divide + str(self.ui.lineEdit_start_voltage.text()) + self.divide + 'mV' + '\n')
                f.write('Frist Peak Voltage' + self.divide + str(self.ui.lineEdit_first_voltage.text()) + self.divide + 'mV' + '\n')
                f.write('Second Peak Voltage' + self.divide + str(self.ui.lineEdit_second_voltage.text()) + self.divide + 'mV' + '\n')
                f.write('End Voltage' + self.divide + str(self.ui.lineEdit_end_voltage.text()) + self.divide + 'mV' + '\n')
                if (self.ui.radioButton_software.isChecked() == True):
                    f.write('Steps Number' + self.divide + str(self.ui.lineEdit_steps_soft.text()) + self.divide + '\n')
                elif (self.ui.radioButton_hardware.isChecked() == True):
                    f.write('Steps Number' + self.divide + str(self.ui.lineEdit_steps_hard.text()) + self.divide + '\n')
                f.write('Current Limit' + self.divide + str(self.ui.lineEdit_current_limit.text()) + self.divide + 'uA' + '\n')
                f.write('Time Step' + self.divide + str(self.ui.lineEdit_voltage_time_measurements.text()) + self.divide + 's' + '\n')
                f.write('Resistance with the First Period Voltage' + self.divide + str(self.resistance_first) + self.divide + self.resistance_first_scale[1] + '\n')
                f.write('Resistance with the Second Period Voltage' + self.divide + str(self.resistance_second) + self.divide + self.resistance_second_scale[1] + '\n')
                f.write('Resistance with the Third Period Voltage' + self.divide + str(self.resistance_third) + self.divide + self.resistance_third_scale[1] + '\n')
                
                f.write('\n')
                f.write('Collected data' + '\n')
                f.write('Time' + self.divide + 'Voltage' + self.divide + 'Current' + self.divide + 'First Period Time' + self.divide + 'First Period Voltage' + self.divide +
                        'Current' + self.divide + 'Second Period Time' + self.divide + 'Second Period Voltage' + self.divide + 'Current' + self.divide + 'Third Period Time' +
                        self.divide + 'Third Period Voltage' + self.divide + 'Current' + self.divide + '\n')
                f.write('s' + self.divide + 'Volts' + self.divide + 'Amps' + self.divide + 's' + self.divide + 'Volts' + self.divide + 'Amps' +self.divide + 's' +self.divide + 'Volts' +
                        self.divide + 'Amps' + self.divide + 's' + self.divide + 'Volts' + self.divide + 'Amps' + '\n')
                for i in range(0, len(self.Time)):
                    full_data = str(self.Time[i]) + self.divide + str(self.voltage_values[i]) + self.divide + str(self.current_values[i])
                    try:
                        first_data = str(self.first_Time[i]) + self.divide + str(self.first_voltage[i]) + self.divide + str(self.first_current[i])
                    except:
                        first_data = '' + self.divide + '' + self.divide + ''
                    try:
                        second_data = str(self.second_Time[i]) + self.divide + str(self.second_voltage[i]) + self.divide + str(self.second_current[i])
                    except:
                        second_data = '' + self.divide + '' + self.divide + ''
                    try:
                        third_data = str(self.third_Time[i]) + self.divide + str(self.third_voltage[i]) + self.divide + str(self.third_current[i])
                    except:
                        third_data = '' + self.divide + '' + self.divide + ''
                    full_string = full_data + self.divide + first_data + self.divide + second_data + self.divide + third_data + '\n'
                    f.write(full_string)
                
                
            else:
                f.write('Start Current' + self.divide + str(self.ui.lineEdit_start_current.text()) + self.divide + 'uA' + '\n')
                f.write('First Peak Current' + self.divide + str(self.ui.lineEdit_first_current.text()) + self.divide + 'uA' + '\n')
                f.write('Second Peak Current' + self.divide + str(self.ui.lineEdit_second_current.text()) + self.divide + 'uA' + '\n')
                f.write('End Current' + self.divide + str(self.ui.lineEdit_end_current.text()) + self.divide + 'uA' + '\n')
                if (self.ui.radioButton_software.isChecked() == True):
                    f.write('Steps Number' + self.divide + str(self.ui.lineEdit_steps_soft.text()) + self.divide + '\n')
                elif (self.ui.radioButton_hardware.isChecked() == True):
                    f.write('Steps Number' + self.divide + str(self.ui.lineEdit_steps_hard.text()) + self.divide + '\n')
                f.write('Voltage Limit' + self.divide + str(self.ui.lineEdit_voltage_limit.text()) + self.divide + 'mV' + '\n')
                f.write('Time Step' + self.divide + str(self.ui.lineEdit_current_time_measurements.text()) + self.divide + 's' + '\n')
                f.write('Resistance with the First Period Current' + self.divide + str(self.resistance_first) + self.divide + str(self.resistance_first_scale[1]) + '\n')
                f.write('Resistance with the Second Period Current' + self.divide + str(self.resistance_second) + self.divide + str(self.resistance_second_scale[1]) + '\n')
                f.write('Resistance with the Third Period Current' + self.divide + str(self.resistance_third) + self.divide + str(self.resistance_third_scale[1]) + '\n')
                
                f.write('\n')
                f.write('Collected data' + '\n')
                f.write('Time' + self.divide + 'Current' + self.divide + 'Voltage' + self.divide + 'First Period Time' + self.divide + 'First Period Current' + self.divide +
                        'Voltage' + self.divide + 'Second Period Time' + self.divide + 'Second Period Current' + self.divide + 'Voltage' + self.divide +
                        'Thrid Period Time' + self.divide + 'Third Period Current' + self.divide + 'Voltage' + '\n')
                f.write('s' + self.divide + 'Amps' + self.divide + 'Volts' + self.divide + 's' + self.divide + 'Amps' + self.divide + 'Volts' + self.divide + 's' + self.divide + 'Amps' +
                        self.divide + 'Volts' + self.divide + 's' + self.divide + 'Amps' + self.divide + 'Volts' + '\n')
                for i in range(0, len(self.Time)):
                    full_data = str(self.Time[i]) + self.divide + str(self.current_values[i]) + self.divide + str(self.voltage_values[i])
                    try:
                        first_data = str(self.first_Time[i]) + self.divide + str(self.first_current[i]) + self.divide + str(self.first_voltage[i])
                    except:
                        first_data = '' + self.divide + '' + self.divide + ''
                    try:
                        second_data = str(self.second_Time[i]) + self.divide + str(self.second_current[i]) + self.divide + str(self.second_voltage[i])
                    except:
                        second_data = '' + self.divide + '' + self.divide + ''
                    try:
                        third_data = str(self.third_Time[i]) + self.divide + str(self.third_current[i]) + self.divide + str(self.third_voltage[i])
                    except:
                        third_data = '' + self.divide + '' + self.divide + ''
                    full_string = full_data + self.divide + up_data + self.divide + down_data + '\n'
                    f.write(full_string)
        f.close()
        self.ui.lineEdit_condition.setText("Your file has been successfully saved.")
        self.ui.pushButton_Open.setEnabled(True)
        
        self.data_collection_path = self.googledrive_directory + '\\' + self.namefolder + '\\' + 'Data' + '\\' + 'Data_Collection_History.txt'
        content = str(self.date + self.divide + self.current_time + self.divide + self.ui.lineEdit_run_name.text() + self.divide + self.file_name + self.divide + self.ui.textEdit_comment.toPlainText() + '\n')
        with open(self.data_collection_path, "a") as myfile:
            myfile.write(content)

        
    def closeEvent(self, event):
        # Creates a message box that displays the quit_msg
        quit_msg = "Do you want to quit the program?"

        # with two pushButtons -- 'Yes' or 'No'
        reply1 = QMessageBox.question(self, 'Message', quit_msg,
                                     QMessageBox.Yes, QMessageBox.No)

        # Yes means the user wants to quit. Thus the window is closed.
        if reply1 == QMessageBox.Yes:
            try:
                self.visa_chosen.close()
                quit_msg = "Do you want to save the parameters?"
                reply2 = QMessageBox.question(self, 'Message', quit_msg,
                                     QMessageBox.Yes, QMessageBox.No)
                if reply2 == QMessageBox.Yes:
                    try:
                        f = open('Triple_parameters.txt', 'w')
                        if self.ui.radioButton_sweep_voltage.isChecked():
                            f.write('Sweep Type' + ',' + 'Sweep Voltage' + '\n')
                        elif self.ui.radioButton_sweep_current.isChecked():
                            f.write('Sweep Type' + ',' + 'Sweep Current' + '\n')
                        if self.ui.radioButton_2_point.isChecked():
                            f.write('Probe Type' + ',' + '2-Point Probe' + '\n')
                        elif self.ui.radioButton_4_point.isChecked():
                            f.write('Probe Type' + ',' + '4-Point Probe' + '\n')
                        f.write('Start Voltage' + ',' + self.ui.lineEdit_start_voltage.text() + '\n')
                        f.write('First Peak Voltage' + ',' + self.ui.lineEdit_first_voltage.text() + '\n')
                        f.write('Second Peak Voltage' + ',' + self.ui.lineEdit_second_voltage.text() + '\n')
                        f.write('End Voltage' + ',' + self.ui.lineEdit_end_voltage.text() + '\n')
                        f.write('Measure Steps' + ',' + self.ui.lineEdit_steps_soft.text() + '\n')
                        f.write('Time Step' + ',' + self.ui.lineEdit_voltage_time_measurements.text() + '\n')
                        f.write('Step Type' + ',' + 'Software Stepping' + '\n')
                        f.write('Run Name' + ',' + self.ui.lineEdit_run_name.text() + '\n')
                        f.close()
                    except:
                        pass
                    event.accept()
            except:
                pass
            event.accept()

        # No means the user does not want to quit and the window is still there.
        else:
            event.ignore()
                
class Collect_data(QThread):
    def __init__(self, parent = None):
        QThread.__init__(self, parent)
        self.exiting = False

    def input(self, inst, sweep_array, sweep_array_first, sweep_array_second, sweep_lim, read_lim, wait_time, ui, sweep, probe):
        self.inst  = inst
        self.sweep_array = sweep_array
        self.sweep_array_first = sweep_array_first
        self.sweep_array_second = sweep_array_second
        self.sweep_lim = sweep_lim
        self.read_lim = read_lim
        self.wait_time = wait_time
        self.ui = ui
        self.sweep = sweep
        self.probe = probe
        #self.run()
        self.start()

    def stop_continue(self):
        self.sweep_stop.continue_check = False

    def start_continue(self):
        self.sweep_stop.continue_check = True
            
    def run(self):
        self.reset_plot_real_time()
        self.reset_plot_first()
        self.reset_plot_second()
        self.reset_plot_third()
        self.reset_plot_allplot()
        if self.sweep == "VOLTAGE":
            if self.ui.radioButton_software.isChecked():
                self.sweep_stop = Sweep.sweep_stop()
                voltage_values, current_values, resistance_first, resistance_second, resistance_third, scaled_best_fit_first, scaled_best_fit_second, scaled_best_fit_third, voltage_scale, current_scale, resistance_first_scale, resistance_second_scale, resistance_third_scale, time, length_first, length_second = self.sweep_stop.voltage_sweep_stop(self.inst, self.sweep_array, self.sweep_array_first, self.sweep_array_second, self.sweep_lim, self.read_lim, self.wait_time, self.probe, self.ui, self.emit)
            
            self.reset_plot_allplot()
            self.axes_allplot.plot(voltage_values, current_values, marker = '.', linestyle = '')
            self.axes_allplot.set_title('\n'.join(wrap('Voltage vs. Current with All Points')))
            self.axes_allplot.set_xlabel('Voltage (' + voltage_scale[1] + ')')
            self.axes_allplot.set_ylabel('Current (' + current_scale[1] + ')')
                
            self.ui.lineEdit_bfr_first.setText(str(round(resistance_first, 4)))
            self.ui.label_resistance_unit_first.setText(resistance_first_scale[1])
            self.ui.lineEdit_bfr_second.setText(str(round(resistance_second, 4)))
            self.ui.label_resistance_unit_second.setText(resistance_second_scale[1])
            self.ui.lineEdit_bfr_third.setText(str(round(resistance_third, 4)))
            self.ui.label_resistance_unit_third.setText(resistance_third_scale[1])
            
            # Add the data table into the TableWidget
            self.addTable(str(round(resistance_first, 4)), resistance_first_scale, str(round(resistance_second, 4)), resistance_second_scale, str(round(resistance_third, 4)), resistance_third_scale)
            
            # Plot the ascending figure
            best_fit_line_first = scaled_best_fit_first[0] * numpy.array(voltage_values[:length_first], dtype = 'float') + scaled_best_fit_first[1]
            
            self.reset_plot_first()
            self.axes_first.plot(voltage_values[:length_first], current_values[:length_first], marker = '.', linestyle = '')
            self.axes_first.plot(voltage_values[:length_first], best_fit_line_first)
            self.axes_first.set_title('\n'.join(wrap('Voltage vs. Current with the first period voltage')))
            self.axes_first.set_xlabel('Voltage (' + voltage_scale[1] + ')')
            self.axes_first.set_ylabel('Current (' + current_scale[1] + ')')
            
            
            # Plot the descending figure
            best_fit_line_second = scaled_best_fit_second[0] * numpy.array(voltage_values[length_first:length_first + length_second], dtype = 'float') + scaled_best_fit_second[1]
            
            self.reset_plot_second()
            self.axes_second.plot(voltage_values[length_first:length_first + length_second], current_values[length_first:length_first + length_second], marker = '.', linestyle = '')
            self.axes_second.plot(voltage_values[length_first:length_first + length_second], best_fit_line_second)
            self.axes_second.set_title('\n'.join(wrap('Voltage vs. Current with the second period voltage' )))
            self.axes_second.set_xlabel('Voltage (' + voltage_scale[1] + ')')
            self.axes_second.set_ylabel('Current (' + current_scale[1] + ')')
            

            best_fit_line_third = scaled_best_fit_third[0] * numpy.array(voltage_values[length_first + length_second:], dtype = 'float') + scaled_best_fit_second[1]
            
            self.reset_plot_third()
            self.axes_third.plot(voltage_values[length_first + length_second:], current_values[length_first + length_second:], marker = '.', linestyle = '')
            self.axes_third.plot(voltage_values[length_first + length_second:], best_fit_line_third)
            self.axes_third.set_title('\n'.join(wrap('Voltage vs. Current with the third period voltage' )))
            self.axes_third.set_xlabel('Voltage (' + voltage_scale[1] + ')')
            self.axes_third.set_ylabel('Current (' + current_scale[1] + ')')
            
            
            self.ui.pushButton_run.setEnabled(True)
            
            # Plot the time figure
            time_step = time / len(voltage_values)
            time_value = []
            voltage_values_double = []
            for i in range(0, len(voltage_values)):
                time_value.append(i * time_step)
                time_value.append((i + 1) * time_step - 0.001)
                voltage_values_double.append(voltage_values[i])
                voltage_values_double.append(voltage_values[i])
            self.reset_plot_real_time()
            self.axes_real_time.plot(time_value, voltage_values_double)
            self.axes_real_time.set_title('\n'.join(wrap('Voltage vs.Real Time')))
            self.axes_real_time.set_xlabel('Time (s)')
            self.axes_real_time.set_ylabel('Voltage (' + voltage_scale[1] + ')')
            
            
            return_data = [voltage_values, current_values, resistance_first, resistance_second, resistance_third, scaled_best_fit_first, scaled_best_fit_second, scaled_best_fit_third, voltage_scale, current_scale, resistance_first_scale, resistance_second_scale, resistance_third_scale, time, length_first, length_second]
            
        elif self.sweep == "CURRENT":
            if self.ui.radioButton_software.isChecked():
                self.sweep_stop = Sweep.sweep_stop()
                
                voltage_values, current_values, resistance_first, resistance_second, resistance_third, scaled_best_fit_first, scaled_best_fit_second, scaled_best_fit_third, voltage_scale, current_scale, resistance_first_scale, resistance_second_scale, resistance_third_scale, time, length_first, length_second = self.sweep_stop.current_sweep_stop(self.inst, self.sweep_array, self.sweep_array_ascending, self.sweep_lim, self.read_lim, self.wait_time, self.probe, self.ui)
            
            self.reset_plot_allplot()
            self.axes_allplot.plot(current_values, voltage_values, marker = '.', linestyle = '')
            self.axes_allplot.set_title('\n'.join(wrap('Current vs. Voltage with All Points')))
            self.axes_allplot.set_xlabel('Current (' + current_scale[1] + ')')
            self.axes_allplot.set_ylabel('Voltage (' + voltage_scale[1] + ')')
            self.ui.mplwidget_allplot.draw()
            
            self.ui.lineEdit_bfr_first.setText(str(round(resistance_first, 4)))
            self.ui.label_resistance_unit_first.setText(resistance_first_scale[1])
            self.ui.lineEdit_bfr_second.setText(str(round(resistance_second, 4)))
            self.ui.label_resistance_unit_second.setText(resistance_second_scale[1])
            self.ui.lineEdit_bfr_third.setText(str(round(resistance_third, 4)))
            self.ui.label_resistance_unit_third.setText(resistance_third_scale[1])
            
            # Add data into the Data Widget
            self.addTable(str(round(resistance_first, 4)), resistance_first_scale, str(round(resistance_second, 4)), resistance_second_scale, str(round(resistance_third, 4)), resistance_third_scale)
            # Plot the ascending figure
            best_fit_line_first = scaled_best_fit_first[0] * numpy.array(current_values[:length_first], dtype = 'float') + scaled_best_fit_first[1]
            
            self.reset_plot_first()
            self.axes_first.plot(current_values[0:length_first], voltage_values[0:length_first], marker = '.', linestyle = '')
            self.axes_first.plot(current_values[0:length_first], best_fit_line_first)
            self.axes_first.set_title('\n'.join(wrap('Current vs. Voltage with ascending current')))
            self.axes_first.set_xlabel('Current (' + current_scale[1] + ')')
            self.axes_first.set_ylabel('Voltage (' + voltage_scale[1] + ')')
            self.ui.mplwidget_first.draw()
            
            # Plot the descending figure
            best_fit_line_second = scaled_best_fit_second[0] * numpy.array(current_values[length_first:length_first + length_second], dtype = 'float') + scaled_best_fit_second[1]
            
            self.reset_plot_second()
            self.axes_second.plot(current_values[length_first:length_first + length_second], voltage_values[length_first:length_first + length_second], marker = '.', linestyle = '')
            self.axes_second.plot(current_values[length_first:length_first + length_second], best_fit_line_second)
            self.axes_second.set_title('\n'.join(wrap('Current vs. Voltage with descending current')))
            self.axes_second.set_xlabel('Current (' + current_scale[1] + ')')
            self.axes_second.set_ylabel('Voltage (' + voltage_scale[1] + ')')
            self.ui.mplwidget_second.draw()
            
            best_fit_line_third = scaled_best_fit_third[0] * numpy.array(current_values[length_first + length_second:], dtype = 'float') + scaled_best_fit_second[1]
            
            self.reset_plot_third()
            self.axes_third.plot(current_values[length_first:length_first + length_second], voltage_values[length_first:length_first + length_second], marker = '.', linestyle = '')
            self.axes_third.plot(current_values[length_first:length_first + length_second], best_fit_line_third)
            self.axes_third.set_title('\n'.join(wrap('Current vs. Voltage with descending current')))
            self.axes_third.set_xlabel('Current (' + current_scale[1] + ')')
            self.axes_third.set_ylabel('Voltage (' + voltage_scale[1] + ')')
            self.ui.mplwidget_third.draw()

            self.ui.pushButton_run.setEnabled(True)
            self.ui.pushButton_Stop.setEnabled(False)
            
            # Plot the time figure
            time_step = time / len(current_values)
            time_value = []
            current_values_double = []
            for i in range(0, len(current_values)):
                time_value.append(i * time_step)
                time_value.append((i + 1) * time_step - 0.001)
                current_values_double.append(current_values[i])
                current_values_double.append(current_values[i])
            self.reset_plot_real_time()
            self.axes_real_time.plot(time_value, current_values_double)
            self.axes_real_time.set_title('\n'.join(wrap('Current vs.Time')))
            self.axes_real_time.set_ylabel('Current (' + current_scale[1] + ')')
            self.axes_real_time.set_xlabel('Time (s)')
            self.ui.mplwidget_real_time.draw()
        
            return_data = [voltage_values, current_values, resistance_first, resistance_second, resistance_third, scaled_best_fit_first, scaled_best_fit_second, scaled_best_fit_third, voltage_scale, current_scale, resistance_first_scale, resistance_second_scale, resistance_third_scale, time, length_first, length_second]
        
        self.ui.lineEdit_condition.setText("Data plotting successfully!")
        self.ui.groupBox_save.setEnabled(True)

        self.emit(SIGNAL('final_plot'))
        self.emit(SIGNAL("Data"), return_data)
    
    def addTable(self, resistance_first, resistance_first_scale, resistance_second, resistance_second_scale, resistance_third, resistance_third_scale):
        
        self.ui.tableWidget_data.insertRow(0)
        checkBoxItem = QTableWidgetItem('')
        checkBoxItem.setFlags(Qt.ItemIsUserCheckable |
                                      Qt.ItemIsEnabled)
        checkBoxItem.setCheckState(Qt.Unchecked)
        
        run_name = str(self.ui.lineEdit_run_name.text())
        if self.sweep == "VOLTAGE":
            start = str(self.ui.lineEdit_start_voltage.text()) + " mV"
            first = str(self.ui.lineEdit_first_voltage.text()) + " mV"
            second = str(self.ui.lineEdit_second_voltage.text()) + ' mV'
            end = str(self.ui.lineEdit_end_voltage.text()) + " mV"
            if (self.ui.radioButton_software.isChecked() == True):
                num_step = self.ui.lineEdit_steps_soft.text()
            limit = str(100) + " mA"
            time = str(self.ui.lineEdit_voltage_time_measurements.text()) + " s"
        elif self.sweep == "CURRENT":
            start = str(self.ui.lineEdit_start_current.text()) + " uA"
            first = str(self.ui.lineEdit_first_current.text()) + " uA"
            second = str(self.ui.lineEdit_second_current.text()) + ' uA'
            end = str(self.ui.lineEdit_end_current.text()) + " uA"
            if (self.ui.radioButton_software.isChecked() == True):
                num_step = self.ui.lineEdit_steps_soft.text()
            limit = str(self.ui.lineEdit_voltage_limit.text()) + " mV"
            time = str(self.ui.lineEdit_current_time_measurements.text()) + " s"
        
        point_data = [checkBoxItem, run_name, resistance_first + " " + resistance_first_scale[1], resistance_second + " " + resistance_second_scale[1], resistance_third + " " + resistance_third_scale[1], self.sweep, start, first, second, end, num_step, limit, time, self.probe + "-point"]
        
        for i in range(len(point_data)):
            self.ui.tableWidget_data.setItem(0, i, QTableWidgetItem(point_data[i]))

    def reset_plot_real_time(self):
        self.ui.mplwidget_real_time.figure.clear()
        # Creates the new plot and is defined to self.axes.
        # All one has to do is to create a plot, which is "self.ui.,plwdget_direction.axes" used equivalently
        # to "self.axes" above and a new subplot does not have to be defined, as done below.)
        self.axes_real_time = self.ui.mplwidget_real_time.figure.add_subplot(111)

    def reset_plot_first(self):
        self.ui.mplwidget_first.figure.clear()        
        self.axes_first = self.ui.mplwidget_first.figure.add_subplot(111)

    def reset_plot_second(self):
        self.ui.mplwidget_second.figure.clear()
        self.axes_second = self.ui.mplwidget_second.figure.add_subplot(111)
        
    def reset_plot_third(self):
        self.ui.mplwidget_third.figure.clear()
        self.axes_third = self.ui.mplwidget_third.figure.add_subplot(111)

    def reset_plot_allplot(self):
        self.ui.mplwidget_allplot.figure.clear()
        self.axes_allplot = self.ui.mplwidget_allplot.figure.add_subplot(111)
        
    def __del__(self):
        self.exiting = True
        self.wait()
        


# The if statement is to check whether this module is the main module and in case that it is imported by another module
# If it is the main module then it starts the GUI under if condition
# This in case it is being imported, then it will not immediately start the GUI upon being imported
if __name__ == "__main__":
    # Opens the GUI
    app = QApplication(sys.argv)
    myapp = MyForm()

    # Shows the GUI
    myapp.show()

    # Exits the GUI when the x button is clicked
    sys.exit(app.exec_())
        
        

        
