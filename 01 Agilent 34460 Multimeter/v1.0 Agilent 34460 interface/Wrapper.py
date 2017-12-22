"""Written by Bruce Wang.
    Inspired by Johnason Vannucci.
    Contact wdmzcjwq@gmail.com if you have any questions"""

"""To compile the .ui file into .py file, it is very simple. Do the following stpes:
   1. Open Command Proment (Terminal if you are using mac), using 'cd' to get the directory that contains the .ui file
   2. Type "pyuic4 -x filename.ui -o filename.py"
   3. If nothing strange happens, it means a .py file is successfully created in the same directory contains your original .ui file
   4. Do not change any of the code in the .py file because recomling any new changes in the .ui file will delete your changes"""

# Import the visa library
try:
    import visa
    Visa_available = True
    rm = visa.ResourceManager()
    rm.list_resources()
except:
    Visa_available = False

# Import datetime
from datetime import datetime

# Import os library
import os

# Import numpy library
import numpy as np

# Import system library
import sys

# Import the time library
import time

# Import the string library
import string

# Import the PyQt4 modules for all the commands that control the GUI.
# Importing as from "Module" import * implies that everything from that module is not part of this module.
# You do not need to put the module name before its commands
from PyQt4.QtCore import *
from PyQt4.QtGui import *

# This is very important because it imports the GUI created earlier using Qt Designer
# To import the GUI from another python file, it is very simple. Just following the following steps:
# 1. Create a empyty file called __init__.py in the same directory as the GUI file
# 2. If the GUI file and __init__.py file are in the same directory as this file, just type "from .GUIfilename import classname"
# 3. If the GUI file and __init__.py file are in the sub file of this file, then type "from subfilename.GUIfilename import classname"
# classname is the name of the class in the GUI file, usually it should be 'Ui_MainWindow'
from Sub_Scripts.GUI import Ui_MainWindow

# These are the modules required for the guiqwt widgets.
# If you do not understand their meaning. You do not have to.
from guiqwt.pyplot import *
from guiqwt.plot import CurveWidget
from guiqwt.builder import make


