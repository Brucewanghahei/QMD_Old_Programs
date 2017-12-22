import visa
import numpy
import time

resistance_a_scale = []
resistance_d_scale = []

        
def analyze(data, sweep, time_difference, length_ascending):
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
        best_fit_a = numpy.polyfit(voltage_values[:length_ascending], current_values[:length_ascending], 1)
        # Therefore the resistance is reciprocal of the best_fit
        resistance_a = 1/best_fit_a[0]
        
        best_fit_d = numpy.polyfit(voltage_values[length_ascending:], current_values[length_ascending:], 1)
        resistance_d = 1/best_fit_d[0]

    elif sweep == "CURRENT":
        for i in range(0, len(data), 2):
            current_values.append(data[i])
            voltage_values.append(data[i + 1])

        # The first degree of the fitting polynomial is voltag/current
        best_fit_a = numpy.polyfit(current_values[:length_ascending], voltage_values[:length_ascending], 1)
        # Therefore the resistance is the best_fit
        resistance_a = best_fit_a[0]
        
        best_fit_d = numpy.polyfit(current_values[length_ascending:], voltage_values[length_ascending:], 1)
        resistance_d = best_fit_d[0]
    
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
    
    resistance_a_scale = [1, "Ohms"]
    if resistance_a > 1E9:
        resistance_a_scale = [1E-9, "GOhms"]
    elif resistance_a > 1E6 and resistance_a < 1E9:
        resistance_a_scale = [1E-6, "MOhms"]
    elif resistance_a > 1E3 and resistance_a < 1E6:
        resistance_a_scale = [1E-3, "kOhms"]
    elif resistance_a > 1 and resistance_a < 1E3:
        resistance_a_scale = [1, "Ohms"]
    elif resistance_a > 1E-3 and resistance_a < 1:
        resistance_a_sclae = [1E3, "mOhms"]
    resistance_a = resistance_a * resistance_a_scale[0]
    
    resistance_d_scale = [1, "Ohms"]
    if resistance_d > 1E9:
        resistance_d_scale = [1E-9, "GOhms"]
    elif resistance_d > 1E6 and resistance_d < 1E9:
        resistance_d_scale = [1E-6, "MOhms"]
    elif resistance_d > 1E3 and resistance_d < 1E6:
        resistance_d_scale = [1E-3, "kOhms"]
    elif resistance_d > 1 and resistance_d < 1E3:
        resistance_d_scale = [1, "Ohms"]
    elif resistance_d > 1E-3 and resistance_d < 1:
        resistance_d_sclae = [1E3, "mOhms"]
    resistance_d = resistance_d * resistance_d_scale[0]

    if sweep == "CURRENT":
        scaled_best_fit_ascending = numpy.polyfit(current_values[:length_ascending], voltage_values[:length_ascending], 1)
        scaled_best_fit_descending = numpy.polyfit(current_values[length_ascending:], voltage_values[length_ascending:], 1)
    elif sweep == "VOLTAGE":
        scaled_best_fit_ascending = numpy.polyfit(voltage_values[:length_ascending], current_values[:length_ascending], 1)
        scaled_best_fit_descending = numpy.polyfit(voltage_values[length_ascending:], current_values[length_ascending:], 1)    

    time = time_difference
    return [voltage_values, current_values, resistance_a, resistance_d, scaled_best_fit_ascending, scaled_best_fit_descending, voltage_scale, current_scale, resistance_a_scale, resistance_d_scale, time, length_ascending]

