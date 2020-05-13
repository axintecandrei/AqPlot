import pandas as pd
from asammdf import MDF, Signal
import numpy as np
import csv
class Model:
    def __init__(self):
        self.number_of_signals = int()
        self.preSignal_list = []
        self.timestamp = []
        self.signal_sample = {}
        self.dsp_header_id = 796737095
        self.import_signal_info('../TestManager/output_test.csv')

    def import_signals(self, file_name):
        with open(file_name, newline='') as f:
            if f != "":
                try:
                    self.meas_data = pd.read_csv(f, low_memory=False)
                except:
                    return "empty_file"
        if len(self.meas_data) != 0:
            self.signal_names = self.meas_data.keys()
            self.number_of_signals = len(self.signal_names)
            #arrange time axis
           #offset = self.meas_data['Time'][0]
           #time_base = 0.0002
           #for i in range(0, len(self.meas_data['Time'])):
           #    self.timestamp.append(round((self.meas_data['Time'][i] - offset) * time_base,4))
                #self.timestamp.append(round(self.meas_data['_200usCnt'][i], 4))

            return 0
        else:
            return "no_data"

    def import_signals_mdf(self, file_name):
        self.meas_data = MDF(file_name)

    def import_signal_info(self, signal_info_file):
        '''decode some sort of a2l file (it will be a txt file)
            some info like:
            - signal name
            - data type/size
            - byte offset
            - unit
            - resolution
        '''
        return_msg = '0'
        with open(signal_info_file, newline='') as dsp:
            if dsp != "":
                try:
                    self.dsp_content= dsp.readlines()
                except:
                    return_msg= "empty_file"
        '''create a loc signal class or create signals here ?'''
        header = preSignal(name="Header",samples=[],size=1,byteoffset=0,unit="-",resolution=1)
        self.preSignal_list.append(header)
        dmaisrcnt = preSignal(name="DmaIsrCnt",samples=[],size=2,byteoffset=1,unit="-",resolution=1)
        self.preSignal_list.append(dmaisrcnt)
        ringbuffcnt = preSignal(name="RingBufferCnt",samples=[],size=2, byteoffset=3,unit="-",resolution=1)
        self.preSignal_list.append(ringbuffcnt)
        head_real = preSignal(name="Head real",samples=[],size=2,byteoffset=5,unit="-",resolution=1)
        self.preSignal_list.append(head_real)
        tail_real = preSignal(name="Tail real", samples=[], size=2, byteoffset=7,unit="-", resolution=1)
        self.preSignal_list.append(tail_real)
        tessdasstate = preSignal(name="TessDasState",samples=[],size=1,byteoffset=10,unit="-",resolution=1)
        self.preSignal_list.append(tessdasstate)
        loop_cnt = preSignal(name="_200usCnt",samples=[],size=4,byteoffset=11,unit="-",resolution=0.0002)
        self.preSignal_list.append(loop_cnt)
        footer = preSignal(name="Footer",samples=[],size=1,byteoffset=15,unit="-",resolution=1)
        self.preSignal_list.append(footer)
        inwaiting = preSignal(name="BytesinWaiting",samples=[],size=1,byteoffset=9,unit="-",resolution=1)
        self.preSignal_list.append(inwaiting)
        print("import dsp ok")
        return return_msg

    def get_pack_from_ecu(self, ecu_pack):
        for presignal in self.preSignal_list:
            presignal.get_sample(ecu_pack)

    def save_measurement(self):
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

    def get_sample(self, ecu_sample_pack):
        self.samples.append(self.covert_due_to_size(ecu_sample_pack) * self.resolution)

    def covert_due_to_size(self, ecu_sample_pack):
        if self.size is 1:
            merged_sample= ecu_sample_pack[self.byteoffset]
            return merged_sample

        elif self.size is 2:
            merged_sample = ecu_sample_pack[self.byteoffset] | ecu_sample_pack[self.byteoffset + 1]<< 8
            return merged_sample

        elif self.size is 4:
            merged_sample = ecu_sample_pack[self.byteoffset] | ecu_sample_pack[self.byteoffset + 1] << 8 | \
                            ecu_sample_pack[self.byteoffset + 2] << 16 | ecu_sample_pack[self.byteoffset + 3] << 24
            return merged_sample


