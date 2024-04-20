from rocketcea.cea_obj_w_units import CEA_Obj
from rocketcea.cea_obj import add_new_fuel

import matplotlib
matplotlib.use('Qt5Agg')  # Use the TkAgg backend

import numpy as np
import matplotlib.pyplot as plt


###want to graph chamber pressure with respect to flame temperature

#input propellants
# RocketCEA doesnt have paraffin built in: CREATE IT BELOW
fuel_name = 'paraffin'
#C32H66 from RPA Paraffin Wax Composition
fuel_properties = f"""
fuel paraffin  C 32   H 66    wt%=100.00
h,KJ/Kgmol=-1860600     t(k)=298.15   rho,kg/m3={900}
"""

add_new_fuel(fuel_name, fuel_properties)
ox_name = 'N2O'

expratio = 12
OF_ratio = [2,4,6,8,10]

#chamber pressure ranges
P_cc_min = 5 #Bar
P_cc_max = 50 #Bar
P_cc_step = 5 #Bar

#create cea object
ceaObj = CEA_Obj(oxName=ox_name, fuelName=fuel_name, pressure_units='Bar', isp_units='sec', cstar_units='m/s', temperature_units='K', sonic_velocity_units='m/s',enthalpy_units='kJ/kg',density_units='kg/m^3',specific_heat_units='kJ/kg-K')
#  CEA_Obj(oxName=oxidizer_name, fuelName=fuel_name, pressure_units='Pa', isp_units='sec', cstar_units='m/s', temperature_units='K', sonic_velocity_units='m/s',enthalpy_units='kJ/kg',density_units='kg/m^3',specific_heat_units='kJ/kg-K')

P_cc_current = P_cc_min


for j in OF_ratio:
#create graph vectors
    flame_temp_mw_ratio_arr = []
    p_cc_arr = []

    #while current chamber pressure < highest chamber pressure
    while(P_cc_current <= P_cc_max):
        i = ceaObj.get_IvacCstrTc_ChmMwGam(Pc=P_cc_current, MR=j, eps=expratio)
        flame_temp_mw_ratio_arr.append(i[2]/i[3])
        p_cc_arr.append(P_cc_current)
        P_cc_current+=P_cc_step

    P_cc_current=P_cc_min
    print(f"O/F Ratio: {j}, gamma = {i[4]}, gas const = {8134/i[3]}, mw = {i[3]}")
    plt.plot(p_cc_arr, flame_temp_mw_ratio_arr, label=f'O/F={j}')

    

#quick calculation of exit velocity

#graph:
plt.title(label=f'Flame Temp/mw vs Chamber Pressure for '+ ox_name + ' ' + fuel_name)
plt.xlabel('Chamber Pressure (Bar)')
plt.ylabel('Flame Temp/mw((mol K)/kg)')
plt.legend()
plt.grid(True)
plt.show()

