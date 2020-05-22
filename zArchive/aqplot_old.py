import tkinter as tk
from _codecs import raw_unicode_escape_decode
from tkinter import ttk, BOTH, Text, Menu, END , filedialog, messagebox
import threading
import pandas as pd
import matplotlib
import serial
import time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
#import matplotlib.animation as animation
import csv
from matplotlib import style
style.use('ggplot')

# Globals
device = 'COM6'
baudrate = 115200
run_meas = threading.Event()
arduino_port = serial.Serial (device,
                              baudrate = baudrate,
                              parity   = serial.PARITY_NONE,
                              stopbits = serial.STOPBITS_ONE,
                              bytesize = serial.EIGHTBITS,
                              rtscts   = False,
                              dsrdtr   = False,
                              xonxoff  = False,
                              timeout  = None)

matplotlib.use("TkAgg")
figure = Figure(figsize=(5, 5), dpi=120)

'''Defining main window layout
Each class inherits from Frame except MAINAPPLICATION wich
shall inherit from Tk '''

class Navbar(tk.Frame):

    def init_navbar(self):
        tk.Frame.__init__(self,background="white", border=0)
        self.pack(side="left", fill="y")


        open_file_btn = ttk.Button(self, text="Open Measurement", command=lambda: open_files())
        open_file_btn.grid(row=0, columnspan=1, sticky="w")
        start_meas_btn = ttk.Button(self, text="Run Measurement  ", command=lambda:on_off_meas() )
        start_meas_btn.grid(row=1, columnspan=1, sticky="w")



    def creat_signal_list_box(self, name_array):
        label = tk.Label(self, text="Select Signals ", bg="white")
        label.grid(row=2, columnspan=1, sticky="w")
        signal_list = tk.Listbox(self)
        for i in range(1,len(name_array)):
            signal_list.insert(i, name_array[i])
        signal_list.bind('<<ListboxSelect>>', add_signal2plot)
        signal_list.grid(row=3, columnspan=1, sticky="w")

class MenuBar(tk.Frame):
    def init_toolbar(self,):
        menubar = Menu(main_app)
        main_app.config(menu=menubar)

        fileMenu = Menu(menubar)
        menubar.add_cascade(label="File", menu=fileMenu)
        fileMenu.add_command(label="Open Measuerement", command=lambda: open_files())

        editMenu = Menu(menubar)
        menubar.add_cascade(label="Edit", menu=editMenu)
        editMenu.add_command(label="Clear Scope", command=lambda: clear_fig())

class Statusbar(tk.Frame):
    def init_statusbar(self):
        tk.Frame.__init__(self, bg="white", border=5)
        self.status_var = tk.StringVar()
        self.pack(side="bottom",fill='x')
        #labe = tk.Label(self, text="Statusbar",bg='white')
        #labe.pack(side='left')
        labe = tk.Label(self, text="Acquisition Status",bg='white')
        labe.pack(side='left')
        #acq_status = ttk.Label(self, textvariable=self.status_var)
        #acq_status.pack(padx = 10,pady =1)

class Scope(tk.Frame):
    def init_main_area(self):
        tk.Frame.__init__(self, background="grey", border=0)
        self.pack(side="right", fill="both", expand=True)
        creat_base_canvas(figure)

class MainApplication(tk.Tk):
    def __init__(self,  *args, **kwargs):
        tk.Tk.__init__(self,  *args, **kwargs)
        tk.Tk.title(self, "Data Analysis")

def creat_base_canvas(fig):
    canvas = FigureCanvasTkAgg(fig, scope)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    toolbar = NavigationToolbar2Tk(canvas, scope)
    toolbar.update()
    canvas._tkcanvas.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

def open_files():
    ftypes = [('CSV File', '*.csv'), ('All files', '*')]
    dlg = filedialog.Open(scope, filetypes=ftypes)
    fl = dlg.show()
    if fl != '':
        load_data(fl)

def load_data(file):
    with open(file, newline='') as f:
        if f != "":
            # data_FileReader = csv.reader(f)
            # raw_data_list = []
            # for row in data_FileReader:
            #     if len(row) != 0:
            #         raw_data_list = raw_data_list + [row]
            global data_signal_name_list, data_FileReader
            data_signal_name_list= []
            data_FileReader = pd.read_csv(f, low_memory=False)
            data_signal_name_list = data_FileReader.keys()

    navbar.creat_signal_list_box(data_signal_name_list)
    nr_signals = len(data_signal_name_list)
    data_lenght = len(data_signal_name_list)
    if data_lenght > 0:
        show_data(data_FileReader[data_signal_name_list[1]], data_signal_name_list[1])
    else:
        tk.messagebox.showinfo("Error", "No data in file ")