def current_sweep(inst, Current, current_ascending, current_lim, voltage_lim, wait_time, probe = '4'):
    length_whole = len(Current)
    length_ascending = len(current_ascending)
    item = 0
    datalist = []
    contact = 'ON'

    start_time = time.time()
    while True:
        inst.write('TRAC:CLE "defbuffer1"')
        inst.write('*RST')
        inst.write('OUTP:SMOD NORM')
        inst.write('SENS:FUNC "VOLT"')
        inst.write('SENS:VOLT:RANG:AUTO ON')
        if probe == '2':
            contact = 'OFF'
        elif probe == '4':
            contact = 'ON'
        inst.write('SENS:VOLT:RSEN ' + contact)
        inst.write('SOUR:FUNC CURR')
        inst.write('SOUR:CURR:RANG:AUTO ON')
        # inst.write('SOUR:CURR:RANG ' + str(current_lim))
        inst.write('SOUR:CURR:VLIM ' + str(voltage_lim))

        Str_Current = ''

        if length_whole >= 100:
            count = 100
            for i in range(item * 100, (item + 1) * 100):
                Str_Current = Str_Current + ', ' + str(Current[i])
        else:
            count = length_whole
            for i in range(item * 100, len(Current)):
                Str_Current = Str_Current + ', ' + str(Current[i])

        Str_Current = Str_Current[1:]
        inst.write('SOUR:LIST:CURR '+ Str_Current)
        inst.write('SOUR:SWE:CURR:LIST 1, ' + str(wait_time))
        inst.write('INIT')
        inst.write('*WAI')
        inst.timeout = 200000

        inst.write('TRAC:DATA? 1, ' + str(count) + ', "defbuffer1", SOUR, READ')

        data = inst.read()
        data = str(data).split(",")
        for i in range(0, len(data)):
            data[i] = float(data[i])
        datalist.extend(data)
        if length_whole <= 100:
            break
        length_whole -= 100
        item += 1
        

    end_time = time.time()
    time_difference = end_time - start_time
    return_data = analyze(datalist, 'CURRENT', time_difference, length_ascending)
    return return_data

def voltage_sweep(inst, Voltage, voltage_ascending, voltage_lim, current_lim, wait_time, probe = "4"):
    length_ascending = len(voltage_ascending)
    length_whole = len(Voltage)
    item = 0
    datalist = []
    contact = 'ON'
    
    start_time = time.time()
    while True:
        inst.write('TRAC:CLE "defbuffer1"')
        inst.write('*RST')
        inst.write('SENS:FUNC "CURR"')
        inst.write('SENS:CURR:RANG:AUTO ON')
        if probe == '2':
            contact = 'OFF'
        elif probe == '4':
            contact = 'ON'
        inst.write('SENS:CURR:RSEN ' + contact)
        inst.write('SOUR:FUNC VOLT')
        inst.write('SOUR:VOLT:RANG:AUTO ON')        
        # inst.write('SOUR:VOLT:RANG: 0.2')
        # inst.write('SOUR:VOLT:RANG: ' + str(voltage_lim))
        inst.write('SOUR:VOLT:ILIM ' + str(current_lim))

        Str_Voltage = ''

        if length_whole >= 100:
            count = 100
            for i in range(item * 100, (item + 1) * 100):
                Str_Voltage = Str_Voltage + ', ' + str(Voltage[i])
        else:
            count = length_whole
            for i in range(item * 100, len(Voltage)):
                Str_Voltage = Str_Voltage + ', ' + str(Voltage[i])
        Str_Voltage = Str_Voltage[1:]
        inst.write('SOUR:LIST:VOLT ' + Str_Voltage)
        inst.write('SOUR:SWE:VOLT:LIST 1, ' + str(wait_time))
        inst.write('INIT')
        inst.write('*WAI')
        inst.timeout = 200000
        
        inst.write('TRAC:DATA? 1, ' + str(len(Voltage)) + ", 'defbuffer1', SOUR, READ")

        data = inst.read()
        data = str(data).split(",")
        for i in range(0, len(data)):
            data[i] = float(data[i])
        datalist.extend(data)
        if length_whole <= 100:
            break
        length_whole -= 100
        item += 1
        
    end_time = time.time()
    time_difference = end_time - start_time
    return_data = analyze(datalist, 'VOLTAGE', time_difference, length_ascending)
    return return_data
    
