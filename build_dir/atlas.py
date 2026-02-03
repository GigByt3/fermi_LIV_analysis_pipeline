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
import statistics
import sys
import traceback

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
significance: #             ==(max_ct-background)/background_var
half_max_t: #               ==half maximum width for error counting

(for LAT)
lat_highs: [[t, E]...]      ==lat highs over 80% highest reading

(general)
redshift: #                 ==redshift source
redshift_src: "foo"         ==source ("def_GCN" (default GCN) if not available)
trig: #                   ==trigger time
name: "GRB###..."           ==general GRB name with letter code
}
'''

#recieves the filepath of a GBM File, Returns Analysis of that file.
class GBM_scraper:
    #Here save_array... does things....
    def pull(file_name, save_array, db, new):
        #get trig_number
        trig_number = file_name.split("bn")[1].split("_v")[0]
        n_num = file_name.split("_n")[1].split("_b")[0]
        working_save = save_array[trig_number]
        
        tte = GbmTte.open(file_name)
        fermi = tte.trigtime
        fermi_met = Time(fermi, format='fermi')
        fermi_met.iso
        trig = fermi_met.value

        save_array[trig_number]["detectors"].append(n_num)
        save_array[trig_number]["det_ct"] = working_save["det_ct"] + 1

        bin_width = 0.5
        try:
            energy_sliced_tte = tte.slice_energy((8, 260.0))
        except:
            energy_sliced_tte = tte
            return save_array

        sliced_phaii = energy_sliced_tte.to_phaii(bin_by_time, bin_width, time_ref=0.0)
        
        time_counts = sliced_phaii.columns_as_array(2, ["TIME"])
        sliced_counts_prime = sliced_phaii.columns_as_array(2, ["COUNTS"])

        #incorperate new data
        if new:
            sliced_counts = np.zeros(len(sliced_counts_prime[0]))
            sys.stdout.write("New array " + str(trig_number) + " of length: " + str(len(sliced_counts_prime[0])) + "\n")
        else:
            sliced_counts = working_save["time_array"]
            sys.stdout.write("Modifying array " + str(trig_number) + " of length: " + str(len(sliced_counts)) +"\n")

        try:
            for i in range(0, len(sliced_counts_prime)-1):
                for j in range(0, len(sliced_counts_prime[i])-1):
                    sliced_counts[j] = sliced_counts[j] + sliced_counts_prime[i][j][0]
        except Exception as e:
            for i in range(0, len(sliced_counts_prime)-1):
                for j in range(0, len(sliced_counts[i])-1):
                    sliced_counts[j] = sliced_counts[j] + sliced_counts_prime[i][j][0]
            traceback.print_exc()
            sys.stdout.write("\n")


        sys.stdout.write("Sliced Counts. \n")

        save_array[trig_number]["time_values"] = time_counts
        save_array[trig_number]["time_array"] = sliced_counts
        
        if save_array[trig_number]["det_ct"] == 10:
            #Get low_t and low_ct
            max = [0,0]
            for i in range(0, len(sliced_counts)):
                if sliced_counts[i] > max[0]:
                    max[0] = sliced_counts[i]
                    max[1] = time_counts[i]
            save_array[trig_number]["low_t"] = max[1][0]
            #low energy time MET
            save_array[trig_number]["low_ct"] = max[0][0]
            save_array[trig_number]["trig"] = trig.astype(float)

            lowfifty = -100
            highfifty = -100
            up = False
            for i in range(0, len(sliced_counts)):
                if sliced_counts[i] > 0.5*max[0]:
                    up = True
                    if lowfifty == -100:
                        lowfifty = time_counts[i]
                
                if sliced_counts[i] < 0.5*max[0] & up:
                    highfifty = time_counts[i]
            
            save_array[trig_number]["half_max_t"] = highfifty - lowfifty

        sys.stdout.write("Returning Save Array. \n")

        return save_array

class LAT_scraper:
    def pull(file_name, save_array, db):
        conversion_x = []
        conversion_y = []
        for i in range(0, len(data)):
            conversion_y.append(data[i][0])
            conversion_x.append(data[i][9])

        high_lat = {}
        for i in range(1, 26):
            max_cap = 100000000
            max_count = 0
            max_time = 0
            max_len = int(len(conversion_y))
            for i in range(0, max_len):
                if conversion_y[i] > max:
                    if conversion_y[i] < max_cap:
                        str(max_count = conversion_y[i])
                        str(max_time = conversion_x[i])
            high_lat[i] = {"Max Time": max_time, "Max Energy": max_count}
            max_cap = max_count - 0.001

        return high_lat.tolist()

class redback_scraper:
    def pull(name, save_array, db):
        print(str(GRB_name))

        GRB_name = save_array[name]["name"]

        Sum_table = pandas.read_sql_query("SELECT * from Summary", db)
        Sum_table = Sum_table.sort_values("GRB_name")
        indices = np.where(Sum_table == GRB_name)
        # Extracting row and column indices
        row_indices, col_indices = indices[0], indices[1]

        index = Sum_table.iloc[row_indices].to_numpy()[0][0] - 1
        redshift = str(Sum_table.iloc[row_indices].redshift.get(index))
        red_source = str(Sum_table.iloc[row_indices].redshift_source.get("Name"))
        name = str(Sum_table.iloc[row_indices].GRB_name.get(index))

        teetop = str(Sum_table.iloc[row_indices].T100.get(index))
        times = save_array[name]["time_values"]
        background = []
        for i in range(0, len(times)):
            if times[i] < save_array[name]["trig"]-10:
                background.append(save_array[name]["time_array"][i])
            if times[i] > teetop + 10:
                background.append(save_array[name]["time_array"][i])
        
        save_array[name]["background"] = statistics.mean(background)
        save_array[name]["background_var"] = statistics.stdev(background)
        save_array[name]["significance"] = (save_array[name]["max_ct"]-statistics.mean(background))/statistics.stdev(background)

        save_array[name]["name"] = str(Sum_table.iloc[row_indices].GRB_name.get(index))

        return save_array
