import pandas as pd

class Model:
    def __init__(self):
        self.number_of_signals = int()
        self.signal_names = []

    def import_signals(self, file_name):

        with open(file_name, newline='') as f:
            if f != "":
                self.meas_data = pd.read_csv(f, low_memory=False)

        self.signal_names = self.meas_data.keys()
        self.number_of_signals = len(self.signal_names)

    def scale(val, in_min, in_max, out_min, out_max):
        return (val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