class sweep_stop():

    def voltage_sweep_stop(self, inst, Voltage, voltage_ascending, voltage_lim, current_lim, wait_time, probe = "4", ui = False):
        length_ascending = len(voltage_ascending)
        length_whole = len(Voltage)
        time_difference = 0
        item = 0
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
                number = 0
                start_time = time.time()
                # Select the front-panel terminals for the measurement
                inst.write('ROUT:TERM FRONT')
                # Set the instrument to measure the current
                inst.write('SENS:FUNC "CURR"')
                # Set the voltage range to be auto
                inst.write('SOUR:VOLT:RANG 5')
                # Set to source voltage
                inst.write('SOUR:FUNC VOLT')
                # Turn on the source read back
                inst.write('SOUR:VOLT:READ:BACK 1')
                # Input the individual voltage to start the measurement
                inst.write("SOUR:VOLT " + str(Voltage[item]))
                inst.write('SENS:CURR:RSEN ' + contact)
                inst.write('OUTP ON')

                voltage = inst.query('READ? "defbuffer1", SOUR')
                x_value.append(round(float(voltage) * 1E3, 3))
                if ui != False:
                    ui.lineEdit_source.setText(str(round(float(voltage)*1000, 3)))
                    ui.label_source_unit.setText('mV')
                datalist.append(voltage)
                current = inst.query('READ? "defbuffer1", READ')
                y_value.append(round(float(current) * 1E6, 3))
                if ui != False:
                    ui.lineEdit_measurement.setText(str(round(float(current)*1E6, 3)))
                    ui.label_measurement_unit.setText('uA')
                datalist.append(current)
                end_time = time.time()
                time_difference += (end_time - start_time)
                length_whole -= 1
                if length_whole == 0:
                    break
                item += 1
            else:
                if number == 0:
                    ui.mplwidget_allplot.figure.clear()
                    axes_allplot = ui.mplwidget_allplot.figure.add_subplot(111)
                    axes_allplot.plot(x_value, y_value, marker = '.', linestyle = '')
                    axes_allplot.set_title('Current vs.Voltage')
                    axes_allplot.set_ylabel('Current (uA)')
                    axes_allplot.set_xlabel('Voltage (mV)')
                    ui.mplwidget_allplot.draw()
                    number += 1
                    

        inst.write("OUTP OFF")
        return_data = analyze(datalist, 'VOLTAGE', time_difference, length_ascending)
        return return_data

    def current_sweep_stop(self, inst, Current, current_ascending, current_lim, voltage_lim, wait_time, probe = '4', ui = False):
        length_whole = len(Current)
        length_ascending = len(current_ascending)
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
            else:
                if number == 0:
                    ui.mplwidget_allplot.figure.clear()
                    axes_allplot = ui.mplwidget_allplot.figure.add_subplot(111)
                    axes_allplot.plot(x_value, y_value, marker = '.', linestyle = '')
                    axes_allplot.set_title('All Points of Voltage vs. Current')
                    axes_allplot.set_xlabel('Current (uA)')
                    axes_allplot.set_ylabel('Voltage (mV)')
                    ui.mplwidget_allplot.draw()
                    number += 1

        inst.write("OUTP OFF")
        return_data = analyze(datalist, 'CURRENT', time_difference, length_ascending)
        return return_data

'''
if __name__ == '__main__':
    rm = visa.ResourceManager()
    visa_list = rm.list_resources()
    # print 'visa_list: ', visa_list
    user_visa = "USB0::0x05E6::0x2450::04068866::INSTR"
    inst = rm.open_resource(str(user_visa))

    current_ascending = range(-10, 10, 1)
    current_descending = range(10, 0, -1)
    current_ascending = numpy.array(list(current_ascending), dtype = 'float')/1E6
    current_descending = numpy.array(list(current_descending), dtype = 'float')/1E6
    Current = numpy.append(current_ascending, current_descending)
    waitTime = 0.001
    #totalWaitTime = (waitTime + 20*waitTime)*len(Voltages) + 1
    if abs(max(Current)) > abs(min(Current)):
        current_lim = (1.01)*abs(max(Current))
    else:
        current_lim = (1.01)*abs(min(Current))
    voltage_lim = 1
    probe = 2
    data = current_sweep(inst, Current, current_ascending, current_lim, voltage_lim, waitTime, probe)
'''
'''if __name__ == '__main__':
    rm = visa.ResourceManager()
    rm.list_resources()
    instr = rm.open_resource('USB0::0x05E6::0x2450::04068866::INSTR')

    Voltages = [0, 0.1, 0.2, 0.4, 0.3, 0.2, 0.1, 0]
    Volt_asc = [0, 0.1, 0.2, 0.4]
    volt_lim = 1
    curr_lim = 1
    wait_time = 0.01
    probe = '2'

    swe = sweep_stop()
    swe.voltage_sweep_stop(instr, Voltages, Volt_asc, volt_lim, curr_lim, wait_time, probe)

    instr.close()
    
    '''
    
    
