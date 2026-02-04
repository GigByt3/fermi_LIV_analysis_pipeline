from gdt.core import data_path
from gdt.missions.fermi.gbm.tte import GbmTte
from gdt.core.binning.unbinned import bin_by_time
from gdt.core.plot.lightcurve import Lightcurve
from gdt.missions.fermi.time import Time
from scipy import stats
from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt
import sqlite3
import pandas
import requests
import atlas
import json
import os
import traceback
import sys

json_object = {}

gbm_dir_name = "./GBM_files/"
lat_dir_name = "./LAT_files/"
gbm_files = os.listdir(gbm_dir_name)
gbm_files = [f for f in gbm_files if os.path.isfile(gbm_dir_name+f)]
lat_files = os.listdir(lat_dir_name)
lat_files = [f for f in lat_files if os.path.isfile(lat_dir_name+f)]

r = requests.get("https://icecube.wisc.edu/~grbweb_public/GRBweb2.sqlite")
f = open('GRBweb2.sqlite', 'wb').write(r.content)
db = sqlite3.connect('GRBweb2.sqlite')

'''
save_array format:

trig_num:
{
(for GBM)
time_array: [#,#,#...]      ==totalled sliced counts across all detectors
time_values: [#,#,#...]     ==time values corresponding to above
detectors: [0,4,9...]       ==detector names
det_ct: 4                   ==number of detectors
low_t: #                    ==time of max counts (met)
low_ct: #                   ==max counts num
background: #               ==background counts (outside of T_90 designation)
background_var: #           ==background counts (outside of T_90 designation)
significance: #             ==(low_ct-background)/background_var
half_max_t: #               ==half maximum width for error counting

(for LAT)
lat_highs: [[t, E]...]      ==lat highs over 80% highest reading

(general)
redshift: #                 ==redshift source
redshift_src: "foo"         ==source ("def_GCN" (default GCN) if not available)
name: "GRB###..."
}
'''

save_array = {}

sys.stdout.write("Init- \n")

for name in gbm_files:
    sys.stdout.write("Checking File: " + str(name) + ".\n")
    if '_bn' in name:
        sys.stdout.write("Analyzing- \n")
        trig_number = name.split("bn")[1].split("_v")[0]
        n_num = name.split("_n")[1].split("_b")[0]
        file_ref = gbm_dir_name + name
        new = True

        if trig_number in save_array:
            if len(save_array[trig_number]["time_array"]) == 0:
                new = True
            else:
                new = False
            sys.stdout.write("Trigger Number " + str(trig_number) + " is in Save Array. \n")
        else:
            sys.stdout.write("Adding " + str(trig_number) + " to Save Array. \n")
            save_array[trig_number] = {
                "time_array": [],
                "time_values": [],
                "detectors": [],
                "det_ct": 0,
                "low_t": 0,
                "low_ct": 0,
                "background": 0,
                "background_var": 0,
                "significance": 0,
                "half_max_t": 0,
                "lat_highs": [],
                "redshift": 0,
                "redshift_src": "def_GCN",
                "trig": 0,
                "name": "GRB" + trig_number
            }

        sys.stdout.write("getting a result- \n")
        result = atlas.GBM_scraper.pull(file_ref, save_array, db, new)

        sys.stdout.write("Time Array has Length " + str(len(save_array[trig_number]["time_array"])) + "\n")
        sys.stdout.write("stop. \n")

        save_array = result

#for name in lat_files:
    #if '_PH00' in name:
        #trig_number = name.split("GRB")[1].split("_P")[0]
        #n_num = name.split("_n")[1].split("_b")[0]
        #result = atlas.LAT_scraper.pull(file_ref, save_array, db)
        #save_array = result

for name in save_array:
    print(name, flush=True)
    result = atlas.redback_scraper.pull(name, save_array, db)
    result[name]["time_array"] = result[name]["time_array"].tolist()
    result[name]["time_values"] = result[name]["time_values"].tolist()
    result[name]["half_max_t"] = result[name]["half_max_t"][0]
    save_array = result

print(save_array, flush=True)

try:
    json_str = json.dumps(save_array, indent=4)
except Exception as e:
    traceback.print_exc()
    sys.stdout.write("\n")

try:
    with open("data/grb_analysis.json", "w") as f:
        f.write(json_str)
except Exception as e:
    traceback.print_exc()
    sys.stdout.write("\n")