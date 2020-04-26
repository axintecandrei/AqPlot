import pandas as pd

class Model:
    def __init__(self):
        self.number_of_signals = int()
        self.signal_names = []
        self.variable_name = ["byte0",
                              "byte1",
                              "byte2",
                              "byte3",
                              "byte4",
                              "byte5",
                              "byte6",
                              "byte7",
                              "byte8",
                              "byte9",
                              "byte10",
                              "byte11",
                              "byte12",
                              "byte13",
                              "byte14",
                              "byte15",
                              "byte16",
                              "byte17",
                              "byte18",
                              "byte19",
                              "byte20",
                              "byte21",
                              "byte22",
                              "byte23",
                              "byte24",
                              "byte25", ]
        self.values = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        loc_db_dict = {self.variable_name[0] : self.values[0],
                       self.variable_name[1] : self.values[1],
                       self.variable_name[2] : self.values[2],
                       self.variable_name[3] : self.values[3],
                       self.variable_name[4] : self.values[4],
                       self.variable_name[5] : self.values[5],
                       self.variable_name[6] : self.values[6],
                       self.variable_name[7] : self.values[7],
                       self.variable_name[8] : self.values[8],
                       self.variable_name[9] : self.values[9],
                       self.variable_name[10] : self.values[10],
                       self.variable_name[11] : self.values[11],
                       self.variable_name[12] : self.values[12],
                       self.variable_name[13] : self.values[13],
                       self.variable_name[14] : self.values[14],
                       self.variable_name[15] : self.values[15],
                       self.variable_name[16] : self.values[16],
                       self.variable_name[17] : self.values[17],
                       self.variable_name[18] : self.values[18],
                       self.variable_name[19] : self.values[19],
                       self.variable_name[20] : self.values[20],
                       self.variable_name[21] : self.values[21],
                       self.variable_name[22] : self.values[22],
                       self.variable_name[23] : self.values[23],
                       self.variable_name[24] : self.values[24],
                       self.variable_name[25] : self.values[25]}
        #self.data_base = pd.DataFrame(loc_db_dict)


    def import_signals(self, file_name):
        with open(file_name, newline='') as f:
            if f != "":
                try:
                    self.meas_data = pd.read_csv(f, low_memory=False)
                    self.signal_names = self.meas_data.keys()
                    self.number_of_signals = len(self.signal_names)
                except:
                      print("something not ok with file. TODO: catch 2-3 common errors, and display msg box")

    def fill_data_base (self, data_values, last_pack_flag):
        loc_dict = { }
        if last_pack_flag:
            pass

    def scale(self, val, in_min, in_max, out_min, out_max):
        return (val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
