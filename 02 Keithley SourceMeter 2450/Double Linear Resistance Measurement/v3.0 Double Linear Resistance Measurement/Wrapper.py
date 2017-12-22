"""Written by Bruce Wang.
    Inspired and helped by Johnathon Vannucci.
    Contact wdmzcjwq@gmail.com if you have any questions"""

"""To compile the .ui file into .py file, it is very simple. Do the following stpes:
   1. Open Command Proment (Terminal if you are using mac), using 'cd' to get the directory that contains the .ui file
   2. Type "pyuic4 -x filename.ui -o filename.py"
   3. If nothing strange happens, it means a .py file is successfully created in the same directory contains your original .ui file
   4. Do not change any of the code in the .py file because recomling any new changes in the .ui file will delete your changes"""

# Import os library
import os

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

from Sub_Scripts.Sweep import voltage_sweep, current_sweep
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
        self.canvas_left = FigureCanvas(self.ui.mplwidget_left.figure)
        self.canvas_left.setParent(self.ui.widget_left)
        # Here is the toolbar widget for the left canvas
        self.mpl_toolbar_left = NavigationToolbar(self.canvas_left, self.ui.widget_left)

        # This is for the middle canvas
        # The independent variable of this plot is ascending
        self.canvas_middle = FigureCanvas(self.ui.mplwidget_middle.figure)
        self.canvas_middle.setParent(self.ui.widget_middle)
        # Here is the toolbar widget for the middle canvas
        self.mpl_toolbar_middle = NavigationToolbar(self.canvas_middle, self.ui.widget_middle)

        # This is for the right canvas
        # The independent variable of this plot is descending
        self.canvas_right = FigureCanvas(self.ui.mplwidget_right.figure)
        self.canvas_right.setParent(self.ui.widget_right)
        # Here is the toolbar widget for the right canvas
        self.mpl_toolbar_right = NavigationToolbar(self.canvas_right, self.ui.widget_right)


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
        vbox_left = QVBoxLayout()
        # The matplotlib canvas
        vbox_left.addWidget(self.canvas_left)
        # The matplotlib toolbar
        vbox_left.addWidget(self.mpl_toolbar_left)
        self.ui.widget_left.setLayout(vbox_left)

        # This is for the middle canvas
        vbox_middle = QVBoxLayout()
        # The matplotlib canvas
        vbox_middle.addWidget(self.canvas_middle)
        # The matplotlib toolbar
        vbox_middle.addWidget(self.mpl_toolbar_middle)
        self.ui.widget_middle.setLayout(vbox_middle)

        # This is for the right canvas
        vbox_right = QVBoxLayout()
        # The matplotlib canvas
        vbox_right.addWidget(self.canvas_right)
        # The matplotlib toolbar
        vbox_right.addWidget(self.mpl_toolbar_right)
        self.ui.widget_right.setLayout(vbox_right)

        # Connect the mplwidget with canvas
        self.ui.mplwidget_allplot = self.canvas_allplot
        self.ui.mplwidget_time = self.canvas_time
        self.ui.mplwidget_left = self.canvas_left
        self.ui.mplwidget_middle = self.canvas_middle
        self.ui.mplwidget_right = self.canvas_right

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
        
        self.connect(self.ui.radioButton_sweep_voltage, SIGNAL("clicked()"), lambda : self.ui.tabWidget.setCurrentIndex(0))
        self.connect(self.ui.radioButton_sweep_current, SIGNAL("clicked()"), lambda : self.ui.tabWidget.setCurrentIndex(1))
        self.connect(self.ui.radioButton_Custom_Name, SIGNAL('clicked()'), self.enable_custom_name)
        self.connect(self.ui.radioButton_Timename, SIGNAL('clicked()'), self.disable_custom_name)
        self.connect(self.ui.radioButton_sweep_voltage, SIGNAL("clicked()"), self.voltageSweep)
        self.connect(self.ui.radioButton_sweep_current, SIGNAL("clicked()"), self.currentSweep)
        self.connect(self.ui.radioButton_software, SIGNAL('clicked()'), self.software_stepping)
        self.connect(self.ui.radioButton_hardware, SIGNAL('clicked()'), self.hardware_stepping)

        self.connect(self.collect_data_thread, SIGNAL('Data'), self.set_data)
        
    def set_data(self, return_data):
        # voltage_values, current_values, resistance_a, resistance_d, scaled_best_fit_ascending, scaled_best_fit_descending, voltage_scale, current_scale, resistance_a_scale, resistance_d_scale, time, length_ascending
        self.data = return_data
        self.voltage_values = return_data[0]
        self.current_values = return_data[1]
        self.resistance_a = return_data[2]
        self.resistance_d = return_data[3]
        self.voltage_scale = return_data[6]
        self.current_scale = return_data[7]
        self.voltage_values = self.voltage_values / self.voltage_scale[0]
        self.current_values = self.current_values / self.current_scale[0]
        self.resistance_a_scale = return_data[8]
        self.resistance_d_scale = return_data[9]
        self.time_length = return_data[10]
        self.time_step = self.time_length / len(self.voltage_values)
        self.Time = []
        for i in range(0, len(self.voltage_values)):
            self.Time.append(i * self.time_step)
        self.length_ascending = return_data[11]
        self.ascending_Time = self.Time[:self.length_ascending]
        self.ascending_voltage = self.voltage_values[:self.length_ascending]
        self.ascending_current = self.current_values[:self.length_ascending]
        self.descending_Time = self.Time[self.length_ascending:]
        self.descending_voltage = self.voltage_values[self.length_ascending:]
        self.descending_current = self.current_values[self.length_ascending:]
        
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
            print self.visa_name
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
        #Reset plots
        self.reset_plot_time()
        self.ui.lineEdit_condition.setText("Collecting data...")
        self.ui.pushButton_Stop.setEnabled(True)
        self.ui.pushButton_run.setEnabled(False)
        if self.ui.radioButton_sweep_voltage.isChecked():
            self.VoltageSweep()
            self.Sweep = 'Voltage'
        elif self.ui.radioButton_sweep_current.isChecked():
            self.CurrentSweep()
            self.Sweep = 'Current'
            
        self.ui.tabWidget_2.setEnabled(True)
        self.ui.pushButton_reset.setEnabled(True)

    # If the user wants to stop the measurement during the process, just click the checkbox
    # And this is to judge whether the checkbox is checked
    def software_stepping(self):
        self.ui.groupBox_stop_continue.setEnabled(True)
        self.ui.pushButton_Stop.setEnabled(False)
        self.ui.pushButton_Continue.setEnabled(False)
        self.ui.groupBox_source.setEnabled(True)
        
    def hardware_stepping(self):
        self.ui.groupBox_stop_continue.setEnabled(False)
        self.ui.groupBox_source.setEnabled(False)
        
    def VoltageSweep(self):
        # Collect parameters from the interface
        start_voltage = float(self.ui.lineEdit_start_voltage.text())/1000
        top_voltage = float(self.ui.lineEdit_top_voltage.text())/1000
        end_voltage = float(self.ui.lineEdit_end_voltage.text())/1000
        num_steps = int(self.ui.lineEdit_time_steps_v.text())

        sweep = 'VOLTAGE'
        
        # For the voltage and current limit
        if abs(start_voltage) > abs(top_voltage) and abs(start_voltage) > abs(top_voltage):
            voltage_lim = (1.01) * abs(start_voltage)
        elif abs(top_voltage) > abs(start_voltage) and abs(top_voltage) > abs(top_voltage):
            voltage_lim = (1.01) * abs(top_voltage)
        else:
            voltage_lim = (1.01) * abs(top_voltage)
        current_lim = float(self.ui.lineEdit_current_limit.text())/1E3

        # Other important parameters
        wait_time = float(self.ui.lineEdit_voltage_time_measurements.text())
        voltage_steps = (2 * top_voltage - start_voltage - end_voltage) / (num_steps - 1)
        voltage_ascending = numpy.arange(start_voltage, top_voltage + voltage_steps, voltage_steps, dtype = 'float')
        voltage_descending = numpy.arange(top_voltage, end_voltage, - voltage_steps, dtype = 'float')
        Voltage = numpy.append(voltage_ascending, voltage_descending)
        
        if self.ui.radioButton_2_point.isChecked():
            probe = '2'
            self.Probe = '2'
        elif self.ui.radioButton_4_point.isChecked():
            probe = '4'
            self.Probe = '4'

        self.collect_data_thread.input(self.visa_chosen, Voltage, voltage_ascending,
                                       voltage_lim, current_lim, wait_time, self.ui, sweep, probe)

    def CurrentSweep(self):
        # Collect parameters from the interface
        start_current = float(self.ui.lineEdit_start_current.text())/1E6
        top_current = float(self.ui.lineEdit_top_current.text())/1E6
        end_current = float(self.ui.lineEdit_end_current.text())/1E6
        num_steps = int(self.ui.lineEdit_time_steps_c.text())

        sweep = 'CURRENT'
        
        if abs(start_current) > abs(top_current) and abs(start_current) > abs(end_current):
            current_lim = (1.01) * abs(start_current)
        elif abs(top_current) > abs(start_current) and abs(top_current) > abs(end_current):
            current_lim = (1.01) * abs(middle_current)
        else:
            current_lim = (1.01) * abs(end_current)
        voltage_lim = float(self.ui.lineEdit_voltage_limit.text())/1E3

        # Other important parameters
        wait_time = float(self.ui.lineEdit_current_time_measurements.text())
        current_steps = (2 * top_current - start_current - end_current) / (num_steps - 1)
        current_ascending = numpy.arange(start_current, top_current + current_steps, current_steps, dtype = 'float')
        current_descending = numpy.arange(top_current, end_current, - current_steps, dtype = 'float')
        Current = numpy.append(current_ascending, current_descending)
        
        if self.ui.radioButton_2_point.isChecked():
            probe = '2'
            self.Probe = '2'
        elif self.ui.radioButton_4_point.isChecked():
            probe = '4'
            self.Probe = '4'

        self.collect_data_thread.input(self.visa_chosen, Current, current_ascending,
                                       current_lim, voltage_lim, wait_time, self.ui, sweep, probe)

    def reset_plot_time(self):
        self.ui.mplwidget_time.figure.clear()

        # Creates the new plot and is defined to self.axes.
        # All one has to do is to create a plot, which is "self.ui.,plwdget_direction.axes" used equivalently
        # to "self.axes" above and a new subplot does not have to be defined, as done below.)
        #self.axes_left = self.ui.mplwidget_left.figure.add_subplot(111)
        #self.axes_middle = self.ui.mplwidget_middle.figure.add_subplot(111)
        self.axes_time = self.ui.mplwidget_time.figure.add_subplot(111)

    def preview(self):
        Time = []
        Values = []
        
        if self.ui.radioButton_sweep_voltage.isChecked():
            start_voltage = float(self.ui.lineEdit_start_voltage.text())
            top_voltage = float(self.ui.lineEdit_top_voltage.text())
            end_voltage = float(self.ui.lineEdit_end_voltage.text())
            num_steps = int(self.ui.lineEdit_time_steps_v.text())
            wait_time = float(self.ui.lineEdit_voltage_time_measurements.text()) * 1E3
            voltage_steps = (2 * top_voltage - start_voltage - end_voltage) / (num_steps - 1)
            voltage_ascending = numpy.arange(start_voltage, top_voltage + voltage_steps, voltage_steps, dtype = 'float')
            voltage_descending = numpy.arange(top_voltage, end_voltage, - voltage_steps, dtype = 'float')
            Voltage = numpy.append(voltage_ascending, voltage_descending)

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
            top_current = float(self.ui.lineEdit_top_current.text())
            end_current = float(self.ui.lineEdit_end_current.text())
            num_steps = int(self.ui.lineEdit_time_steps_c.text())
            wait_time = float(self.ui.lineEdit_current_time_measurements.text()) * 1E3
            current_steps = (2 * top_current - start_current - end_current) / (num_steps - 1)
            current_ascending = numpy.arange(start_current, top_current + current_steps, current_steps, dtype = 'float')
            current_descending = numpy.arange(top_current, end_current, -current_steps, dtype = 'float')
            Current = numpy.append(current_ascending, current_descending)

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
        self.onedrive_directory = str(self.ui.lineEdit_OneDrive.text())
        self.namefolder = str(self.ui.comboBox_Name_Folder.currentText())
        if self.namefolder == 'None':
            self.ui.lineEdit_condition.setText('Please choose a name folder to save.')
        else:
            self.date = '%s-%s-%s' % (now.year, now.month, now.day)
            self.ui.lineEdit_condition.setText("Save file to OneDrive\\" + self.namefolder + "\Date" + '\\' + self.date)
            self.ui.groupBox_File_Type.setEnabled(True)
            self.ui.groupBox_Filename.setEnabled(True)
            
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
        variables = ["Select", "Run", "Resistance (Ascending)", "Resistance (Descending)", "Sweep", "Start", "Top", "End", "Num Steps", "Limit", "Time Step", "Probe Type"]
        for i in range(len(variables)):
            self.ui.tableWidget_data.insertColumn(0)
        #self.ui.tableWidgetSPreviousBounds.insertRow(0)
        self.ui.tableWidget_data.setHorizontalHeaderLabels(variables)
        #self.PreviousBounds = []
        #self.previousBounds_num = 0
    
    def open(self):
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
            self.ui.lineEdit_condition.setText('Please enter a valid file name')
        else:
            self.path = self.onedrive_directory + '\\' + self.namefolder + '\\' + 'Data' + '\\' + self.date + '\\' + 'Keithley for Resistance'
            # Create a folder at this address
            if not os.path.isdir(self.path):
                os.makedirs(self.path)
            # This the name of the file
            self.name = self.onedrive_directory + '\\' + self.namefolder + '\\' + 'Data' + '\\' + self.date + '\\' + 'Keithley for Resistance' + '\\' + self.file_name + self.type
            
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
                f.write('Top Voltage' + self.divide + str(self.ui.lineEdit_top_voltage.text()) + self.divide + 'mV' + '\n')
                f.write('End Voltage' + self.divide + str(self.ui.lineEdit_end_voltage.text()) + self.divide + 'mV' + '\n')
                f.write('Steps Number' + self.divide + str(self.ui.lineEdit_time_steps_v.text()) + self.divide + '\n')
                f.write('Current Limit' + self.divide + str(self.ui.lineEdit_current_limit.text()) + self.divide + 'uA' + '\n')
                f.write('Time Step' + self.divide + str(self.ui.lineEdit_voltage_time_measurements.text()) + self.divide + 's' + '\n')
                f.write('Resistance with Ascending Voltage' + self.divide + str(self.resistance_a) + self.divide + self.resistance_a_scale[1] + '\n')
                f.write('Resistance with Descending Voltage' + self.divide + str(self.resistance_d) + self.divide + self.resistance_d_scale[1] + '\n')
                
                f.write('\n')
                f.write('Collected data' + '\n')
                f.write('Time' + self.divide + 'Voltage' + self.divide + 'Current' + self.divide + 'Ascending Time' + self.divide + 'Ascending Voltage' + self.divide +
                        'Current' + self.divide + 'Descending Time' + self.divide + 'Descending Voltage' + self.divide + 'Current' + '\n')
                f.write('s' + self.divide + 'Volts' + self.divide + 'Amps' + self.divide + 's' + self.divide + 'Volts' + self.divide + 'Amps' +self.divide + 's' +self.divide + 'Volts' +
                        self.divide + 'Amps' + '\n')
                for i in range(0, len(self.Time)):
                    full_data = str(self.Time[i]) + self.divide + str(self.voltage_values[i]) + self.divide + str(self.current_values[i])
                    try:
                        up_data = str(self.ascending_Time[i]) + self.divide + str(self.ascending_voltage[i]) + self.divide + str(self.ascending_current[i])
                    except:
                        up_data = '' + self.divide + '' + self.divide + ''
                    try:
                        down_data = str(self.descending_Time[i]) + self.divide + str(self.descending_voltage[i]) + self.divide + str(self.descending_current[i])
                    except:
                        down_data = '' + self.divide + '' + self.divide + ''
                    full_string = full_data + self.divide + up_data + self.divide + down_data + '\n'
                    f.write(full_string)
                
                
            else:
                f.write('Start Current' + self.divide + str(self.ui.lineEdit_start_current.text()) + self.divide + 'uA' + '\n')
                f.write('Top Current' + self.divide + str(self.ui.lineEdit_top_current.text()) + self.divide + 'uA' + '\n')
                f.write('End Current' + self.divide + str(self.ui.lineEdit_end_current.text()) + self.divide + 'uA' + '\n')
                f.write('Steps Number' + self.divide + str(self.ui.lineEdit_time_steps_v.text()) + self.divide + '\n')
                f.write('Voltage Limit' + self.divide + str(self.ui.lineEdit_voltage_limit.text()) + self.divide + 'mV' + '\n')
                f.write('Time Step' + self.divide + str(self.ui.lineEdit_current_time_measurements.text()) + self.divide + 's' + '\n')
                f.write('Resistance with Ascending Current' + self.divide + str(self.resistance_a) + self.divide + str(self.resistance_a_scale[1]) + '\n')
                f.write('Resistance with Descending Current' + self.divide + str(self.resistance_d) + self.divide + str(self.resistance_d_scale[1]) + '\n')
                
                f.write('\n')
                f.write('Collected data' + '\n')
                f.write('Time' + self.divide + 'Current' + self.divide + 'Voltage' + self.divide + 'Ascending Time' + self.divide + 'Ascending Current' + self.divide +
                        'Voltage' + self.divide + 'Descending Time' + self.divide + 'Descending Current' + self.divide + 'Voltage' + '\n')
                f.write('s' + self.divide + 'Amps' + self.divide + 'Volts' + self.divide + 's' + self.divide + 'Amps' + self.divide + 'Volts' + self.divide + 's' + self.divide + 'Amps' +
                        self.divide + 'Volts' + '\n')
                for i in range(0, len(self.Time)):
                    full_data = str(self.Time[i]) + self.divide + str(self.current_values[i]) + self.divide + str(self.voltage_values[i])
                    try:
                        up_data = str(self.ascending_Time[i]) + self.divide + str(self.ascending_current[i]) + self.divide + str(self.ascending_voltage[i])
                    except:
                        up_data = '' + self.divide + '' + self.divide + ''
                    try:
                        down_data = str(self.descending_Time[i]) + self.divide + str(self.descending_current[i]) + self.divide + str(self.descending_voltage[i])
                    except:
                        down_data = '' + self.divide + '' + self.divide + ''
                    full_string = full_data + self.divide + up_data + self.divide + down_data + '\n'
                    f.write(full_string)
    
            
        f.close()
        self.ui.lineEdit_condition.setText("Your file has been successfully saved.")
        self.ui.pushButton_Open.setEnabled(True)
            
     
    def closeEvent(self, event):
        # Creates a message box that displays the quit_msg
        quit_msg = "Do you want to quit the program?"

        # with two pushButtons -- 'Yes' or 'No'
        reply = QMessageBox.question(self, 'Message', quit_msg,
                                     QMessageBox.Yes, QMessageBox.No)

        # Yes means the user wants to quit. Thus the window is closed.
        if reply == QMessageBox.Yes:
            try:
                self.visa_chosen.close()
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

    def input(self, inst, sweep_array, sweep_array_ascending, sweep_lim, read_lim, wait_time, ui, sweep, probe):
        self.inst  = inst
        self.sweep_array = sweep_array
        self.sweep_array_ascending = sweep_array_ascending
        self.sweep_lim = sweep_lim
        self.read_lim = read_lim
        self.wait_time = wait_time
        self.ui = ui
        self.sweep = sweep
        self.probe = probe
        # self.run()
        self.start()

    def stop_continue(self):
        self.sweep_stop.continue_check = False

    def start_continue(self):
        self.sweep_stop.continue_check = True
            
    def run(self):
        self.reset_plot_left()
        self.reset_plot_middle()
        self.reset_plot_right()
        self.reset_plot_allplot()
        if self.sweep == "VOLTAGE":
            if self.ui.radioButton_hardware.isChecked():
                voltage_values, current_values, resistance_a, resistance_d, scaled_best_fit_ascending, scaled_best_fit_descending, voltage_scale, current_scale, resistance_a_scale, resistance_d_scale, time, length_ascending = voltage_sweep(self.inst, self.sweep_array, self.sweep_array_ascending, self.sweep_lim, self.read_lim, self.wait_time, self.probe)
                
                self.reset_plot_allplot()
                self.axes_allplot.plot(voltage_values, current_values, marker = '.', linestyle = '')
                self.axes_allplot.set_title('\n'.join(wrap('Voltage vs. Current with All Points')))
                self.axes_allplot.set_xlabel('Voltage (' + voltage_scale[1] + ')')
                self.axes_allplot.set_ylabel('Current (' + current_scale[1] + ')')
                self.ui.mplwidget_allplot.draw()
            else:
                self.sweep_stop = Sweep.sweep_stop()
                voltage_values, current_values, resistance_a, resistance_d, scaled_best_fit_ascending, scaled_best_fit_descending, voltage_scale, current_scale, resistance_a_scale, resistance_d_scale, time, length_ascending = self.sweep_stop.voltage_sweep_stop(self.inst, self.sweep_array, self.sweep_array_ascending, self.sweep_lim, self.read_lim, self.wait_time, self.probe, self.ui)

            self.ui.lineEdit_best_fit_resistance.setText(str(round(resistance_a, 4)))
            self.ui.label_resistance_unit.setText(resistance_a_scale[1])
            self.ui.lineEdit_best_fit_resistance_descending.setText(str(round(resistance_d, 4)))
            self.ui.label_resistance_unit_descending.setText(resistance_d_scale[1])
            
            # Add the data table into the TableWidget
            self.addTable(str(round(resistance_a, 4)), resistance_a_scale, str(round(resistance_d, 4)), resistance_d_scale)
            
            # Plot the ascending figure
            best_fit_line_ascending = scaled_best_fit_ascending[0] * numpy.array(voltage_values[:length_ascending], dtype = 'float') + scaled_best_fit_ascending[1]
            
            
            self.reset_plot_middle()
            self.axes_middle.plot(voltage_values[:length_ascending], current_values[:length_ascending], marker = '.', linestyle = '')
            self.axes_middle.plot(voltage_values[:length_ascending], best_fit_line_ascending)
            self.axes_middle.set_title('\n'.join(wrap('Voltage vs. Current with ascending voltage')))
            self.axes_middle.set_xlabel('Voltage (' + voltage_scale[1] + ')')
            self.axes_middle.set_ylabel('Current (' + current_scale[1] + ')')
            self.ui.mplwidget_middle.draw()
            
            # Plot the descending figure
            best_fit_line_descending = scaled_best_fit_descending[0] * numpy.array(voltage_values[length_ascending:], dtype = 'float') + scaled_best_fit_descending[1]
            
            self.reset_plot_right()
            self.axes_right.plot(voltage_values[length_ascending:], current_values[length_ascending:], marker = '.', linestyle = '')
            self.axes_right.plot(voltage_values[length_ascending:], best_fit_line_descending)
            self.axes_right.set_title('\n'.join(wrap('Voltage vs. Current with descending voltage' )))
            self.axes_right.set_xlabel('Voltage (' + voltage_scale[1] + ')')
            self.axes_right.set_ylabel('Current (' + current_scale[1] + ')')
            self.ui.mplwidget_right.draw()

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
            self.reset_plot_left()
            self.axes_left.plot(time_value, voltage_values_double)
            self.axes_left.set_title('\n'.join(wrap('Voltage vs.Real Time')))
            self.axes_left.set_xlabel('Time (s)')
            self.axes_left.set_ylabel('Voltage (' + voltage_scale[1] + ')')
            self.ui.mplwidget_left.draw()
            
            return_data = [voltage_values, current_values, resistance_a, resistance_d, scaled_best_fit_ascending, scaled_best_fit_descending, voltage_scale, current_scale, resistance_a_scale, resistance_d_scale, time, length_ascending]
            
        elif self.sweep == "CURRENT":
            if self.ui.radioButton_hardware.isChecked():
                voltage_values, current_values, resistance_a, resistance_d, scaled_best_fit_ascending, scaled_best_fit_descending, voltage_scale, current_scale, resistance_a_scale, resistance_d_scale, time, length_ascending = current_sweep(self.inst, self.sweep_array, self.sweep_array_ascending, self.sweep_lim, self.read_lim, self.wait_time, self.probe)
            
                self.reset_plot_allplot()
                self.axes_allplot.plot(current_values, voltage_values, marker = '.', linestyle = '')
                self.axes_allplot.set_title('\n'.join(wrap('Current vs. Voltage with All Points')))
                self.axes_allplot.set_xlabel('Current (' + current_scale[1] + ')')
                self.axes_allplot.set_ylabel('Voltage (' + voltage_scale[1] + ')')
                self.ui.mplwidget_allplot.draw()
                
            else:
                self.sweep_stop = Sweep.sweep_stop()
                voltage_values, current_values, resistance_a, resistance_d, scaled_best_fit_ascending, scaled_best_fit_descending, voltage_scale, current_scale, resistance_a_scale, resistance_d_scale, time, length_ascending = self.sweep_stop.current_sweep_stop(self.inst, self.sweep_array, self.sweep_array_ascending, self.sweep_lim, self.read_lim, self.wait_time, self.probe, self.ui)

            self.ui.lineEdit_best_fit_resistance.setText(str(round(resistance_a, 4)))
            self.ui.label_resistance_unit.setText(resistance_a_scale[1])
            self.ui.lineEdit_best_fit_resistance_descending.setText(str(round(resistance_d, 4)))
            self.ui.label_resistance_unit_descending.setText(resistance_d_scale[1])
            
            # Add data into the Data Widget
            self.addTable(str(round(resistance_a, 4)), resistance_a_scale, str(round(resistance_d, 4)), resistance_d_scale)
            # Plot the ascending figure
            best_fit_line_ascending = scaled_best_fit_ascending[0] * numpy.array(current_values[:length_ascending], dtype = 'float') + scaled_best_fit_ascending[1]
            
            self.reset_plot_middle()
            self.axes_middle.plot(current_values[0:length_ascending], voltage_values[0:length_ascending], marker = '.', linestyle = '')
            self.axes_middle.plot(current_values[0:length_ascending], best_fit_line_ascending)
            self.axes_middle.set_title('\n'.join(wrap('Current vs. Voltage with ascending current')))
            self.axes_middle.set_xlabel('Current (' + current_scale[1] + ')')
            self.axes_middle.set_ylabel('Voltage (' + voltage_scale[1] + ')')
            self.ui.mplwidget_middle.draw()
            
            # Plot the descending figure
            best_fit_line_descending = scaled_best_fit_descending[0] * numpy.array(current_values[length_ascending:], dtype = 'float') + scaled_best_fit_descending[1]
            
            self.reset_plot_right()
            self.axes_right.plot(current_values[length_ascending:], voltage_values[length_ascending:], marker = '.', linestyle = '')
            self.axes_right.plot(current_values[length_ascending:], best_fit_line_descending)
            self.axes_right.set_title('\n'.join(wrap('Current vs. Voltage with descending current')))
            self.axes_right.set_xlabel('Current (' + current_scale[1] + ')')
            self.axes_right.set_ylabel('Voltage (' + voltage_scale[1] + ')')
            self.ui.mplwidget_right.draw()

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
            self.reset_plot_left()
            self.axes_left.plot(time_value, current_values_double)
            self.axes_left.set_title('\n'.join(wrap('Current vs.Time')))
            self.axes_left.set_ylabel('Current (' + current_scale[1] + ')')
            self.axes_left.set_xlabel('Time (s)')
            self.ui.mplwidget_left.draw()
        
            return_data = [voltage_values, current_values, resistance_a, resistance_d, scaled_best_fit_ascending, scaled_best_fit_descending, voltage_scale, current_scale, resistance_a_scale, resistance_d_scale, time, length_ascending]
        
        self.ui.lineEdit_condition.setText("Data plotting successfully!")
        self.ui.groupBox_save.setEnabled(True)
        
        self.emit(SIGNAL("Data"), return_data)
    
    def addTable(self, resistance_a, resistance_a_scale, resistance_d, resistance_d_scale):
        
        self.ui.tableWidget_data.insertRow(0)
        checkBoxItem = QTableWidgetItem('')
        checkBoxItem.setFlags(Qt.ItemIsUserCheckable |
                                      Qt.ItemIsEnabled)
        checkBoxItem.setCheckState(Qt.Unchecked)
        
        run_name = str(self.ui.lineEdit_run_name.text())
        if self.sweep == "VOLTAGE":
            start = str(self.ui.lineEdit_start_voltage.text()) + " mV"
            top = str(self.ui.lineEdit_top_voltage.text()) + " mV"
            end = str(self.ui.lineEdit_end_voltage.text()) + " mV"
            num_step = str(self.ui.lineEdit_time_steps_v.text())
            limit = str(self.ui.lineEdit_current_limit.text()) + " mA"
            time = str(self.ui.lineEdit_voltage_time_measurements.text()) + " s"
        elif self.sweep == "CURRENT":
            start = str(self.ui.lineEdit_start_current.text()) + " uA"
            top = str(self.ui.lineEdit_top_current.text()) + " uA"
            end = str(self.ui.lineEdit_end_current.text()) + " uA"
            num_step = str(self.ui.lineEdit_time_steps_c.text())
            limit = str(self.ui.lineEdit_voltage_limit.text()) + " mV"
            time = str(self.ui.lineEdit_current_time_measurements.text()) + " s"
        
        point_data = [checkBoxItem, run_name, resistance_a + " " + resistance_a_scale[1], resistance_d + " " + resistance_d_scale[1], self.sweep, start, top, end, num_step, limit, time, self.probe + "-point"]
        
        for i in range(len(point_data)):
            self.ui.tableWidget_data.setItem(0, i, QTableWidgetItem(point_data[i]))

    def reset_plot_left(self):
        self.ui.mplwidget_left.figure.clear()
        # Creates the new plot and is defined to self.axes.
        # All one has to do is to create a plot, which is "self.ui.,plwdget_direction.axes" used equivalently
        # to "self.axes" above and a new subplot does not have to be defined, as done below.)
        self.axes_left = self.ui.mplwidget_left.figure.add_subplot(111)

    def reset_plot_middle(self):
        self.ui.mplwidget_middle.figure.clear()        
        self.axes_middle = self.ui.mplwidget_middle.figure.add_subplot(111)

    def reset_plot_right(self):
        self.ui.mplwidget_right.figure.clear()
        self.axes_right = self.ui.mplwidget_right.figure.add_subplot(111)

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
        
        

        
