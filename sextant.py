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

json_object = {}

gbm_dir_name = "./fermi_tte_GBM/"
lat_dir_name = "./fermi_LAT/"
gbm_files = os.listdir(gbm_dir_name)
gbm_files = [f for f in gbm_files if os.path.isfile(gbm_dir_name+f)]
lat_files = os.listdir(lat_dir_name)
lat_files = [f for f in lat_files if os.path.isfile(lat_dir_name+f)]

for name in gbm_files:
    if '_bn' in name:
        trig_number = name.split("bn")[1].split("_v")[0]
        result = atlas.GBM_scraper.pull(name)
        try:
            json_object[str(trig_number)]["GBM"] = result
        except:
            json_object[str(trig_number)] = {}
            json_object[str(trig_number)]["GBM"] = result


for name in lat_files:
    if '_PH00' in name:
        trig_number = name.split("GRB")[1].split("_P")[0]
        result = atlas.LAT_scraper.pull(name)
        json_object[str(trig_number)]
        try:
            json_object[str(trig_number)]["LAT"] = result
        except:
            json_object[str(trig_number)] = {}
            json_object[str(trig_number)]["LAT"] = result

for name in json_object:
    fermi_name = "GBM" + name
    result = atlas.red_scraper.pull(fermi_name)
    json_object[name]["Name"] = result["Name"]
    json_object[name]["Redshift"] = result["Redshift"]
    json_object[name]["Redshift Source"] = result["Redshift Source"]


json_str = json.dumps(json_object, indent=4)

with open("grb_analysis.json", "w") as f:
    f.write(json_str)