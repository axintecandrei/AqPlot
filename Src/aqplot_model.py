import pandas as pd
from asammdf import MDF, Signal
import numpy as np
import csv
class Model:
    def __init__(self, view):
        self.view = view
        self.signal_names = []
        self.preSignal_list = []
        self.Signal_list = []
        self.timestamp = []
        self.save_ok = 0

    def import_signals_csv(self, file_name):
        with open(file_name, newline='') as f:
            if f != "":
                try:
                    self.meas_data = pd.read_csv(f, low_memory=False)
                except:
                    return "empty_file"
        if len(self.meas_data) != 0:
            self.signal_names = self.meas_data.keys()
            #arrange time axis
            offset = self.meas_data['Time'][0]
            time_base = 0.0002
            for i in range(0, len(self.meas_data['Time'])):
                self.timestamp.append(round((self.meas_data['Time'][i] - offset) * time_base,4))

            return 0
        else:
            return "no_data"

    def import_signals_mdf(self, file_name):
        try:
            self.meas_data = MDF(file_name)
            self.signal_names = sorted(self.meas_data.channels_db, key=lambda x: x.lower())
        except:
            return "Error opening file"

    def import_signal_info(self, signal_info_file):
        '''decode some sort of a2l file (it will be a txt file)
            some info like:
            - signal name
            - data type/size
            - byte offset
            - unit
            - resolution
        '''
        #clear the preSignal list in care it will be called multiple times
        self.preSignal_list.clear()
        return_msg = 0
        with open(signal_info_file) as dsp:
            if dsp != "":
                try:
                    self.dsp_content = pd.read_csv(dsp, delimiter=';',low_memory=False,
                                                   names=['SignalName','Size','ByteOffset','Unit','Resolution'],
                                                   skiprows=1)
                except:
                    return_msg= "SomeError"
                    return return_msg
            else:
                return_msg = "empty_file"
                return return_msg

        if len(self.dsp_content) != 0:
            # check so no fileds are Nan
            if not self.dsp_content.isnull().values.any():
                for signal_idx in range(self.dsp_content.SignalName.count()):
                     pre_signal = preSignal(name=self.dsp_content.SignalName[signal_idx],
                                           samples=[],
                                           size=self.dsp_content.Size[signal_idx],
                                           byteoffset=int(self.dsp_content.ByteOffset[signal_idx]),
                                           unit=self.dsp_content.Unit[signal_idx],
                                           resolution=self.dsp_content.Resolution[signal_idx])
                     self.preSignal_list.append(pre_signal)

            else:
                return_msg = "nan_fields"
                return return_msg
        else:
            return_msg = "no_data"
            return return_msg

    def get_pack_from_ecu(self, ecu_pack):
        # get the received package and arrange each sample to the proper signal
        for presignal in self.preSignal_list:
            presignal.get_sample(ecu_pack)

    def save_measurement_csv(self):
        signal_name_list = []
        #wirte header with signal names
        f = open('../TestManager/output_test.csv', 'w+')
        csv_out = csv.writer(f, dialect='excel')
        for signal in self.preSignal_list:
           signal_name_list.append(signal.name)

        csv_out.writerow(signal_name_list)
        for sample_idx in range(0, len(self.preSignal_list[0].samples)):
            samples_to_csv = []
            for signal in self.preSignal_list:
                samples_to_csv.append(signal.samples[sample_idx])
            csv_out.writerow(samples_to_csv)

        f.close()

    def save_measurement_mdf(self):
        #ask user if wants to save the measurement
        yes = 16384
        no = 65536
        #check if there is something to be saved
        if self.preSignal_list[0].samples:
            user_reply = self.view.ask_user_binary_question('Save Measurement', 'Want to save measurement?')
            if user_reply == yes:
                #create timestamp
                timestamps = []
                for sample_idx in range(len(self.preSignal_list[0].samples)):
                    timestamps.append(sample_idx * 0.0002)

                #create the Signal list with the members from preSignal ones
                for presignal in self.preSignal_list:
                    signal = Signal(samples=np.array(presignal.samples, dtype=presignal.dtype),
                                    timestamps=np.array(timestamps, dtype=np.float32),
                                    name=presignal.name,
                                    unit=presignal.unit
                                    )
                    self.Signal_list.append(signal)

                meas_path_name = self.view.get_saved_file_name("Select destination", "*.mf4")

                with MDF(version='4.10') as new_meas:
                    new_meas.append(self.Signal_list, "AqPlot")
                    new_meas.save(meas_path_name)
                self.save_ok = 1
                self.view.msg_box("Info", "Succesfull!")
            elif user_reply == no:
                pass
            #discard all data
            if self.save_ok:
                for preSignal in self.preSignal_list:
                    preSignal.samples.clear()
                self.Signal_list.clear()
        else:
            self.view.msg_box("Info", "Nothing to save.")


    def scale(self, val, in_min, in_max, out_min, out_max):
        return (val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

class preSignal(object):
    def __init__(self,
                 name="",
                 samples=None,
                 size=None,
                 byteoffset=None,
                 unit="",
                 resolution=0.0
    ):
        self.name = name
        self.samples = samples
        self.size= size
        self.byteoffset = byteoffset
        self.unit = unit
        self.resolution = resolution
        self.dtype = np.float32

    def get_sample(self, ecu_sample_pack):
        self.samples.append(self.covert_due_to_size(ecu_sample_pack))

    def covert_due_to_size(self, ecu_sample_pack):
        merged_sample = 0
        if abs(self.size) == 1:
            merged_sample = ecu_sample_pack[self.byteoffset]
            if self.size < 0:
                self.dtype = np.int8
                merged_sample = np.cast['int8'](merged_sample - 128)
            else:
                self.dtype = np.uint8
        elif abs(self.size) == 2:
            merged_sample = ecu_sample_pack[self.byteoffset] | (ecu_sample_pack[self.byteoffset + 1]<< 8)
            if self.size < 0:
                self.dtype = np.int16
                merged_sample = np.cast['int16'](merged_sample - 32768)
            else:
                self.dtype = np.uint16
        elif abs(self.size) == 4:
            merged_sample = ecu_sample_pack[self.byteoffset] | (ecu_sample_pack[self.byteoffset + 1] << 8) | \
                            (ecu_sample_pack[self.byteoffset + 2] << 16) | (ecu_sample_pack[self.byteoffset + 3] << 24)
            if self.size < 0:
                self.dtype = np.int32
                merged_sample = np.cast['int32'](merged_sample - 2147483648)
            else:
                self.dtype = np.uint32
        if self.resolution < 1:
            self.dtype = np.float32
        return merged_sample * self.resolution



