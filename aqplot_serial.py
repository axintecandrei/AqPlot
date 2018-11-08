import threading
import serial
import serial.tools.list_ports




class ser_thread(threading.Thread):
    def __init__(self, thread_name):
        super(ser_thread, self).__init__()
        self.name = thread_name
        self.ser = serial.Serial()
        self.com_port_list = []

    # gets called when thread is started with .start()
    def run(self):
        while True:
            self.com_port_list = serial.tools.list_ports.comports()
            if self.ser.is_open:
                while self.ser.inWaiting() > 0:
                    line = self.ser.read(3)
                    print(line)


    def open_close(self):
        if self.ser.is_open :
            self.ser.close()
            print("close")
        else:
            self.ser.open()
            print("open")

    def set_port(self, port):
        self.ser.setPort(port)

    def set_baud(self, baud):
        self.ser.baudrate = baud

    def list_comports(self):
        return self.com_port_list


'''
class someThread(threading.Thread):
    def __init__(self, function):
        self.running = False
        self.function = function
        super(someThread, self).__init__()

    def start(self):
        self.running = True
        super(someThread, self).start()

    def run(self):
        while self.running:
            self.function()

    def stop(self):
        self.running = False
'''