def show_data(y_data, sign_name):
    figure.clear()
    subplot = figure.add_subplot(111)
    subplot.set_title(sign_name, fontsize=16)
    subplot.set_xlabel("Time(us)", fontsize=12)
    subplot.set_ylabel(sign_name, fontsize=12)
    try:
        subplot.plot(y_data)
    except ValueError :
        tk.messagebox.showinfo("Error", "Value error")
    figure.canvas.draw()

def add_signal2plot(event):
    w = event.widget
    index = int(w.curselection()[0])
    value = w.get(index)
    try:
        show_data(data_FileReader[data_signal_name_list[index + 1]], value)
    except IndexError:
        tk.messagebox.showinfo("Error", "No data for this signal")

def clear_fig():
    figure.clear()
    figure.canvas.draw()


def scale(val, in_min, in_max,out_min, out_max):
    return (val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min



class ser_thread(threading.Thread):
    # initialize class
    def __init__(self, name, ser):
        threading.Thread.__init__(self)
        # Name of thread
        self.name = name
        # Serial port information
        self.ser = ser
        self.first_time_flag = 0
        self.f = open('output_test.csv', 'w+')

    # gets called when thread is started with .start()
    def run(self):
        while True:
            if run_meas.is_set() is False:
                self.first_time_flag = 0
                speed_request = 16000
                rx = chr(int(scale(speed_request, 0, 32000, 0, 127)))
                #self.ser.write(rx.encode())
                self.ser.close()
                self.f.close()
            run_meas.wait()
            if self.first_time_flag is 0:
                self.f = open('output_test.csv', 'w+')
                self.name_list = ["Time", "Req Speed", "ADC Bemf U", "ADC Bemf V", "Speed Error", "Voltage Request",
                                  "Current Left", "BEMF U", "BEMF V", "BEMF W", "Right PWM", "Speed Prop Part"]
                self.csv_out = csv.writer(self.f, delimiter=',', dialect='excel-tab')
                self.csv_out.writerow(self.name_list)
                self.first_time_flag = 1

            speed_request = 24000
            #rx = chr(int(scale(speed_request, 0, 32000, 0, 127)))
            rx = chr(0x31)

            if self.ser.isOpen() == False:
                self.ser.open()
                time.sleep(0.1)

            self.ser.write(rx.encode())

            while self.ser.inWaiting() >= 26:
                line = self.ser.read(26)
                header = line[0] & 0xFF
                counter = ((line[1] | line[2] << 8) * 2) * 0.0005
                adc_bemf_u = (line[3] | line[4] << 8) - 32768
                left_voltage_req = ((line[5] | (line[6] << 8)) - 32768) * 0.001
                # dir_left = line[5]
                # dir_right = line[6]
                left_current = (line[7] | line[8] << 8) * 0.001
                right_pwm = (line[9] | line[10] << 8)
                bemf_u = ((line[11] | line[12] << 8) - 32768)
                bemf_v = ((line[13] | line[14] << 8) - 32768)
                bemf_w = ((line[15] | line[16] << 8) - 32768)
                speed_error = ((line[17] | line[18] << 8) - 32768)
                speed_p_part = ((line[19] | line[20] << 8) - 32768) * 0.001
                req_speed = ((line[21] | (line[22] << 8)) - 32768)
                adc_bemf_v = ((line[23] | (line[24] << 8)) - 32768)
                footer = line[25]
                data = [counter, req_speed, adc_bemf_u, adc_bemf_v, speed_error, left_voltage_req, left_current,
                        bemf_u, bemf_v, bemf_w,right_pwm, speed_p_part]

                self.csv_out.writerow(data)
                if ((header is 126) and (footer is 129)):
                    statusbar.status_var = 1
                else:
                    statusbar.status_var = -1
                print("Ser.inWaitning {}".format(self.ser.inWaiting()))
                print('Header = ', header)
                print('2ms Counter = ', counter)
                print('Footer = ', footer)

SerialThread = ser_thread("Data_Aquisition", arduino_port)
main_app = MainApplication()
global statusbar
statusbar = Statusbar()
toolbar = MenuBar()
navbar = Navbar()
scope = Scope()

statusbar.init_statusbar()
toolbar.init_toolbar()
navbar.init_navbar()
scope.init_main_area()


main_app.geometry('1080x720+0+0')
SerialThread.start()
main_app.mainloop()
