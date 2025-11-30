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


#recieves the filepath of a GBM File, Returns Analysis of that file.
class GBM_scraper:
    def pull(file_name):
        #get trig_number
        trig_number = file_name.split("bn")[1].split("_v")
        
        tte = GbmTte.open(file_name)
        fermi = tte.trigtime
        fermi_met = Time(fermi, format='fermi')
        fermi_met.iso
        trig = fermi_met.value

        bin_width = 0.5
        energy_sliced_tte = tte.slice_energy((8, 260.0))
        sliced_phaii = energy_sliced_tte.to_phaii(bin_by_time, bin_width, time_ref=0.0)

        lcplot = Lightcurve(data=sliced_phaii.to_lightcurve())
        plt.xlim(-10,30)
        #save
        
        lcplot_two = Lightcurve(data=sliced_phaii.to_lightcurve())
        #save
        
        time_counts = sliced_phaii.columns_as_array(2, ["TIME"])
        sliced_counts_prime = sliced_phaii.columns_as_array(2, ["COUNTS"])
        sliced_counts = np.zeros(len(sliced_counts_prime[0]))
        for i in range(0, len(sliced_counts_prime)):
            for j in range(0, len(sliced_counts_prime[i])):
                sliced_counts[j] = sliced_counts[j] + sliced_counts_prime[i][j]
        max = [0,0]
        for i in range(0, len(sliced_counts)):
            if sliced_counts[i] > max[0]:
                max[0] = sliced_counts[i]
                max[1] = time_counts[i]

        low_met = max[1][0]
        #low energy time MET

        low_trig = max[1].astype(float) - trig.astype(float)
        #low energy time TRIG

        back50=sliced_counts[50:]
        back100=sliced_counts[100:]
        back250=sliced_counts[250:]

        result = {"Trig Number": trig_number, "Trig Time": trig, "Low met": low_met, "Low trig": low_trig, "Max": max[0], "Back50": np.average(back50), "Var50": np.std(back50), "Back100": np.average(back100), "Var100": np.std(back100), "Back250": np.average(back250), "Var250": np.std(back250)}

        return result

class LAT_scraper:
    def pull(file_name):
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
                        max_count = conversion_y[i]
                        max_time = conversion_x[i]
            high_lat[i] = {"Max Time": max_time, "Max Energy": max_count}
            max_cap = max_count - 0.001

        return high_lat

class red_scraper:
    def pull(GRB_name):
        r = requests.get("https://icecube.wisc.edu/~grbweb_public/GRBweb2.sqlite")
        f = open('GRBweb2.sqlite', 'wb').write(r.content)
        db = sqlite3.connect('GRBweb2.sqlite')

        Sum_table = pandas.read_sql_query("SELECT * from Summary", db)
        Sum_table = Sum_table.sort_values("GRB_name")
        indices = np.where(Sum_table == GRB_name)
        # Extracting row and column indices
        row_indices, col_indices = indices[0], indices[1]

        index = Sum_table.iloc[row_indices].to_numpy()[0][0] - 1
        redshift = Sum_table.iloc[row_indices].redshift.get(index)
        red_source = str(Sum_table.iloc[row_indices].redshift_source.get("Name"))
        name = str(Sum_table.iloc[row_indices].GRB_name.get(index))
        
        return {"Name": name, "Redshift": redshift, "Redshift Source": red_source}