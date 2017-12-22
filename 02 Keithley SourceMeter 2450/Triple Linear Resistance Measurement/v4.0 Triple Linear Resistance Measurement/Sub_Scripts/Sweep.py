import visa
import numpy
import time

from PyQt4.QtCore import *
from PyQt4.QtGui import *

resistance_first_scale = []
resistance_second_scale = []

        
def analyze(data, sweep, time_difference, length_first, length_second):
    for i in range(0, len(data)):
        data[i] = float(data[i])

    total_num = int(len(data)/2)
    voltage_values = []
    current_values = []

    if sweep == "VOLTAGE":
        for i in range(0, len(data), 2):
            voltage_values.append(data[i])
            current_values.append(data[i + 1])
    
        # The first degree of the fitting polynomial is current/voltage
        best_fit_first = numpy.polyfit(voltage_values[:length_first], current_values[:length_first], 1)
        # Therefore the resistance is reciprocal of the best_fit
        resistance_first = 1/best_fit_first[0]
        
        best_fit_second = numpy.polyfit(voltage_values[length_first:length_first + length_second], current_values[length_first:length_first + length_second], 1)
        resistance_second = 1/best_fit_second[0]

        best_fit_third = numpy.polyfit(voltage_values[length_first + length_second:], current_values[length_first + length_second:], 1)
        resistance_third = 1/best_fit_third[0]
        
    elif sweep == "CURRENT":
        for i in range(0, len(data), 2):
            current_values.append(data[i])
            voltage_values.append(data[i + 1])

        # The first degree of the fitting polynomial is voltag/current
        best_fit_first = numpy.polyfit(current_values[:length_first], voltage_values[:length_first], 1)
        # Therefore the resistance is the best_fit
        resistance_first = best_fit_first[0]
        
        best_fit_second = numpy.polyfit(current_values[length_first:length_first + length_second], voltage_values[length_first:length_first + length_second], 1)
        resistance_second = best_fit_second[0]
        
        best_fit_third = numpy.polyfit(current_values[length_first + length_second:], voltage_values[length_first + length_second:], 1)
        resistance_third = best_fit_third[0]
    
    voltage_scale = [1, "Volts"]
    if abs(max(voltage_values)) >= 1:
        voltage_scale = [1, "Volts"]
    elif abs(max(voltage_values)) >= 1E-3 and abs(max(voltage_values)) < 1:
        voltage_scale = [1E3, "mVolts"]
    elif abs(max(voltage_values)) >= 1E-6 and abs(max(voltage_values)) < 1E-3:
        voltage_scale = [1E6, "uVolts"]
    elif abs(max(voltage_values)) >= 1E-9 and abs(max(voltage_values)) < 1E-6:
        voltage_scale = [1E9, "nVolts"]
    elif abs(max(voltage_values)) >= 1E-12 and abs(max(voltage_values)) < 1E-9:
        voltage_scale = [1E12, "pVolts"]
    voltage_values = numpy.array(voltage_values, dtype = 'float') * voltage_scale[0]
    
    current_scale = [1, "Amps"]
    if abs(max(current_values)) > 1:
        current_scale = [1, "Amps"]
    elif abs(max(current_values)) > 1E-3 and abs(max(current_values)) < 1:
        current_scale = [1E3, "mAmps"]
    elif abs(max(current_values)) > 1E-6 and abs(max(current_values)) < 1E-3:
        current_scale = [1E6, "uAmps"]
    elif abs(max(current_values)) > 1E-9 and abs(max(current_values)) < 1E-6:
        current_scale = [1E9, "nAmps"]
    elif abs(max(current_values)) > 1E-12 and abs(max(current_values)) < 1E-9:
        current_scale = [1E12, "pAmps"]
    current_values = numpy.array(current_values, dtype = 'float') * current_scale[0]
    
    resistance_first_scale = [1, "Ohms"]
    if resistance_first > 1E9:
        resistance_first_scale = [1E-9, "GOhms"]
    elif resistance_first > 1E6 and resistance_first < 1E9:
        resistance_first_scale = [1E-6, "MOhms"]
    elif resistance_first > 1E3 and resistance_first < 1E6:
        resistance_first_scale = [1E-3, "kOhms"]
    elif resistance_first > 1 and resistance_first < 1E3:
        resistance_first_scale = [1, "Ohms"]
    elif resistance_first > 1E-3 and resistance_first < 1:
        resistance_first_sclae = [1E3, "mOhms"]
    resistance_first = resistance_first * resistance_first_scale[0]
    
    resistance_second_scale = [1, "Ohms"]
    if resistance_second > 1E9:
        resistance_second_scale = [1E-9, "GOhms"]
    elif resistance_second > 1E6 and resistance_second < 1E9:
        resistance_second_scale = [1E-6, "MOhms"]
    elif resistance_second > 1E3 and resistance_second < 1E6:
        resistance_second_scale = [1E-3, "kOhms"]
    elif resistance_second > 1 and resistance_second < 1E3:
        resistance_second_scale = [1, "Ohms"]
    elif resistance_second > 1E-3 and resistance_second < 1:
        resistance_second_sclae = [1E3, "mOhms"]
    resistance_second = resistance_second * resistance_second_scale[0]
    
    resistance_third_scale = [1, "Ohms"]
    if resistance_third > 1E9:
        resistance_third_scale = [1E-9, "GOhms"]
    elif resistance_third > 1E6 and resistance_third < 1E9:
        resistance_third_scale = [1E-6, "MOhms"]
    elif resistance_third > 1E3 and resistance_third < 1E6:
        resistance_third_scale = [1E-3, "kOhms"]
    elif resistance_third > 1 and resistance_third < 1E3:
        resistance_third_scale = [1, "Ohms"]
    elif resistance_third > 1E-3 and resistance_third < 1:
        resistance_third_sclae = [1E3, "mOhms"]
    resistance_third = resistance_third * resistance_third_scale[0]

    if sweep == "CURRENT":
        scaled_best_fit_first = numpy.polyfit(current_values[:length_first], voltage_values[:length_first], 1)
        scaled_best_fit_second = numpy.polyfit(current_values[length_first:length_first + length_second], voltage_values[length_first:length_first + length_second], 1)
        scaled_best_fit_third = numpy.polyfit(current_values[length_first + length_second:], voltage_values[length_first + length_second:], 1)
        
    elif sweep == "VOLTAGE":
        scaled_best_fit_first = numpy.polyfit(voltage_values[:length_first], current_values[:length_first], 1)
        scaled_best_fit_second = numpy.polyfit(voltage_values[length_first:length_first + length_second], current_values[length_first:length_first + length_second], 1)    
        scaled_best_fit_third = numpy.polyfit(voltage_values[length_first + length_second:], current_values[length_first + length_second:], 1)  

    time = time_difference
    return [voltage_values, current_values, resistance_first, resistance_second, resistance_third, scaled_best_fit_first, scaled_best_fit_second, scaled_best_fit_third, voltage_scale, current_scale, resistance_first_scale, resistance_second_scale, resistance_third_scale, time, length_first, length_second]

