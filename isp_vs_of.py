from rocketcea.cea_obj_w_units import CEA_Obj
from rocketcea.cea_obj import add_new_fuel

#import PyQt5, PySide2

import matplotlib
matplotlib.use('Qt5Agg')  # Use the TkAgg backend

import numpy as np
import matplotlib.pyplot as plt

def bar_to_psi(x):
    return x*14.5038


# RocketCEA doesnt have paraffin built in: CREATE IT BELOW
fuel_name = 'paraffin'
#C32H66 from RPA Paraffin Wax Composition
fuel_properties = f"""
fuel paraffin  C 32   H 66    wt%=100.00
h,KJ/Kgmol=-1860600     t(k)=298.15   rho,kg/m3={900}
"""

add_new_fuel(fuel_name, fuel_properties)

#names
ox_name = 'N2O'
fuel_name = 'CH4'

# Define the range of chamber pressures
chamber_pressures = [10, 20, 30, 40, 50]


expratio = 12

# Plotting
plt.figure(figsize=(10, 6))  # Optional: Adjust the figure size

for Pc in chamber_pressures:
    ispObj = CEA_Obj(oxName=ox_name, fuelName=fuel_name, pressure_units='Bar', isp_units='sec', cstar_units='m/s', temperature_units='K', sonic_velocity_units='m/s',enthalpy_units='kJ/kg',density_units='kg/m^3',specific_heat_units='kJ/kg-K')

    of_arr = []
    isp_arr = []

    isp_prev = 0
    max_isp = 0
    of_store = 0
    i = 0.55

    while i < 16:
        isp = ispObj.get_Isp(Pc=Pc, MR=i, eps=expratio, frozen=0, frozenAtThroat=0)
        of_arr.append(i)
        isp_arr.append(isp)
        if isp > isp_prev:
            max_isp = isp
            of_store = i
        i = i + 0.5
        isp_prev = isp

    print(f"For Pc={Pc} bar, Max ISP: {max_isp}, O/F Ratio: {of_store}")
    plt.plot(of_arr, isp_arr, label=f'Pc={Pc} bar  [{bar_to_psi(Pc)} PSI]')

plt.xlabel('O/F Ratio')
plt.ylabel('ISP (s)')
plt.title('ISP VS O/F RATIO at Different Chamber Pressures For ' + ox_name + ' ' + fuel_name+ f' at exp ratio {expratio}')
plt.legend()
plt.grid(True)
plt.show()