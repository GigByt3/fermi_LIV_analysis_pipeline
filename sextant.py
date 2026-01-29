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

for name in gbm_files:
    if '_bn' in name:
        trig_number = name.split("bn")[1].split("_v")[0]
        n_num = name.split("_n")[1].split("_b")[0]
        result = atlas.GBM_scraper.pull(gbm_dir_name + name)
        try:
            json_object[str(trig_number)+"at"+str(n_num)]["GBM"] = result
        except:
            json_object[str(trig_number)+"at"+str(n_num)] = {}
            json_object[str(trig_number)+"at"+str(n_num)]["GBM"] = result


for name in lat_files:
    if '_PH00' in name:
        trig_number = name.split("GRB")[1].split("_P")[0]
        n_num = name.split("_n")[1].split("_b")[0]
        result = atlas.LAT_scraper.pull(name)
        json_object[str(trig_number)]
        try:
            json_object[str(trig_number)+"at"+str(n_num)]["LAT"] = result
        except:
            json_object[str(trig_number)+"at"+str(n_num)] = {}
            json_object[str(trig_number)+"at"+str(n_num)]["LAT"] = result

for name in json_object:
    fermi_name = "GRB" + name.split("at")[0]
    result = atlas.red_scraper.pull(fermi_name, db)
    json_object[name]["Name"] = result["Name"]
    json_object[name]["Redshift"] = result["Redshift"]
    json_object[name]["Redshift Source"] = result["Redshift Source"]

print(json_object)

json_str = json.dumps(json_object, indent=4)

with open("data/grb_analysis.json", "w") as f:
    f.write(json_str)
