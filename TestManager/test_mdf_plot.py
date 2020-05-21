from asammdf import MDF, Signal, plot
import numpy as np
import pandas as pd

with open("d:\casdev\sbxs\github_com\TESS\TESS_Sim\Measurements\_signal_info.csv") as dsp:
        if dsp != "":
                try:
                        dsp_content = pd.read_csv(dsp, delimiter=';', low_memory=False,
                                                       names=['SignalName', 'Size', 'ByteOffset', 'Unit', 'Resolution'],
                                                       skiprows=1)
                except:
                        pass
        else:
                pass
signals_name=[]
for signal_idx in range(dsp_content.SignalName.count()):
    signals_name.append(dsp_content.SignalName[signal_idx])

#with open("d:\casdev\sbxs\github_com\AqPlot\TestManager\_30bytes_1536_overwrite_3.mf4")  as test_mdf:
meas_data = MDF("d:\casdev\sbxs\github_com\AqPlot\TestManager\_30bytes_1536_overwrite_3.mf4")
signal_list = meas_data.select(signals_name)
#_200usCnt =   meas_data.select(dsp_content.SignalName[1])


plot(signal_list, title="TestPlot")