# This class controls all the operations of the GUI. This is the main class that contains all the functions that control the GUI.
class MyForm(QMainWindow):

    # The __init__ function is what everything the user wants to be initialized when the class is called.
    # Here we shall define the tring functions to corresponding variables.
    # The 'self' variable means that the function is part of the class and can be called inside and outside the class.
    def __init__(self, parent = None):

        # Standard GUI code
        QWidget.__init__(self, parent)

        # All the GUI data and widgets in the Ui_MainWindow() class is defined to "self.ui"
        # Thus to do anything on the GUI, the commands must go through this variable
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # When you open the window, the visas get refreshed
        self.refresh_visa()

        # This is to check whether user click start before they save
        self.data_check = False
        
        # We set up a QTimer variable called collect_timer.
        # It runs as a countdown clock that runs in the background and emits a timeout signal when it reaches 0.
        # Because this variable, we do not to use a for loop function for collecting and timing since the for loop can not be stopped in progress and can cause program frozen.
        # Also it allows the rest of the commands to run normally
        self.collect_timer = QTimer()

        # Set up guiqwt plot
        self.curve_item = make.curve([], [], color = 'r')
        self.ui.curvewidgetPlot.plot.add_item(self.curve_item)
        self.ui.curvewidgetPlot.plot.set_antialiasing(True)
        self.ui.curvewidgetPlot.plot.set_titles("Agilent 34460A Digit Multimeter", "Time (s)", "Y-Axis")

        # The following connects the signals sent from an action on the GUI to a function that does something
        # When the button is clicked, it does the corresponding function
        self.connect(self.ui.pushButton_Select_Visa, SIGNAL("clicked()"), self.choose_visa)
        self.connect(self.ui.pushButton_Start, SIGNAL("clicked()"), self.start)
        self.connect(self.ui.pushButton_Stop, SIGNAL("clicked()"), self.stop)
        self.connect(self.ui.pushButton_Refresh, SIGNAL("clicked()"), self.refresh_visa)

        # This works as a clock running in the background, different functions can use this clock at the same time
        # It is better than .sleep() function because during the sleep time, the whole program is frozen and cannot do anything else
        # Everytime collect_timer gets the time_step, it sends a "timeout()" signal to the device and runs the collect function
        self.connect(self.collect_timer, SIGNAL("timeout()"), self.collect)        

        self.connect(self.ui.comboBox_Meas_Type, SIGNAL("clicked()"), self.meas_type)
                                                         
        # To give a click signal to the checkBox
        self.connect(self.ui.checkBox_Continue, SIGNAL("clicked()"), self.continue_check)

        # I add a slect button for the measurement type
        # Only if you click the button, the computer knows your measurement type
        # It shows the current measurement type and warning at the same time
        self.connect(self.ui.pushButton_Select_Measurement, SIGNAL("clicked()"), self.choose_meas)

        # To save the data
        self.connect(self.ui.pushButton_Save, SIGNAL("clicked()"), self.save)

        # To see and change the directory
        self.connect(self.ui.pushButton_Browse, SIGNAL("clicked()"), self.browse)

        # To choose a name folder to save file
        self.connect(self.ui.pushButton_Select_Directory, SIGNAL("clicked()"), self.select_directory)

        # To select name for the file, date and time or custom name entered by the user
        self.connect(self.ui.radioButton_Timename, SIGNAL("clicked()"), self.select_name)
        self.connect(self.ui.radioButton_Custom_Name, SIGNAL("clicked()"), self.select_name)

        # To select a file type, either .csv or .txt
        self.connect(self.ui.radioButton_csv, SIGNAL('clicked()'), self.select_type)
        self.connect(self.ui.radioButton_csv, SIGNAL('clicked()'), self.select_type)

    def refresh_visa(self):
        # Put all the visa resources into all_visas
        # If there is no visa resource at all, an error is returned. So this helps to prevent this kind of situation
        rm = visa.ResourceManager()
        try:
            # put the visa resources into a list
            all_visas = rm.list_resources()
        except:
            # return "No visas available" if there is no visa
            all_visas = 'No visa available right now.'

        # Remove the previous results in the comboBox        
        self.ui.comboBox_All_Visas.clear()
        # Show all the visas in the combox
        for item in all_visas:
            self.ui.comboBox_All_Visas.addItem(item)

    # Click select button and choose the visa you want
    def choose_visa(self):
        self.visa_address = str(self.ui.comboBox_All_Visas.currentText())
        rm = visa.ResourceManager()
        rm.list_resources()
        dmm = rm.open_resource(self.visa_address)
        valid = self.check_visa(dmm)
        if valid == True:
            self.ui.lineEdit_Error.setText("Everything goes well right now.")
            self.ui.label_CurrentVisa.setText(self.visa_address)
        elif valid == False:
            self.ui.lineEdit_Error.setText("Invalid visa address.")
            self.ui.label_CurrentVisa.setText('None')

    # This one is used to check whether the Agilent is connected correctly
    # It can be frequently used in the beginning of each function because if the Agilent is not linked it would report error when program running.
    def check_visa(self, dmm):
        try:
            dmm.ask('*IDN?')
            valid = True
        except:
            valid = False
        return valid
    
    def set_timestep(self):
        try:
            self.timestep = float(self.ui.lineEdit_Steps.text())
        except:
            self.timestep = -1
        if self.timestep <= 0:
            self.ui.lineEdit_Error.setText("Invalid time step input")

    # This is the number of points you want to collect
    # Also it is the number of points plotted on the figure
    def set_points(self):
        try:
            self.points = int(self.ui.lineEdit_Points.text())
            print self.points
        except:
            self.points = -1
        if self.points <= 0:
            self.ui.lineEdit_Error.setText("Invalid data points input")
            
    # Set two numpy arrays to store data and time
    def init_nparray(self):
        # self.data is used to store the response collected from the device
        self.data = np.array([0], dtype = float)
        # self.time is used to store the time each response is collected
        self.time = np.array([0], dtype = float)

    # To judge whether the checkBox is checked or not
    def continue_check(self):
        # If the checkBox is checked, return true and store it into cont_check
        if self.ui.checkBox_Continue.isChecked() == True:
            self.cont_check = True
        # If the checkBox hasn't been checked, return false and store it into cont_check
        elif self.ui.checkBox_Continue.isChecked() == False:
            self.cont_check = False
        # Return the result
        return self.cont_check

    # To vary from which types of measurements the user want to do
    def meas_type(self):
        self.meas = str(self.ui.comboBox_Meas_Type.currentText())
        self.meas_type_check = True
        self.unit = 'V'
        if self.meas == 'None':
            self.meas_type_check = False
        elif self.meas == 'AC Current':
            self.command = 'MEAS:CURR:AC?'
            self.delay_correct = 0.5143113484
            self.unit = 'A'
        elif self.meas == 'DC Current':
            self.command = 'MEAS:CURR:DC?'
            self.delay_correct = 0.4683864132
            self.unit = 'A'
        elif self.meas == 'AC Voltage':
            self.command = 'MEAS:VOLT:AC?'
            self.delay_correct = 0.7460769785
        elif self.meas == 'DC Voltage':
            self.command = 'MEAS:VOLT:DC?'
            self.delay_correct = 0.3845665093
        elif self.meas == 'Resistance':
            self.unit = 'Ohms'
            self.command = 'MEAS:RES?'

    def choose_meas(self):
        self.meas_type()
        self.ui.label_CurrentMeasurement.setText(self.meas)
        if self.meas == 'AC Current': 
            self.ui.label_Step_Reminder.setText("Please enter a time step larger than 0.6s.")
        elif self.meas == 'DC Current':
            self.ui.label_Step_Reminder.setText("Please enter a time step larger than 0.5s.")
        elif self.meas == 'AC Voltage':
            self.ui.label_Step_Reminder.setText("Please enter a time step larger than 0.8s.")
        elif self.meas == 'DC Voltage':
            self.ui.label_Step_Reminder.setText("Please enter a time step larger than 0.4s.")
        elif self.meas == 'None':
            self.ui.lineEdit_Error.setText("Please choose a valid command")
            
    def start(self):
        self.meas_type()
        # If user does not choose a meas_type
        if self.meas_type_check == False:
            self.ui.lineEdit_Error.setText("Please choose a valid command")
            self.meas_type()
        else:
            start_check = False
            # Collect the time steps entered by the user
            try:
                self.steps = float(self.ui.lineEdit_Steps.text())
            # In case the user type something instead of a number
            except:
                self.steps = -1
            # To judge whether the checkBox is checked or not
            self.continue_check()
            # If the user does not choose the continue measurement mode
            if self.cont_check == False:
                # Collect the points entered by the user in the edit line
                try:
                    self.points = float(self.ui.lineEdit_Points.text())
                # In case the user enters anything strange instead of a number
                except:
                    self.points = -1
            # If the user choose the continue mode, then the points do not matter
            # So set it to be a positive number such as 1
            elif self.cont_check == True:
                self.points = 1

            # Both the time steps and points are invalid
            if self.steps <= 0 and self.points <= 0:
                self.ui.lineEdit_Error.setText("Invalid time steps and points input")
            # Only the time steps are invalid
            elif self.steps <= 0:
                self.ui.lineEdit_Error.setText("Invalid ti  me steps input")
            # Only the points number are invalid
            elif self.points <= 0:
                self.ui.lineEdit_Error.setText("Invalid points input")
            # Both the time steps and points are valid
            else:
                start_check = True

            # This helps to check whther the input time step is in the range
            # If it is smaller than the minimum step, 
            if self.steps < self.delay_correct:
                self.ui.lineEdit_Error.setText("Your time step is too small. Please enter again.")
                start_check = False

            # Set the address of the digit multimeter
            # I do not use self.rm & self.dmm, so I need to put them here before the data collection
            rm = visa.ResourceManager()
            rm.list_resources()
            dmm = rm.open_resource(self.visa_address)
            # Check if everything is ready to start
            if start_check == True:
                valid = self.check_visa(dmm)
                # If the visa address is valid
                if valid == True:
                    self.data_check = True
                    # Tell user there is no error right now
                    self.ui.lineEdit_Error.setText("Everything goes well right now.")
                    self.meas_type()
                    # Set the numpy arrays for time and data
                    self.init_nparray()
                    # To calculate the time difference for system responce, set starting time t1
                    self.t1 = time.clock()
                    # The default time step for collect_timer function is 1ms
                    # So for 1 second, we have to multiply 1000
                    self.collect_timer.start(1000*self.steps)
                    # Run the collect function
                    self.collect()   

    # This is to collect the data from the device
    def collect(self):
        self.meas_type()
        
        self.t2 = time.clock()
        self.t = self.t2 - self.t1
        self.t1 = time.clock()

        self.time_now = self.time[-1] + self.t

        collect_check = True
        rm = visa.ResourceManager()
        rm.list_resources()
        dmm = rm.open_resource(self.visa_address)
        try:
            reading = float(dmm.ask(self.command))
            self.ui.lineEdit_Error.setText("Start to collect data and plot.")
        except:
            collect_check = False
            valid = self.check_visa(self.visa_address)
            if valid == True:
                self.ui.lineEdit_Error.setText("Invalid command syntax.")
            elif valid == False:
                self.ui.lineEdit_Error.setText("Connection disabled")

        # The problem here is that the numpy array is going to append automatically and in the end the length will surplus the number of points we want to plot
        # Therefore we have to make sure the points on the plot is less than or equal to the number we want
        if collect_check == True:
            self.continue_check()
            # If the continue checkBox is checked, run the collect until the user click stop
            self.data = np.append(self.data, reading)
            self.time = np.append(self.time, self.time_now)
            if self.cont_check == True:
                # We do not need the zero point, so we start plot from the first data
                self.x = self.time[1:]
                self.y = self.data[1:]
            elif self.cont_check == False:
                if len(self.time)  > self.points:
                    self.x = self.time[(len(self.time) - self.points):]
                else:
                    self.x = self.time[1:]
                if len(self.data)  > self.points:
                    self.y = self.data[(len(self.data) - self.points):]
                else:
                    self.y = self.data[1:]

            # To adjust the scale of the result
            # You do not want to see E-9 in the y-axis on the plot
            # Take absolute for all the data in the self.data in case some data are negative 
            self.abs_y = np.absolute(self.y)
            # Set the first number in the self.abs_y
            First = self.abs_y[0]
            # Set a specific string for scale
            self.scale = ''
            self.out_y = self.y
            # The scale is E-3
            if First < 1E-1 and First >= 1E-4:
                self.out_y = 1E3*self.y
                self.scale = 'm'
            # The scale is E-6
            elif First < 1E-4 and First >= 1E-7:
                self.out_y = 1E6*self.y
                self.scale = 'u'
            # The scale is E-9
            elif First < 1E-7 and First >= 1E-10:
                self.out_y = 1E9*self.y
                self.scale = 'n'

            # Refresh the lables, especially the scally for yLable
            self.refresh_labels()
            # Sets the data in the guiqwt plot
            self.curve_item.set_data(self.x, self.out_y)
            self.curve_item.plot().replot()    
        else:
            self.stop()

    # Refresh the lables when it starts to plot        
    def refresh_labels(self):
        self.title = "Measure " + self.meas + " by Agilent 34460A Digit Multimeter"
        self.yLabel = self.meas + ' (' + self.scale + self.unit + ')'
        self.ui.curvewidgetPlot.plot.set_titles(self.title, "Time (s)", self.yLabel)
    
    def stop(self):
        self.collect_timer.stop()

    # This function let user to search for the OneDrive folder
    # The lineEdit_OneDrive has already shown the directory of OneDrive in this computer
    # However, the directory maybe different in different computer
    # So if someone use different pc or mac, they can use browse to find the OneDrive folder
    def browse(self):
        # The default OneDrive folder directory
        self.pre_directory = self.ui.lineEdit_OneDrive.text()
        # Open the browse window and let use to choose a new OneDrive directory
        self.directory = QFileDialog.getExistingDirectory(self, 'Select GoogleDrive Directory')
        # If there is a new directory, refresh the default OneDrive directory to this new one
        if self.directory != '':
            # Chang the '/' into '\'
            string.replace(self.directory, '/', '\\')
            # Switch the OneDrive to the new directory
            self.ui.lineEdit_OneDrive.setText(self.directory)

    # This function works to locate the address to the namefolder\Data
    def select_directory(self):
        # The previous directory
        self.pre_directory = str(self.ui.lineEdit_OneDrive.text())
        # The name of the folder you want to save
        self.namefolder = str(self.ui.comboBox_Name_Folder.currentText())
        self.select_directory_check = True
        if self.namefolder == 'None':
            self.ui.lineEdit_Error.setText("Please choose a name folder to save file.")
            self.select_directory_check = False
        else:
            self.ui.lineEdit_Error.setText("Save to GoogleDrive\\" + self.namefolder +"\Data" + '\\' + self.date)

    # Set the file name
    # User can choose whether to save the data by date and time or their custom name
    def select_name(self):
        self.custom_name_check = True
        if self.ui.radioButton_DateTime.isChecked() == True:
            self.now = datetime.now()
            self.date = '%s-%s-%s' % (now.year, now.month, now.day)
            self.current_time = '%s.%s.%s' % (now.hour, now.minute, now.second)
            self.date_and_time = self.date + ' ' + self.current_time 
            self.file_name = str(self.date_and_time)
        else:
            self.custom_name_check = False

    # Let user to choose which type of the file they want to save
    def select_type(self):
        self.select_type_check = True
        if self.ui.radioButton_csv.isChecked() == True:
            self.type = '.csv'
            self.divide = ','
            self.form = ''
        elif self.ui.radioButton_txt.isChecked() == True:
            self.type = '.txt'
            self.divide = '\t'
            self.form = '              '
        else:
            self.select_type_check = False

    # To save the data 
    def save(self):        
        self.select_directory()
        self.select_name()
        self.select_type()
        # Check whether user collect data before they save
        if self.data_check == False:
            self.ui.lineEdit_Error.setText("There is no data to be saved.")
        else:
            # If the user choose to type their own file name, set their input to be the file name
            if self.ui.radioButton_Custom_Name.isChecked() == True:             
                self.custom_name_check = True
                self.file_name = str(self.ui.lineEdit_custom_Name.text())        
            # Check if the user choose one of the name folder to save
            # If they do not choose one, ask them to pick up a name folder
            if self.select_directory_check == False:
                self.ui.lineEdit_Error.setText("Please pick up a name folder to save file.")
            else:
                # If user does not choose any of two radio buttons for the file name, ask them to choose one
                if self.custom_name_check == False:
                    self.ui.lineEdit_Error.setText("Please choose a kind of file name.")
                # If user input nothing in the text line for the custom file name, ask them to fill in a name
                elif self.file_name == '':
                    self.ui.lineEdit_Error.setText("Please enter a valid file name.")
                else:
                    # If user does not choose any of two types of the file, ask them to choose one
                    if self.select_type_check == False:
                        self.ui.lineEdit_Error.setText("Please select a file type to save.")
                    else:
                        self.path = self.pre_directory + '\\' + self.namefolder + '\\' + 'Data' + '\\' + self.date
                        if not os.path.isdir(self.path):
                            os.makedirs(self.path)
                        # Complete the file adddress to OneDrive\NameFolder\Data
                        self.name = self.pre_directory + '\\' + self.namefolder + '\\' + 'Data' + '\\' + self.date + '\\' + self.file_name +  self.type
                        # Open a file
                        f = open(self.name, 'w')
                        # Write the name in the first line
                        f.write('Name: ' + self.namefolder + '\n')
                        # Write the time in the second line
                        f.write('Time: ' + str(datetime.now()) + '\n')
                        # This is all the measurements Agilent can do in this program
                        f.write('#' + self.divide + 'Time (s)' + self.divide + 'AC Current (A)' + self.divide + 'DC Current (A)' + self.divide + 'AC Voltage (V)' + self.divide + 'DC Voltage (V)' + self.divide+ 'Resistance (Ohms)' + '\n')
                        # The number of measurements
                        n = 1
                        for i in range(1, len(self.data)):
                            # self.divide is to divide the different types of data. For .csv file it's ',' while for .txt file it's '\t'
                            # self.form is to make the data looks better
                            if self.meas == 'AC Current':
                                f.write(str(n) + self.divide + str(self.time[i]) + self.divide + str(self.data[i]) + '\n')
                            elif self.meas == 'DC Current':
                                f.write(str(n) + self.divide + str(self.time[i]) + self.divide + self.form + self.divide + str(self.data[i]) + '\n')
                            elif self.meas == 'AC Voltage':
                                f.write(str(n) + self.divide + str(self.time[i]) + self.divide + self.form + self.divide + self.form + self.divide + str(self.data[i]) + '\n')
                            elif self.meas == 'DC Voltage':
                                f.write(str(n) + self.divide + str(self.time[i]) + self.divide + self.form + self.divide + self.form + self.divide + self.form + self.divide + str(self.data[i]) + '\n')
                            elif self.meas == 'Resistance':
                                f.write(str(n) + self.divide + str(self.time[i]) + self.divide + self.form + self.divide + self.form + self.divide + self.form + self.divide + self.form + self.divide + str(self.data[i]) + '\n')
                            n += 1
                        # Don't forget to close the file in the end
                        f.close()
                        self.ui.lineEdit_Error.setText("Your file has been successfully saved!")

    # When you close the window, there will be a new window comes out and ask you "Do you want to quit the program?"
    def closeEvent(self, question):
        print question
        quit_msg = "Do you want to quit the program?"
        reply = QMessageBox.question(self, 'Message', quit_msg, QMessageBox.Yes, QMessageBox.No)
        # If your answer is "yes", then quit
        if reply == QMessageBox.Yes:
            question.accept()
        # If your answer is "no", then get back
        else:
            question.ignore()

if __name__ == "__main__":
    # To open the GUI
    app = QApplication(sys.argv)
    myapp = MyForm()

    # It shows the GUI
    myapp.show()

    # Exit the GUI when "x" button is clicked
    sys.exit(app.exec_())