class sweep_stop():

    def voltage_sweep_stop(self, inst, Voltage, voltage_first, voltage_second, voltage_lim, current_lim, wait_time, probe = "4", ui = False, emit = None):
        length_first = len(voltage_first)
        length_second = len(voltage_second)
        length_whole = len(Voltage)
        time_difference = 0
        item = 0
        datalist = []
        x_value = []
        y_value = []
        x_double_value = []
        Time = [0.001]
        if probe == '4':
            contact = 'ON'
        elif probe == '2':
            contact = 'OFF'
        self.continue_check = True
        ui.mplwidget_allplot.figure.clear()
        
        while True:
            if self.continue_check == True:
                axes_allplot = ui.mplwidget_allplot.figure.add_subplot(111)
                axes_allplot.set_title('Current vs.Voltage')
                axes_allplot.set_ylabel('Current (uA)')
                axes_allplot.set_xlabel('Voltage (mV)')
            
                axes_real_time = ui.mplwidget_real_time.figure.add_subplot(111)
                axes_real_time.set_title('Voltage vs.Time')
                axes_real_time.set_ylabel('Voltage (mV)')
                axes_real_time.set_xlabel('Time (s)')
                number = 0
                start_time = time.time()
                # Select the front-panel terminals for the measurement
                inst.write('ROUT:TERM FRONT')
                # Set the instrument to measure the current
                inst.write('SENS:FUNC "CURR"')
                inst.write("SOUR:VOLT:ILIM 1.05")
                # Set the voltage range to be auto
                inst.write('SOUR:VOLT:RANG:AUTO ON')
                # Set to source voltage
                inst.write('SOUR:FUNC VOLT')
                # Turn on the source read back
                inst.write('SOUR:VOLT:READ:BACK 1')
                # Input the individual voltage to start the measurement
                inst.write("SOUR:VOLT " + str(Voltage[item]))
                inst.write('SENS:CURR:RSEN ' + contact)
                inst.write('OUTP ON')

                voltage = inst.query('READ? "defbuffer1", SOUR')
                x_value.append(float(voltage) * 1E3)
                x_double_value.append(float(voltage) * 1E3)
                x_double_value.append(float(voltage) * 1E3)
                if ui != False:
                    ui.lineEdit_source.setText(str(round(float(voltage)*1000, 3)))
                    ui.label_source_unit.setText('mV')
                datalist.append(voltage)
                current = inst.query('READ? "defbuffer1", READ')
                y_value.append(float(current) * 1E6)
                if ui != False:
                    ui.lineEdit_measurement.setText(str(round(float(current)*1E6, 3)))
                    ui.label_measurement_unit.setText('uA')
                datalist.append(current)
                end_time = time.time()
                time_difference += (end_time - start_time)
                Time.append(time_difference)
                length_whole -= 1
                if length_whole == 0:
                    break
                item += 1
                ui.mplwidget_allplot.figure.clear()
                axes_allplot = ui.mplwidget_allplot.figure.add_subplot(111)
                axes_allplot.set_title('Current vs.Voltage')
                axes_allplot.set_ylabel('Current (uA)')
                axes_allplot.set_xlabel('Voltage (mV)')
                axes_allplot.plot(x_value, y_value, marker = '.', linestyle = '')
                
                ui.mplwidget_real_time.figure.clear()
                axes_real_time = ui.mplwidget_real_time.figure.add_subplot(111)
                axes_real_time.set_title('Voltage vs.Time')
                axes_real_time.set_ylabel('Voltage (mV)')
                axes_real_time.set_xlabel('Time (s)')
                axes_real_time.plot(Time, x_double_value, marker = '.', linestyle = '-')
                if emit != None:
                    emit(SIGNAL("plot"))

                time.sleep(float(wait_time))
                Time.append(time_difference + 0.001)

        inst.write("OUTP OFF")
        return_data = analyze(datalist, 'VOLTAGE', time_difference, length_first, length_second)
        return return_data

    def current_sweep_stop(self, inst, Current, current_first, current_second, current_lim, voltage_lim, wait_time, probe = '4', ui = False):
        length_whole = len(Current)
        length_first = len(current_first)
        length_second = len(current_second)
        item = 0
        time_difference = 0
        datalist = []
        x_value = []
        y_value = []
        if probe == '4':
            contact = 'ON'
        elif probe == '2':
            contact = 'OFF'
        self.continue_check = True

        while True:
            if self.continue_check == True:
                #ui.mplwidget_allplot.figure.clear()
                axes_allplot = ui.mplwidget_allplot.figure.add_subplot(111)
                axes_allplot.plot(x_value, y_value, marker = '.', linestyle = '')
                axes_allplot.set_title('All Points of Voltage vs. Current')
                axes_allplot.set_xlabel('Current (uA)')
                axes_allplot.set_ylabel('Voltage (mV)')
                number = 0
                start_time = time.time()
                # Select the front-panel terminals for the measurement
                inst.write('ROUT:TERM FRONT')
                # Set the instrument to measure the current
                inst.write('SENS:FUNC "VOLT"')
                # Set the vsoltage range to be auto
                inst.write('SOUR:CURR:RANG:AUTO ON')
                # Set to source voltage
                inst.write('SOUR:FUNC CURR')
                # Turn on the source read back
                inst.write('SOUR:VOLT:READ:BACK 1')
                # Input the individual voltage to start the measurement
                inst.write("SOUR:CURR " + str(Current[item]))
                inst.write('SENS:VOLT:RSEN ' + contact)
                inst.write('OUTP ON')

                current = inst.query('READ? "defbuffer1", SOUR')
                x_value.append(round(float(current) * 1E6, 3))
                if ui != False:
                    ui.lineEdit_source.setText(str(round(float(current)*1E6, 3)))
                    ui.label_source_unit.setText('uA')
                datalist.append(current)
                voltage = inst.query('READ? "defbuffer1", READ')
                y_value.append(round(float(voltage) * 1E3, 3))
                if ui != False:
                    ui.lineEdit_measurement.setText(str(round(float(voltage)*1E3, 3)))
                    ui.label_measurement_unit.setText('mV')
                datalist.append(voltage)
                end_time = time.time()
                time_difference += (end_time - start_time)
                length_whole -= 1
                if length_whole == 0:
                    break
                item += 1
                ui.mplwidget_allplot.figure.clear()
                axes_allplot = ui.mplwidget_allplot.figure.add_subplot(111)
                axes_allplot.plot(x_value, y_value, marker = '.', linestyle = '')
                axes_allplot.set_title('All Points of Voltage vs. Current')
                axes_allplot.set_xlabel('Current (uA)')
                axes_allplot.set_ylabel('Voltage (mV)')
                
                if emit != None:
                    emit(SIGNAL("plot"))
            else:
                if number == 0:
                    ui.mplwidget_allplot.figure.clear()
                    axes_allplot = ui.mplwidget_allplot.figure.add_subplot(111)
                    axes_allplot.plot(x_value, y_value, marker = '.', linestyle = '')
                    axes_allplot.set_title('All Points of Voltage vs. Current')
                    axes_allplot.set_xlabel('Current (uA)')
                    axes_allplot.set_ylabel('Voltage (mV)')
                    #ui.mplwidget_allplot.draw()
                    if emit != None:
                        emit(SIGNAL("plot"))
                    number += 1

        inst.write("OUTP OFF")
        return_data = analyze(datalist, 'CURRENT', time_difference, length_first, length_second)
        return return_data
    
